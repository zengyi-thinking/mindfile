from typing import Optional, List, Dict, Any
from pydantic import BaseModel
from datetime import datetime
from .tag import Tag

class MaterialBase(BaseModel):
    title: str
    description: Optional[str] = None
    
class MaterialCreate(MaterialBase):
    content: Optional[str] = None
    file_type: Optional[str] = None
    tags: Optional[List[int]] = None  # 标签ID列表
    mindmap_id: Optional[int] = None
    is_public: bool = False

class MaterialUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    content: Optional[str] = None
    file_type: Optional[str] = None
    tags: Optional[List[int]] = None
    mindmap_id: Optional[int] = None
    is_public: Optional[bool] = None

class Material(MaterialBase):
    id: int
    owner_id: int
    file_path: Optional[str] = None
    file_type: Optional[str] = None
    created_at: datetime
    updated_at: datetime
    view_count: int
    like_count: int
    is_public: bool = False
    
    model_config = {
        "from_attributes": True
    }

class MaterialWithDetails(Material):
    tags: List[Tag] = []
    mindmap_id: Optional[int] = None 