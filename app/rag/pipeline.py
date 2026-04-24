# EN: End-to-end RAG pipeline orchestration.
# FR: Orchestration de bout en bout du pipeline RAG.

from app.llm.client import DummyLLMClient, LLMClient
from app.rag.chunking import recursive_chunk
from app.rag.ingestion import ingest_document
from app.rag.retrieval import Retriever
from app.rag.vector_store import VectorStore


class RAGPipeline:
    """
    EN: High-level RAG pipeline: ingest → chunk → index → retrieve → generate.
    FR: Pipeline RAG de haut niveau : ingestion → découpage → indexation → recherche → génération.
    """

    def __init__(
        self,
        vector_store: VectorStore | None = None,
        retriever: Retriever | None = None,
        llm_client: LLMClient | None = None,
    ) -> None:
        """
        EN: Initialize the RAG pipeline with optional custom components.
        FR: Initialiser le pipeline RAG avec des composants personnalisés optionnels.
        """
        self._store = vector_store or VectorStore()
        self._retriever = retriever or Retriever(self._store)
        self._llm = llm_client or DummyLLMClient()

    def index_document(self, path: str) -> None:
        """
        EN: Ingest a document from disk, chunk it, and add to the vector store.
        FR: Ingérer un document depuis le disque, le découper et l'ajouter à la base vectorielle.
        """
        text = ingest_document(path)
        chunks: list[str] = recursive_chunk(text)
        ids = [f"{path}::chunk-{i}" for i in range(len(chunks))]
        self._store.add_documents(chunks, ids=ids)
        # PersistentClient auto-saves; .persist() is deprecated in modern ChromaDB

    def answer_question(self, query: str, top_k: int = 5) -> str:
        """
        EN: Retrieve relevant chunks and ask the LLM to answer based on them.
        FR: Récupérer les blocs pertinents et demander au LLM de répondre à partir de ceux-ci.
        """
        documents = self._retriever.retrieve(query, top_k=top_k)
        context = "\n\n".join(documents)

        prompt = (
            "You are a helpful assistant. Use the following context to answer the question.\n\n"
            f"Context:\n{context}\n\n"
            f"Question: {query}\n\n"
            "Answer:"
        )

        return self._llm.generate(prompt)
