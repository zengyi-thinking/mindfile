import logging
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from backend.app.api.api import api_router
from backend.app.core.config import settings
from backend.app.core.events import create_start_app_handler, create_stop_app_handler
from fastapi.responses import HTMLResponse

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)

# 创建FastAPI应用
app = FastAPI(
    title="MindFile API",
    description="思维导图文件管理系统API",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url=f"{settings.API_PREFIX}/openapi.json",
)

# 设置CORS
if settings.BACKEND_CORS_ORIGINS:
    app.add_middleware(
        CORSMiddleware,
        allow_origins=[str(origin) for origin in settings.BACKEND_CORS_ORIGINS],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
else:
    # 开发环境，允许所有源
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

# 注册路由
app.include_router(api_router, prefix=settings.API_PREFIX)

# 注册启动和关闭事件
app.add_event_handler("startup", create_start_app_handler(app))
app.add_event_handler("shutdown", create_stop_app_handler(app))

@app.get("/", response_class=HTMLResponse)
async def get_html():
    return """
    <!DOCTYPE html>
    <html>
    <head>
        <title>思维导图系统</title>
        <style>
            body { font-family: Arial, sans-serif; margin: 0; padding: 0; display: flex; justify-content: center; align-items: center; height: 100vh; flex-direction: column; background-color: #f5f7fa; }
            .login-card { width: 400px; padding: 30px; border-radius: 8px; background-color: white; box-shadow: 0 4px 15px rgba(0, 0, 0, 0.1); }
            h2 { text-align: center; color: #333; margin-bottom: 10px; }
            h3 { text-align: center; color: #555; margin-bottom: 30px; }
            .form-group { margin-bottom: 20px; }
            label { display: block; margin-bottom: 8px; font-weight: 500; color: #555; }
            .form-control { width: 100%; padding: 12px 15px; border: 1px solid #ddd; border-radius: 4px; font-size: 16px; box-sizing: border-box; }
            .btn { width: 100%; padding: 12px; border: none; border-radius: 4px; font-size: 16px; font-weight: 500; cursor: pointer; background-color: #4a90e2; color: white; }
            .login-footer { margin-top: 25px; text-align: center; color: #777; }
            a { color: #4a90e2; text-decoration: none; }
        </style>
    </head>
    <body>
        <div class="login-card">
            <h2>思维导图系统</h2>
            <h3>用户登录</h3>
            
            <form id="loginForm">
                <div class="form-group">
                    <label for="email">邮箱</label>
                    <input type="email" id="email" class="form-control" required placeholder="请输入邮箱">
                </div>
                
                <div class="form-group">
                    <label for="password">密码</label>
                    <input type="password" id="password" class="form-control" required placeholder="请输入密码">
                </div>
                
                <button type="submit" class="btn">登录</button>
            </form>
            
            <div class="login-footer">
                <p>还没有账号？ <a href="/register">立即注册</a></p>
            </div>
        </div>

        <script>
            document.getElementById('loginForm').addEventListener('submit', async (e) => {
                e.preventDefault();
                const email = document.getElementById('email').value;
                const password = document.getElementById('password').value;
                
                try {
                    const formData = new FormData();
                    formData.append('username', email);
                    formData.append('password', password);
                    
                    const response = await fetch('/api/auth/login', {
                        method: 'POST',
                        body: formData
                    });
                    
                    if (!response.ok) {
                        throw new Error('登录失败');
                    }
                    
                    const data = await response.json();
                    localStorage.setItem('token', data.access_token);
                    
                    // 重定向到仪表板
                    window.location.href = '/dashboard';
                } catch (error) {
                    alert('登录失败，请检查邮箱和密码');
                    console.error('登录错误:', error);
                }
            });
        </script>
    </body>
    </html>
    """

@app.get("/dashboard", response_class=HTMLResponse)
async def get_dashboard():
    return """
    <!DOCTYPE html>
    <html>
    <head>
        <title>思维导图系统 - 仪表板</title>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <style>
            body {
                font-family: Arial, sans-serif;
                margin: 0;
                padding: 0;
                background-color: #f5f7fa;
                color: #333;
            }
            .dashboard-container {
                display: flex;
                min-height: 100vh;
            }
            .sidebar {
                width: 240px;
                background-color: #2c3e50;
                color: white;
                padding: 20px 0;
            }
            .sidebar-header {
                padding: 0 20px 20px 20px;
                border-bottom: 1px solid #3d556c;
                margin-bottom: 20px;
            }
            .sidebar-header h1 {
                font-size: 20px;
                margin: 0;
            }
            .sidebar-menu {
                list-style: none;
                padding: 0;
                margin: 0;
            }
            .sidebar-menu li {
                padding: 12px 20px;
                cursor: pointer;
                transition: background-color 0.3s;
            }
            .sidebar-menu li:hover, .sidebar-menu li.active {
                background-color: #3d556c;
            }
            .sidebar-menu a {
                color: white;
                text-decoration: none;
                display: block;
            }
            .main-content {
                flex: 1;
                padding: 30px;
            }
            .header {
                display: flex;
                justify-content: space-between;
                align-items: center;
                margin-bottom: 30px;
            }
            .header h1 {
                margin: 0;
                font-size: 24px;
            }
            .user-info {
                display: flex;
                align-items: center;
                gap: 10px;
            }
            .avatar {
                width: 40px;
                height: 40px;
                border-radius: 50%;
                background-color: #4a90e2;
                color: white;
                display: flex;
                justify-content: center;
                align-items: center;
                font-weight: bold;
            }
            .card-grid {
                display: grid;
                grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
                gap: 20px;
                margin-bottom: 30px;
            }
            .card {
                background-color: white;
                border-radius: 8px;
                box-shadow: 0 2px 10px rgba(0, 0, 0, 0.05);
                padding: 20px;
                transition: transform 0.3s, box-shadow 0.3s;
            }
            .card:hover {
                transform: translateY(-5px);
                box-shadow: 0 5px 15px rgba(0, 0, 0, 0.1);
            }
            .card h2 {
                margin-top: 0;
                font-size: 18px;
                display: flex;
                align-items: center;
                gap: 10px;
            }
            .card-icon {
                font-size: 24px;
            }
            .card p {
                color: #666;
                margin-bottom: 0;
            }
            .chart-container {
                background-color: white;
                border-radius: 8px;
                box-shadow: 0 2px 10px rgba(0, 0, 0, 0.05);
                padding: 20px;
                margin-bottom: 20px;
            }
            .chart-header {
                display: flex;
                justify-content: space-between;
                align-items: center;
                margin-bottom: 20px;
            }
            .chart-header h2 {
                margin: 0;
                font-size: 18px;
            }
            .mock-chart {
                height: 300px;
                background-color: #f5f7fa;
                border-radius: 4px;
                display: flex;
                justify-content: center;
                align-items: center;
                color: #999;
            }
            .btn {
                padding: 8px 16px;
                background-color: #4a90e2;
                color: white;
                border: none;
                border-radius: 4px;
                cursor: pointer;
                font-size: 14px;
                transition: background-color 0.3s;
            }
            .btn:hover {
                background-color: #3a7fcb;
            }
        </style>
    </head>
    <body>
        <div class="dashboard-container">
            <div class="sidebar">
                <div class="sidebar-header">
                    <h1>思维导图系统</h1>
                </div>
                <ul class="sidebar-menu">
                    <li class="active"><a href="/dashboard">仪表板</a></li>
                    <li><a href="/mindmaps-page">思维导图</a></li>
                    <li><a href="/materials-page">资料管理</a></li>
                    <li><a href="/forum-page">讨论交流</a></li>
                    <li><a href="/settings-page">个人中心</a></li>
                </ul>
            </div>
            <div class="main-content">
                <div class="header">
                    <h1>仪表板</h1>
                    <div class="user-info">
                        <span>管理员</span>
                        <div class="avatar">A</div>
                    </div>
                </div>
                
                <div class="card-grid">
                    <div class="card">
                        <h2><span class="card-icon">📊</span> 思维导图</h2>
                        <p>已创建的思维导图: 5</p>
                        <p>最近更新: 2023-06-15</p>
                    </div>
                    <div class="card">
                        <h2><span class="card-icon">📚</span> 学习资料</h2>
                        <p>上传的资料: 12</p>
                        <p>总浏览量: 230</p>
                    </div>
                    <div class="card">
                        <h2><span class="card-icon">💬</span> 讨论交流</h2>
                        <p>发表的帖子: 8</p>
                        <p>收到的回复: 27</p>
                    </div>
                </div>
                
                <div class="chart-container">
                    <div class="chart-header">
                        <h2>最近活动</h2>
                        <button class="btn">查看详情</button>
                    </div>
                    <div class="mock-chart">
                        [最近一周的活动图表将显示在这里]
                    </div>
                </div>
                
                <div class="chart-container">
                    <div class="chart-header">
                        <h2>学习进度</h2>
                        <button class="btn">查看全部</button>
                    </div>
                    <div class="mock-chart">
                        [学习进度追踪图表将显示在这里]
                    </div>
                </div>
            </div>
        </div>
        
        <script>
            // 获取用户信息
            document.addEventListener('DOMContentLoaded', async () => {
                const token = localStorage.getItem('token');
                if (!token) {
                    window.location.href = '/';
                    return;
                }
                
                try {
                    const response = await fetch('/api/users/me', {
                        headers: {
                            'Authorization': `Bearer ${token}`
                        }
                    });
                    
                    if (!response.ok) {
                        throw new Error('未授权');
                    }
                    
                    const user = await response.json();
                    // 更新用户信息显示
                    document.querySelector('.user-info span').textContent = user.username;
                    document.querySelector('.avatar').textContent = user.username.charAt(0).toUpperCase();
                } catch (error) {
                    console.error('获取用户信息失败:', error);
                    // 如果获取用户信息失败，重定向到登录页
                    localStorage.removeItem('token');
                    window.location.href = '/';
                }
            });
        </script>
    </body>
    </html>
    """

@app.get("/mindmaps-page", response_class=HTMLResponse)
async def get_mindmaps_page():
    return """
    <!DOCTYPE html>
    <html>
    <head>
        <title>思维导图系统 - 思维导图</title>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <style>
            /* 基础样式，和仪表板页面相同 */
            body {
                font-family: Arial, sans-serif;
                margin: 0;
                padding: 0;
                background-color: #f5f7fa;
                color: #333;
            }
            .dashboard-container {
                display: flex;
                min-height: 100vh;
            }
            .sidebar {
                width: 240px;
                background-color: #2c3e50;
                color: white;
                padding: 20px 0;
            }
            .sidebar-header {
                padding: 0 20px 20px 20px;
                border-bottom: 1px solid #3d556c;
                margin-bottom: 20px;
            }
            .sidebar-header h1 {
                font-size: 20px;
                margin: 0;
            }
            .sidebar-menu {
                list-style: none;
                padding: 0;
                margin: 0;
            }
            .sidebar-menu li {
                padding: 12px 20px;
                cursor: pointer;
                transition: background-color 0.3s;
            }
            .sidebar-menu li:hover, .sidebar-menu li.active {
                background-color: #3d556c;
            }
            .sidebar-menu a {
                color: white;
                text-decoration: none;
                display: block;
            }
            .main-content {
                flex: 1;
                padding: 30px;
            }
            .header {
                display: flex;
                justify-content: space-between;
                align-items: center;
                margin-bottom: 30px;
            }
            .header h1 {
                margin: 0;
                font-size: 24px;
            }
            .user-info {
                display: flex;
                align-items: center;
                gap: 10px;
            }
            .avatar {
                width: 40px;
                height: 40px;
                border-radius: 50%;
                background-color: #4a90e2;
                color: white;
                display: flex;
                justify-content: center;
                align-items: center;
                font-weight: bold;
            }
            /* 思维导图特定样式 */
            .page-actions {
                display: flex;
                justify-content: space-between;
                align-items: center;
                margin-bottom: 20px;
            }
            .search-bar {
                display: flex;
                gap: 10px;
                flex: 1;
                max-width: 500px;
            }
            .search-input {
                flex: 1;
                padding: 10px 15px;
                border: 1px solid #ddd;
                border-radius: 4px;
                font-size: 14px;
            }
            .btn {
                padding: 10px 20px;
                background-color: #4a90e2;
                color: white;
                border: none;
                border-radius: 4px;
                cursor: pointer;
                font-size: 14px;
                transition: background-color 0.3s;
            }
            .btn:hover {
                background-color: #3a7fcb;
            }
            .mindmap-grid {
                display: grid;
                grid-template-columns: repeat(auto-fill, minmax(250px, 1fr));
                gap: 20px;
            }
            .mindmap-card {
                background-color: white;
                border-radius: 8px;
                box-shadow: 0 2px 10px rgba(0, 0, 0, 0.05);
                overflow: hidden;
                transition: transform 0.3s, box-shadow 0.3s;
            }
            .mindmap-card:hover {
                transform: translateY(-5px);
                box-shadow: 0 5px 15px rgba(0, 0, 0, 0.1);
            }
            .mindmap-preview {
                height: 150px;
                background-color: #eef5fd;
                display: flex;
                justify-content: center;
                align-items: center;
                color: #4a90e2;
                font-size: 36px;
            }
            .mindmap-info {
                padding: 15px;
            }
            .mindmap-title {
                margin: 0 0 10px 0;
                font-size: 16px;
                font-weight: 500;
            }
            .mindmap-desc {
                margin: 0 0 15px 0;
                font-size: 14px;
                color: #666;
                height: 40px;
                overflow: hidden;
            }
            .mindmap-meta {
                display: flex;
                justify-content: space-between;
                font-size: 12px;
                color: #999;
            }
            /* 模态框样式 */
            .modal {
                display: none;
                position: fixed;
                top: 0;
                left: 0;
                right: 0;
                bottom: 0;
                background-color: rgba(0, 0, 0, 0.5);
                z-index: 1000;
                justify-content: center;
                align-items: center;
            }
            .modal-content {
                background-color: white;
                border-radius: 8px;
                width: 500px;
                max-width: 90%;
                padding: 25px;
            }
            .modal-header {
                display: flex;
                justify-content: space-between;
                align-items: center;
                margin-bottom: 20px;
            }
            .modal-header h2 {
                margin: 0;
                font-size: 20px;
            }
            .close-btn {
                background: none;
                border: none;
                font-size: 20px;
                cursor: pointer;
                color: #999;
            }
            .form-group {
                margin-bottom: 20px;
            }
            .form-group label {
                display: block;
                margin-bottom: 8px;
                font-weight: 500;
            }
            .form-control {
                width: 100%;
                padding: 10px 15px;
                border: 1px solid #ddd;
                border-radius: 4px;
                font-size: 14px;
                box-sizing: border-box;
            }
            .modal-footer {
                display: flex;
                justify-content: flex-end;
                gap: 10px;
            }
        </style>
    </head>
    <body>
        <div class="dashboard-container">
            <div class="sidebar">
                <div class="sidebar-header">
                    <h1>思维导图系统</h1>
                </div>
                <ul class="sidebar-menu">
                    <li><a href="/dashboard">仪表板</a></li>
                    <li class="active"><a href="/mindmaps-page">思维导图</a></li>
                    <li><a href="/materials-page">资料管理</a></li>
                    <li><a href="/forum-page">讨论交流</a></li>
                    <li><a href="/settings-page">个人中心</a></li>
                </ul>
            </div>
            <div class="main-content">
                <div class="header">
                    <h1>我的思维导图</h1>
                    <div class="user-info">
                        <span>管理员</span>
                        <div class="avatar">A</div>
                    </div>
                </div>
                
                <div class="page-actions">
                    <div class="search-bar">
                        <input type="text" class="search-input" placeholder="搜索思维导图...">
                        <button class="btn">搜索</button>
                    </div>
                    <button class="btn" id="createBtn">创建新思维导图</button>
                </div>
                
                <div class="mindmap-grid">
                    <div class="mindmap-card">
                        <div class="mindmap-preview">🧠</div>
                        <div class="mindmap-info">
                            <h3 class="mindmap-title">Python基础知识</h3>
                            <p class="mindmap-desc">Python语言核心概念和基础语法的思维导图</p>
                            <div class="mindmap-meta">
                                <span>创建于: 2023-06-10</span>
                                <span>节点数: 35</span>
                            </div>
                        </div>
                    </div>
                    <div class="mindmap-card">
                        <div class="mindmap-preview">🧠</div>
                        <div class="mindmap-info">
                            <h3 class="mindmap-title">数据结构与算法</h3>
                            <p class="mindmap-desc">常见数据结构和算法的整理与分析</p>
                            <div class="mindmap-meta">
                                <span>创建于: 2023-05-22</span>
                                <span>节点数: 42</span>
                            </div>
                        </div>
                    </div>
                    <div class="mindmap-card">
                        <div class="mindmap-preview">🧠</div>
                        <div class="mindmap-info">
                            <h3 class="mindmap-title">Web开发技术栈</h3>
                            <p class="mindmap-desc">前后端开发技术栈的全面梳理</p>
                            <div class="mindmap-meta">
                                <span>创建于: 2023-06-01</span>
                                <span>节点数: 50</span>
                            </div>
                        </div>
                    </div>
                    <div class="mindmap-card">
                        <div class="mindmap-preview">🧠</div>
                        <div class="mindmap-info">
                            <h3 class="mindmap-title">机器学习基础</h3>
                            <p class="mindmap-desc">机器学习基本概念与常用算法</p>
                            <div class="mindmap-meta">
                                <span>创建于: 2023-04-15</span>
                                <span>节点数: 28</span>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
        
        <!-- 创建思维导图的模态框 -->
        <div class="modal" id="createModal">
            <div class="modal-content">
                <div class="modal-header">
                    <h2>创建新思维导图</h2>
                    <button class="close-btn">&times;</button>
                </div>
                <form id="createForm">
                    <div class="form-group">
                        <label for="title">标题</label>
                        <input type="text" id="title" class="form-control" required>
                    </div>
                    <div class="form-group">
                        <label for="description">描述</label>
                        <textarea id="description" class="form-control" rows="3"></textarea>
                    </div>
                    <div class="modal-footer">
                        <button type="button" class="btn" style="background-color: #6c757d;">取消</button>
                        <button type="submit" class="btn">创建</button>
                    </div>
                </form>
            </div>
        </div>
        
        <script>
            // 模态框操作
            const modal = document.getElementById('createModal');
            const createBtn = document.getElementById('createBtn');
            const closeBtn = document.querySelector('.close-btn');
            const cancelBtn = document.querySelector('.modal-footer button:first-child');
            
            createBtn.addEventListener('click', () => {
                modal.style.display = 'flex';
            });
            
            closeBtn.addEventListener('click', () => {
                modal.style.display = 'none';
            });
            
            cancelBtn.addEventListener('click', () => {
                modal.style.display = 'none';
            });
            
            // 点击模态框外部关闭
            window.addEventListener('click', (e) => {
                if (e.target === modal) {
                    modal.style.display = 'none';
                }
            });
            
            // 表单提交
            document.getElementById('createForm').addEventListener('submit', (e) => {
                e.preventDefault();
                const title = document.getElementById('title').value;
                const description = document.getElementById('description').value;
                
                // 这里可以添加API调用来创建思维导图
                console.log('创建思维导图:', { title, description });
                
                // 关闭模态框
                modal.style.display = 'none';
                
                // 清空表单
                e.target.reset();
            });
        </script>
    </body>
    </html>
    """

@app.get("/materials-page", response_class=HTMLResponse)
async def get_materials_page():
    return """
    <!DOCTYPE html>
    <html>
    <head>
        <title>思维导图系统 - 资料管理</title>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <style>
            /* 基础样式，和仪表板页面相同 */
            body {
                font-family: Arial, sans-serif;
                margin: 0;
                padding: 0;
                background-color: #f5f7fa;
                color: #333;
            }
            .dashboard-container {
                display: flex;
                min-height: 100vh;
            }
            .sidebar {
                width: 240px;
                background-color: #2c3e50;
                color: white;
                padding: 20px 0;
            }
            .sidebar-header {
                padding: 0 20px 20px 20px;
                border-bottom: 1px solid #3d556c;
                margin-bottom: 20px;
            }
            .sidebar-header h1 {
                font-size: 20px;
                margin: 0;
            }
            .sidebar-menu {
                list-style: none;
                padding: 0;
                margin: 0;
            }
            .sidebar-menu li {
                padding: 12px 20px;
                cursor: pointer;
                transition: background-color 0.3s;
            }
            .sidebar-menu li:hover, .sidebar-menu li.active {
                background-color: #3d556c;
            }
            .sidebar-menu a {
                color: white;
                text-decoration: none;
                display: block;
            }
            .main-content {
                flex: 1;
                padding: 30px;
            }
            .header {
                display: flex;
                justify-content: space-between;
                align-items: center;
                margin-bottom: 30px;
            }
            .header h1 {
                margin: 0;
                font-size: 24px;
            }
            .user-info {
                display: flex;
                align-items: center;
                gap: 10px;
            }
            .avatar {
                width: 40px;
                height: 40px;
                border-radius: 50%;
                background-color: #4a90e2;
                color: white;
                display: flex;
                justify-content: center;
                align-items: center;
                font-weight: bold;
            }
            /* 资料管理特定样式 */
            .page-actions {
                display: flex;
                justify-content: space-between;
                align-items: center;
                margin-bottom: 20px;
            }
            .search-filters {
                display: flex;
                gap: 10px;
                flex: 1;
            }
            .search-input {
                flex: 1;
                padding: 10px 15px;
                border: 1px solid #ddd;
                border-radius: 4px;
                font-size: 14px;
            }
            .filter-select {
                padding: 10px;
                border: 1px solid #ddd;
                border-radius: 4px;
                background-color: white;
            }
            .btn {
                padding: 10px 20px;
                background-color: #4a90e2;
                color: white;
                border: none;
                border-radius: 4px;
                cursor: pointer;
                font-size: 14px;
                transition: background-color 0.3s;
            }
            .btn:hover {
                background-color: #3a7fcb;
            }
            .materials-list {
                background-color: white;
                border-radius: 8px;
                box-shadow: 0 2px 10px rgba(0, 0, 0, 0.05);
                overflow: hidden;
            }
            .material-item {
                display: flex;
                padding: 15px 20px;
                border-bottom: 1px solid #eee;
                transition: background-color 0.3s;
            }
            .material-item:hover {
                background-color: #f9f9f9;
            }
            .material-item:last-child {
                border-bottom: none;
            }
            .material-icon {
                font-size: 24px;
                margin-right: 15px;
                display: flex;
                align-items: center;
                color: #4a90e2;
            }
            .material-info {
                flex: 1;
            }
            .material-title {
                font-size: 16px;
                font-weight: 500;
                margin: 0 0 5px 0;
            }
            .material-desc {
                font-size: 14px;
                color: #666;
                margin: 0 0 10px 0;
            }
            .material-meta {
                display: flex;
                font-size: 12px;
                color: #999;
                gap: 15px;
            }
            .material-actions {
                display: flex;
                align-items: center;
                gap: 10px;
            }
            .action-btn {
                background: none;
                border: none;
                color: #4a90e2;
                cursor: pointer;
                font-size: 14px;
            }
            .action-btn:hover {
                text-decoration: underline;
            }
            /* 模态框样式 */
            .modal {
                display: none;
                position: fixed;
                top: 0;
                left: 0;
                right: 0;
                bottom: 0;
                background-color: rgba(0, 0, 0, 0.5);
                z-index: 1000;
                justify-content: center;
                align-items: center;
            }
            .modal-content {
                background-color: white;
                border-radius: 8px;
                width: 500px;
                max-width: 90%;
                padding: 25px;
            }
            .modal-header {
                display: flex;
                justify-content: space-between;
                align-items: center;
                margin-bottom: 20px;
            }
            .modal-header h2 {
                margin: 0;
                font-size: 20px;
            }
            .close-btn {
                background: none;
                border: none;
                font-size: 20px;
                cursor: pointer;
                color: #999;
            }
            .form-group {
                margin-bottom: 20px;
            }
            .form-group label {
                display: block;
                margin-bottom: 8px;
                font-weight: 500;
            }
            .form-control {
                width: 100%;
                padding: 10px 15px;
                border: 1px solid #ddd;
                border-radius: 4px;
                font-size: 14px;
                box-sizing: border-box;
            }
            .modal-footer {
                display: flex;
                justify-content: flex-end;
                gap: 10px;
            }
        </style>
    </head>
    <body>
        <div class="dashboard-container">
            <div class="sidebar">
                <div class="sidebar-header">
                    <h1>思维导图系统</h1>
                </div>
                <ul class="sidebar-menu">
                    <li><a href="/dashboard">仪表板</a></li>
                    <li><a href="/mindmaps-page">思维导图</a></li>
                    <li class="active"><a href="/materials-page">资料管理</a></li>
                    <li><a href="/forum-page">讨论交流</a></li>
                    <li><a href="/settings-page">个人中心</a></li>
                </ul>
            </div>
            <div class="main-content">
                <div class="header">
                    <h1>资料管理</h1>
                    <div class="user-info">
                        <span>管理员</span>
                        <div class="avatar">A</div>
                    </div>
                </div>
                
                <div class="page-actions">
                    <div class="search-filters">
                        <input type="text" class="search-input" placeholder="搜索资料...">
                        <select class="filter-select">
                            <option value="">所有类型</option>
                            <option value="document">文档</option>
                            <option value="image">图片</option>
                            <option value="video">视频</option>
                            <option value="other">其他</option>
                        </select>
                        <select class="filter-select">
                            <option value="newest">最新上传</option>
                            <option value="name">按名称排序</option>
                            <option value="size">按大小排序</option>
                        </select>
                    </div>
                    <button class="btn" id="uploadBtn">上传资料</button>
                </div>
                
                <div class="materials-list">
                    <div class="material-item">
                        <div class="material-icon">📄</div>
                        <div class="material-info">
                            <h3 class="material-title">Python编程指南.pdf</h3>
                            <p class="material-desc">全面的Python编程语言指南，包含从基础到高级的全部内容</p>
                            <div class="material-meta">
                                <span>上传于: 2023-06-15</span>
                                <span>大小: 5.2MB</span>
                                <span>下载: 28次</span>
                            </div>
                        </div>
                        <div class="material-actions">
                            <button class="action-btn">下载</button>
                            <button class="action-btn">分享</button>
                            <button class="action-btn">删除</button>
                        </div>
                    </div>
                    <div class="material-item">
                        <div class="material-icon">🖼️</div>
                        <div class="material-info">
                            <h3 class="material-title">数据结构思维导图.png</h3>
                            <p class="material-desc">包含常见数据结构的思维导图，直观展示各种数据结构的特点和应用</p>
                            <div class="material-meta">
                                <span>上传于: 2023-06-10</span>
                                <span>大小: 1.8MB</span>
                                <span>下载: 15次</span>
                            </div>
                        </div>
                        <div class="material-actions">
                            <button class="action-btn">下载</button>
                            <button class="action-btn">分享</button>
                            <button class="action-btn">删除</button>
                        </div>
                    </div>
                    <div class="material-item">
                        <div class="material-icon">📄</div>
                        <div class="material-info">
                            <h3 class="material-title">机器学习算法总结.docx</h3>
                            <p class="material-desc">常用机器学习算法的原理和应用场景总结</p>
                            <div class="material-meta">
                                <span>上传于: 2023-05-22</span>
                                <span>大小: 3.5MB</span>
                                <span>下载: 42次</span>
                            </div>
                        </div>
                        <div class="material-actions">
                            <button class="action-btn">下载</button>
                            <button class="action-btn">分享</button>
                            <button class="action-btn">删除</button>
                        </div>
                    </div>
                    <div class="material-item">
                        <div class="material-icon">🎬</div>
                        <div class="material-info">
                            <h3 class="material-title">Web开发入门教程.mp4</h3>
                            <p class="material-desc">Web开发入门视频教程，包含HTML、CSS和JavaScript基础知识</p>
                            <div class="material-meta">
                                <span>上传于: 2023-04-18</span>
                                <span>大小: 120MB</span>
                                <span>下载: 56次</span>
                            </div>
                        </div>
                        <div class="material-actions">
                            <button class="action-btn">下载</button>
                            <button class="action-btn">分享</button>
                            <button class="action-btn">删除</button>
                        </div>
                    </div>
                </div>
            </div>
        </div>
        
        <!-- 上传资料的模态框 -->
        <div class="modal" id="uploadModal">
            <div class="modal-content">
                <div class="modal-header">
                    <h2>上传资料</h2>
                    <button class="close-btn">&times;</button>
                </div>
                <form id="uploadForm">
                    <div class="form-group">
                        <label for="file">选择文件</label>
                        <input type="file" id="file" class="form-control" required>
                    </div>
                    <div class="form-group">
                        <label for="title">标题</label>
                        <input type="text" id="title" class="form-control" required>
                    </div>
                    <div class="form-group">
                        <label for="description">描述</label>
                        <textarea id="description" class="form-control" rows="3"></textarea>
                    </div>
                    <div class="form-group">
                        <label for="type">类型</label>
                        <select id="type" class="form-control">
                            <option value="document">文档</option>
                            <option value="image">图片</option>
                            <option value="video">视频</option>
                            <option value="other">其他</option>
                        </select>
                    </div>
                    <div class="modal-footer">
                        <button type="button" class="btn" style="background-color: #6c757d;">取消</button>
                        <button type="submit" class="btn">上传</button>
                    </div>
                </form>
            </div>
        </div>
        
        <script>
            // 模态框操作
            const modal = document.getElementById('uploadModal');
            const uploadBtn = document.getElementById('uploadBtn');
            const closeBtn = document.querySelector('.close-btn');
            const cancelBtn = document.querySelector('.modal-footer button:first-child');
            
            uploadBtn.addEventListener('click', () => {
                modal.style.display = 'flex';
            });
            
            closeBtn.addEventListener('click', () => {
                modal.style.display = 'none';
            });
            
            cancelBtn.addEventListener('click', () => {
                modal.style.display = 'none';
            });
            
            // 点击模态框外部关闭
            window.addEventListener('click', (e) => {
                if (e.target === modal) {
                    modal.style.display = 'none';
                }
            });
            
            // 表单提交
            document.getElementById('uploadForm').addEventListener('submit', (e) => {
                e.preventDefault();
                const file = document.getElementById('file').files[0];
                const title = document.getElementById('title').value;
                const description = document.getElementById('description').value;
                const type = document.getElementById('type').value;
                
                // 这里可以添加API调用来上传资料
                console.log('上传资料:', { file, title, description, type });
                
                // 关闭模态框
                modal.style.display = 'none';
                
                // 清空表单
                e.target.reset();
            });
        </script>
    </body>
    </html>
    """

@app.get("/settings-page", response_class=HTMLResponse)
async def get_settings_page():
    return """
    <!DOCTYPE html>
    <html>
    <head>
        <title>思维导图系统 - 个人中心</title>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <style>
            /* 基础样式，和仪表板页面相同 */
            body {
                font-family: Arial, sans-serif;
                margin: 0;
                padding: 0;
                background-color: #f5f7fa;
                color: #333;
            }
            .dashboard-container {
                display: flex;
                min-height: 100vh;
            }
            .sidebar {
                width: 240px;
                background-color: #2c3e50;
                color: white;
                padding: 20px 0;
            }
            .sidebar-header {
                padding: 0 20px 20px 20px;
                border-bottom: 1px solid #3d556c;
                margin-bottom: 20px;
            }
            .sidebar-header h1 {
                font-size: 20px;
                margin: 0;
            }
            .sidebar-menu {
                list-style: none;
                padding: 0;
                margin: 0;
            }
            .sidebar-menu li {
                padding: 12px 20px;
                cursor: pointer;
                transition: background-color 0.3s;
            }
            .sidebar-menu li:hover, .sidebar-menu li.active {
                background-color: #3d556c;
            }
            .sidebar-menu a {
                color: white;
                text-decoration: none;
                display: block;
            }
            .main-content {
                flex: 1;
                padding: 30px;
            }
            .header {
                display: flex;
                justify-content: space-between;
                align-items: center;
                margin-bottom: 30px;
            }
            .header h1 {
                margin: 0;
                font-size: 24px;
            }
            .user-info {
                display: flex;
                align-items: center;
                gap: 10px;
            }
            .avatar {
                width: 40px;
                height: 40px;
                border-radius: 50%;
                background-color: #4a90e2;
                color: white;
                display: flex;
                justify-content: center;
                align-items: center;
                font-weight: bold;
            }
            /* 个人中心特定样式 */
            .settings-card {
                background-color: white;
                border-radius: 8px;
                box-shadow: 0 2px 10px rgba(0, 0, 0, 0.05);
                padding: 25px;
                margin-bottom: 20px;
            }
            .settings-card h2 {
                margin-top: 0;
                font-size: 18px;
                margin-bottom: 20px;
                padding-bottom: 10px;
                border-bottom: 1px solid #eee;
            }
            .form-row {
                display: flex;
                gap: 20px;
                margin-bottom: 20px;
            }
            .form-column {
                flex: 1;
            }
            .form-group {
                margin-bottom: 20px;
            }
            label {
                display: block;
                margin-bottom: 8px;
                font-weight: 500;
                color: #555;
            }
            .form-control {
                width: 100%;
                padding: 12px 15px;
                border: 1px solid #ddd;
                border-radius: 4px;
                font-size: 16px;
                box-sizing: border-box;
            }
            .btn {
                padding: 12px 20px;
                border: none;
                border-radius: 4px;
                font-size: 16px;
                font-weight: 500;
                cursor: pointer;
                background-color: #4a90e2;
                color: white;
            }
            .btn-danger {
                background-color: #dc3545;
            }
            .profile-header {
                display: flex;
                align-items: center;
                gap: 30px;
                margin-bottom: 20px;
            }
            .profile-avatar {
                width: 100px;
                height: 100px;
                border-radius: 50%;
                background-color: #4a90e2;
                color: white;
                display: flex;
                justify-content: center;
                align-items: center;
                font-size: 48px;
                font-weight: bold;
            }
            .profile-info {
                flex: 1;
            }
            .danger-zone {
                border: 1px solid #f5c6cb;
                background-color: #fff8f8;
            }
            .danger-zone h2 {
                color: #721c24;
            }
            .danger-action {
                display: flex;
                justify-content: space-between;
                align-items: center;
            }
            .danger-action h3 {
                margin: 0 0 5px 0;
                color: #721c24;
            }
            .danger-action p {
                margin: 0;
                color: #6c757d;
            }
            .modal {
                display: none;
                position: fixed;
                top: 0;
                left: 0;
                right: 0;
                bottom: 0;
                background-color: rgba(0, 0, 0, 0.5);
                z-index: 100;
                justify-content: center;
                align-items: center;
            }
            .modal-content {
                width: 400px;
                background-color: white;
                border-radius: 8px;
                padding: 20px;
            }
            .modal-content h2 {
                margin-top: 0;
            }
            .modal-footer {
                display: flex;
                justify-content: flex-end;
                gap: 10px;
                margin-top: 20px;
            }
        </style>
    </head>
    <body>
        <div class="dashboard-container">
            <div class="sidebar">
                <div class="sidebar-header">
                    <h1>思维导图系统</h1>
                </div>
                <ul class="sidebar-menu">
                    <li><a href="/dashboard">仪表板</a></li>
                    <li><a href="/mindmaps-page">思维导图</a></li>
                    <li><a href="/materials-page">资料管理</a></li>
                    <li><a href="/forum-page">讨论交流</a></li>
                    <li class="active"><a href="/settings-page">个人中心</a></li>
                </ul>
            </div>
            <div class="main-content">
                <div class="header">
                    <h1>个人中心</h1>
                    <div class="user-info">
                        <span>管理员</span>
                        <div class="avatar">A</div>
                    </div>
                </div>
                
                <div class="settings-card">
                    <div class="profile-header">
                        <div class="profile-avatar">A</div>
                        <div class="profile-info">
                            <h2>管理员</h2>
                            <p>管理员账户</p>
                            <p>邮箱: admin@example.com</p>
                            <p>注册时间: 2023-01-01</p>
                        </div>
                    </div>
                </div>
                
                <div class="settings-card">
                    <h2>个人资料</h2>
                    <form id="profileForm">
                        <div class="form-row">
                            <div class="form-column">
                                <div class="form-group">
                                    <label for="username">用户名</label>
                                    <input type="text" id="username" class="form-control" value="管理员">
                                </div>
                                <div class="form-group">
                                    <label for="email">邮箱</label>
                                    <input type="email" id="email" class="form-control" value="admin@example.com">
                                </div>
                            </div>
                            <div class="form-column">
                                <div class="form-group">
                                    <label for="bio">个人简介</label>
                                    <textarea id="bio" class="form-control" rows="5">系统管理员账户，负责管理系统各项功能和用户。</textarea>
                                </div>
                            </div>
                        </div>
                        <button type="submit" class="btn">保存修改</button>
                    </form>
                </div>
                
                <div class="settings-card">
                    <h2>修改密码</h2>
                    <form id="passwordForm">
                        <div class="form-row">
                            <div class="form-column">
                                <div class="form-group">
                                    <label for="currentPassword">当前密码</label>
                                    <input type="password" id="currentPassword" class="form-control" placeholder="请输入当前密码">
                                </div>
                            </div>
                            <div class="form-column">
                                <div class="form-group">
                                    <label for="newPassword">新密码</label>
                                    <input type="password" id="newPassword" class="form-control" placeholder="请输入新密码">
                                </div>
                                <div class="form-group">
                                    <label for="confirmPassword">确认新密码</label>
                                    <input type="password" id="confirmPassword" class="form-control" placeholder="请再次输入新密码">
                                </div>
                            </div>
                        </div>
                        <button type="submit" class="btn">更改密码</button>
                    </form>
                </div>
                
                <div class="settings-card danger-zone">
                    <h2>危险操作</h2>
                    <div class="danger-action">
                        <div>
                            <h3>注销账户</h3>
                            <p>注销后，您的所有数据将被永久删除，且无法恢复</p>
                        </div>
                        <button id="deleteAccountBtn" class="btn btn-danger">注销账户</button>
                    </div>
                </div>
            </div>
        </div>
        
        <!-- 确认注销账户的模态框 -->
        <div id="deleteModal" class="modal">
            <div class="modal-content">
                <h2>确认注销账户?</h2>
                <p>此操作无法撤销，您的所有数据将被永久删除。</p>
                <div class="modal-footer">
                    <button id="cancelDeleteBtn" class="btn" style="background-color: #6c757d;">取消</button>
                    <button id="confirmDeleteBtn" class="btn btn-danger">确认注销</button>
                </div>
            </div>
        </div>
        
        <script>
            // 表单提交处理
            document.getElementById('profileForm').addEventListener('submit', function(e) {
                e.preventDefault();
                // 这里应该添加API调用来保存个人资料
                alert('个人资料已更新！');
            });
            
            document.getElementById('passwordForm').addEventListener('submit', function(e) {
                e.preventDefault();
                const currentPassword = document.getElementById('currentPassword').value;
                const newPassword = document.getElementById('newPassword').value;
                const confirmPassword = document.getElementById('confirmPassword').value;
                
                if (newPassword !== confirmPassword) {
                    alert('两次输入的新密码不一致');
                    return;
                }
                
                // 这里应该添加API调用来更改密码
                alert('密码已更改！');
                this.reset();
            });
            
            // 注销账户模态框处理
            const deleteModal = document.getElementById('deleteModal');
            const deleteAccountBtn = document.getElementById('deleteAccountBtn');
            const cancelDeleteBtn = document.getElementById('cancelDeleteBtn');
            const confirmDeleteBtn = document.getElementById('confirmDeleteBtn');
            
            deleteAccountBtn.addEventListener('click', function() {
                deleteModal.style.display = 'flex';
            });
            
            cancelDeleteBtn.addEventListener('click', function() {
                deleteModal.style.display = 'none';
            });
            
            confirmDeleteBtn.addEventListener('click', function() {
                // 这里应该添加API调用来注销账户
                alert('账户已注销！');
                window.location.href = '/';
            });
            
            // 点击模态框外部关闭
            window.addEventListener('click', function(e) {
                if (e.target === deleteModal) {
                    deleteModal.style.display = 'none';
                }
            });
        </script>
    </body>
    </html>
    """

@app.get("/forum-page", response_class=HTMLResponse)
async def get_forum_page():
    return """
    <!DOCTYPE html>
    <html>
    <head>
        <title>思维导图系统 - 讨论交流</title>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <style>
            /* 基础样式，和仪表板页面相同 */
            body {
                font-family: Arial, sans-serif;
                margin: 0;
                padding: 0;
                background-color: #f5f7fa;
                color: #333;
            }
            .dashboard-container {
                display: flex;
                min-height: 100vh;
            }
            .sidebar {
                width: 240px;
                background-color: #2c3e50;
                color: white;
                padding: 20px 0;
            }
            .sidebar-header {
                padding: 0 20px 20px 20px;
                border-bottom: 1px solid #3d556c;
                margin-bottom: 20px;
            }
            .sidebar-header h1 {
                font-size: 20px;
                margin: 0;
            }
            .sidebar-menu {
                list-style: none;
                padding: 0;
                margin: 0;
            }
            .sidebar-menu li {
                padding: 12px 20px;
                cursor: pointer;
                transition: background-color 0.3s;
            }
            .sidebar-menu li:hover, .sidebar-menu li.active {
                background-color: #3d556c;
            }
            .sidebar-menu a {
                color: white;
                text-decoration: none;
                display: block;
            }
            .main-content {
                flex: 1;
                padding: 30px;
            }
            .header {
                display: flex;
                justify-content: space-between;
                align-items: center;
                margin-bottom: 30px;
            }
            .header h1 {
                margin: 0;
                font-size: 24px;
            }
            .user-info {
                display: flex;
                align-items: center;
                gap: 10px;
            }
            .avatar {
                width: 40px;
                height: 40px;
                border-radius: 50%;
                background-color: #4a90e2;
                color: white;
                display: flex;
                justify-content: center;
                align-items: center;
                font-weight: bold;
            }
            /* 讨论交流特定样式 */
            .page-actions {
                display: flex;
                justify-content: space-between;
                align-items: center;
                margin-bottom: 20px;
            }
            .search-bar {
                display: flex;
                gap: 10px;
                flex: 1;
                max-width: 400px;
            }
            .search-input {
                flex: 1;
                padding: 10px 15px;
                border: 1px solid #ddd;
                border-radius: 4px;
                font-size: 14px;
            }
            .btn {
                padding: 10px 20px;
                border: none;
                border-radius: 4px;
                font-size: 14px;
                font-weight: 500;
                cursor: pointer;
                background-color: #4a90e2;
                color: white;
            }
            .topic-list {
                background-color: white;
                border-radius: 8px;
                box-shadow: 0 2px 10px rgba(0, 0, 0, 0.05);
                overflow: hidden;
            }
            .topic {
                padding: 15px 20px;
                border-bottom: 1px solid #eee;
                display: flex;
                gap: 15px;
            }
            .topic:last-child {
                border-bottom: none;
            }
            .topic-content {
                flex: 1;
            }
            .topic-title {
                font-size: 16px;
                font-weight: 500;
                margin-bottom: 5px;
            }
            .topic-title a {
                color: #333;
                text-decoration: none;
            }
            .topic-title a:hover {
                color: #4a90e2;
            }
            .topic-meta {
                color: #777;
                font-size: 12px;
                display: flex;
                gap: 15px;
            }
            .topic-stats {
                min-width: 100px;
                display: flex;
                flex-direction: column;
                align-items: center;
                justify-content: center;
            }
            .stats-item {
                font-size: 12px;
                color: #777;
                text-align: center;
            }
            .stats-value {
                font-size: 16px;
                font-weight: 500;
                color: #333;
            }
            .topic-last-reply {
                min-width: 150px;
                font-size: 12px;
                color: #777;
            }
            .reply-time {
                margin-top: 5px;
            }
            .pagination {
                display: flex;
                justify-content: center;
                margin-top: 30px;
                gap: 5px;
            }
            .page-item {
                padding: 8px 12px;
                border: 1px solid #ddd;
                border-radius: 4px;
                background-color: white;
                color: #333;
                text-decoration: none;
                transition: background-color 0.3s;
            }
            .page-item.active {
                background-color: #4a90e2;
                color: white;
                border-color: #4a90e2;
            }
            .page-item:hover:not(.active) {
                background-color: #f5f5f5;
            }
            .modal {
                display: none;
                position: fixed;
                top: 0;
                left: 0;
                right: 0;
                bottom: 0;
                background-color: rgba(0, 0, 0, 0.5);
                z-index: 100;
                justify-content: center;
                align-items: center;
            }
            .modal-content {
                width: 600px;
                background-color: white;
                border-radius: 8px;
                padding: 20px;
            }
            .modal-header {
                display: flex;
                justify-content: space-between;
                align-items: center;
                margin-bottom: 20px;
                padding-bottom: 10px;
                border-bottom: 1px solid #eee;
            }
            .modal-header h2 {
                margin: 0;
                font-size: 18px;
            }
            .close-btn {
                background: none;
                border: none;
                font-size: 20px;
                cursor: pointer;
                color: #777;
            }
            .form-group {
                margin-bottom: 20px;
            }
            label {
                display: block;
                margin-bottom: 8px;
                font-weight: 500;
                color: #555;
            }
            .form-control {
                width: 100%;
                padding: 12px 15px;
                border: 1px solid #ddd;
                border-radius: 4px;
                font-size: 14px;
                box-sizing: border-box;
            }
            .modal-footer {
                display: flex;
                justify-content: flex-end;
                gap: 10px;
                margin-top: 20px;
            }
        </style>
    </head>
    <body>
        <div class="dashboard-container">
            <div class="sidebar">
                <div class="sidebar-header">
                    <h1>思维导图系统</h1>
                </div>
                <ul class="sidebar-menu">
                    <li><a href="/dashboard">仪表板</a></li>
                    <li><a href="/mindmaps-page">思维导图</a></li>
                    <li><a href="/materials-page">资料管理</a></li>
                    <li class="active"><a href="/forum-page">讨论交流</a></li>
                    <li><a href="/settings-page">个人中心</a></li>
                </ul>
            </div>
            <div class="main-content">
                <div class="header">
                    <h1>讨论交流</h1>
                    <div class="user-info">
                        <span>管理员</span>
                        <div class="avatar">A</div>
                    </div>
                </div>
                
                <div class="page-actions">
                    <div class="search-bar">
                        <input type="text" class="search-input" placeholder="搜索讨论...">
                        <button class="btn">搜索</button>
                    </div>
                    <button id="newTopicBtn" class="btn">发起讨论</button>
                </div>
                
                <div class="topic-list">
                    <div class="topic">
                        <div class="topic-content">
                            <div class="topic-title">
                                <a href="#">思维导图在学习Python编程中的应用</a>
                            </div>
                            <div class="topic-meta">
                                <span>作者: 管理员</span>
                                <span>发布于: 2023-06-10</span>
                                <span>分类: Python学习</span>
                            </div>
                        </div>
                        <div class="topic-stats">
                            <div class="stats-item">
                                <div class="stats-value">24</div>
                                <div>浏览</div>
                            </div>
                        </div>
                        <div class="topic-stats">
                            <div class="stats-item">
                                <div class="stats-value">5</div>
                                <div>回复</div>
                            </div>
                        </div>
                        <div class="topic-last-reply">
                            <div>最后回复: 李明</div>
                            <div class="reply-time">2023-06-12 14:30</div>
                        </div>
                    </div>
                    
                    <div class="topic">
                        <div class="topic-content">
                            <div class="topic-title">
                                <a href="#">关于如何构建高效的思维导图的讨论</a>
                            </div>
                            <div class="topic-meta">
                                <span>作者: 张三</span>
                                <span>发布于: 2023-06-08</span>
                                <span>分类: 思维导图方法</span>
                            </div>
                        </div>
                        <div class="topic-stats">
                            <div class="stats-item">
                                <div class="stats-value">32</div>
                                <div>浏览</div>
                            </div>
                        </div>
                        <div class="topic-stats">
                            <div class="stats-item">
                                <div class="stats-value">7</div>
                                <div>回复</div>
                            </div>
                        </div>
                        <div class="topic-last-reply">
                            <div>最后回复: 王五</div>
                            <div class="reply-time">2023-06-11 09:15</div>
                        </div>
                    </div>
                    
                    <div class="topic">
                        <div class="topic-content">
                            <div class="topic-title">
                                <a href="#">使用思维导图整理数据结构与算法</a>
                            </div>
                            <div class="topic-meta">
                                <span>作者: 李四</span>
                                <span>发布于: 2023-06-05</span>
                                <span>分类: 算法学习</span>
                            </div>
                        </div>
                        <div class="topic-stats">
                            <div class="stats-item">
                                <div class="stats-value">45</div>
                                <div>浏览</div>
                            </div>
                        </div>
                        <div class="topic-stats">
                            <div class="stats-item">
                                <div class="stats-value">12</div>
                                <div>回复</div>
                            </div>
                        </div>
                        <div class="topic-last-reply">
                            <div>最后回复: 管理员</div>
                            <div class="reply-time">2023-06-13 16:45</div>
                        </div>
                    </div>
                    
                    <div class="topic">
                        <div class="topic-content">
                            <div class="topic-title">
                                <a href="#">思维导图在项目管理中的应用经验分享</a>
                            </div>
                            <div class="topic-meta">
                                <span>作者: 赵六</span>
                                <span>发布于: 2023-06-02</span>
                                <span>分类: 项目管理</span>
                            </div>
                        </div>
                        <div class="topic-stats">
                            <div class="stats-item">
                                <div class="stats-value">38</div>
                                <div>浏览</div>
                            </div>
                        </div>
                        <div class="topic-stats">
                            <div class="stats-item">
                                <div class="stats-value">9</div>
                                <div>回复</div>
                            </div>
                        </div>
                        <div class="topic-last-reply">
                            <div>最后回复: 张三</div>
                            <div class="reply-time">2023-06-10 11:20</div>
                        </div>
                    </div>
                    
                    <div class="topic">
                        <div class="topic-content">
                            <div class="topic-title">
                                <a href="#">推荐几款好用的思维导图软件</a>
                            </div>
                            <div class="topic-meta">
                                <span>作者: 王五</span>
                                <span>发布于: 2023-05-30</span>
                                <span>分类: 工具推荐</span>
                            </div>
                        </div>
                        <div class="topic-stats">
                            <div class="stats-item">
                                <div class="stats-value">56</div>
                                <div>浏览</div>
                            </div>
                        </div>
                        <div class="topic-stats">
                            <div class="stats-item">
                                <div class="stats-value">15</div>
                                <div>回复</div>
                            </div>
                        </div>
                        <div class="topic-last-reply">
                            <div>最后回复: 李四</div>
                            <div class="reply-time">2023-06-09 08:40</div>
                        </div>
                    </div>
                </div>
                
                <div class="pagination">
                    <a href="#" class="page-item">上一页</a>
                    <a href="#" class="page-item active">1</a>
                    <a href="#" class="page-item">2</a>
                    <a href="#" class="page-item">3</a>
                    <a href="#" class="page-item">4</a>
                    <a href="#" class="page-item">5</a>
                    <a href="#" class="page-item">下一页</a>
                </div>
            </div>
        </div>
        
        <!-- 发起讨论的模态框 -->
        <div id="newTopicModal" class="modal">
            <div class="modal-content">
                <div class="modal-header">
                    <h2>发起新讨论</h2>
                    <button class="close-btn">&times;</button>
                </div>
                <form id="newTopicForm">
                    <div class="form-group">
                        <label for="topicTitle">标题</label>
                        <input type="text" id="topicTitle" class="form-control" required placeholder="请输入讨论标题">
                    </div>
                    <div class="form-group">
                        <label for="topicCategory">分类</label>
                        <select id="topicCategory" class="form-control">
                            <option value="mind-map-method">思维导图方法</option>
                            <option value="programming">编程学习</option>
                            <option value="tool">工具推荐</option>
                            <option value="project">项目管理</option>
                            <option value="other">其他</option>
                        </select>
                    </div>
                    <div class="form-group">
                        <label for="topicContent">内容</label>
                        <textarea id="topicContent" class="form-control" rows="10" required placeholder="请输入讨论内容..."></textarea>
                    </div>
                    <div class="modal-footer">
                        <button type="button" class="btn" style="background-color: #6c757d;">取消</button>
                        <button type="submit" class="btn">发布</button>
                    </div>
                </form>
            </div>
        </div>
        
        <script>
            // 模态框操作
            const modal = document.getElementById('newTopicModal');
            const newTopicBtn = document.getElementById('newTopicBtn');
            const closeBtn = document.querySelector('.close-btn');
            const cancelBtn = document.querySelector('.modal-footer button:first-child');
            
            newTopicBtn.addEventListener('click', () => {
                modal.style.display = 'flex';
            });
            
            closeBtn.addEventListener('click', () => {
                modal.style.display = 'none';
            });
            
            cancelBtn.addEventListener('click', () => {
                modal.style.display = 'none';
            });
            
            // 点击模态框外部关闭
            window.addEventListener('click', (e) => {
                if (e.target === modal) {
                    modal.style.display = 'none';
                }
            });
            
            // 表单提交
            document.getElementById('newTopicForm').addEventListener('submit', (e) => {
                e.preventDefault();
                const title = document.getElementById('topicTitle').value;
                const category = document.getElementById('topicCategory').value;
                const content = document.getElementById('topicContent').value;
                
                // 这里可以添加API调用来创建新讨论
                console.log('发起讨论:', { title, category, content });
                
                // 提示用户
                alert('讨论已发布！');
                
                // 关闭模态框
                modal.style.display = 'none';
                
                // 清空表单
                e.target.reset();
            });
        </script>
    </body>
    </html>
    """

@app.get("/register", response_class=HTMLResponse)
async def get_register_page():
    return """
    <!DOCTYPE html>
    <html>
    <head>
        <title>思维导图系统 - 注册</title>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <style>
            body { 
                font-family: Arial, sans-serif; 
                margin: 0; 
                padding: 0; 
                display: flex; 
                justify-content: center; 
                align-items: center; 
                height: 100vh; 
                flex-direction: column; 
                background-color: #f5f7fa; 
            }
            .register-card { 
                width: 400px; 
                padding: 30px; 
                border-radius: 8px; 
                background-color: white; 
                box-shadow: 0 4px 15px rgba(0, 0, 0, 0.1); 
            }
            h2 { 
                text-align: center; 
                color: #333; 
                margin-bottom: 10px; 
            }
            h3 { 
                text-align: center; 
                color: #555; 
                margin-bottom: 30px; 
            }
            .form-group { 
                margin-bottom: 20px; 
            }
            label { 
                display: block; 
                margin-bottom: 8px; 
                font-weight: 500; 
                color: #555; 
            }
            .form-control { 
                width: 100%; 
                padding: 12px 15px; 
                border: 1px solid #ddd; 
                border-radius: 4px; 
                font-size: 16px; 
                box-sizing: border-box; 
            }
            .btn { 
                width: 100%; 
                padding: 12px; 
                border: none; 
                border-radius: 4px; 
                font-size: 16px; 
                font-weight: 500; 
                cursor: pointer; 
                background-color: #4a90e2; 
                color: white; 
            }
            .register-footer { 
                margin-top: 25px; 
                text-align: center; 
                color: #777; 
            }
            a { 
                color: #4a90e2; 
                text-decoration: none; 
            }
            .alert {
                padding: 12px;
                border-radius: 4px;
                margin-bottom: 20px;
                background-color: #f8d7da;
                color: #721c24;
                border: 1px solid #f5c6cb;
                display: none;
            }
        </style>
    </head>
    <body>
        <div class="register-card">
            <h2>思维导图系统</h2>
            <h3>用户注册</h3>
            
            <div id="errorAlert" class="alert"></div>
            
            <form id="registerForm">
                <div class="form-group">
                    <label for="username">用户名</label>
                    <input type="text" id="username" class="form-control" required placeholder="请输入用户名">
                </div>
                
                <div class="form-group">
                    <label for="email">邮箱</label>
                    <input type="email" id="email" class="form-control" required placeholder="请输入邮箱">
                </div>
                
                <div class="form-group">
                    <label for="password">密码</label>
                    <input type="password" id="password" class="form-control" required placeholder="请输入密码 (至少6位)" minlength="6">
                </div>
                
                <div class="form-group">
                    <label for="confirmPassword">确认密码</label>
                    <input type="password" id="confirmPassword" class="form-control" required placeholder="请再次输入密码">
                </div>
                
                <button type="submit" class="btn" id="registerBtn">注册</button>
            </form>
            
            <div class="register-footer">
                <p>已有账号？ <a href="/">登录</a></p>
            </div>
        </div>

        <script>
            const registerForm = document.getElementById('registerForm');
            const errorAlert = document.getElementById('errorAlert');
            const passwordInput = document.getElementById('password');
            const confirmPasswordInput = document.getElementById('confirmPassword');
            const registerBtn = document.getElementById('registerBtn');
            
            // 注册表单提交
            registerForm.addEventListener('submit', async (e) => {
                e.preventDefault();
                
                // 表单验证
                const username = document.getElementById('username').value;
                const email = document.getElementById('email').value;
                const password = passwordInput.value;
                const confirmPassword = confirmPasswordInput.value;
                
                // 检查密码是否匹配
                if (password !== confirmPassword) {
                    showError('两次输入的密码不一致');
                    return;
                }
                
                try {
                    // 禁用按钮，防止重复提交
                    registerBtn.disabled = true;
                    registerBtn.textContent = '注册中...';
                    
                    // 发送注册请求
                    const response = await fetch('/api/auth/register', {
                        method: 'POST',
                        headers: {
                            'Content-Type': 'application/json'
                        },
                        body: JSON.stringify({
                            username,
                            email,
                            password
                        })
                    });
                    
                    if (!response.ok) {
                        const errorData = await response.json();
                        throw new Error(errorData.detail || '注册失败');
                    }
                    
                    // 注册成功，跳转到登录页
                    alert('注册成功！请登录');
                    window.location.href = '/';
                } catch (error) {
                    showError(error.message);
                } finally {
                    // 恢复按钮状态
                    registerBtn.disabled = false;
                    registerBtn.textContent = '注册';
                }
            });
            
            // 显示错误信息
            function showError(message) {
                errorAlert.textContent = message;
                errorAlert.style.display = 'block';
                
                // 5秒后自动隐藏错误信息
                setTimeout(() => {
                    errorAlert.style.display = 'none';
                }, 5000);
            }
            
            // 实时验证两次密码是否一致
            confirmPasswordInput.addEventListener('input', () => {
                if (passwordInput.value !== confirmPasswordInput.value) {
                    confirmPasswordInput.setCustomValidity('两次输入的密码不一致');
                } else {
                    confirmPasswordInput.setCustomValidity('');
                }
            });
        </script>
    </body>
    </html>
    """

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True) 