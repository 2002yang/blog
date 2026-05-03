# 服务器部署指南

## 前置要求

- 一台 Linux 服务器（Ubuntu 22.04 / Debian 12 推荐）
- 域名（可选，建议配置）
- SSH 访问权限
- 至少 2GB RAM，10GB 磁盘空间

## 部署步骤

### 1. 服务器环境准备

```bash
# 更新系统
sudo apt update && sudo apt upgrade -y

# 安装 Docker
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh

# 安装 Docker Compose
sudo apt install docker-compose-plugin -y

# 将当前用户加入 docker 组（避免每次都用 sudo）
sudo usermod -aG docker $USER
newgrp docker

# 验证安装
docker --version
docker compose version
```

### 2. 上传项目文件

**方法 A：使用 Git（推荐）**

```bash
# 在服务器上
cd /opt
sudo mkdir blog && sudo chown $USER:$USER blog
cd blog

# 如果项目已推送到 Git 仓库
git clone https://github.com/your-username/blog.git .

# 如果没有 Git 仓库，先在本地初始化并推送
# 本地执行：
# git init
# git add .
# git commit -m "Initial commit"
# git remote add origin https://github.com/your-username/blog.git
# git push -u origin main
```

**方法 B：使用 SCP 直接上传**

```bash
# 在本地执行（Windows 使用 PowerShell 或 Git Bash）
cd e:\ProjectCollection2026\blog
scp -r . user@your-server-ip:/opt/blog/
```

### 3. 配置生产环境变量

```bash
# 在服务器上
cd /opt/blog
cp .env.example .env
nano .env
```

修改以下关键配置：

```env
# 数据库配置（使用强密码）
POSTGRES_DB=blog_prod
POSTGRES_USER=blog_prod
POSTGRES_PASSWORD=your-strong-password-here

# JWT 密钥（生成随机字符串）
SECRET_KEY=your-secret-key-here

# 管理员账号
ADMIN_USERNAME=admin
ADMIN_PASSWORD=your-admin-password-here
ADMIN_EMAIL=admin@yourdomain.com

# CORS 配置（改为你的域名）
CORS_ORIGINS=["https://yourdomain.com", "https://www.yourdomain.com"]
```

生成安全的密钥：

```bash
# 生成 SECRET_KEY
python3 -c "import secrets; print(secrets.token_urlsafe(32))"

# 生成数据库密码
openssl rand -base64 32
```

### 4. 启动服务

```bash
cd /opt/blog

# 构建并启动所有服务
docker compose -f docker-compose.prod.yml up -d --build

# 查看服务状态
docker compose ps

# 查看日志
docker compose logs -f
```

### 5. 初始化数据库

```bash
# 创建管理员账号
docker compose exec backend python seed_admin.py

# （可选）填充示例数据
docker compose exec backend python seed_data.py
```

### 6. 配置域名和 HTTPS（使用 Nginx + Let's Encrypt）

**安装 Certbot**

```bash
sudo apt install certbot python3-certbot-nginx -y
```

**创建 Nginx 配置**

```bash
sudo nano /etc/nginx/sites-available/blog
```

内容：

```nginx
server {
    listen 80;
    server_name yourdomain.com www.yourdomain.com;

    location / {
        proxy_pass http://localhost:8080;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

**启用配置并获取 SSL 证书**

```bash
# 启用站点
sudo ln -s /etc/nginx/sites-available/blog /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl reload nginx

# 获取 SSL 证书（自动配置 HTTPS）
sudo certbot --nginx -d yourdomain.com -d www.yourdomain.com
```

### 7. 防火墙配置

```bash
# 允许 HTTP/HTTPS
sudo ufw allow 80/tcp
sudo ufw allow 443/tcp
sudo ufw allow 22/tcp  # SSH
sudo ufw enable
```

## 维护命令

### 查看日志

```bash
# 所有服务
docker compose logs -f

# 特定服务
docker compose logs -f backend
docker compose logs -f frontend
docker compose logs -f db
```

### 重启服务

```bash
# 重启所有服务
docker compose restart

# 重启特定服务
docker compose restart backend
```

### 更新代码

```bash
cd /opt/blog

# 拉取最新代码
git pull

# 重新构建并启动
docker compose down
docker compose up -d --build
```

### 备份数据库

```bash
# 创建备份目录
mkdir -p ~/backups

