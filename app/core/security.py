# EN: Security utilities: API key authentication middleware.
# FR: Utilitaires de sécurité : middleware d'authentification par clé API.

from fastapi import Depends, HTTPException, status, Request
from fastapi.security import APIKeyHeader

from app.core.settings import settings

# EN: Define the header name for API key
# FR: Définir le nom de l'en-tête pour la clé API
API_KEY_HEADER = APIKeyHeader(name="X-API-Key", auto_error=False)


async def verify_api_key(
    request: Request,
    api_key_header: str = Depends(API_KEY_HEADER),
) -> None:
    """
    EN: Verify the X-API-Key header matches the configured API_KEY.
        Raises 401 if missing, 403 if invalid.
    FR: Vérifier que l'en-tête X-API-Key correspond à API_KEY configurée.
        Lève 401 si manquant, 403 si invalide.
    """
    # EN: Skip authentication for public endpoints (health checks, docs)
    # FR: Ignorer l'authentification pour les endpoints publics (health checks, docs)
    public_paths = {"/", "/docs", "/redoc", "/openapi.json", "/health"}
    if request.url.path in public_paths or request.url.path.startswith("/static"):
        return

    # EN: Check if API key is provided
    # FR: Vérifier si la clé API est fournie
    if not api_key_header:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Missing API key. Provide it via X-API-Key header.",
            headers={"WWW-Authenticate": "ApiKey"},
        )

    # EN: Validate the key
    # FR: Valider la clé
    if api_key_header != settings.api_key:
        raise HTTPException(
            status_code=status.HTTP_03_FORBIDDEN,
            detail="Invalid API key.",
            headers={"WWW-Authenticate": "ApiKey"},
        )