from fastapi import APIRouter
from backend.app.api.endpoints import mindmaps, search, materials, forum, users, auth

api_router = APIRouter()

api_router.include_router(auth.router, prefix="/auth", tags=["认证"])
api_router.include_router(users.router, prefix="/users", tags=["用户"])
api_router.include_router(mindmaps.router, prefix="/mindmaps", tags=["思维导图"])
api_router.include_router(materials.router, prefix="/materials", tags=["资料"])
api_router.include_router(forum.router, prefix="/forum", tags=["论坛"])
api_router.include_router(search.router, prefix="/search", tags=["搜索"]) 