from pydantic_settings import BaseSettings
from functools import lru_cache

class Settings(BaseSettings):
    # App
    app_name: str = "KairoCal"
    debug: bool = True
    
    # Database
    database_url: str = "postgresql://kairocal_user:Test123@localhost:5432/kairocal"
    
    # Redis
    redis_url: str = "redis://localhost:6379"
    
    # AWS
    aws_region: str = "eu-west-2"
    cognito_user_pool_id: str = "eu-west-2_n6vDQdu5N"
    cognito_app_client_id: str = "cncih8g9fhdcnirv8q3vjht7g"
    
    # Security
    secret_key: str = "your-secret-key-here-change-in-production"
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 30
    
    class Config:
        env_file = ".env"

@lru_cache()
def get_settings():
    return Settings()