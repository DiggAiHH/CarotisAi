FROM python:3.11-slim

LABEL maintainer="Carotis-AI <carotis@diggai.de>"
LABEL description="Hermes Agent — local AI orchestration for Carotis-AI"

# System deps (curl for healthcheck)
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Install Hermes Agent + lightweight deps
RUN pip install --no-cache-dir \
    hermes-agent>=0.3.0 \
    requests>=2.31.0 \
    toml>=0.10.2

# Copy skills and config
COPY hermes/skills/ ./skills/
COPY hermes/config.toml ./config.toml

# Schema access (for decision-tree validation skill)
COPY schemas/ ./schemas/

# Persistent memory volume
VOLUME ["/app/memory"]

EXPOSE 8200

HEALTHCHECK --interval=15s --timeout=5s --start-period=30s --retries=3 \
    CMD curl -sf http://localhost:8200/health || exit 1

ENV OLLAMA_URL="http://ollama:11434"

CMD ["hermes", "serve", "--config", "config.toml"]