# 备份数据库
docker compose exec db pg_dump -U blog_prod blog_prod > ~/backups/blog_$(date +%Y%m%d_%H%M%S).sql

# 恢复数据库
docker compose exec -T db psql -U blog_prod blog_prod < ~/backups/blog_20260502_120000.sql
```

### 查看资源使用

```bash
# 容器资源使用
docker stats

# 磁盘使用
docker system df
```

### 清理旧镜像

```bash
docker system prune -a
```

## 性能优化建议

### 1. 启用 Gzip 压缩

已在 `nginx.conf` 中配置。

### 2. 配置 CDN

将 `/uploads/` 目录同步到 CDN（如阿里云 OSS、腾讯云 COS）。

### 3. 数据库优化

```bash
# 进入数据库容器
docker compose exec db psql -U blog_prod blog_prod

-- 创建索引（如果还没有）
CREATE INDEX IF NOT EXISTS idx_articles_status ON articles(status);
CREATE INDEX IF NOT EXISTS idx_articles_published_at ON articles(published_at DESC);
CREATE INDEX IF NOT EXISTS idx_articles_slug ON articles(slug);

-- 定期清理
VACUUM ANALYZE;
```

### 4. 配置自动备份

```bash
# 创建备份脚本
sudo nano /usr/local/bin/backup-blog.sh
```

内容：

```bash
#!/bin/bash
BACKUP_DIR="/root/backups"
DATE=$(date +%Y%m%d_%H%M%S)

mkdir -p $BACKUP_DIR

# 备份数据库
docker compose -f /opt/blog/docker-compose.prod.yml exec -T db \
  pg_dump -U blog_prod blog_prod > $BACKUP_DIR/blog_$DATE.sql

# 备份上传文件
tar -czf $BACKUP_DIR/uploads_$DATE.tar.gz /opt/blog/uploads

# 删除 7 天前的备份
find $BACKUP_DIR -name "*.sql" -mtime +7 -delete
find $BACKUP_DIR -name "*.tar.gz" -mtime +7 -delete
```

```bash
# 添加执行权限
sudo chmod +x /usr/local/bin/backup-blog.sh

# 添加定时任务（每天凌晨 2 点备份）
sudo crontab -e
# 添加：0 2 * * * /usr/local/bin/backup-blog.sh
```

## 监控

### 使用 Portainer（可选）

```bash
docker volume create portainer_data
docker run -d -p 9000:9000 --name=portainer --restart=always \
  -v /var/run/docker.sock:/var/run/docker.sock \
  -v portainer_data:/data \
  portainer/portainer-ce
```

访问 `http://your-server-ip:9000` 进行可视化管理。

## 故障排查

### 服务无法启动

```bash
# 查看详细日志
docker compose logs backend
docker compose logs db

# 检查端口占用
sudo netstat -tulpn | grep 8080
```

### 数据库连接失败

```bash
# 检查数据库是否健康
docker compose exec db pg_isready -U blog_prod

# 进入数据库检查
docker compose exec db psql -U blog_prod blog_prod
```

### 磁盘空间不足

```bash
# 清理 Docker 资源
docker system prune -a --volumes

# 清理日志
sudo journalctl --vacuum-time=7d
```

## 安全建议

1. **定期更新系统和 Docker**
   ```bash
   sudo apt update && sudo apt upgrade -y
   ```

2. **使用强密码**
   - 数据库密码至少 32 位随机字符
   - 管理员密码至少 16 位

3. **限制 SSH 访问**
   ```bash
   # 禁用密码登录，只允许密钥
   sudo nano /etc/ssh/sshd_config
   # 设置：PasswordAuthentication no
   sudo systemctl restart sshd
   ```

4. **配置 fail2ban**
   ```bash
   sudo apt install fail2ban -y
   sudo systemctl enable fail2ban
   ```

5. **定期备份**
   - 数据库每天备份
   - 上传文件每周备份
   - 备份文件存储到异地

## 访问地址

部署完成后：

- **前台**: https://yourdomain.com
- **后台**: https://yourdomain.com/admin
- **API 文档**: https://yourdomain.com/api/docs

---

**部署完成！** 如有问题，查看日志：`docker compose logs -f`
