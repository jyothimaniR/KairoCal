# backend/app/config.py
from pydantic_settings import BaseSettings
from functools import lru_cache

class Settings(BaseSettings):
    # App
    app_name: str = "KairoCal"
    debug: bool = True
    
    # Database - Will use Docker service name when in container
    database_url: str = "postgresql://kairocal_user:Test123@postgres:5432/kairocal"
    
    # Redis
    redis_url: str = "redis://redis:6379"
    
    # AWS Region (kept for potential future use with boto3)
    aws_region: str = "eu-west-2"
    
    class Config:
        env_file = ".env"
        case_sensitive = False
        extra = "ignore"  # Ignore extra environment variables

@lru_cache()
def get_settings():
    return Settings()