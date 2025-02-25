import datetime
from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey, Table, Boolean
from sqlalchemy.orm import relationship
from backend.app.db.base import Base, TimestampMixin

# 思维导图和标签的多对多关系表
mindmap_tag = Table(
    "mindmap_tags",
    Base.metadata,
    Column("mindmap_id", Integer, ForeignKey("mindmaps.id")),
    Column("tag_id", Integer, ForeignKey("tags.id"))
)

class MindMap(Base, TimestampMixin):
    __tablename__ = "mindmaps"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(100), nullable=False)
    description = Column(String(200), nullable=True)
    content = Column(Text, nullable=True)  # 存储思维导图的JSON结构
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow)
    
    # 外键关联
    user_id = Column(Integer, ForeignKey("users.id"))
    
    # 关系
    user = relationship("User", back_populates="mindmaps")
    tags = relationship("Tag", secondary=mindmap_tag, back_populates="mindmaps")
    materials = relationship("Material", back_populates="mindmap") 