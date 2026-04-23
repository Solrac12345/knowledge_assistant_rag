# EN: Logging configuration for the application.
# FR: Configuration du système de logs pour l'application.

import logging
from logging import Logger


def configure_logging() -> None:
    """
    EN: Configure root logger with consistent formatting.
    FR: Configurer le logger racine avec un formatage cohérent.
    """
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
        force=True,  # Ensure reconfiguration works in tests/reloads
    )


def get_logger(name: str) -> Logger:
    """
    EN: Get a named logger instance (consistent with app logging config).
    FR: Obtenir une instance de logger nommée (cohérente avec la config de l'app).

    Args:
        name: Typically __name__ of the calling module.

    Returns:
        Configured Logger instance.
    """
    return logging.getLogger(name)
