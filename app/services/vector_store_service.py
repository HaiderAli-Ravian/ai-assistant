import chromadb
from llama_index.vector_stores.chroma import ChromaVectorStore

from app.core.config import settings


def get_vector_store(collection_name: str = "documents"):
    """Returns the active vector store."""
    
    chroma_client = chromadb.PersistentClient(
        path=settings.CHROMA_PERSIST_DIR,
    )

    chroma_collection = chroma_client.get_or_create_collection(
        name=collection_name,
    )

    return ChromaVectorStore(
        chroma_collection=chroma_collection,
    )