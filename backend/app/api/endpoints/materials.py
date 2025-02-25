from typing import List, Optional, Any
import os
import shutil
from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Form, Query
from sqlalchemy.orm import Session
from backend.app.api import deps
from backend.app.services import materials as materials_service
from backend.app.schemas.material import Material, MaterialCreate, MaterialUpdate, MaterialWithDetails
from backend.app.core.config import settings
from backend.app.schemas.user import User

router = APIRouter()

@router.get("/", response_model=List[Material])
def get_materials(
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_user),
    skip: int = 0,
    limit: int = 100,
    is_public: Optional[bool] = None
):
    """
    获取资料列表
    """
    return materials_service.get_materials(db, current_user.id, skip, limit, is_public)

@router.get("/{material_id}", response_model=MaterialWithDetails)
def get_material(
    material_id: int,
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_user)
):
    """
    获取资料详情
    """
    material = materials_service.get_material(db, material_id)
    if not material:
        raise HTTPException(status_code=404, detail="资料不存在")
    
    # 权限检查：只有公开资料或用户自己的资料可以访问
    if material.owner_id != current_user.id and not material.is_public:
        raise HTTPException(status_code=403, detail="无权访问此资料")
    
    # 增加浏览次数
    materials_service.increment_view_count(db, material)
    
    return material

@router.post("/upload", response_model=Material)
async def upload_material(
    file: UploadFile = File(...),
    title: str = Form(...),
    description: Optional[str] = Form(None),
    tags: Optional[str] = Form(None),  # 逗号分隔的标签ID
    mindmap_id: Optional[int] = Form(None),
    is_public: bool = Form(False),
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_user)
):
    """
    上传资料文件
    """
    # 检查文件大小
    file_size = 0
    file_content = await file.read()
    file_size = len(file_content)
    
    if file_size > settings.MAX_UPLOAD_SIZE:
        raise HTTPException(status_code=400, detail=f"文件大小超过限制（{settings.MAX_UPLOAD_SIZE / 1024 / 1024}MB）")
    
    # 获取文件类型
    file_extension = os.path.splitext(file.filename)[1].lower()
    file_type = _get_file_type(file_extension)
    
    # 创建上传目录
    upload_dir = os.path.join(settings.UPLOAD_DIR, str(current_user.id))
    os.makedirs(upload_dir, exist_ok=True)
    
    # 保存文件
    file_path = os.path.join(upload_dir, file.filename)
    with open(file_path, "wb") as buffer:
        buffer.write(file_content)
    
    # 处理标签
    tag_ids = []
    if tags:
        tag_ids = [int(tag_id) for tag_id in tags.split(",") if tag_id.isdigit()]
    
    # 创建资料记录
    material_in = MaterialCreate(
        title=title,
        description=description,
        file_type=file_type,
        tags=tag_ids,
        mindmap_id=mindmap_id,
        is_public=is_public
    )
    
    return materials_service.create_material(db, material_in, current_user.id, file_path)

@router.put("/{material_id}", response_model=Material)
def update_material(
    material_id: int,
    material_in: MaterialUpdate,
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_user)
):
    """
    更新资料
    """
    material = materials_service.get_material(db, material_id)
    if not material:
        raise HTTPException(status_code=404, detail="资料不存在")
    
    if material.owner_id != current_user.id:
        raise HTTPException(status_code=403, detail="无权修改此资料")
    
    return materials_service.update_material(db, material, material_in)

@router.delete("/{material_id}")
def delete_material(
    material_id: int,
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_user)
):
    """
    删除资料
    """
    material = materials_service.get_material(db, material_id)
    if not material:
        raise HTTPException(status_code=404, detail="资料不存在")
    
    if material.owner_id != current_user.id and not current_user.is_admin:
        raise HTTPException(status_code=403, detail="无权删除此资料")
    
    # 删除资料及其关联文件
    materials_service.delete_material(db, material_id)
    
    # 如果有关联文件，删除文件
    if material.file_path and os.path.exists(material.file_path):
        os.remove(material.file_path)
    
    return {"status": "success"}

@router.get("/by-tags", response_model=List[Material])
def get_materials_by_tags(
    tag_ids: str = Query(..., description="标签ID，多个以逗号分隔"),
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_user),
    skip: int = 0,
    limit: int = 20
):
    """
    根据标签获取资料
    """
    tag_id_list = [int(id) for id in tag_ids.split(",") if id.isdigit()]
    if not tag_id_list:
        raise HTTPException(status_code=400, detail="必须提供至少一个有效的标签ID")
    
    return materials_service.get_materials_by_tags(db, current_user.id, tag_id_list, skip, limit)

@router.post("/{material_id}/like")
def like_material(
    material_id: int,
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_user)
):
    """
    点赞资料
    """
    material = materials_service.get_material(db, material_id)
    if not material:
        raise HTTPException(status_code=404, detail="资料不存在")
    
    # 只有公开资料或用户自己的资料可以点赞
    if material.owner_id != current_user.id and not material.is_public:
        raise HTTPException(status_code=403, detail="无权访问此资料")
    
    materials_service.increment_like_count(db, material)
    
    return {"status": "success"}

def _get_file_type(extension: str) -> str:
    """
    根据文件扩展名获取文件类型
    """
    document_types = [".doc", ".docx", ".pdf", ".txt", ".md", ".xls", ".xlsx", ".ppt", ".pptx"]
    image_types = [".jpg", ".jpeg", ".png", ".gif", ".svg", ".webp"]
    video_types = [".mp4", ".avi", ".mov", ".wmv", ".flv", ".mkv"]
    audio_types = [".mp3", ".wav", ".ogg", ".flac", ".aac"]
    
    if extension in document_types:
        return "document"
    elif extension in image_types:
        return "image"
    elif extension in video_types:
        return "video"
    elif extension in audio_types:
        return "audio"
    else:
        return "other" 