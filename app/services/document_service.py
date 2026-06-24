from uuid import UUID

from fastapi import UploadFile
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.document import Document
from app.models.enums import DocumentStatus
from app.services.cloudinary_service import upload_file_to_cloudinary


async def create_document_from_upload(
    file: UploadFile,
    db: AsyncSession,
    business_id: UUID,
) -> Document:
    """Upload and persist document metadata."""

    uploaded_file = await upload_file_to_cloudinary(file)

    document = Document(
        business_id=business_id,
        filename=file.filename,
        cloudinary_url=uploaded_file["url"],
        cloudinary_public_id=uploaded_file["public_id"],
        status=DocumentStatus.UPLOADED,
    )

    db.add(document)
    await db.commit()
    await db.refresh(document)

    return document


async def get_document(
    db: AsyncSession,
    document_id: UUID,
    business_id: UUID,
) -> Document | None:
    """Return document metadata by ID for the current business."""

    result = await db.execute(
        select(Document).where(
            Document.id == document_id,
            Document.business_id == business_id,
        )
    )

    return result.scalar_one_or_none()