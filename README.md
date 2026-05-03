# DevBlog — 现代化极简技术博客

完整的全栈技术博客系统，采用前后端分离架构，具有现代 SaaS 风格的设计和完整的后台管理功能。

## 技术栈

- **前端**: Vue3 + Vite + TypeScript + Pinia + Vue Router + Tailwind CSS
- **后端**: Python FastAPI + SQLAlchemy + Pydantic + JWT
- **数据库**: PostgreSQL
- **部署**: Docker Compose + Nginx

## 功能特性

### 公开页面
- 首页（Hero + 精选文章 + 最新文章）
- 文章列表（分页、标签筛选）
- 文章详情（Markdown 渲染、代码高亮、目录导航）
- 标签页面
- 全文搜索
- SEO 优化（meta tags、OG tags）

### 后台管理
- JWT 认证（登录/登出）
- 管理员仪表盘（统计数据）
- 文章管理（CRUD、发布/草稿切换、精选标记）
- CodeMirror 6 Markdown 编辑器（分屏预览）
- 图片上传（拖拽/点击上传）
- 标签管理

## 快速开始

### 1. 环境准备

复制环境变量模板：
```bash
cp .env.example .env
```

编辑 `.env` 文件，设置数据库密码、JWT 密钥和管理员账号：
```env
POSTGRES_PASSWORD=your-secure-password
SECRET_KEY=your-secret-key-here  # 使用 openssl rand -hex 32 生成
ADMIN_USERNAME=admin
ADMIN_EMAIL=admin@example.com
ADMIN_PASSWORD=your-admin-password
```

### 2. 启动服务

使用 Docker Compose 一键启动：
```bash
docker-compose up --build
```

首次启动后，进入 backend 容器创建管理员账号：
```bash
docker-compose exec backend python seed_admin.py
```

### 3. 访问应用

- **前台**: http://localhost
- **后台**: http://localhost/admin
- **API 文档**: http://localhost/api/docs

使用 `.env` 中设置的管理员账号登录后台。

## 本地开发

### 前端开发

```bash
cd frontend
npm install
npm run dev  # 开发服务器运行在 http://localhost:5173
```

### 后端开发

```bash
cd backend
pip install -r requirements.txt
alembic upgrade head  # 运行数据库迁移
uvicorn app.main:app --reload  # 开发服务器运行在 http://localhost:8000
```

需要本地 PostgreSQL 数据库，或修改 `app/config.py` 中的 `DATABASE_URL`。

## 项目结构

```
blog/
├── frontend/          # Vue3 前端
│   ├── src/
│   │   ├── components/  # 组件（layout, common, article, editor, admin）
│   │   ├── views/       # 页面视图
│   │   ├── router/      # 路由配置
│   │   ├── stores/      # Pinia 状态管理
│   │   ├── api/         # API 客户端
│   │   ├── types/       # TypeScript 类型
│   │   └── utils/       # 工具函数（markdown, date）
│   ├── Dockerfile
│   └── nginx.conf
├── backend/           # FastAPI 后端
│   ├── app/
│   │   ├── models/      # SQLAlchemy 模型
│   │   ├── schemas/     # Pydantic schemas
│   │   ├── routers/     # API 路由
│   │   ├── services/    # 业务逻辑
│   │   └── utils/       # 工具函数（security, slug）
│   ├── alembic/         # 数据库迁移
│   ├── seed_admin.py    # 管理员账号初始化脚本
│   └── Dockerfile
├── docker-compose.yml
└── nginx.conf         # Nginx 反向代理配置
```

## 设计系统

采用 Notion + Vue 官网 + Vercel 风格，大量留白、卡片式布局、圆角设计、柔和阴影。

**颜色**:
- 主色: `#18A058`
- Hover: `#36B37E`
- 背景: `#F7F8FA`
- 卡片: `#FFFFFF`
- 标题: `#1F2329`
- 正文: `#4E5969`
- 边框: `#E5E6EB`

