from typing import List, Optional, Any
from fastapi import APIRouter, Depends, Query, HTTPException, Body
from sqlalchemy.orm import Session
from backend.app.api import deps
from backend.app.services import search as search_service
from backend.app.schemas.search import (
    SearchQuery, 
    KeywordSearchResult, 
    MindMapSearchResult,
    SearchHistoryItem
)
from backend.app.schemas.material import Material

router = APIRouter()

@router.get("/keyword", response_model=KeywordSearchResult)
def search_by_keyword(
    query: str = Query(..., description="搜索关键词"),
    file_type: Optional[str] = Query(None, description="文件类型过滤"),
    tags: Optional[List[int]] = Query(None, description="标签过滤"),
    date_from: Optional[str] = Query(None, description="日期范围(开始)"),
    date_to: Optional[str] = Query(None, description="日期范围(结束)"),
    sort_by: str = Query("relevance", description="排序方式"),
    page: int = Query(1, description="页码"),
    limit: int = Query(10, description="每页数量"),
    db: Session = Depends(deps.get_db),
    current_user = Depends(deps.get_current_user)
):
    """
    关键词搜索API
    """
    filters = {
        "file_type": file_type,
        "tags": tags,
        "date_from": date_from,
        "date_to": date_to
    }
    
    result = search_service.search_by_keyword(
        db, 
        current_user.id, 
        query, 
        filters, 
        sort_by, 
        page, 
        limit
    )
    
    # 记录搜索历史
    search_service.add_search_history(db, current_user.id, query, "keyword")
    
    return result

@router.get("/mindmap", response_model=MindMapSearchResult)
def search_by_mindmap(
    tag_ids: str = Query(..., description="标签ID，多个以逗号分隔"),
    file_type: Optional[str] = Query(None, description="文件类型过滤"),
    date_from: Optional[str] = Query(None, description="日期范围(开始)"),
    date_to: Optional[str] = Query(None, description="日期范围(结束)"),
    sort_by: str = Query("relevance", description="排序方式"),
    page: int = Query(1, description="页码"),
    limit: int = Query(10, description="每页数量"),
    db: Session = Depends(deps.get_db),
    current_user = Depends(deps.get_current_user)
):
    """
    思维导图搜索API
    """
    tag_id_list = [int(id) for id in tag_ids.split(",") if id.isdigit()]
    if not tag_id_list:
        raise HTTPException(status_code=400, detail="必须提供至少一个有效的标签ID")
    
    filters = {
        "file_type": file_type,
        "date_from": date_from,
        "date_to": date_to
    }
    
    result = search_service.search_by_mindmap(
        db, 
        current_user.id, 
        tag_id_list, 
        filters, 
        sort_by, 
        page, 
        limit
    )
    
    # 记录搜索历史（使用标签名称作为查询词）
    tag_names = search_service.get_tag_names(db, tag_id_list)
    search_query = ", ".join(tag_names)
    search_service.add_search_history(db, current_user.id, search_query, "mindmap")
    
    return result

@router.get("/history", response_model=List[SearchHistoryItem])
def get_search_history(
    limit: int = Query(10, description="历史记录数量"),
    db: Session = Depends(deps.get_db),
    current_user = Depends(deps.get_current_user)
):
    """
    获取用户搜索历史
    """
    return search_service.get_user_search_history(db, current_user.id, limit)

@router.delete("/history")
def clear_search_history(
    db: Session = Depends(deps.get_db),
    current_user = Depends(deps.get_current_user)
):
    """
    清除用户搜索历史
    """
    search_service.clear_user_search_history(db, current_user.id)
    return {"status": "success"} 