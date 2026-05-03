# 服务器部署快速清单

## 📋 部署前准备

- [ ] 准备一台 Linux 服务器（Ubuntu 22.04 推荐）
- [ ] 准备域名并解析到服务器 IP
- [ ] 确保服务器可以 SSH 访问
- [ ] 服务器至少 2GB RAM，10GB 磁盘

## 🚀 部署步骤（5 分钟）

### 1️⃣ 安装 Docker（服务器上执行）

```bash
curl -fsSL https://get.docker.com | sh
sudo usermod -aG docker $USER
newgrp docker
```

### 2️⃣ 上传项目文件

**方法 A：使用 Git**
```bash
cd /opt
sudo mkdir blog && sudo chown $USER:$USER blog
cd blog
git clone https://github.com/your-repo/blog.git .
```

**方法 B：直接上传（本地执行）**
```bash
scp -r e:\ProjectCollection2026\blog user@your-server-ip:/opt/blog/
```

### 3️⃣ 配置环境变量

```bash
cd /opt/blog
cp .env.example .env
nano .env
```

修改以下内容：
```env
POSTGRES_PASSWORD=你的强密码
SECRET_KEY=随机密钥（见下方生成命令）
ADMIN_PASSWORD=管理员密码
CORS_ORIGINS=["https://yourdomain.com"]
```

生成密钥：
```bash
python3 -c "import secrets; print(secrets.token_urlsafe(32))"
```

### 4️⃣ 启动服务

```bash
bash deploy.sh
```

或手动执行：
```bash
docker compose -f docker-compose.prod.yml up -d --build
docker compose -f docker-compose.prod.yml exec backend python seed_admin.py
```

### 5️⃣ 配置 HTTPS（可选但推荐）

```bash
# 安装 Nginx 和 Certbot
sudo apt install nginx certbot python3-certbot-nginx -y

# 复制配置文件
sudo cp nginx-server.conf /etc/nginx/sites-available/blog
# 编辑配置，替换 yourdomain.com 为你的域名
sudo nano /etc/nginx/sites-available/blog

# 启用站点
sudo ln -s /etc/nginx/sites-available/blog /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl reload nginx

# 获取 SSL 证书
sudo certbot --nginx -d yourdomain.com -d www.yourdomain.com
```

## ✅ 验证部署

访问以下地址：
- 前台：https://yourdomain.com
- 后台：https://yourdomain.com/admin
- API 文档：https://yourdomain.com/api/docs

## 🔧 常用命令

```bash
# 查看服务状态
docker compose -f docker-compose.prod.yml ps

# 查看日志
docker compose -f docker-compose.prod.yml logs -f backend

# 重启服务
docker compose -f docker-compose.prod.yml restart

# 更新代码
git pull
docker compose -f docker-compose.prod.yml up -d --build

# 备份数据库
docker compose -f docker-compose.prod.yml exec db \
  pg_dump -U blog_prod blog_prod > backup_$(date +%Y%m%d).sql
```

## 🛡️ 安全建议

1. **修改默认端口**（可选）
   - 编辑 `docker-compose.prod.yml`，将 `8080:80` 改为其他端口

2. **配置防火墙**
   ```bash
   sudo ufw allow 80/tcp
   sudo ufw allow 443/tcp
   sudo ufw allow 22/tcp
   sudo ufw enable
   ```

3. **定期备份**
   - 设置定时任务每天备份数据库
   - 备份 `/opt/blog/uploads` 目录

4. **监控日志**
   ```bash
   docker compose -f docker-compose.prod.yml logs -f
   ```

## 📞 故障排查

**服务无法启动**
```bash
docker compose -f docker-compose.prod.yml logs backend
```

**数据库连接失败**
```bash
docker compose -f docker-compose.prod.yml exec db pg_isready -U blog_prod
```

**端口被占用**
```bash
sudo netstat -tulpn | grep 8080
```

---

详细文档请查看 [DEPLOYMENT.md](DEPLOYMENT.md)
