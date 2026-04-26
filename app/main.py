# EN: FastAPI application entry point.
# FR: Point d'entrée de l'application FastAPI.

from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager

from fastapi import Depends, FastAPI

from app.api.v1.routes_rag import router as rag_router
from app.core.security import verify_api_key
from app.llm import get_llm_client
from app.rag.pipeline import RAGPipeline


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
    """
    EN: Application lifespan: Initialize RAG pipeline once at startup.
    FR: Cycle de vie : Initialiser le pipeline RAG une seule fois au démarrage.
    """
    # EN: Use the factory to get the correct LLM client (Ollama or Dummy) based on .env
    # FR: Utiliser la factory pour obtenir le client LLM correct (Ollama ou Dummy) selon .env
    app.state.pipeline = RAGPipeline(llm_client=get_llm_client())

    yield  # Application runs here


# EN: Create FastAPI app with lifespan
# FR: Créer l'application FastAPI avec cycle de vie
app = FastAPI(
    title="RAG Knowledge Assistant",
    description="A Mid-Pro RAG system built with Python 3.11+, FastAPI, ChromaDB, and Ollama.",
    version="0.1.0",
    lifespan=lifespan,
)

# EN: Include RAG router WITH authentication dependency
# FR: Inclure le routeur RAG AVEC dépendance d'authentification
app.include_router(
    rag_router,
    prefix="/api/v1/rag",
    tags=["rag"],
    dependencies=[Depends(verify_api_key)],  # ← Now Depends is imported
)


@app.get("/", tags=["health"])
async def health_check() -> dict[str, str]:
    """
    EN: Basic health check.
    FR: Vérification de santé basique.
    """
    return {"status": "ok", "environment": "development"}
