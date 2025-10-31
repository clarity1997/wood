# 家具购物后端API

基于FastAPI构建的家具购物平台后端服务，支持用户和商家两种角色。

## 功能特性

- 用户注册和登录（JWT认证）
- 用户和商家角色管理
- 商家产品管理（CRUD）
- 产品图片上传
- 产品搜索（关键词、价格、分类）
- DeepSeek AI智能聊天助手
- 产品推荐系统

## 技术栈

- FastAPI
- PostgreSQL
- SQLAlchemy
- JWT认证
- DeepSeek API

## 快速开始

### 1. 安装依赖

```bash
# 创建虚拟环境
python -m venv venv

# 激活虚拟环境
# Windows:
venv\Scripts\activate
# macOS/Linux:
source venv/bin/activate

# 安装依赖
pip install -r requirements.txt
```

### 2. 配置环境变量

复制`.env.example`到`.env`并修改配置：

```bash
cp .env.example .env
```

修改`.env`文件中的配置：
- `DATABASE_URL`: PostgreSQL数据库连接URL
- `SECRET_KEY`: JWT密钥（请使用强密码）
- `DEEPSEEK_API_KEY`: DeepSeek API密钥

### 3. 设置PostgreSQL数据库

```bash
# 创建数据库
createdb furniture_db

# 或使用psql
psql -U postgres
CREATE DATABASE furniture_db;
```

### 4. 启动服务

```bash
cd backend
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

服务将运行在 `http://localhost:8000`

### 5. 访问API文档

- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

## API端点

### 认证
- `POST /api/auth/register` - 用户注册
- `POST /api/auth/login` - 用户登录

### 产品管理
- `GET /api/products/` - 获取产品列表
- `POST /api/products/` - 创建产品（商家）
- `GET /api/products/{id}` - 获取产品详情
- `PUT /api/products/{id}` - 更新产品（商家）
- `DELETE /api/products/{id}` - 删除产品（商家）
- `GET /api/products/merchant/my-products` - 获取商家自己的产品

### 图片上传
- `POST /api/upload/product/{id}/images` - 上传产品图片（商家）
- `DELETE /api/upload/product/{id}/images` - 删除产品图片（商家）

### 搜索
- `GET /api/search/?q=关键词&min_price=100&max_price=500` - 搜索产品

### 聊天助手
- `POST /api/chat/` - 与商家智能助手聊天

## 数据库表结构

- `users` - 用户表
- `merchants` - 商家信息表
- `products` - 产品表
- `categories` - 分类表
- `chat_history` - 聊天历史表

## 开发说明

数据库会在首次启动时自动创建表结构。

上传的图片存储在`uploads`目录，通过`/uploads`路径访问。
