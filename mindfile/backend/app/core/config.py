import os
import secrets
from typing import Optional, Dict, Any, List
from pydantic_settings import BaseSettings
from pydantic import field_validator
from pathlib import Path

class Settings(BaseSettings):
    # 基本配置
    API_PREFIX: str = "/api"
    SECRET_KEY: str = secrets.token_urlsafe(32)
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 7  # 7天
    
    # CORS配置
    BACKEND_CORS_ORIGINS: List[str] = []
    
    # 数据库配置
    DATABASE_URL: str = os.getenv(
        "DATABASE_URL", 
        f"mysql+pymysql://root:Zhuqing5201314@localhost/mindfile"
    )
    
    # 文件上传配置
    UPLOAD_DIR: str = os.getenv("UPLOAD_DIR", "./uploads")
    MAX_UPLOAD_SIZE: int = 100 * 1024 * 1024  # 默认最大100MB
    
    # 默认管理员账户
    FIRST_ADMIN_EMAIL: str = os.getenv("FIRST_ADMIN_EMAIL", "admin@example.com")
    FIRST_ADMIN_PASSWORD: str = os.getenv("FIRST_ADMIN_PASSWORD", "admin123")
    
    # pydantic v2中使用model_config替代Config
    model_config = {
        "case_sensitive": True,
        "env_file": ".env"
    }

# 全局设置实例
settings = Settings()

# 确保上传目录存在
os.makedirs(settings.UPLOAD_DIR, exist_ok=True) 