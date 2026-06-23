import cloudinary
import cloudinary.uploader
from fastapi import UploadFile

from app.core.config import settings


cloudinary.config(
    cloud_name=settings.CLOUDINARY_CLOUD_NAME,
    api_key=settings.CLOUDINARY_API_KEY,
    api_secret=settings.CLOUDINARY_API_SECRET,
    secure=True,
)


async def upload_file_to_cloudinary(file: UploadFile) -> dict:
    """Upload a file to Cloudinary and return its metadata."""

    result = cloudinary.uploader.upload(
        file.file,
        folder=settings.CLOUDINARY_FOLDER,
        resource_type="auto",
    )

    return {
        "url": result["secure_url"],
        "public_id": result["public_id"],
    }