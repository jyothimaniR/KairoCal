FROM python:3.11-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    postgresql-client \
    && rm -rf /var/lib/apt/lists/*

# Run transformers in offline mode and reduce noisy warnings
ENV TRANSFORMERS_OFFLINE=1 \
    HF_HUB_DISABLE_TELEMETRY=1 \
    TOKENIZERS_PARALLELISM=false

COPY requirements/ ./requirements/

# Unified image: install full development (runtime + ML) dependencies for complete API (NLP, analytics, conflicts, websocket)
RUN pip install --no-cache-dir -r requirements/dev.txt

# Copy application code
COPY . .

EXPOSE 8000

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]