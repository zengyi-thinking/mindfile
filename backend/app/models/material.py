from sqlalchemy import Column, Integer, String, ForeignKey, Table, Boolean
from sqlalchemy.orm import relationship
from app.db.base import Base, TimestampMixin

# 资料和标签的多对多关系表
material_tag = Table(
    "material_tags",
    Base.metadata,
    Column("material_id", Integer, ForeignKey("materials.id")),
    Column("tag_id", Integer, ForeignKey("tags.id"))
)

class Material(Base, TimestampMixin):
    __tablename__ = "materials"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True, nullable=False)
    description = Column(String, nullable=True)
    content = Column(String, nullable=True)  # 可以是文本内容或JSON格式
    file_path = Column(String, nullable=True)  # 文件路径，如果是上传的文件
    file_type = Column(String, nullable=True)  # 文件类型
    owner_id = Column(Integer, ForeignKey("users.id"))
    mindmap_id = Column(Integer, ForeignKey("mindmaps.id"), nullable=True)
    
    # 统计数据
    view_count = Column(Integer, default=0)
    like_count = Column(Integer, default=0)
    
    # 关系
    owner = relationship("User", back_populates="materials")
    mindmap = relationship("MindMap", back_populates="materials")
    tags = relationship("Tag", secondary=material_tag, back_populates="materials")
    comments = relationship("Comment", back_populates="material")
    favorites = relationship("Favorite", back_populates="material") 