# EN: ChromaDB vector store wrapper for the RAG pipeline.
# FR: Wrapper ChromaDB pour la base vectorielle du pipeline RAG.

import logging
from pathlib import Path
from typing import Optional

import chromadb
from chromadb.config import Settings as ChromaSettings

from app.core.settings import settings
from app.rag.embeddings import EmbeddingClient

logger = logging.getLogger(__name__)


class VectorStore:
    """
    EN: Wrapper around ChromaDB PersistentClient for document storage & retrieval.
    FR: Wrapper autour de ChromaDB PersistentClient pour le stockage et la récupération de documents.
    """

    def __init__(
        self,
        collection_name: str = "rag_documents",
        persist_directory: Optional[Path] = None,
    ) -> None:
        """
        EN: Initialize the ChromaDB persistent client and collection.
        FR: Initialiser le client persistant ChromaDB et la collection.
        """
        self._persist_dir = persist_directory or settings.chroma_db_path
        self._persist_dir.mkdir(parents=True, exist_ok=True)

        self._client = chromadb.PersistentClient(
            path=str(self._persist_dir),
            settings=ChromaSettings(anonymized_telemetry=False),
        )
        self._collection = self._client.get_or_create_collection(name=collection_name)
        self._embedder = EmbeddingClient(model_name=settings.embedding_model)

    def add_documents(self, documents: list[str], ids: list[str]) -> None:
        """
        EN: Add documents to the vector store with auto-generated embeddings.
        FR: Ajouter des documents à la base vectorielle avec embeddings auto-générés.
        """
        if not documents:
            return

        embeddings = self._embedder.embed_documents(documents)
        
        # EN: ChromaDB accepts list[list[float]] at runtime; stubs are overly strict
        # FR: ChromaDB accepte list[list[float]] à l'exécution; les stubs sont trop stricts
        self._collection.add(
            ids=ids,
            documents=documents,
            embeddings=embeddings,  # type: ignore[arg-type]
        )

    def retrieve(self, query: str, top_k: int = 5) -> list[str]:
        """
        EN: Retrieve the top_k most relevant documents for a query.
        FR: Récupérer les top_k documents les plus pertinents pour une requête.
        """
        query_embedding = self._embedder.embed_text(query)
        
        # EN: ChromaDB accepts list[float] at runtime; stubs are overly strict
        # FR: ChromaDB accepte list[float] à l'exécution; les stubs sont trop stricts
        results = self._collection.query(
            query_embeddings=[query_embedding],  # type: ignore[arg-type]
            n_results=top_k,
            include=["documents"],
        )

        # EN: Handle Optional return types safely
        # FR: Gérer les types de retour Optionnels de manière sûre
        documents = results.get("documents")
        if documents and documents[0]:
            return documents[0]
        
        return []