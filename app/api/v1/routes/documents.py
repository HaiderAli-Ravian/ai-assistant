from uuid import UUID

from fastapi import (
    APIRouter,
    BackgroundTasks,
    Depends,
    File,
    HTTPException,
    UploadFile,
)
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.responses import ApiResponse
from app.db.session import get_db
from app.jobs.indexing_job import index_document_job
from app.schemas.api_response import ApiResponseSchema
from app.schemas.document import DocumentResponse
from app.services.document_service import (
    create_document_from_upload,
    get_document,
)
from app.schemas.search import SearchRequest, SearchResponse
from app.services.retrieval_service import search_documents

router = APIRouter()


@router.post("/upload", response_model=ApiResponseSchema[DocumentResponse])
async def upload_document(
    background_tasks: BackgroundTasks,
    file: UploadFile = File(...),
    db: AsyncSession = Depends(get_db),
):
    """Upload a document to the knowledge base."""

    document = await create_document_from_upload(file=file, db=db)

    background_tasks.add_task(index_document_job, document.id)

    return ApiResponse(
        data=document,
        message="Document uploaded successfully",
    )


@router.get("/{document_id}", response_model=ApiResponseSchema[DocumentResponse])
async def get_document_by_id(
    document_id: UUID,
    db: AsyncSession = Depends(get_db),
):
    """Get document metadata by ID."""

    document = await get_document(
        db=db,
        document_id=document_id,
    )

    if document is None:
        raise HTTPException(
            status_code=404,
            detail="Document not found",
        )

    return ApiResponse(
        data=document,
        message="Document fetched successfully",
    )


@router.post("/search", response_model=ApiResponseSchema[SearchResponse])
async def search_document_chunks(
    payload: SearchRequest,
):
    """Search indexed document chunks."""

    results = search_documents(
        query=payload.query,
        top_k=payload.top_k,
    )

    return ApiResponse(
        data={
            "query": payload.query,
            "results": results,
        },
        message="Document chunks retrieved successfully",
    )