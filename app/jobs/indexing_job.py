import asyncio
import logging
from uuid import UUID

from sqlalchemy import select

from app.db.session import AsyncSessionLocal
from app.models.document import Document, DocumentStatus
from app.services.indexing_service import index_document

logger = logging.getLogger(__name__)


async def index_document_job(document_id: UUID) -> None:
    """Index a document in the background."""

    async with AsyncSessionLocal() as db:
        result = await db.execute(
            select(Document).where(Document.id == document_id)
        )
        document = result.scalar_one_or_none()

        if document is None:
            logger.warning("Indexing skipped. Document not found: %s", document_id)
            return

        try:
            document.status = DocumentStatus.INDEXING
            await db.commit()

            await asyncio.to_thread(index_document, document)

            document.status = DocumentStatus.INDEXED
            await db.commit()

        except Exception:
            logger.exception("Document indexing failed: %s", document_id)

            await db.rollback()

            document.status = DocumentStatus.FAILED
            await db.commit()