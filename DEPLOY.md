# 部署指南

## 当前状态

✅ 所有代码已完成
✅ 环境变量已配置（.env）
✅ Docker 配置文件已就绪

## 需要安装 Docker

### Windows 安装 Docker Desktop

1. 下载 Docker Desktop:
   https://www.docker.com/products/docker-desktop/

2. 安装后重启电脑

3. 启动 Docker Desktop，等待 Docker 引擎启动

### 验证安装

打开命令行，运行：
```bash
docker --version
docker compose version
```

## 启动项目

安装 Docker 后，在项目目录运行：

```bash
cd e:\ProjectCollection2026\blog
docker compose up -d --build
```

首次启动需要 5-10 分钟（下载镜像 + 构建）。

## 创建管理员账号

等待所有服务启动后（约 2 分钟），运行：

```bash
docker compose exec backend python seed_admin.py
```

## 访问应用

- **前台**: http://localhost
- **后台**: http://localhost/admin
- **API 文档**: http://localhost/api/docs

**管理员登录**:
- 用户名: `admin`
- 密码: `admin123456`

## 本地开发（不使用 Docker）

如果不想用 Docker，可以本地运行：

### 前端
```bash
cd frontend
npm install
npm run dev
# 访问 http://localhost:5173
```

### 后端
需要先安装 PostgreSQL，然后：
```bash
cd backend
pip install -r requirements.txt
# 修改 app/config.py 中的 DATABASE_URL
alembic upgrade head
python seed_admin.py
uvicorn app.main:app --reload
# 访问 http://localhost:8000
```

## 项目文件说明

```
blog/
├── .env                    # 环境变量（已配置）
├── docker-compose.yml      # Docker 编排配置
├── nginx.conf              # Nginx 反向代理配置
├── README.md               # 完整文档
├── QUICKSTART.md           # 快速启动指南
├── frontend/               # Vue3 前端
│   ├── Dockerfile
│   ├── nginx.conf
│   └── src/
└── backend/                # FastAPI 后端
    ├── Dockerfile
    ├── requirements.txt
    ├── seed_admin.py       # 管理员初始化脚本
    └── app/
```

所有代码已完成，前端已成功构建。安装 Docker 后即可一键启动。
