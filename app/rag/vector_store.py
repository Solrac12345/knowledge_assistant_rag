# EN: Vector store wrapper around ChromaDB for the RAG pipeline.
# FR: Wrapper de base de données vectorielle autour de ChromaDB pour le pipeline RAG.

import chromadb

from app.rag.embeddings import EmbeddingClient


class VectorStore:
    """
    EN: Simple wrapper for a ChromaDB collection.
    FR: Wrapper simple pour une collection ChromaDB.
    """

    def __init__(
        self,
        collection_name: str = "documents",
        persist_directory: str = "data/chroma",
        embedding_model: str = "sentence-transformers/all-MiniLM-L6-v2",
    ) -> None:
        """
        EN: Initialize ChromaDB persistent client and collection.
        FR: Initialiser le client persistant ChromaDB et la collection.
        """
        self._client = chromadb.PersistentClient(path=persist_directory)
        self._collection = self._client.get_or_create_collection(name=collection_name)
        self._embeddings = EmbeddingClient(model_name=embedding_model)

    def add_documents(self, texts: list[str], ids: list[str] | None = None) -> None:
        """
        EN: Add documents to the vector store.
        FR: Ajouter des documents dans la base vectorielle.
        """
        if ids is None:
            ids = [str(i) for i in range(len(texts))]

        embeddings = self._embeddings.embed_documents(texts)
        self._collection.add(
            ids=ids,
            documents=texts,
            embeddings=embeddings,
        )

    def query(self, query_text: str, top_k: int = 5) -> list[tuple[str, float]]:
        """
        EN: Query the most similar documents.
        FR: Rechercher les documents les plus similaires.
        """
        query_embedding = self._embeddings.embed_text(query_text)
        results = self._collection.query(
            query_embeddings=[query_embedding],
            n_results=top_k,
        )

        documents = results.get("documents", [[]])[0]
        distances = results.get("distances", [[]])[0]

        # Safely pair documents with distances (handle potential None values)
        # Safely pair documents with distances (handle potential None values)
        return [
            (doc, dist if dist is not None else 0.0)
            for doc, dist in zip(documents, distances, strict=True)
        ]
