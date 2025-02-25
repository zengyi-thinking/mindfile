from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from backend.app.db.base import Base, TimestampMixin

class User(Base, TimestampMixin):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    is_active = Column(Boolean, default=True)
    is_admin = Column(Boolean, default=False)
    avatar_url = Column(String, nullable=True)

    # 关系
    materials = relationship("Material", back_populates="owner")
    mindmaps = relationship("MindMap", back_populates="user", cascade="all, delete-orphan")
    posts = relationship("Post", back_populates="owner")
    comments = relationship("Comment", back_populates="owner")
    favorites = relationship("Favorite", back_populates="user")
    search_histories = relationship("SearchHistory", back_populates="user") 