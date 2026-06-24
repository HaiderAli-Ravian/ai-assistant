from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    APP_NAME: str = "RAG Chatbot"
    ENV: str = "development"

    DATABASE_URL: str

    JWT_SECRET_KEY: str
    JWT_ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 1440

    CLOUDINARY_CLOUD_NAME: str
    CLOUDINARY_API_KEY: str
    CLOUDINARY_API_SECRET: str
    CLOUDINARY_FOLDER: str

    GOOGLE_API_KEY: str
    GEMINI_MODEL: str = "gemini-2.5-flash"

    CHROMA_PERSIST_DIR: str = "./storage/chroma"

    model_config = SettingsConfigDict(env_file=".env")


settings = Settings()