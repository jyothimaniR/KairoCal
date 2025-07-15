# backend/app/config.py
from pydantic_settings import BaseSettings
from functools import lru_cache

class Settings(BaseSettings):
    # App
    app_name: str = "KairoCal"
    debug: bool = True
    
    # Database - Use IPv4 explicitly (127.0.0.1 instead of localhost)
    database_url: str = "postgresql://kairocal_user:Test123@127.0.0.1:5432/kairocal"
    
    # Redis
    redis_url: str = "redis://127.0.0.1:6379"
    
    # AWS Cognito - Your preserved configuration
    aws_region: str = "eu-west-2"
    cognito_user_pool_id: str = "eu-west-2_n6vDQdu5N"
    cognito_app_client_id: str = "cncih8g9fhdcnirv8q3vjht7g"
    
    # Security
    secret_key: str = "your-secret-key-here-change-in-production"
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 30
    
    class Config:
        env_file = ".env"
        case_sensitive = False

@lru_cache()
def get_settings():
    return Settings()