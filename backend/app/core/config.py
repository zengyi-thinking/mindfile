from typing import List
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    PROJECT_NAME: str = "MindFile"
    VERSION: str = "1.0.0"
    API_V1_STR: str = "/api/v1"
    
    # CORS设置
    ALLOWED_HOSTS: List[str] = ["*"]
    
    # 数据库设置
    POSTGRES_SERVER: str = "localhost"
    POSTGRES_USER: str = "postgres"
    POSTGRES_PASSWORD: str = "postgres"
    POSTGRES_DB: str = "mindfile"
    DATABASE_URL: str = f"postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_SERVER}/{POSTGRES_DB}"
    
    # Redis设置
    REDIS_URL: str = "redis://localhost:6379/0"
    
    # Elasticsearch设置
    ELASTICSEARCH_URL: str = "http://localhost:9200"
    
    # JWT设置
    SECRET_KEY: str = "your-secret-key"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 8  # 8 days
    
    class Config:
        case_sensitive = True
        env_file = ".env"

settings = Settings() 