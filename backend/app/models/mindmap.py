from sqlalchemy import Column, Integer, String, ForeignKey, Table
from sqlalchemy.orm import relationship
from app.db.base import Base, TimestampMixin

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
    title = Column(String, index=True, nullable=False)
    description = Column(String, nullable=True)
    owner_id = Column(Integer, ForeignKey("users.id"))
    
    # 存储思维导图数据结构
    data = Column(String, nullable=False)  # JSON格式存储
    
    # 关系
    owner = relationship("User", back_populates="mindmaps")
    tags = relationship("Tag", secondary=mindmap_tag, back_populates="mindmaps")
    materials = relationship("Material", back_populates="mindmap") 