**字体**: Inter (sans-serif), JetBrains Mono (monospace)

## API 端点

### 认证
- `POST /api/v1/auth/login` - 登录
- `POST /api/v1/auth/refresh` - 刷新 token
- `GET /api/v1/auth/me` - 获取当前用户
- `POST /api/v1/auth/logout` - 登出

### 文章（公开）
- `GET /api/v1/articles` - 文章列表（支持分页、标签筛选）
- `GET /api/v1/articles/featured` - 精选文章
- `GET /api/v1/articles/search?q=` - 搜索文章
- `GET /api/v1/articles/{slug}` - 文章详情
- `POST /api/v1/articles/{id}/view` - 增加阅读量

### 文章（管理员）
- `GET /api/v1/admin/articles` - 管理员文章列表
- `POST /api/v1/admin/articles` - 创建文章
- `PUT /api/v1/admin/articles/{id}` - 更新文章
- `DELETE /api/v1/admin/articles/{id}` - 删除文章
- `PATCH /api/v1/admin/articles/{id}/publish` - 切换发布状态
- `PATCH /api/v1/admin/articles/{id}/feature` - 切换精选状态

### 标签
- `GET /api/v1/tags` - 标签列表
- `GET /api/v1/tags/{slug}` - 标签详情
- `POST /api/v1/admin/tags` - 创建标签（管理员）
- `PUT /api/v1/admin/tags/{id}` - 更新标签（管理员）
- `DELETE /api/v1/admin/tags/{id}` - 删除标签（管理员）

### 上传 & 统计
- `POST /api/v1/upload/image` - 上传图片（需认证）
- `GET /api/v1/admin/stats` - 统计数据（管理员）

## 技术亮点

1. **CodeMirror 6 编辑器**: 分屏实时预览，支持 Markdown 语法高亮
2. **JWT 双 token 机制**: Access token 存内存（15分钟），Refresh token 存 httpOnly cookie（7天）
3. **Axios 拦截器**: 自动刷新 token，无感续期
4. **图片上传**: 本地存储 + Nginx 静态服务，零成本
5. **SEO 友好**: 动态 meta tags、OG tags、JSON-LD 结构化数据
6. **响应式设计**: 移动端适配，汉堡菜单
7. **Docker 部署**: 一键启动，包含数据库、后端、前端、Nginx 四个服务

## 生产环境部署

### 快速部署（5 分钟）

查看 [部署清单](DEPLOY_CHECKLIST.md) 获取快速部署指南。

### 详细部署文档

完整的服务器部署指南请查看 [DEPLOYMENT.md](DEPLOYMENT.md)，包括：

- 服务器环境准备
- Docker 安装配置
- HTTPS 证书配置（Let's Encrypt）
- 域名配置
- 数据库备份策略
- 性能优化建议
- 监控和日志管理
- 故障排查

### 一键部署脚本

```bash
# 在服务器上执行
bash deploy.sh
```

该脚本会自动：
1. 检查 Docker 环境
2. 构建镜像
3. 启动所有服务
4. 初始化管理员账号

### 生产环境配置

使用 `docker-compose.prod.yml` 进行生产部署：

```bash
# 配置环境变量
cp .env.example .env
nano .env  # 修改密码和密钥

# 启动生产环境
docker compose -f docker-compose.prod.yml up -d --build

# 初始化管理员
docker compose -f docker-compose.prod.yml exec backend python seed_admin.py
```

### HTTPS 配置

使用 Nginx + Let's Encrypt 配置 HTTPS：

```bash
# 安装 Certbot
sudo apt install certbot python3-certbot-nginx -y

# 配置 Nginx（参考 nginx-server.conf）
sudo cp nginx-server.conf /etc/nginx/sites-available/blog
sudo ln -s /etc/nginx/sites-available/blog /etc/nginx/sites-enabled/

# 获取 SSL 证书
sudo certbot --nginx -d yourdomain.com
```

## License

MIT
