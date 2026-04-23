# EN: Application settings using Pydantic v2 Settings.
# FR: Paramètres de l'application utilisant Pydantic v2 Settings.

from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """
    EN: Centralized application configuration.
    FR: Configuration centralisée de l'application.
    """

    # EN: Environment name (dev, prod, staging)
    # FR: Nom de l'environnement (dev, prod, staging)
    environment: str = "development"

    # EN: ChromaDB storage path
    # FR: Chemin de stockage pour ChromaDB
    chroma_db_path: Path = Path("data/chroma")

    # EN: Embedding model name
    # FR: Nom du modèle d'embedding
    embedding_model: str = "sentence-transformers/all-MiniLM-L6-v2"

    # EN: LLM API configuration
    # FR: Configuration API pour le LLM
    llm_api_key: str | None = None
    llm_base_url: str | None = None

    # EN: Pydantic v2 configuration
    # FR: Configuration Pydantic v2
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")


settings = Settings()
