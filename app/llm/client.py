# EN: LLM client abstraction for the RAG pipeline.
# FR: Abstraction de client LLM pour le pipeline RAG.

from typing import Protocol


class LLMClient(Protocol):
    """
    EN: Protocol defining the interface for any LLM client.
    FR: Protocole définissant l'interface pour tout client LLM.
    """

    def generate(self, prompt: str) -> str:
        """
        EN: Generate a response given a prompt.
        FR: Générer une réponse à partir d'un prompt.
        """
        ...


class DummyLLMClient:
    """
    EN: Simple placeholder LLM client used during early development.
    FR: Client LLM factice utilisé pendant le développement initial.
    """

    def generate(self, prompt: str) -> str:
        """
        EN: Return a deterministic placeholder response.
        FR: Retourner une réponse factice déterministe.
        """
        return f"[DUMMY LLM RESPONSE] {prompt[:200]}"
