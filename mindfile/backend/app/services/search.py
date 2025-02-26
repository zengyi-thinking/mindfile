from typing import List, Dict, Any, Optional
from datetime import datetime
from sqlalchemy import or_, func, desc
from sqlalchemy.orm import Session, joinedload
from backend.app.models.material import Material
from backend.app.models.mindmap import MindMap
from backend.app.models.tag import Tag
from backend.app.models.user_activity import SearchHistory

def search_by_keyword(
    db: Session, 
    user_id: int, 
    query: str, 
    filters: Dict[str, Any] = None, 
    sort_by: str = "relevance", 
    page: int = 1, 
    limit: int = 10
):
    """
    关键词搜索服务
    """
    # 基础查询 - 只查询公开资料和用户自己的资料
    base_query = db.query(Material).filter(
        or_(
            Material.owner_id == user_id,
            Material.is_public == True
        )
    )
    
    # 关键词搜索
    if query:
        search_terms = [f"%{term}%" for term in query.split()]
        search_conditions = []
        for term in search_terms:
            search_conditions.append(Material.title.ilike(term))
            search_conditions.append(Material.description.ilike(term))
            search_conditions.append(Material.content.ilike(term))
        
        base_query = base_query.filter(or_(*search_conditions))
    
    # 应用过滤器
    if filters:
        if filters.get("file_type"):
            base_query = base_query.filter(Material.file_type == filters["file_type"])
        
        if filters.get("tags"):
            base_query = base_query.join(Material.tags).filter(Tag.id.in_(filters["tags"]))
        
        if filters.get("date_from"):
            date_from = datetime.fromisoformat(filters["date_from"])
            base_query = base_query.filter(Material.created_at >= date_from)
        
        if filters.get("date_to"):
            date_to = datetime.fromisoformat(filters["date_to"])
            base_query = base_query.filter(Material.created_at <= date_to)
    
    # 计算总数
    total = base_query.count()
    
    # 排序
    if sort_by == "newest":
        base_query = base_query.order_by(desc(Material.created_at))
    elif sort_by == "popularity":
        base_query = base_query.order_by(desc(Material.view_count), desc(Material.like_count))
    else:  # relevance - 默认排序
        # 对于相关性排序，可以根据匹配度来排序
        # 这里简化处理，仍按创建时间排序
        base_query = base_query.order_by(desc(Material.created_at))
    
    # 分页
    offset = (page - 1) * limit
    items = base_query.offset(offset).limit(limit).all()
    
    # 构建返回结果
    return {
        "total": total,
        "items": items,
        "page": page,
        "limit": limit,
        "query": query
    }

def search_by_mindmap(
    db: Session, 
    user_id: int, 
    tag_ids: List[int], 
    filters: Dict[str, Any] = None, 
    sort_by: str = "relevance", 
    page: int = 1, 
    limit: int = 10
):
    """
    思维导图搜索服务
    """
    # 查找标签关联的思维导图
    mindmaps_query = db.query(MindMap).filter(
        MindMap.owner_id == user_id
    ).join(MindMap.tags).filter(
        Tag.id.in_(tag_ids)
    ).distinct()
    
    # 获取相关标签
    related_tags_query = db.query(Tag).filter(
        Tag.id.in_(
            db.query(Tag.id).join(
                Tag.mindmaps
            ).filter(
                MindMap.id.in_([m.id for m in mindmaps_query])
            )
        )
    )
    related_tags = [{"id": tag.id, "name": tag.name, "color": tag.color} for tag in related_tags_query]
    
    # 分页
    total = mindmaps_query.count()
    offset = (page - 1) * limit
    mindmaps = mindmaps_query.offset(offset).limit(limit).all()
    
    # 构建每个思维导图的数据
    mindmap_items = []
    for mindmap in mindmaps:
        # 根据标签查找相关资料
        materials = db.query(Material).join(
            Material.tags
        ).filter(
            Tag.id.in_(tag_ids),
            or_(
                Material.owner_id == user_id,
                Material.is_public == True
            )
        ).distinct().all()
        
        # 过滤资料
        if filters:
            if filters.get("file_type"):
                materials = [m for m in materials if m.file_type == filters["file_type"]]
            
            if filters.get("date_from"):
                date_from = datetime.fromisoformat(filters["date_from"])
                materials = [m for m in materials if m.created_at >= date_from]
            
            if filters.get("date_to"):
                date_to = datetime.fromisoformat(filters["date_to"])
                materials = [m for m in materials if m.created_at <= date_to]
        
        # 添加到结果中
        mindmap_items.append({
            "id": mindmap.id,
            "title": mindmap.title,
            "description": mindmap.description,
            "owner_id": mindmap.owner_id,
            "created_at": mindmap.created_at,
            "updated_at": mindmap.updated_at,
            "tags": [{"id": tag.id, "name": tag.name, "color": tag.color} for tag in mindmap.tags],
            "materials": materials
        })
    
    # 构建返回结果
    return {
        "total": total,
        "items": mindmap_items,
        "page": page,
        "limit": limit,
        "query": ", ".join([tag["name"] for tag in related_tags if tag["id"] in tag_ids]),
        "related_tags": related_tags
    }

def add_search_history(db: Session, user_id: int, query: str, search_type: str = "keyword"):
    """
    添加搜索历史
    """
    history = SearchHistory(
        user_id=user_id,
        query=query,
        search_type=search_type
    )
    db.add(history)
    db.commit()
    db.refresh(history)
    return history

def get_user_search_history(db: Session, user_id: int, limit: int = 10):
    """
    获取用户搜索历史
    """
    return db.query(SearchHistory).filter(
        SearchHistory.user_id == user_id
    ).order_by(desc(SearchHistory.created_at)).limit(limit).all()

def clear_user_search_history(db: Session, user_id: int):
    """
    清除用户搜索历史
    """
    db.query(SearchHistory).filter(
        SearchHistory.user_id == user_id
    ).delete()
    db.commit()

def get_tag_names(db: Session, tag_ids: List[int]) -> List[str]:
    """
    根据标签ID获取标签名称
    """
    tags = db.query(Tag).filter(Tag.id.in_(tag_ids)).all()
    return [tag.name for tag in tags] 