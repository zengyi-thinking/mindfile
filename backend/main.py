from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import settings
from app.api.endpoints import mindmap, search, materials, forum, users
from app.core.events import create_start_app_handler, create_stop_app_handler

def create_application() -> FastAPI:
    application = FastAPI(
        title=settings.PROJECT_NAME,
        version=settings.VERSION,
        description="文件思维导图管理系统API"
    )
    
    # 注册中间件
    application.add_middleware(
        CORSMiddleware,
        allow_origins=settings.ALLOWED_HOSTS,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    
    # 注册事件处理器
    application.add_event_handler("startup", create_start_app_handler(application))
    application.add_event_handler("shutdown", create_stop_app_handler(application))
    
    # 注册路由
    application.include_router(mindmap.router, prefix="/api/mindmap", tags=["思维导图"])
    application.include_router(search.router, prefix="/api/search", tags=["搜索"])
    application.include_router(materials.router, prefix="/api/materials", tags=["资料"])
    application.include_router(forum.router, prefix="/api/forum", tags=["论坛"])
    application.include_router(users.router, prefix="/api/users", tags=["用户"])
    
    return application

app = create_application() 