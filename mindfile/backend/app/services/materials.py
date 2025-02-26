from typing import List, Dict, Any, Optional
from sqlalchemy import or_, func
from sqlalchemy.orm import Session, joinedload
from backend.app.models.material import Material
from backend.app.models.tag import Tag
from backend.app.schemas.material import MaterialCreate, MaterialUpdate

def get_material(db: Session, material_id: int) -> Optional[Material]:
    """
    获取特定资料
    """
    return db.query(Material).filter(Material.id == material_id).first()

def get_materials(
    db: Session, 
    user_id: int, 
    skip: int = 0, 
    limit: int = 100,
    is_public: Optional[bool] = None
) -> List[Material]:
    """
    获取资料列表
    """
    query = db.query(Material).filter(
        or_(
            Material.owner_id == user_id,
            Material.is_public == True
        )
    )
    
    if is_public is not None:
        query = query.filter(Material.is_public == is_public)
    
    return query.order_by(Material.created_at.desc()).offset(skip).limit(limit).all()

def create_material(
    db: Session, 
    material_in: MaterialCreate, 
    user_id: int,
    file_path: Optional[str] = None
) -> Material:
    """
    创建新资料
    """
    material = Material(
        title=material_in.title,
        description=material_in.description,
        content=material_in.content,
        file_path=file_path,
        file_type=material_in.file_type,
        owner_id=user_id,
        mindmap_id=material_in.mindmap_id,
        is_public=material_in.is_public
    )
    
    db.add(material)
    db.commit()
    db.refresh(material)
    
    # 添加标签（如果有）
    if material_in.tags:
        for tag_id in material_in.tags:
            tag = db.query(Tag).filter(Tag.id == tag_id).first()
            if tag:
                material.tags.append(tag)
        
        db.commit()
        db.refresh(material)
    
    return material

def update_material(
    db: Session, 
    material: Material, 
    material_in: MaterialUpdate
) -> Material:
    """
    更新资料
    """
    update_data = material_in.dict(exclude_unset=True)
    
    # 特殊处理标签
    if "tags" in update_data:
        tags = update_data.pop("tags")
        # 清除现有标签
        material.tags = []
        # 添加新标签
        for tag_id in tags:
            tag = db.query(Tag).filter(Tag.id == tag_id).first()
            if tag:
                material.tags.append(tag)
    
    # 更新其他字段
    for field, value in update_data.items():
        setattr(material, field, value)
    
    db.commit()
    db.refresh(material)
    return material

def delete_material(db: Session, material_id: int) -> bool:
    """
    删除资料
    """
    material = db.query(Material).filter(Material.id == material_id).first()
    if not material:
        return False
    
    db.delete(material)
    db.commit()
    return True

def get_materials_by_tags(
    db: Session, 
    user_id: int, 
    tag_ids: List[int],
    skip: int = 0,
    limit: int = 20
) -> List[Material]:
    """
    根据标签获取资料
    """
    # 查询同时具有所有指定标签的资料
    materials = db.query(Material).join(
        Material.tags
    ).filter(
        Tag.id.in_(tag_ids),
        or_(
            Material.owner_id == user_id,
            Material.is_public == True
        )
    ).group_by(
        Material.id
    ).having(
        func.count(Tag.id) == len(tag_ids)
    ).offset(skip).limit(limit).all()
    
    return materials

def increment_view_count(db: Session, material: Material) -> Material:
    """
    增加资料浏览次数
    """
    material.view_count += 1
    db.commit()
    db.refresh(material)
    return material

def increment_like_count(db: Session, material: Material) -> Material:
    """
    增加资料点赞次数
    """
    material.like_count += 1
    db.commit()
    db.refresh(material)
    return material 