from typing import Any, List, Optional
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from backend.app.api import deps
from backend.app.models.user import User
from backend.app.models.mindmap import MindMap
from backend.app.schemas.mindmap import MindMapCreate, MindMapUpdate, MindMapResponse

router = APIRouter()

@router.post("/", response_model=MindMapResponse)
def create_mindmap(
    *,
    db: Session = Depends(deps.get_db),
    mindmap_in: MindMapCreate,
    current_user: User = Depends(deps.get_current_user)
) -> Any:
    """
    创建新思维导图
    """
    mindmap = MindMap(
        title=mindmap_in.title,
        description=mindmap_in.description,
        content=mindmap_in.content,
        user_id=current_user.id
    )
    db.add(mindmap)
    db.commit()
    db.refresh(mindmap)
    return mindmap

@router.get("/", response_model=List[MindMapResponse])
def get_mindmaps(
    db: Session = Depends(deps.get_db),
    skip: int = 0,
    limit: int = 100,
    current_user: User = Depends(deps.get_current_user)
) -> Any:
    """
    获取当前用户的所有思维导图
    """
    mindmaps = db.query(MindMap).filter(
        MindMap.user_id == current_user.id
    ).offset(skip).limit(limit).all()
    return mindmaps

@router.get("/{mindmap_id}", response_model=MindMapResponse)
def get_mindmap(
    *,
    db: Session = Depends(deps.get_db),
    mindmap_id: int,
    current_user: User = Depends(deps.get_current_user)
) -> Any:
    """
    根据ID获取思维导图
    """
    mindmap = db.query(MindMap).filter(
        MindMap.id == mindmap_id,
        MindMap.user_id == current_user.id
    ).first()
    if not mindmap:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="思维导图不存在"
        )
    return mindmap

@router.put("/{mindmap_id}", response_model=MindMapResponse)
def update_mindmap(
    *,
    db: Session = Depends(deps.get_db),
    mindmap_id: int,
    mindmap_in: MindMapUpdate,
    current_user: User = Depends(deps.get_current_user)
) -> Any:
    """
    更新思维导图
    """
    mindmap = db.query(MindMap).filter(
        MindMap.id == mindmap_id,
        MindMap.user_id == current_user.id
    ).first()
    if not mindmap:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="思维导图不存在"
        )
    
    update_data = mindmap_in.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(mindmap, field, value)
    
    db.add(mindmap)
    db.commit()
    db.refresh(mindmap)
    return mindmap

@router.delete("/{mindmap_id}", response_model=MindMapResponse)
def delete_mindmap(
    *,
    db: Session = Depends(deps.get_db),
    mindmap_id: int,
    current_user: User = Depends(deps.get_current_user)
) -> Any:
    """
    删除思维导图
    """
    mindmap = db.query(MindMap).filter(
        MindMap.id == mindmap_id,
        MindMap.user_id == current_user.id
    ).first()
    if not mindmap:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="思维导图不存在"
        )
    
    db.delete(mindmap)
    db.commit()
    return mindmap 