from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.core.app_state import initialize_app_state


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application startup and shutdown lifecycle."""

    initialize_app_state()

    yield