# AI Assistant

AI Assistant is a FastAPI document-assistant prototype exploring business-scoped retrieval and streamed chat responses. It combines PostgreSQL and SQLAlchemy for application data, Chroma and LlamaIndex for document retrieval, and Gemini for response generation.

The implementation includes JWT authentication, document upload, and in-process background indexing. Durable jobs, automated isolation tests, deployment configuration, and operational hardening remain areas for improvement.

## Architecture

- Versioned FastAPI routes under `/api/v1`: authentication, documents, and chat.
- PostgreSQL application data managed through async SQLAlchemy and Alembic migrations.
- Cloudinary document storage, with indexing coordinated by FastAPI background tasks.
- LlamaIndex retrieval backed by Chroma, with business-scoped filtering.
- Gemini response generation with streaming chat delivery.

```text
app/api/       Route handlers and authentication dependencies
app/core/      Configuration, lifecycle, security, and error handling
app/db/        Database session and model metadata
app/models/    Business, user, and document persistence
app/schemas/   Request and response contracts
app/services/  Authentication, storage, indexing, retrieval, and chat
app/jobs/      In-process indexing orchestration
migrations/    Alembic schema migrations
```

## Local setup

Requirements: Python 3.13+, uv, PostgreSQL, and separate development accounts for Gemini and Cloudinary.

```bash
git clone https://github.com/HaiderAli-Ravian/ai-assistant.git
cd ai-assistant
uv sync --frozen
```

Create an untracked `.env` file using these configuration keys. Supply your own development values; never commit real credentials.

```dotenv
DATABASE_URL=postgresql+asyncpg://USER:PASSWORD@localhost:5432/ai_assistant
JWT_SECRET_KEY=REPLACE_WITH_A_LONG_RANDOM_SECRET
CLOUDINARY_CLOUD_NAME=YOUR_CLOUD_NAME
CLOUDINARY_API_KEY=YOUR_API_KEY
CLOUDINARY_API_SECRET=YOUR_API_SECRET
CLOUDINARY_FOLDER=ai-assistant-dev
GOOGLE_API_KEY=YOUR_GOOGLE_API_KEY
GEMINI_MODEL=gemini-2.5-flash
CHROMA_PERSIST_DIR=./storage/chroma
```

Create the database, then apply migrations and start the API:

```bash
uv run alembic upgrade head
uv run fastapi dev app/main.py
```

Review the generated API documentation at `http://localhost:8000/docs`. Register a development user through the documented authentication endpoints, authorize with the returned token, and use synthetic documents to evaluate upload and chat. Provider usage may incur charges.

## Scope and limitations

- This is a reference prototype, separate from proprietary client work.
- Indexing uses in-process background tasks; it is not a durable queue with retry and recovery guarantees.
- Business-scoped retrieval needs automated cross-business isolation tests before production use.
- `scripts/test_models.py` is a model-import check, not a comprehensive test suite.
- Docker, CI, operational monitoring, upload-policy tests, and deployment instructions are not yet provided.
- No public live demo is advertised. Local startup instructions are based on the repository configuration and have not been verified against external provider accounts.
