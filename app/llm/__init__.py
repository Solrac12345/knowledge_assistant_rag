# EN: Public exports and factory for the LLM package.
# FR: Exports publics et factory pour le package LLM.

from .base import LLMClient
from .dummy_client import DummyLLMClient
from .ollama_client import OllamaLLMClient

__all__ = [
    "LLMClient",
    "DummyLLMClient",
    "OllamaLLMClient",
    "get_llm_client",
]


def get_llm_client() -> LLMClient:
    """
    EN: Factory function that returns the configured LLM client based on .env.
    FR: Fonction factory qui retourne le client LLM configuré selon .env.
    """
    from app.core.settings import settings

    if settings.llm_provider == "ollama":
        return OllamaLLMClient()

    # Default fallback
    return DummyLLMClient()
