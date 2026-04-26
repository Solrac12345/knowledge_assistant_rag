# EN: Application settings using Pydantic v2 Settings.
# FR: Paramètres de l'application utilisant Pydantic v2 Settings.

from pathlib import Path
from typing import Literal

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """
    EN: Centralized application configuration.
    FR: Configuration centralisée de l'application.
    """

    environment: str = "development"
    chroma_db_path: Path = Path("data/chroma")
    embedding_model: str = "sentence-transformers/all-MiniLM-L6-v2"
    llm_api_key: str | None = None
    llm_base_url: str | None = None

    # 🔐 API Key for endpoint protection (required in production)
    api_key: str = Field(
        default="dev-key-do-not-use-in-production",
        description="API key for protecting /api/v1/rag/* endpoints",
        validation_alias="API_KEY",  # ← Pydantic v2 syntax (not 'env')
    )

    # 🔑 NEW: LLM Provider selector (matches factory logic)
    llm_provider: Literal["ollama", "dummy"] = "dummy"

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",  # Prevents Windows encoding issues
        extra="ignore",
    )


settings = Settings()
