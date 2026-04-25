# EN: Base interface for all LLM clients.
# FR: Interface de base pour tous les clients LLM.

from abc import ABC, abstractmethod


class LLMClient(ABC):
    """
    EN: Abstract base class for any LLM backend (Dummy, Ollama, HF, etc.).
    FR: Classe de base abstraite pour tout backend LLM (Dummy, Ollama, HF, etc.).
    """

    @abstractmethod
    async def generate(self, prompt: str) -> str:
        """
        EN: Generate a text response from the LLM.
        FR: Générer une réponse textuelle depuis le LLM.
        """
        pass
