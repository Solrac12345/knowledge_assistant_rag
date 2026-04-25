# EN: Concrete LLM client implementations.
# FR: Implémentations concrètes des clients LLM.

from app.llm.base import LLMClient


class DummyLLMClient(LLMClient):
    """
    EN: Simple placeholder LLM client used during early development.
    FR: Client LLM factice utilisé pendant le développement initial.
    """

    async def generate(self, prompt: str) -> str:
        """
        EN: Return a deterministic placeholder response.
        FR: Retourner une réponse factice déterministe.
        """
        return f"[DUMMY LLM RESPONSE] {prompt[:200]}"
