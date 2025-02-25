from sqlalchemy import Column, Integer, String, ForeignKey, Table
from sqlalchemy.orm import relationship
from app.db.base import Base, TimestampMixin

# 标签之间的层级关系
tag_hierarchy = Table(
    "tag_hierarchy",
    Base.metadata,
    Column("parent_id", Integer, ForeignKey("tags.id")),
    Column("child_id", Integer, ForeignKey("tags.id"))
)

class Tag(Base, TimestampMixin):
    __tablename__ = "tags"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True, nullable=False)
    color = Column(String, default="#3498db")  # 标签颜色，默认蓝色
    
    # 关系
    mindmaps = relationship("MindMap", secondary="mindmap_tags", back_populates="tags")
    materials = relationship("Material", secondary="material_tags", back_populates="tags")
    
    # 自引用关系，用于标签层级结构
    parent_tags = relationship(
        "Tag", 
        secondary=tag_hierarchy,
        primaryjoin=(tag_hierarchy.c.child_id == id),
        secondaryjoin=(tag_hierarchy.c.parent_id == id),
        backref="child_tags"
    ) 