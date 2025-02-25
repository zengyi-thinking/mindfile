from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from backend.app.api import deps
from backend.app.services import mindmap as mindmap_service
from backend.app.schemas.mindmap import MindMap, MindMapCreate, MindMapUpdate, MindMapWithDetails
from backend.app.schemas.tag import Tag, TagCreate

router = APIRouter()

@router.get("/", response_model=List[MindMap])
def get_mindmaps(
    db: Session = Depends(deps.get_db),
    current_user = Depends(deps.get_current_user),
    skip: int = 0, 
    limit: int = 100
):
    """获取用户的所有思维导图"""
    return mindmap_service.get_user_mindmaps(db, current_user.id, skip=skip, limit=limit)

@router.get("/{mindmap_id}", response_model=MindMapWithDetails)
def get_mindmap(
    mindmap_id: int,
    db: Session = Depends(deps.get_db),
    current_user = Depends(deps.get_current_user)
):
    """获取特定思维导图详情"""
    mindmap = mindmap_service.get_mindmap(db, mindmap_id)
    if not mindmap:
        raise HTTPException(status_code=404, detail="思维导图不存在")
    if mindmap.owner_id != current_user.id:
        raise HTTPException(status_code=403, detail="无权访问此思维导图")
    return mindmap

@router.post("/", response_model=MindMap)
def create_mindmap(
    mindmap_in: MindMapCreate,
    db: Session = Depends(deps.get_db),
    current_user = Depends(deps.get_current_user)
):
    """创建新思维导图"""
    return mindmap_service.create_mindmap(db, mindmap_in, current_user.id)

@router.put("/{mindmap_id}", response_model=MindMap)
def update_mindmap(
    mindmap_id: int,
    mindmap_in: MindMapUpdate,
    db: Session = Depends(deps.get_db),
    current_user = Depends(deps.get_current_user)
):
    """更新思维导图"""
    mindmap = mindmap_service.get_mindmap(db, mindmap_id)
    if not mindmap:
        raise HTTPException(status_code=404, detail="思维导图不存在")
    if mindmap.owner_id != current_user.id:
        raise HTTPException(status_code=403, detail="无权修改此思维导图")
    return mindmap_service.update_mindmap(db, mindmap, mindmap_in)

@router.delete("/{mindmap_id}")
def delete_mindmap(
    mindmap_id: int,
    db: Session = Depends(deps.get_db),
    current_user = Depends(deps.get_current_user)
):
    """删除思维导图"""
    mindmap = mindmap_service.get_mindmap(db, mindmap_id)
    if not mindmap:
        raise HTTPException(status_code=404, detail="思维导图不存在")
    if mindmap.owner_id != current_user.id:
        raise HTTPException(status_code=403, detail="无权删除此思维导图")
    mindmap_service.delete_mindmap(db, mindmap_id)
    return {"status": "success"}

@router.get("/by-tag/{tag_id}", response_model=List[MindMap])
def get_mindmaps_by_tag(
    tag_id: int,
    db: Session = Depends(deps.get_db),
    current_user = Depends(deps.get_current_user)
):
    """根据标签获取思维导图"""
    return mindmap_service.get_mindmaps_by_tag(db, tag_id, current_user.id)

@router.post("/{mindmap_id}/tags/", response_model=MindMap)
def add_tag_to_mindmap(
    mindmap_id: int,
    tag_in: TagCreate,
    db: Session = Depends(deps.get_db),
    current_user = Depends(deps.get_current_user)
):
    """为思维导图添加标签"""
    mindmap = mindmap_service.get_mindmap(db, mindmap_id)
    if not mindmap:
        raise HTTPException(status_code=404, detail="思维导图不存在")
    if mindmap.owner_id != current_user.id:
        raise HTTPException(status_code=403, detail="无权修改此思维导图")
    return mindmap_service.add_tag_to_mindmap(db, mindmap_id, tag_in) 