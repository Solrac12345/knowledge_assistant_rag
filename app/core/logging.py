# EN: Production logging configuration.
# FR: Configuration de journalisation de production.

import logging
import sys
import uuid
from time import time
from typing import Any

from fastapi import Request, Response
from pythonjsonlogger import jsonlogger  # ✅ Removed unused ignore

# EN: Initialize the application logger
# FR: Initialiser le logger de l'application
logger = logging.getLogger("rag_assistant")
logger.setLevel(logging.INFO)


class CustomJsonFormatter(jsonlogger.JsonFormatter):  # type: ignore[misc]
    """
    EN: Custom formatter to add fields like process time and request ID.
    FR: Formateur personnalisé pour ajouter des champs comme le temps de traitement et l'ID de requête.
    """

    def add_fields(
        self, log_record: dict[str, Any], record: logging.LogRecord, message_dict: dict[str, Any]
    ) -> None:
        super().add_fields(log_record, record, message_dict)

        # EN: Ensure standard fields are present and correctly named
        # FR: S'assurer que les champs standards sont présents et correctement nommés
        if not log_record.get("timestamp"):
            log_record["timestamp"] = self.formatTime(record, record.created)

        if log_record.get("level"):
            log_record["level"] = log_record["level"].upper()
        else:
            log_record["level"] = record.levelname


def setup_logging() -> None:
    """
    EN: Configure the root logger to output JSON to stdout.
    FR: Configurer le logger racine pour sortir du JSON vers stdout.
    """
    if logger.handlers:
        for handler in logger.handlers:
            logger.removeHandler(handler)

    handler = logging.StreamHandler(sys.stdout)
    formatter = CustomJsonFormatter("%(timestamp)s %(level)s %(name)s %(message)s")
    handler.setFormatter(formatter)
    logger.addHandler(handler)

    logger.info("Structured logging initialized.")


async def logging_middleware(request: Request, call_next: Any) -> Response:
    """
    EN: Middleware to log every request with correlation IDs and latency.
    FR: Middleware pour logger chaque requête avec des IDs de corrélation et la latence.
    """
    start_time = time()

    correlation_id = request.headers.get("X-Request-ID", str(uuid.uuid4()))
    request.state.correlation_id = correlation_id

    response: Response = await call_next(request)

    process_time = time() - start_time

    response.headers["X-Request-ID"] = correlation_id

    logger.info(
        f"{request.method} {request.url.path}",
        extra={
            "correlation_id": correlation_id,
            "method": request.method,
            "path": request.url.path,
            "status_code": response.status_code,
            "process_time": f"{process_time:.4f}s",
            "ip": request.client.host if request.client else None,
        },
    )

    return response
