# EN: Rate limiter configuration using SlowAPI.
# FR: Configuration du limiteur de débit avec SlowAPI.

from typing import TYPE_CHECKING

from slowapi import Limiter
from slowapi.util import get_remote_address

if TYPE_CHECKING:
    pass

from app.core.settings import settings

# EN: Initialize limiter with in-memory storage (swap to "redis://..." in production)
# FR: Initialiser le limiteur avec stockage en mémoire (remplacer par "redis://..." en prod)
limiter = Limiter(
    key_func=get_remote_address,
    storage_uri="memory://",
    default_limits=[f"{settings.rate_limit_requests}/{settings.rate_limit_window}seconds"],
)
