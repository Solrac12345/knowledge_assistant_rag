# EN: Multi-stage production Dockerfile for RAG Knowledge Assistant
# FR: Dockerfile de production multi-étapes pour l'Assistant de Connaissance RAG

# ─────────────────────────────────────────────────────────────
# Stage 1: Build dependencies with uv
# ─────────────────────────────────────────────────────────────
FROM ghcr.io/astral-sh/uv:python3.11-bookworm-slim AS builder

WORKDIR /app

# Copy dependency manifests
COPY pyproject.toml uv.lock* ./

# Install dependencies into a virtual environment
RUN uv sync --frozen --no-dev --no-editable

# Copy application source
COPY . .

# ─────────────────────────────────────────────────────────────
# Stage 2: Runtime (minimal image)
# ─────────────────────────────────────────────────────────────
FROM python:3.11-slim

WORKDIR /app

# Create non-root user for security
RUN groupadd -r appuser && useradd -r -g appuser -d /app -s /sbin/nologin appuser

# Copy virtual environment from builder
COPY --from=builder /app/.venv /app/.venv
COPY --from=builder /app /app

# 🔧 FIX: Create ALL directories appuser needs and set ownership
RUN mkdir -p /app/data/chroma /app/.cache /app/.local && \
    chown -R appuser:appuser /app/data /app/.cache /app/.local

# Environment configuration
ENV PATH="/app/.venv/bin:$PATH" \
    PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PORT=8000 \
    TRANSFORMERS_CACHE=/app/.cache \
    SENTENCE_TRANSFORMERS_HOME=/app/.cache

EXPOSE 8000

# Health check (increased start_period for model download)
HEALTHCHECK --interval=30s --timeout=10s --start-period=120s --retries=3 \
    CMD python -c "import urllib.request; urllib.request.urlopen('http://localhost:8000/')" || exit 1

# Drop root privileges
USER appuser

# Start Uvicorn with 2 workers
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--workers", "2"]