# EN: Main entry point of the FastAPI application.
# FR: Point d'entrée principal de l'application FastAPI.

from fastapi import FastAPI

from app.api.v1.routes_rag import router as rag_router
from app.core.logging import configure_logging
from app.core.settings import settings

# EN: Initialize logging before creating the app.
# FR: Initialiser les logs avant de créer l'application.
configure_logging()

# EN: Create FastAPI instance with OpenAPI metadata.
# FR: Créer l'instance FastAPI avec les métadonnées OpenAPI.
app = FastAPI(
    title="RAG Knowledge Assistant",
    version="0.1.0",
    description="RAG system built with Python 3.11+",
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/openapi.json",
)

# EN: Include RAG API routes.
# FR: Inclure les routes de l'API RAG.
app.include_router(rag_router, prefix="/api/v1/rag")


# EN: Root endpoint for health check.
# FR: Endpoint racine pour vérifier l'état du service.
@app.get("/")
def root() -> dict[str, str]:
    """Health check endpoint returning service status."""
    return {"status": "ok", "environment": settings.environment}
