from pydantic import BaseModel
from datetime import datetime


class TagBase(BaseModel):
    name: str
    slug: str | None = None
    color: str = "#18A058"
    description: str | None = None


class TagCreate(TagBase):
    pass


class TagUpdate(BaseModel):
    name: str | None = None
    slug: str | None = None
    color: str | None = None
    description: str | None = None


class TagOut(BaseModel):
    id: int
    name: str
    slug: str
    color: str
    description: str | None
    article_count: int | None = None
    created_at: datetime

    model_config = {"from_attributes": True}
