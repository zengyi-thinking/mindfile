from sqlalchemy.orm import Session
from app.db.base import Base
from app.db.session import engine
from app.models import user, mindmap, tag, material, forum, user_activity

def init_db():
    # 创建所有表
    Base.metadata.create_all(bind=engine)

def get_all_models():
    # 返回所有模型类，用于导入
    return [
        user.User,
        mindmap.MindMap,
        tag.Tag,
        material.Material,
        forum.Post,
        forum.Comment,
        user_activity.Favorite,
        user_activity.SearchHistory
    ] 