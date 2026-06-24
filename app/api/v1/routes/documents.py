from uuid import UUID

from fastapi import APIRouter, BackgroundTasks, Depends, File, UploadFile
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.dependencies.auth import get_current_user
from app.core.exceptions import ApiException
from app.core.responses import ApiResponse
from app.db.session import get_db
from app.jobs.indexing_job import index_document_job
from app.models.user import User
from app.schemas.api_response import ApiResponseSchema
from app.schemas.document import DocumentResponse
from app.schemas.search import SearchRequest, SearchResponse
from app.services.document_service import create_document_from_upload, get_document
from app.services.retrieval_service import search_documents

router = APIRouter()


@router.post("/upload", response_model=ApiResponseSchema[DocumentResponse])
async def upload_document(
    background_tasks: BackgroundTasks,
    current_user: User = Depends(get_current_user),
    file: UploadFile = File(...),
    db: AsyncSession = Depends(get_db),
):
    """Upload a document to the knowledge base."""

    document = await create_document_from_upload(
        file=file,
        db=db,
        business_id=current_user.business_id,
    )

    background_tasks.add_task(index_document_job, document.id)

    return ApiResponse(
        data=DocumentResponse.model_validate(document),
        message="Document uploaded successfully",
    )


@router.get("/{document_id}", response_model=ApiResponseSchema[DocumentResponse])
async def get_document_by_id(
    document_id: UUID,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """Get document metadata by ID."""

    document = await get_document(
        db=db,
        document_id=document_id,
        business_id=current_user.business_id,
    )

    if document is None:
        raise ApiException(
            message="Document not found",
            status_code=404,
        )

    return ApiResponse(
        data=DocumentResponse.model_validate(document),
        message="Document fetched successfully",
    )


@router.post("/search", response_model=ApiResponseSchema[SearchResponse])
async def search_document_chunks(
    payload: SearchRequest,
    current_user: User = Depends(get_current_user),
):
    """Search indexed document chunks."""

    results = search_documents(
        query=payload.query,
        top_k=payload.top_k,
        business_id=str(current_user.business_id),
    )

    return ApiResponse(
        data=SearchResponse(
            query=payload.query,
            results=results,
        ),
        message="Document chunks retrieved successfully",
    )