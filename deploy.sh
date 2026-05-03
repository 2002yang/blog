#!/bin/bash

# 博客系统快速部署脚本
# 使用方法：bash deploy.sh

set -e

echo "🚀 开始部署博客系统..."

# 检查 Docker 是否安装
if ! command -v docker &> /dev/null; then
    echo "❌ Docker 未安装，请先安装 Docker"
    exit 1
fi

if ! command -v docker compose &> /dev/null; then
    echo "❌ Docker Compose 未安装，请先安装 Docker Compose"
    exit 1
fi

# 检查 .env 文件
if [ ! -f .env ]; then
    echo "⚠️  .env 文件不存在，从模板创建..."
    cp .env.example .env
    echo "📝 请编辑 .env 文件，配置数据库密码、JWT 密钥等"
    echo "   生成密钥命令："
    echo "   python3 -c \"import secrets; print(secrets.token_urlsafe(32))\""
    echo ""
    read -p "配置完成后按回车继续..."
fi

# 停止旧容器
echo "🛑 停止旧容器..."
docker compose -f docker-compose.prod.yml down || true

# 构建镜像
echo "🔨 构建 Docker 镜像..."
docker compose -f docker-compose.prod.yml build --no-cache

# 启动服务
echo "🚀 启动服务..."
docker compose -f docker-compose.prod.yml up -d

# 等待数据库就绪
echo "⏳ 等待数据库启动..."
sleep 10

# 初始化管理员账号
echo "👤 创建管理员账号..."
docker compose -f docker-compose.prod.yml exec -T backend python seed_admin.py || true

# 显示服务状态
echo ""
echo "✅ 部署完成！"
echo ""
echo "📊 服务状态："
docker compose -f docker-compose.prod.yml ps
echo ""
echo "🌐 访问地址："
echo "   前台: http://localhost:8080"
echo "   后台: http://localhost:8080/admin"
echo "   API 文档: http://localhost:8080/api/docs"
echo ""
echo "🔑 管理员登录信息请查看 .env 文件"
echo ""
echo "📝 查看日志："
echo "   docker compose -f docker-compose.prod.yml logs -f"
echo ""
echo "🛠️  常用命令："
echo "   重启服务: docker compose -f docker-compose.prod.yml restart"
echo "   停止服务: docker compose -f docker-compose.prod.yml down"
echo "   查看状态: docker compose -f docker-compose.prod.yml ps"
