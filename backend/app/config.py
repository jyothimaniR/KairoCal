# backend/app/config.py
from pydantic_settings import BaseSettings
from pydantic import ConfigDict
from functools import lru_cache

class Settings(BaseSettings):
    # App
    app_name: str = "KairoCal"
    app_debug: bool = True
    
    # Database - Will use Docker service name when in container
    database_url: str = "postgresql://kairocal_user:Test123@postgres:5432/kairocal"
    
    # Redis
    redis_url: str = "redis://redis:6379"
    
    # AWS Region (kept for potential future use with boto3)
    aws_region: str = "eu-west-2"
    
    # BERT/ML Configuration
    # Path is relative to the project root (WORKDIR=/app in Docker). Our trained
    # In the container, build context copies backend/models -> /app/models
    # so default to models/bert_priority_classifier (relative to /app)
    bert_model_path: str = "models/bert_priority_classifier"
    training_data_path: str = "data/training"
    model_confidence_threshold: float = 0.85
    device_preference: str = "auto"  # auto, cpu, cuda
    batch_size: int = 16
    max_sequence_length: int = 512
    priority_levels: int = 5  # 1=Very Low, 2=Low, 3=Medium, 4=High, 5=Critical
    
    # Pydantic v2 configuration (replaces legacy inner Config class)
    # We override protected_namespaces to DROP the default "model_" so fields named model_* are allowed
    model_config = ConfigDict(
        env_file=".env",
        case_sensitive=False,
        extra="ignore",
        protected_namespaces=("settings_",),  # allow model_* usage elsewhere in code
    )

@lru_cache()
def get_settings():
    return Settings()