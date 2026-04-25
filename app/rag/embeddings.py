# EN: Embedding utilities for the RAG pipeline.
# FR: Utilitaires d'embedding pour le pipeline RAG.

from sentence_transformers import SentenceTransformer


class EmbeddingClient:
    """
    EN: Wrapper around SentenceTransformer for embedding generation.
    FR: Wrapper autour de SentenceTransformer pour la génération d'embeddings.
    """

    def __init__(self, model_name: str = "sentence-transformers/all-MiniLM-L6-v2") -> None:
        """
        EN: Initialize the embedding model.
        FR: Initialiser le modèle d'embedding.
        """
        self._model = SentenceTransformer(model_name)

    def embed_text(self, text: str) -> list[float]:
        """
        EN: Generate an embedding for a single text.
        FR: Générer un embedding pour un texte unique.
        """
        embedding = self._model.encode(text)
        return embedding.tolist()  # type: ignore[no-any-return]

    def embed_documents(self, texts: list[str]) -> list[list[float]]:
        """
        EN: Generate embeddings for multiple documents/chunks.
        FR: Générer des embeddings pour plusieurs documents/blocs.
        """
        embeddings = self._model.encode(texts)
        return [e.tolist() for e in embeddings]
