from fastapi import FastAPI

from app.api.v1.routes import api_router
from app.core.lifespan import lifespan
from app.core.config import settings
from fastapi.exceptions import RequestValidationError
from app.core.exceptions import ApiException
from app.core.handlers import api_exception_handler, validation_exception_handler

app = FastAPI(
    title=settings.APP_NAME,
    version="1.0.0",
    lifespan=lifespan,
)

app.add_exception_handler(ApiException, api_exception_handler)
app.add_exception_handler(RequestValidationError, validation_exception_handler)

app.include_router(api_router)


@app.get("/")
async def root():
    return {"message": "AI Assistant API running"}