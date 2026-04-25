# EN: Ollama-based LLM client for local inference.
# FR: Client LLM basé sur Ollama pour l'inférence locale.

import logging

import httpx

from app.llm.base import LLMClient

logger = logging.getLogger(__name__)


class OllamaLLMClient(LLMClient):
    """
    EN: Local LLM client using Ollama (Qwen 2.5) via async HTTP.
    FR: Client LLM local utilisant Ollama (Qwen 2.5) via HTTP asynchrone.
    """

    def __init__(
        self,
        model: str = "qwen2.5:7b",
        host: str = "http://localhost:11434",
        timeout: float = 60.0,
    ) -> None:
        """
        EN: Initialize the Ollama client.
        FR: Initialiser le client Ollama.
        """
        self.model = model
        self.host = host.rstrip("/")
        self.timeout = timeout

    # ... imports and class definition ...

    async def generate(self, prompt: str) -> str:
        """
        EN: Generate text using Ollama's /api/generate endpoint.
        FR: Générer du texte via l'endpoint /api/generate d'Ollama.
        """
        url = f"{self.host}/api/generate"
        payload = {"model": self.model, "prompt": prompt, "stream": False}

        try:
            async with httpx.AsyncClient(timeout=self.timeout) as client:
                response = await client.post(url, json=payload)
                response.raise_for_status()
                data = response.json()
                return data.get("response", "").strip()  # type: ignore[no-any-return]

        except httpx.TimeoutException:
            logger.error("Ollama request timed out for model %s", self.model)
            raise
        except httpx.HTTPStatusError as e:
            logger.error("Ollama returned HTTP %s: %s", e.response.status_code, e)
            raise
        except Exception as e:
            logger.error("Unexpected error calling Ollama: %s", e, exc_info=True)
            raise
