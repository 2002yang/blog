import math
from datetime import datetime, timezone
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from sqlalchemy import or_, func
from app.database import get_db
from app.models import Article, Tag
from app.schemas import ArticleOut, ArticleListItem, ArticleCreate, ArticleUpdate
from app.schemas.common import PaginatedResponse
from app.dependencies import require_admin
from app.utils.slug import make_slug, ensure_unique_slug

router = APIRouter(tags=["articles"])


def _read_time(content: str) -> int:
    words = len(content.split())
    return max(1, round(words / 200))


def _paginate(query, page: int, size: int):
    total = query.count()
    items = query.offset((page - 1) * size).limit(size).all()
    pages = math.ceil(total / size) if size else 1
    return total, items, pages


# ── Public ──────────────────────────────────────────────────────────────────

@router.get("/articles", response_model=PaginatedResponse[ArticleListItem])
def list_articles(
    page: int = Query(1, ge=1),
    size: int = Query(9, ge=1, le=50),
    tag: str | None = None,
    db: Session = Depends(get_db),
):
    q = db.query(Article).filter(Article.status == "published")
    if tag:
        q = q.join(Article.tags).filter(Tag.slug == tag)
    q = q.order_by(Article.published_at.desc())
    total, items, pages = _paginate(q, page, size)
    return PaginatedResponse(items=items, total=total, page=page, size=size, pages=pages)


@router.get("/articles/featured", response_model=list[ArticleListItem])
def featured_articles(db: Session = Depends(get_db)):
    return db.query(Article).filter(Article.status == "published", Article.is_featured == True).order_by(Article.published_at.desc()).limit(5).all()


@router.get("/articles/search", response_model=PaginatedResponse[ArticleListItem])
def search_articles(
    q: str = Query(..., min_length=1),
    page: int = Query(1, ge=1),
    size: int = Query(9, ge=1, le=50),
    db: Session = Depends(get_db),
):
    query = db.query(Article).filter(
        Article.status == "published",
        or_(
            Article.title.ilike(f"%{q}%"),
            Article.summary.ilike(f"%{q}%"),
            Article.content.ilike(f"%{q}%"),
        ),
    ).order_by(Article.published_at.desc())
    total, items, pages = _paginate(query, page, size)
    return PaginatedResponse(items=items, total=total, page=page, size=size, pages=pages)


@router.get("/articles/{slug}", response_model=ArticleOut)
def get_article(slug: str, db: Session = Depends(get_db)):
    article = db.query(Article).filter(Article.slug == slug, Article.status == "published").first()
    if not article:
        raise HTTPException(status_code=404, detail="Article not found")
    return article


@router.post("/articles/{article_id}/view", status_code=204)
def increment_view(article_id: int, db: Session = Depends(get_db)):
    article = db.get(Article, article_id)
    if article:
        article.view_count += 1
        db.commit()


# ── Admin ────────────────────────────────────────────────────────────────────

@router.get("/admin/articles", response_model=PaginatedResponse[ArticleListItem])
def admin_list_articles(
    page: int = Query(1, ge=1),
    size: int = Query(15, ge=1, le=100),
    status: str | None = None,
    db: Session = Depends(get_db),
    _=Depends(require_admin),
):
    q = db.query(Article)
    if status:
        q = q.filter(Article.status == status)
    q = q.order_by(Article.created_at.desc())
    total, items, pages = _paginate(q, page, size)
    return PaginatedResponse(items=items, total=total, page=page, size=size, pages=pages)


@router.post("/admin/articles", response_model=ArticleOut, status_code=201)
def create_article(data: ArticleCreate, db: Session = Depends(get_db), _=Depends(require_admin)):
    slug = data.slug or make_slug(data.title)
    existing = {a.slug for a in db.query(Article.slug).all()}
    slug = ensure_unique_slug(slug, existing)
    tags = db.query(Tag).filter(Tag.id.in_(data.tag_ids)).all() if data.tag_ids else []
    published_at = data.published_at
    if data.status == "published" and not published_at:
        published_at = datetime.now(timezone.utc)
    article = Article(
        title=data.title, slug=slug, summary=data.summary, content=data.content,
        cover_image=data.cover_image, status=data.status, is_featured=data.is_featured,
        read_time=_read_time(data.content), tags=tags, published_at=published_at,
    )
    db.add(article)
    db.commit()
    db.refresh(article)
    return article


@router.put("/admin/articles/{article_id}", response_model=ArticleOut)
def update_article(article_id: int, data: ArticleUpdate, db: Session = Depends(get_db), _=Depends(require_admin)):
    article = db.get(Article, article_id)
    if not article:
        raise HTTPException(status_code=404, detail="Article not found")
    update_data = data.model_dump(exclude_none=True)
    tag_ids = update_data.pop("tag_ids", None)
    if tag_ids is not None:
        article.tags = db.query(Tag).filter(Tag.id.in_(tag_ids)).all()
    if "content" in update_data:
        article.read_time = _read_time(update_data["content"])
    if update_data.get("status") == "published" and not article.published_at:
        article.published_at = datetime.now(timezone.utc)
    for field, value in update_data.items():
        setattr(article, field, value)
    db.commit()
    db.refresh(article)
    return article


@router.delete("/admin/articles/{article_id}", status_code=204)
def delete_article(article_id: int, db: Session = Depends(get_db), _=Depends(require_admin)):
    article = db.get(Article, article_id)
    if not article:
        raise HTTPException(status_code=404, detail="Article not found")
    db.delete(article)
    db.commit()


@router.patch("/admin/articles/{article_id}/publish", response_model=ArticleOut)
def toggle_publish(article_id: int, db: Session = Depends(get_db), _=Depends(require_admin)):
    article = db.get(Article, article_id)
    if not article:
        raise HTTPException(status_code=404, detail="Article not found")
    if article.status == "published":
        article.status = "draft"
    else:
        article.status = "published"
        if not article.published_at:
            article.published_at = datetime.now(timezone.utc)
    db.commit()
    db.refresh(article)
    return article


@router.patch("/admin/articles/{article_id}/feature", response_model=ArticleOut)
def toggle_feature(article_id: int, db: Session = Depends(get_db), _=Depends(require_admin)):
    article = db.get(Article, article_id)
    if not article:
        raise HTTPException(status_code=404, detail="Article not found")
    article.is_featured = not article.is_featured
    db.commit()
    db.refresh(article)
    return article


@router.get("/admin/stats")
def admin_stats(db: Session = Depends(get_db), _=Depends(require_admin)):
    total = db.query(func.count(Article.id)).scalar()
    published = db.query(func.count(Article.id)).filter(Article.status == "published").scalar()
    draft = db.query(func.count(Article.id)).filter(Article.status == "draft").scalar()
    views = db.query(func.sum(Article.view_count)).scalar() or 0
    tags = db.query(func.count(Tag.id)).scalar()
    return {
        "total_articles": total,
        "published_articles": published,
        "draft_articles": draft,
        "total_views": views,
        "total_tags": tags,
    }
