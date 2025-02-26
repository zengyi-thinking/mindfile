from typing import List, Optional, Dict, Any
import json
from sqlalchemy.orm import Session
from backend.app.models.mindmap import MindMap
from backend.app.models.tag import Tag
from backend.app.schemas.mindmap import MindMapCreate, MindMapUpdate
from backend.app.schemas.tag import TagCreate

def get_mindmap(db: Session, mindmap_id: int) -> Optional[MindMap]:
    """获取特定思维导图"""
    return db.query(MindMap).filter(MindMap.id == mindmap_id).first()

def get_user_mindmaps(db: Session, user_id: int, skip: int = 0, limit: int = 100) -> List[MindMap]:
    """获取用户的所有思维导图"""
    return db.query(MindMap).filter(MindMap.owner_id == user_id).offset(skip).limit(limit).all()

def create_mindmap(db: Session, mindmap_in: MindMapCreate, user_id: int) -> MindMap:
    """创建新思维导图"""
    # 将思维导图数据转为JSON字符串
    data_str = json.dumps(mindmap_in.data) if mindmap_in.data else "{}"
    
    # 创建思维导图
    mindmap = MindMap(
        title=mindmap_in.title,
        description=mindmap_in.description,
        owner_id=user_id,
        data=data_str
    )
    
    db.add(mindmap)
    db.commit()
    db.refresh(mindmap)
    
    # 添加标签（如果有）
    if mindmap_in.tags:
        for tag_id in mindmap_in.tags:
            tag = db.query(Tag).filter(Tag.id == tag_id).first()
            if tag:
                mindmap.tags.append(tag)
        
        db.commit()
        db.refresh(mindmap)
    
    return mindmap

def update_mindmap(db: Session, mindmap: MindMap, mindmap_in: MindMapUpdate) -> MindMap:
    """更新思维导图"""
    # 更新基本信息
    update_data = mindmap_in.dict(exclude_unset=True)
    
    # 特殊处理思维导图数据，将其转为JSON字符串
    if "data" in update_data:
        update_data["data"] = json.dumps(update_data["data"])
    
    # 特殊处理标签
    if "tags" in update_data:
        tags = update_data.pop("tags")
        # 清除现有标签
        mindmap.tags = []
        # 添加新标签
        for tag_id in tags:
            tag = db.query(Tag).filter(Tag.id == tag_id).first()
            if tag:
                mindmap.tags.append(tag)
    
    # 更新其他字段
    for key, value in update_data.items():
        setattr(mindmap, key, value)
    
    db.commit()
    db.refresh(mindmap)
    return mindmap

def delete_mindmap(db: Session, mindmap_id: int) -> None:
    """删除思维导图"""
    mindmap = db.query(MindMap).filter(MindMap.id == mindmap_id).first()
    if mindmap:
        db.delete(mindmap)
        db.commit()

def get_mindmaps_by_tag(db: Session, tag_id: int, user_id: int) -> List[MindMap]:
    """根据标签获取思维导图"""
    tag = db.query(Tag).filter(Tag.id == tag_id).first()
    if not tag:
        return []
    
    return [m for m in tag.mindmaps if m.owner_id == user_id]

def add_tag_to_mindmap(db: Session, mindmap_id: int, tag_in: TagCreate) -> MindMap:
    """为思维导图添加标签"""
    mindmap = db.query(MindMap).filter(MindMap.id == mindmap_id).first()
    if not mindmap:
        return None
    
    # 查找是否已存在该标签
    tag = db.query(Tag).filter(Tag.name == tag_in.name).first()
    
    # 如果标签不存在，创建新标签
    if not tag:
        tag = Tag(
            name=tag_in.name,
            color=tag_in.color if tag_in.color else "#3498db"
        )
        db.add(tag)
        db.commit()
        db.refresh(tag)
    
    # 添加关联
    if tag not in mindmap.tags:
        mindmap.tags.append(tag)
        db.commit()
        db.refresh(mindmap)
    
    return mindmap 