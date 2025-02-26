import os
import logging
import sys

# 确保当前目录在导入路径中
sys.path.insert(0, os.path.abspath('.'))

from backend.app.db.init_db import init_db

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger(__name__)
    
    logger.info("开始初始化项目...")
    
    # 初始化数据库
    logger.info("正在初始化数据库...")
    init_db()
    logger.info("数据库初始化完成！")
    
    logger.info("项目初始化完成！") 