from sqlalchemy import Column, Integer, String, ForeignKey, Boolean
from sqlalchemy.orm import relationship
from app.db.base import Base, TimestampMixin

class Post(Base, TimestampMixin):
    __tablename__ = "posts"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True, nullable=False)
    content = Column(String, nullable=False)
    author_id = Column(Integer, ForeignKey("users.id"))
    is_pinned = Column(Boolean, default=False)  # 是否置顶
    
    # 统计数据
    view_count = Column(Integer, default=0)
    like_count = Column(Integer, default=0)
    
    # 关系
    author = relationship("User", back_populates="posts")
    comments = relationship("Comment", back_populates="post")

class Comment(Base, TimestampMixin):
    __tablename__ = "comments"

    id = Column(Integer, primary_key=True, index=True)
    content = Column(String, nullable=False)
    author_id = Column(Integer, ForeignKey("users.id"))
    post_id = Column(Integer, ForeignKey("posts.id"), nullable=True)
    material_id = Column(Integer, ForeignKey("materials.id"), nullable=True)
    parent_id = Column(Integer, ForeignKey("comments.id"), nullable=True)  # 回复其他评论
    
    # 关系
    author = relationship("User", back_populates="comments")
    post = relationship("Post", back_populates="comments")
    material = relationship("Material", back_populates="comments")
    replies = relationship("Comment", backref="parent", remote_side=[id])  # 自引用关系 