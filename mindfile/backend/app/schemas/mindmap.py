from typing import List, Dict, Any, Optional
from pydantic import BaseModel
from datetime import datetime
from .tag import Tag

# 共享属性
class MindMapBase(BaseModel):
    title: str
    description: Optional[str] = None
    content: Optional[str] = None

# 创建思维导图时使用
class MindMapCreate(MindMapBase):
    tags: Optional[List[int]] = None  # 标签ID列表
    data: Optional[Dict[str, Any]] = None  # 思维导图数据

# 更新思维导图时使用
class MindMapUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    tags: Optional[List[int]] = None  # 标签ID列表
    data: Optional[Dict[str, Any]] = None  # 思维导图数据

# API响应使用
class MindMapResponse(MindMapBase):
    id: int
    user_id: int
    created_at: datetime
    updated_at: datetime
    
    class Config:
        orm_mode = True

class MindMap(MindMapBase):
    id: int
    owner_id: int
    created_at: datetime
    updated_at: datetime
    
    model_config = {
        "from_attributes": True
    }

class MindMapWithDetails(MindMap):
    tags: List[Tag] = []
    data: Dict[str, Any]  # 思维导图数据 