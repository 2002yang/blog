from app.routers.auth import router as auth_router
from app.routers.articles import router as articles_router
from app.routers.tags import router as tags_router
from app.routers.upload import router as upload_router

__all__ = ["auth_router", "articles_router", "tags_router", "upload_router"]
