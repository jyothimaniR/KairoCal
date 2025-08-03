# backend/Dockerfile.bert-training
FROM python:3.11-slim

WORKDIR /app

# Install system dependencies for ML/AI
RUN apt-get update && apt-get install -y \
    gcc \
    g++ \
    postgresql-client \
    git \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY requirements/ ./requirements/
RUN pip install --no-cache-dir -r requirements/dev.txt

# Install additional ML dependencies for training
RUN pip install --no-cache-dir \
    jupyter \
    tensorboard \
    wandb \
    optuna

# Create necessary directories
RUN mkdir -p /app/models /app/data /app/results /app/logs

# Copy application code
COPY . .

# Set environment variables
ENV PYTHONPATH=/app
ENV TOKENIZERS_PARALLELISM=false

# Default command (can be overridden)
CMD ["python", "app/scripts/train_bert_priority_model.py"]