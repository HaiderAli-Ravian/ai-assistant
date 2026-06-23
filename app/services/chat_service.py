from app.services.llm_service import generate_answer, stream_answer
from app.services.retrieval_service import search_documents
from collections.abc import Generator
import json



def build_rag_prompt(question: str, chunks: list[dict]) -> str:
    """Build the RAG prompt from retrieved chunks."""

    context = "\n\n---\n\n".join(
        chunk["text"] for chunk in chunks
    )

    return f"""
You are a helpful AI assistant.

Answer the user's question using only the provided context.
If the answer is not in the context, say you don't know.

Return the answer in clean Markdown.

Context:
{context}

Question:
{question}

Answer:
""".strip()


def chat_with_documents(message: str, top_k: int = 5) -> dict:
    """Answer a user message using retrieved document context."""

    chunks = search_documents(
        query=message,
        top_k=top_k,
    )

    prompt = build_rag_prompt(
        question=message,
        chunks=chunks,
    )

    answer = generate_answer(prompt)

    sources = build_unique_sources(chunks)

    return {
        "answer": answer,
        "sources": sources,
    }


def stream_chat_with_documents(message: str, top_k: int = 5):
    chunks = search_documents(query=message, top_k=top_k)

    sources = build_unique_sources(chunks)

    yield format_sse_event({
        "type": "metadata",
        "citations": sources,
    })

    prompt = build_rag_prompt(question=message, chunks=chunks)

    for token in stream_answer(prompt):
        yield format_sse_event({
            "type": "chunk",
            "content": token,
        })

    yield format_sse_event({
        "type": "done",
    })


def format_sse_event(payload: dict) -> str:
    return f"data: {json.dumps(payload)}\n\n"


def build_unique_sources(chunks: list[dict]) -> list[dict]:
    """Build unique source list from retrieved chunks."""

    seen_document_ids = set()
    sources = []

    for chunk in chunks:
        metadata = chunk["metadata"]
        document_id = metadata.get("document_id")

        if document_id in seen_document_ids:
            continue

        seen_document_ids.add(document_id)

        sources.append(
            {
                "filename": metadata.get("filename"),
                "document_id": document_id,
                "cloudinary_url": metadata.get("cloudinary_url"),
            }
        )

    return sources