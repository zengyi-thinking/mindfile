from typing import List, Optional, Any, Dict
from pydantic import BaseModel
from datetime import datetime
from .material import Material
from .mindmap import MindMap

class SearchQuery(BaseModel):
    query: str
    type: str = "keyword"  # "keyword" 或 "mindmap"
    filters: Optional[Dict[str, Any]] = None
    page: int = 1
    limit: int = 10
    sort_by: str = "relevance"  # "relevance", "newest", "popularity"

class SearchResult(BaseModel):
    total: int
    items: List[Any]
    page: int
    limit: int
    query: str
    
class KeywordSearchResult(SearchResult):
    items: List[Material]
    
class MindMapSearchResult(SearchResult):
    items: List[MindMap]
    related_tags: List[Dict[str, Any]] = []

class SearchHistoryItem(BaseModel):
    id: int
    query: str
    search_type: str
    created_at: datetime
    
    model_config = {
        "from_attributes": True
    } 