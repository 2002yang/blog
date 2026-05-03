from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy import func
from app.database import get_db
from app.models import Tag
from app.schemas import TagOut, TagCreate, TagUpdate
from app.dependencies import require_admin
from app.utils.slug import make_slug, ensure_unique_slug

router = APIRouter(tags=["tags"])


@router.get("/tags", response_model=list[TagOut])
def list_tags(db: Session = Depends(get_db)):
    tags = db.query(Tag).all()
    result = []
    for tag in tags:
        count = len([a for a in tag.articles if a.status == "published"])
        out = TagOut.model_validate(tag)
        out.article_count = count
        result.append(out)
    return result


@router.get("/tags/{slug}", response_model=TagOut)
def get_tag(slug: str, db: Session = Depends(get_db)):
    tag = db.query(Tag).filter(Tag.slug == slug).first()
    if not tag:
        raise HTTPException(status_code=404, detail="Tag not found")
    out = TagOut.model_validate(tag)
    out.article_count = len([a for a in tag.articles if a.status == "published"])
    return out


@router.post("/admin/tags", response_model=TagOut, status_code=201)
def create_tag(data: TagCreate, db: Session = Depends(get_db), _=Depends(require_admin)):
    slug = data.slug or make_slug(data.name)
    existing = {t.slug for t in db.query(Tag.slug).all()}
    slug = ensure_unique_slug(slug, existing)
    tag = Tag(name=data.name, slug=slug, color=data.color, description=data.description)
    db.add(tag)
    db.commit()
    db.refresh(tag)
    return tag


@router.put("/admin/tags/{tag_id}", response_model=TagOut)
def update_tag(tag_id: int, data: TagUpdate, db: Session = Depends(get_db), _=Depends(require_admin)):
    tag = db.get(Tag, tag_id)
    if not tag:
        raise HTTPException(status_code=404, detail="Tag not found")
    for field, value in data.model_dump(exclude_none=True).items():
        setattr(tag, field, value)
    db.commit()
    db.refresh(tag)
    return tag


@router.delete("/admin/tags/{tag_id}", status_code=204)
def delete_tag(tag_id: int, db: Session = Depends(get_db), _=Depends(require_admin)):
    tag = db.get(Tag, tag_id)
    if not tag:
        raise HTTPException(status_code=404, detail="Tag not found")
    db.delete(tag)
    db.commit()
