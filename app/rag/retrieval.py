# EN: Retrieval logic for the RAG pipeline.
# FR: Logique de récupération pour le pipeline RAG.

import logging

from app.rag.vector_store import VectorStore

logger = logging.getLogger(__name__)


class Retriever:
    """
    EN: Handles semantic retrieval from the vector store.
    FR: Gère la récupération sémantique depuis la base vectorielle.
    """

    def __init__(self, vector_store: VectorStore) -> None:
        """
        EN: Initialize the retriever with a vector store.
        FR: Initialiser le récupérateur avec une base vectorielle.
        """
        self._store = vector_store

    def retrieve(self, query: str, top_k: int = 5) -> list[str]:
        """
        EN: Retrieve top_k relevant documents for a query.
        FR: Récupérer les top_k documents pertinents pour une requête.
        """
        try:
            # EN: Call the correct method name: retrieve() not query()
            # FR: Appeler le nom de méthode correct : retrieve() et non query()
            return self._store.retrieve(query, top_k=top_k)
        except Exception as e:
            logger.error("Retrieval failed for query '%s': %s", query, e, exc_info=True)
            return []