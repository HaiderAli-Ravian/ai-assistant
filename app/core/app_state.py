from llama_index.embeddings.huggingface import HuggingFaceEmbedding


class AppState:
    """Container for application-level shared resources."""

    embedding_model = None


def initialize_app_state() -> None:
    """Initialize shared application resources."""

    AppState.embedding_model = HuggingFaceEmbedding(
        model_name="BAAI/bge-small-en-v1.5",
    )