from llama_index.core import StorageContext, VectorStoreIndex
from llama_index.core.vector_stores import MetadataFilter, MetadataFilters

from app.services.embedding_service import get_embedding_model
from app.services.vector_store_service import get_vector_store


def search_documents(
    query: str,
    top_k: int = 5,
    business_id: str | None = None,
) -> list[dict]:
    """Search indexed document chunks from the vector store."""

    vector_store = get_vector_store(collection_name="documents")

    storage_context = StorageContext.from_defaults(
        vector_store=vector_store,
    )

    index = VectorStoreIndex.from_vector_store(
        vector_store=vector_store,
        storage_context=storage_context,
        embed_model=get_embedding_model(),
    )

    filters = None

    if business_id:
        filters = MetadataFilters(
            filters=[
                MetadataFilter(
                    key="business_id",
                    value=business_id,
                )
            ]
        )

    retriever = index.as_retriever(
        similarity_top_k=top_k,
        filters=filters,
    )

    nodes = retriever.retrieve(query)

    return [
        {
            "text": node.node.get_content(),
            "score": node.score,
            "metadata": node.node.metadata,
        }
        for node in nodes
    ]