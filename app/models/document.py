import uuid

from sqlalchemy import Enum, ForeignKey, String, Text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base, TimestampMixin, UUIDMixin
from app.models.enums import DocumentStatus


class Document(UUIDMixin, TimestampMixin, Base):
    __tablename__ = "documents"

    business_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("businesses.id"),
        nullable=False,
    )

    filename: Mapped[str] = mapped_column(String(255), nullable=False)

    cloudinary_url: Mapped[str] = mapped_column(Text, nullable=False)

    cloudinary_public_id: Mapped[str] = mapped_column(String(255), nullable=False)

    status: Mapped[DocumentStatus] = mapped_column(
        Enum(DocumentStatus, name="document_status"),
        default=DocumentStatus.UPLOADED,
        nullable=False,
    )

    business = relationship(
        "Business",
        back_populates="documents",
    )