from typing import Optional, List
from pydantic import BaseModel
from datetime import datetime
from .user import User

class CommentBase(BaseModel):
    content: str

class CommentCreate(CommentBase):
    post_id: int
    parent_id: Optional[int] = None

class Comment(CommentBase):
    id: int
    owner_id: int
    post_id: int
    parent_id: Optional[int] = None
    created_at: datetime
    updated_at: datetime
    owner: User
    
    model_config = {
        "from_attributes": True
    }

class CommentWithReplies(Comment):
    replies: List[Comment] = []

class PostBase(BaseModel):
    title: str
    content: str

class PostCreate(PostBase):
    pass

class PostUpdate(BaseModel):
    title: Optional[str] = None
    content: Optional[str] = None

class Post(PostBase):
    id: int
    owner_id: int
    created_at: datetime
    updated_at: datetime
    view_count: int
    like_count: int
    comment_count: int
    owner: User
    
    model_config = {
        "from_attributes": True
    }

class PostWithComments(Post):
    comments: List[CommentWithReplies] = [] 