from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base, TimestampMixin, UUIDMixin


class Business(UUIDMixin, TimestampMixin, Base):
    __tablename__ = "businesses"

    name: Mapped[str] = mapped_column(String(255), nullable=False)

    website_url: Mapped[str | None] = mapped_column(String(500), nullable=True)

    phone: Mapped[str | None] = mapped_column(String(50), nullable=True)

    timezone: Mapped[str | None] = mapped_column(String(100), nullable=True)

    users = relationship(
        "User",
        back_populates="business",
        cascade="all, delete-orphan",
    )

    documents = relationship(
        "Document",
        back_populates="business",
        cascade="all, delete-orphan",
    )