import os
import shutil
import uuid
from pathlib import Path
from fastapi import UploadFile
from app.core.config import settings
from app.core.errors import BadRequestError


ALLOWED_IMAGE_TYPES = {
    "image/jpeg",
    "image/png",
    "image/jpg",
    "image/webp",
    "image/bmp",
    "image/tiff",
}


def ensure_tmp_dir() -> Path:
    path = Path(settings.TMP_DIR)
    path.mkdir(parents=True, exist_ok=True)
    return path


def validate_upload_file(file: UploadFile) -> None:
    if file is None:
        raise BadRequestError("No file uploaded.")

    if not file.filename:
        raise BadRequestError("Uploaded file must have a filename.")

    if file.content_type not in ALLOWED_IMAGE_TYPES:
        raise BadRequestError(
            f"Unsupported file type: {file.content_type}. Allowed types: {sorted(ALLOWED_IMAGE_TYPES)}"
        )


async def save_upload_to_temp(file: UploadFile) -> str:
    validate_upload_file(file)
    tmp_dir = ensure_tmp_dir()

    suffix = Path(file.filename).suffix or ".bin"
    temp_filename = f"{uuid.uuid4().hex}{suffix}"
    temp_path = tmp_dir / temp_filename

    with open(temp_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    size_mb = os.path.getsize(temp_path) / (1024 * 1024)
    if size_mb > settings.MAX_UPLOAD_SIZE_MB:
        try:
            os.remove(temp_path)
        except FileNotFoundError:
            pass
        raise BadRequestError(
            f"File too large: {size_mb:.2f} MB. Max allowed: {settings.MAX_UPLOAD_SIZE_MB} MB."
        )

    return str(temp_path)


def cleanup_temp_file(path: str) -> None:
    try:
        if path and os.path.exists(path):
            os.remove(path)
    except Exception:
        pass