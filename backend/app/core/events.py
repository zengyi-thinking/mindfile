import logging
from typing import Callable
from fastapi import FastAPI
from backend.app.db.init_db import init_db

logger = logging.getLogger(__name__)

def create_start_app_handler(app: FastAPI) -> Callable:
    """
    应用程序启动时执行的函数
    """
    async def start_app() -> None:
        logger.info("正在初始化数据库...")
        init_db()
        logger.info("数据库初始化完成！")

    return start_app

def create_stop_app_handler(app: FastAPI) -> Callable:
    """
    应用程序关闭时执行的函数
    """
    async def stop_app() -> None:
        logger.info("应用程序关闭...")

    return stop_app 