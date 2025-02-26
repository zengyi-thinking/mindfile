from typing import Optional, List
from pydantic import BaseModel
from datetime import datetime

class TagBase(BaseModel):
    name: str
    color: Optional[str] = "#3498db"  # 默认颜色
    
class TagCreate(TagBase):
    pass

class TagUpdate(TagBase):
    name: Optional[str] = None
    
class Tag(TagBase):
    id: int
    created_at: datetime
    updated_at: datetime
    
    model_config = {
        "from_attributes": True
    }

class TagWithHierarchy(Tag):
    parent_tags: List['Tag'] = []
    child_tags: List['Tag'] = [] 