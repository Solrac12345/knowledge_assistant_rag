# EN: Placeholder for Pydantic v2 schemas.
# FR: Espace réservé pour les schémas Pydantic v2.

from pydantic import BaseModel


class PlaceholderSchema(BaseModel):
    """
    EN: Temporary schema for API request/response validation.
    FR: Schéma temporaire pour la validation des requêtes/réponses API.
    """

    message: str
