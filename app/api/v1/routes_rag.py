# EN: RAG API endpoints.
# FR: Endpoints API pour le pipeline RAG.

import logging
import shutil
import tempfile
from pathlib import Path

from fastapi import APIRouter, File, HTTPException, Request, UploadFile

from app.api.v1.models_rag import ErrorResponse, IndexResponse, QueryResponse
from app.rag.pipeline import RAGPipeline

router = APIRouter()
logger = logging.getLogger(__name__)
# REMOVED: _pipeline = RAGPipeline()
# Reason: Initialization is now handled in main.py lifespan

@router.post(
    "/index",
    status_code=201,
    response_model=IndexResponse,
    responses={500: {"model": ErrorResponse}},
)
async def index_document(
    request: Request,  # <--- Access app.state here
    file: UploadFile = File(...),  # noqa: B008
) -> IndexResponse:
    if not file.filename:
        raise HTTPException(status_code=400, detail="Filename is required")

    # EN: Get the shared pipeline instance
    # FR: Récupérer l'instance partagée du pipeline
    pipeline: RAGPipeline = request.app.state.pipeline

    with tempfile.NamedTemporaryFile(delete=False, suffix=Path(file.filename).suffix) as tmp:
        tmp_path = Path(tmp.name)
        shutil.copyfileobj(file.file, tmp)

    try:
        pipeline.index_document(str(tmp_path))
        return IndexResponse(status="indexed", filename=file.filename)
    except Exception as e:
        logger.error("Indexing failed for %s: %s", file.filename, e, exc_info=True)
        raise HTTPException(status_code=500, detail="Internal server error during indexing") from e
    finally:
        tmp_path.unlink(missing_ok=True)


@router.get(
    "/ask",
    response_model=QueryResponse,
    responses={500: {"model": ErrorResponse}},
)
async def ask_question(
    request: Request,  # <--- Access app.state here
    query: str,
    top_k: int = 5,
) -> QueryResponse:
    if not query.strip():
        raise HTTPException(status_code=400, detail="Query cannot be empty")

    # EN: Get the shared pipeline instance
    # FR: Récupérer l'instance partagée du pipeline
    pipeline: RAGPipeline = request.app.state.pipeline

    try:
        answer = await pipeline.answer_question(query, top_k=top_k)
        return QueryResponse(query=query, answer=answer)
    except Exception as e:
        logger.error("Query failed: %s", e, exc_info=True)
        raise HTTPException(status_code=500, detail="Internal server error during query") from e
