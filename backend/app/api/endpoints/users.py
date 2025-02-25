from typing import List, Any
from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File, Form, Body
from sqlalchemy.orm import Session
import os

from backend.app.api import deps
from backend.app.services import user as user_service
from backend.app.schemas.user import User, UserUpdate, UserCreate
from backend.app.core.config import settings

router = APIRouter()

@router.get("/me", response_model=User)
def read_user_me(
    current_user = Depends(deps.get_current_user),
):
    """
    获取当前用户信息
    """
    return current_user

@router.put("/me", response_model=User)
def update_user_me(
    *,
    db: Session = Depends(deps.get_db),
    user_in: UserUpdate,
    current_user = Depends(deps.get_current_user),
):
    """
    更新当前用户信息
    """
    user = user_service.update_user(db, current_user, user_in)
    return user

@router.post("/avatar", response_model=User)
async def upload_avatar(
    *,
    db: Session = Depends(deps.get_db),
    file: UploadFile = File(...),
    current_user = Depends(deps.get_current_user),
):
    """
    上传用户头像
    """
    # 检查文件是否为图片
    content_type = file.content_type
    if not content_type.startswith("image/"):
        raise HTTPException(
            status_code=400, 
            detail="只允许上传图片文件"
        )
    
    # 创建头像文件夹
    avatar_dir = os.path.join(settings.UPLOAD_DIR, "avatars")
    os.makedirs(avatar_dir, exist_ok=True)
    
    # 文件名格式：user_{user_id}_{原始文件名}
    file_extension = os.path.splitext(file.filename)[1]
    avatar_filename = f"user_{current_user.id}{file_extension}"
    avatar_path = os.path.join(avatar_dir, avatar_filename)
    
    # 保存文件
    file_content = await file.read()
    with open(avatar_path, "wb") as f:
        f.write(file_content)
    
    # 更新用户头像URL
    avatar_url = f"/uploads/avatars/{avatar_filename}"
    user_in = UserUpdate(avatar_url=avatar_url)
    user = user_service.update_user(db, current_user, user_in)
    
    return user

# 管理员接口
@router.get("/", response_model=List[User])
def read_users(
    db: Session = Depends(deps.get_db),
    skip: int = 0,
    limit: int = 100,
    current_user = Depends(deps.get_current_admin),
):
    """
    获取所有用户列表（仅管理员）
    """
    users = user_service.get_users(db, skip=skip, limit=limit)
    return users

@router.post("/", response_model=User)
def create_user(
    *,
    db: Session = Depends(deps.get_db),
    user_in: UserCreate,
    current_user = Depends(deps.get_current_admin),
):
    """
    创建新用户（仅管理员）
    """
    user = user_service.get_user_by_email(db, email=user_in.email)
    if user:
        raise HTTPException(
            status_code=400,
            detail="该邮箱已被注册",
        )
    user = user_service.create_user(db, user_in)
    return user

@router.get("/{user_id}", response_model=User)
def read_user(
    user_id: int,
    current_user = Depends(deps.get_current_user),
    db: Session = Depends(deps.get_db),
):
    """
    获取指定用户信息
    """
    user = user_service.get_user_by_id(db, user_id=user_id)
    if not user:
        raise HTTPException(
            status_code=404,
            detail="用户不存在",
        )
    return user

@router.delete("/{user_id}")
def delete_user(
    user_id: int,
    db: Session = Depends(deps.get_db),
    current_user = Depends(deps.get_current_admin),
):
    """
    删除用户（仅管理员）
    """
    user = user_service.get_user_by_id(db, user_id=user_id)
    if not user:
        raise HTTPException(
            status_code=404,
            detail="用户不存在",
        )
    user_service.delete_user(db, user_id=user_id)
    return {"status": "success"} 