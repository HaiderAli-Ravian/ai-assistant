import uuid

from sqlalchemy import String, Text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column
from enum import Enum

from app.db.base import Base, TimestampMixin


class DocumentStatus(str, Enum):
    UPLOADED = "uploaded"
    INDEXING = "indexing"
    INDEXED = "indexed"
    FAILED = "failed"


class Document(Base, TimestampMixin):
    __tablename__ = "documents"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
    )

    filename: Mapped[str] = mapped_column(String(255), nullable=False)
    cloudinary_url: Mapped[str] = mapped_column(Text, nullable=False)
    cloudinary_public_id: Mapped[str] = mapped_column(String(255), nullable=False)

    status: Mapped[DocumentStatus] = mapped_column(
        String(50),
        default=DocumentStatus.UPLOADED,
        nullable=False,
    )