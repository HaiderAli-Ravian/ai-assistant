import tempfile
from pathlib import Path

import httpx
from llama_index.core import SimpleDirectoryReader, StorageContext, VectorStoreIndex
from llama_index.core.node_parser import SentenceSplitter
from llama_index.readers.file import PyMuPDFReader

from app.models.document import Document
from app.services.embedding_service import get_embedding_model
from app.services.vector_store_service import get_vector_store


def index_document(document: Document) -> None:
    """
    Index a document from its stored Cloudinary URL.

    Flow:
    1. Save uploaded file temporarily
    2. Read file using LlamaIndex
    3. Split text into chunks/nodes
    4. Add metadata
    5. Generate embeddings
    6. Store embeddings in ChromaDB
    """

    with tempfile.TemporaryDirectory() as temp_dir:
        temp_path = Path(temp_dir) / document.filename

        response = httpx.get(document.cloudinary_url)
        response.raise_for_status()

        temp_path.write_bytes(response.content)

        reader = PyMuPDFReader()
        documents = reader.load(file_path=str(temp_path))

        splitter = SentenceSplitter(
            chunk_size=512,
            chunk_overlap=80,
        )

        nodes = splitter.get_nodes_from_documents(documents)

        for node in nodes:
            node.metadata["document_id"] = str(document.id)
            node.metadata["business_id"] = str(document.business_id)
            node.metadata["filename"] = document.filename
            node.metadata["cloudinary_url"] = document.cloudinary_url

        vector_store = get_vector_store(collection_name="documents")

        storage_context = StorageContext.from_defaults(
            vector_store=vector_store,
        )

        VectorStoreIndex(
            nodes=nodes,
            storage_context=storage_context,
            embed_model=get_embedding_model(),
        )