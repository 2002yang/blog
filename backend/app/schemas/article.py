from pydantic import BaseModel
from datetime import datetime
from app.schemas.tag import TagOut
from app.schemas.user import UserOut


class ArticleAuthor(BaseModel):
    id: int
    username: str
    avatar_url: str | None

    model_config = {"from_attributes": True}


class ArticleBase(BaseModel):
    title: str
    slug: str | None = None
    summary: str | None = None
    content: str = ""
    cover_image: str | None = None
    status: str = "draft"
    is_featured: bool = False
    tag_ids: list[int] = []
    published_at: datetime | None = None


class ArticleCreate(ArticleBase):
    pass


class ArticleUpdate(BaseModel):
    title: str | None = None
    slug: str | None = None
    summary: str | None = None
    content: str | None = None
    cover_image: str | None = None
    status: str | None = None
    is_featured: bool | None = None
    tag_ids: list[int] | None = None
    published_at: datetime | None = None


class ArticleListItem(BaseModel):
    id: int
    title: str
    slug: str
    summary: str | None
    cover_image: str | None
    author: ArticleAuthor | None
    status: str
    is_featured: bool
    view_count: int
    read_time: int
    tags: list[TagOut]
    published_at: datetime | None
    created_at: datetime

    model_config = {"from_attributes": True}


class ArticleOut(ArticleListItem):
    content: str
    updated_at: datetime
