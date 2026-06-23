from app.core.app_state import AppState


def get_embedding_model():
    """Return the application's embedding model."""

    return AppState.embedding_model