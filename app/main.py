# EN: FastAPI application entry point.
# FR: Point d'entrée de l'application FastAPI.

from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager

from fastapi import Depends, FastAPI, Request
from fastapi.responses import JSONResponse
from slowapi.errors import RateLimitExceeded
from slowapi.middleware import SlowAPIMiddleware

from app.api.v1.routes_rag import router as rag_router
from app.core.limiter import limiter
from app.core.security import verify_api_key
from app.core.settings import settings
from app.llm import get_llm_client
from app.rag.pipeline import RAGPipeline


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
    """
    EN: Application lifespan: Initialize RAG pipeline once at startup.
    FR: Cycle de vie : Initialiser le pipeline RAG une seule fois au démarrage.
    """
    app.state.pipeline = RAGPipeline(llm_client=get_llm_client())
    yield


app = FastAPI(
    title="RAG Knowledge Assistant",
    description="A Mid-Pro RAG system built with Python 3.11+, FastAPI, ChromaDB, and Ollama.",
    version="0.1.0",
    lifespan=lifespan,
)

# EN: Attach limiter to app state & add middleware for automatic headers
# FR: Attacher le limiteur à l'état de l'app & ajouter le middleware pour les en-têtes automatiques
app.state.limiter = limiter
app.add_middleware(SlowAPIMiddleware)


@app.exception_handler(RateLimitExceeded)
async def rate_limit_handler(request: Request, exc: RateLimitExceeded) -> JSONResponse:
    retry_after = getattr(exc, "retry_after", 60)

    return JSONResponse(
        status_code=429,
        content={
            "error": "rate_limit_exceeded",
            "detail": (
                f"Too many requests. Limit: {settings.rate_limit_requests} per {settings.rate_limit_window}s."
            ),  # ✅ Removed type: ignore
            "retry_after": retry_after,
        },
        headers={"Retry-After": str(retry_after)},
    )


app.include_router(
    rag_router,
    prefix="/api/v1/rag",
    tags=["rag"],
    dependencies=[Depends(verify_api_key)],
)


@app.get("/", tags=["health"])
async def health_check() -> dict[str, str]:
    return {"status": "ok", "environment": "development"}
