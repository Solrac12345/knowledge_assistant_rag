# EN: Retrieval utilities for the RAG pipeline.
# FR: Utilitaires de recherche pour le pipeline RAG.

from app.rag.vector_store import VectorStore


class Retriever:
    """
    EN: High-level retriever built on top of the vector store.
    FR: Composant de haut niveau pour la recherche basé sur la base vectorielle.
    """

    def __init__(self, vector_store: VectorStore | None = None) -> None:
        """
        EN: Initialize retriever with an optional vector store instance.
        FR: Initialiser le retriever avec une instance de base vectorielle optionnelle.
        """
        self._store = vector_store or VectorStore()

    def retrieve(self, query: str, top_k: int = 5) -> list[str]:
        """
        EN: Retrieve the most relevant documents for a query.
        FR: Récupérer les documents les plus pertinents pour une requête.
        """
        results = self._store.query(query_text=query, top_k=top_k)
        return [doc for doc, _score in results]
