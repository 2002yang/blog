import os
import uuid
from datetime import datetime
from pathlib import Path
from fastapi import APIRouter, Depends, UploadFile, File, HTTPException
from app.dependencies import get_current_user
from app.models import User, Image
from app.database import get_db
from app.config import settings
from sqlalchemy.orm import Session

router = APIRouter(tags=["upload"])

ALLOWED_TYPES = {"image/jpeg", "image/png", "image/webp", "image/gif"}


@router.post("/upload/image")
async def upload_image(
    file: UploadFile = File(...),
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    if file.content_type not in ALLOWED_TYPES:
        raise HTTPException(status_code=400, detail="Unsupported image type")

    content = await file.read()
    if len(content) > settings.MAX_UPLOAD_SIZE:
        raise HTTPException(status_code=400, detail="File too large (max 5MB)")

    ext = Path(file.filename or "image.jpg").suffix.lower() or ".jpg"
    now = datetime.now()
    rel_dir = Path(str(now.year)) / str(now.month).zfill(2)
    abs_dir = Path(settings.UPLOAD_DIR) / rel_dir
    abs_dir.mkdir(parents=True, exist_ok=True)

    filename = f"{uuid.uuid4().hex}{ext}"
    abs_path = abs_dir / filename
    abs_path.write_bytes(content)

    url = f"/uploads/{rel_dir}/{filename}".replace("\\", "/")
    image = Image(filename=filename, url=url, size=len(content), mime_type=file.content_type, uploader_id=user.id)
    db.add(image)
    db.commit()

    return {"url": url, "filename": filename}
