from sqlalchemy import Column, Integer, String, ForeignKey, Text, Boolean
from sqlalchemy.orm import relationship
from backend.app.db.base import Base, TimestampMixin

class Post(Base, TimestampMixin):
    __tablename__ = "forum_posts"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True, nullable=False)
    content = Column(Text, nullable=False)
    owner_id = Column(Integer, ForeignKey("users.id"))
    
    # 帖子统计
    view_count = Column(Integer, default=0)
    like_count = Column(Integer, default=0)
    comment_count = Column(Integer, default=0)
    
    # 关系
    owner = relationship("User", back_populates="posts")
    comments = relationship("Comment", back_populates="post", cascade="all, delete-orphan")
    
    def __repr__(self):
        return f"<Post(id={self.id}, title={self.title})>"
    
class Comment(Base, TimestampMixin):
    __tablename__ = "forum_comments"
    
    id = Column(Integer, primary_key=True, index=True)
    content = Column(Text, nullable=False)
    owner_id = Column(Integer, ForeignKey("users.id"))
    post_id = Column(Integer, ForeignKey("forum_posts.id"))
    parent_id = Column(Integer, ForeignKey("forum_comments.id"), nullable=True)
    
    # 关系
    owner = relationship("User", back_populates="comments")
    post = relationship("Post", back_populates="comments")
    replies = relationship("Comment", back_populates="parent", cascade="all, delete-orphan")
    parent = relationship("Comment", back_populates="replies", remote_side=[id])
    
    def __repr__(self):
        return f"<Comment(id={self.id}, owner_id={self.owner_id})>" 