from typing import Optional, List
from pydantic import BaseModel, EmailStr, Field, field_validator
from datetime import datetime

class UserBase(BaseModel):
    username: str
    email: EmailStr
    is_admin: Optional[bool] = False
    avatar_url: Optional[str] = None

    # Pydantic v2 配置方式
    model_config = {
        "from_attributes": True  # 替代原来的 "from_attributes": True
    }

class UserCreate(UserBase):
    password: str
    
    @field_validator('password')
    def password_min_length(cls, v):
        if len(v) < 6:
            raise ValueError('密码长度必须至少为6位')
        return v

class UserUpdate(BaseModel):
    username: Optional[str] = None
    email: Optional[EmailStr] = None
    avatar_url: Optional[str] = None
    password: Optional[str] = None
    
    @field_validator('password')
    def password_min_length(cls, v):
        if v is not None and len(v) < 6:
            raise ValueError('密码长度必须至少为6位')
        return v

class UserInDB(UserBase):
    id: int
    hashed_password: str
    is_active: bool = True
    created_at: datetime
    updated_at: datetime
    
    model_config = {
        "from_attributes": True  # 替代原来的 "from_attributes": True
    }

class User(UserBase):
    id: int
    is_active: bool
    created_at: datetime
    updated_at: datetime
    
    model_config = {
        "from_attributes": True  # 替代原来的 "from_attributes": True
    }

class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"
    
class TokenPayload(BaseModel):
    sub: int  # 用户ID
    exp: datetime  # 过期时间 