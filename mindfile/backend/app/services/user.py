from typing import Optional, List
from sqlalchemy.orm import Session
from backend.app.models.user import User
from backend.app.schemas.user import UserCreate, UserUpdate
from backend.app.core.security import get_password_hash, verify_password

def get_user_by_id(db: Session, user_id: int) -> Optional[User]:
    """
    通过ID获取用户
    """
    return db.query(User).filter(User.id == user_id).first()

def get_user_by_email(db: Session, email: str) -> Optional[User]:
    """
    通过邮箱获取用户
    """
    return db.query(User).filter(User.email == email).first()

def get_user_by_username(db: Session, username: str) -> Optional[User]:
    """
    通过用户名获取用户
    """
    return db.query(User).filter(User.username == username).first()

def get_users(db: Session, skip: int = 0, limit: int = 100) -> List[User]:
    """
    获取用户列表
    """
    return db.query(User).offset(skip).limit(limit).all()

def create_user(db: Session, user_in: UserCreate) -> User:
    """
    创建新用户
    """
    user = User(
        username=user_in.username,
        email=user_in.email,
        hashed_password=get_password_hash(user_in.password),
        is_admin=user_in.is_admin,
        avatar_url=user_in.avatar_url
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user

def update_user(db: Session, user: User, user_in: UserUpdate) -> User:
    """
    更新用户信息
    """
    update_data = user_in.dict(exclude_unset=True)
    
    # 如果更新密码，需要哈希处理
    if "password" in update_data:
        hashed_password = get_password_hash(update_data["password"])
        del update_data["password"]
        update_data["hashed_password"] = hashed_password
    
    for field, value in update_data.items():
        setattr(user, field, value)
    
    db.commit()
    db.refresh(user)
    return user

def delete_user(db: Session, user_id: int) -> bool:
    """
    删除用户
    """
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        return False
    
    db.delete(user)
    db.commit()
    return True 