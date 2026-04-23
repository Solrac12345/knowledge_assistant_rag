# EN: Placeholder for RAG API routes.
# FR: Espace réservé pour les routes API du RAG.

from fastapi import APIRouter

router = APIRouter()


@router.get("/placeholder")
def placeholder() -> dict[str, str]:
    """
    EN: Temporary endpoint to verify RAG router registration.
    FR: Endpoint temporaire pour vérifier l'enregistrement du routeur RAG.
    """
    return {"message": "RAG API placeholder"}
