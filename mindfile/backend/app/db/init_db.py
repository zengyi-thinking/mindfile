import logging
from sqlalchemy.orm import Session
from backend.app.db.base import Base
from backend.app.db.session import engine, SessionLocal
from backend.app.core.config import settings
from backend.app.core.security import get_password_hash
from backend.app.models import user, mindmap, tag, material, forum, user_activity
from backend.app.models.user import User
from backend.app.models.mindmap import MindMap

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def init_db():
    # 创建所有表
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    create_first_admin(db)
    db.close()

def create_first_admin(db: Session):
    # 检查是否已存在管理员用户
    admin = db.query(user.User).filter(user.User.is_admin == True).first()
    if admin:
        logger.info("管理员用户已存在，跳过创建")
        return
    
    # 创建默认管理员用户
    admin_user = user.User(
        username="admin",
        email=settings.FIRST_ADMIN_EMAIL,
        hashed_password=get_password_hash(settings.FIRST_ADMIN_PASSWORD),
        is_admin=True,
        is_active=True
    )
    db.add(admin_user)
    db.commit()
    logger.info(f"已创建管理员用户: {settings.FIRST_ADMIN_EMAIL}")

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

if __name__ == "__main__":
    logger.info("初始化数据库...")
    init_db()
    logger.info("数据库初始化完成！") 