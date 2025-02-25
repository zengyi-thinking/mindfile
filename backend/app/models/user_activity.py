from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from app.db.base import Base, TimestampMixin

class Favorite(Base, TimestampMixin):
    __tablename__ = "favorites"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    material_id = Column(Integer, ForeignKey("materials.id"))
    
    # 关系
    user = relationship("User", back_populates="favorites")
    material = relationship("Material", back_populates="favorites")

class SearchHistory(Base, TimestampMixin):
    __tablename__ = "search_histories"

    id = Column(Integer, primary_key=True, index=True)
    query = Column(String, nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"))
    search_type = Column(String, nullable=False)  # "keyword" 或 "mindmap"
    
    # 关系
    user = relationship("User", back_populates="search_histories") 