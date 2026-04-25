# EN: Pydantic models for RAG API responses.
# FR: Modèles Pydantic pour les réponses de l'API RAG.

from pydantic import BaseModel, Field


class IndexResponse(BaseModel):
    """
    EN: Response model for successful document indexing.
    FR: Modèle de réponse pour l'indexation réussie d'un document.
    """

    status: str = Field(..., description="EN: Operation status / FR: Statut de l'opération")
    filename: str = Field(
        ..., description="EN: Name of the indexed file / FR: Nom du fichier indexé"
    )


class QueryResponse(BaseModel):
    """
    EN: Response model for RAG query results.
    FR: Modèle de réponse pour les résultats de requête RAG.
    """

    query: str = Field(
        ..., description="EN: Original user query / FR: Requête originale de l'utilisateur"
    )
    answer: str = Field(
        ...,
        description="EN: Generated answer from the RAG pipeline / FR: Réponse générée par le pipeline RAG",
    )


class ErrorResponse(BaseModel):
    """
    EN: Standardized error response model.
    FR: Modèle de réponse d'erreur standardisé.
    """

    detail: str = Field(..., description="EN: Error description / FR: Description de l'erreur")
