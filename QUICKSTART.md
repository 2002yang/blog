# 🎉 博客系统已成功启动！

## ✅ 当前状态

所有服务正在运行：
- ✅ PostgreSQL 数据库
- ✅ FastAPI 后端
- ✅ Vue3 前端
- ✅ Nginx 反向代理
- ✅ 管理员账号已创建

## 🌐 访问地址

- **前台首页**: http://localhost:8080
- **后台管理**: http://localhost:8080/admin
- **API 文档**: http://localhost:8080/api/docs

## 🔑 登录信息

**管理员账号**:
- 用户名: `admin`
- 密码: `admin123456`

## 📝 使用指南

### 1. 访问后台
打开浏览器访问 http://localhost:8080/admin，使用上面的账号登录。

### 2. 创建第一篇文章
1. 登录后台
2. 点击「新建文章」
3. 输入标题和内容（支持 Markdown）
4. 上传封面图片（可选）
5. 选择标签
6. 点击「发布」

### 3. 查看前台
访问 http://localhost:8080 查看发布的文章。

## 🛠️ 常用命令

```bash
# 查看服务状态
docker compose ps

# 查看日志
docker compose logs -f backend
docker compose logs -f frontend

# 停止服务
docker compose down

# 重启服务
docker compose restart

# 完全重建
docker compose down -v
docker compose up -d --build
```

## 📊 服务端口

- Nginx: 8080 (对外)
- Backend: 8000 (内部)
- Frontend: 80 (内部)
- PostgreSQL: 5432 (内部)

## 🎨 设计系统

- 主色: #18A058
- Hover: #36B37E
- 背景: #F7F8FA
- 字体: Inter, JetBrains Mono

## 📚 技术栈

- **前端**: Vue3 + Vite + TypeScript + Pinia + Tailwind CSS
- **后端**: FastAPI + SQLAlchemy + PostgreSQL
- **编辑器**: CodeMirror 6 (分屏 Markdown 预览)
- **部署**: Docker Compose + Nginx

## 🔧 故障排查

### 端口被占用
如果 8080 端口被占用，修改 `docker-compose.yml` 中的端口映射：
```yaml
ports:
  - "3000:80"  # 改为其他端口
```

### 重置数据库
```bash
docker compose down -v
docker compose up -d
docker compose exec backend python seed_admin.py
```

### 查看详细错误
```bash
docker compose logs backend --tail 100
```

---

**项目位置**: `e:\ProjectCollection2026\blog`

**完整文档**: 查看 `README.md`
