#!/usr/bin/env python3
"""填充示例数据到博客数据库"""
import sys
import os
from datetime import datetime, timezone, timedelta

sys.path.insert(0, os.path.dirname(__file__))

from app.database import SessionLocal
from app.models import User, Tag, Article
from app.utils.slug import make_slug

db = SessionLocal()

try:
    # 获取管理员用户
    admin = db.query(User).filter(User.username == "admin").first()
    if not admin:
        print("Error: Admin user not found. Run seed_admin.py first.")
        sys.exit(1)

    # 创建标签
    tags_data = [
        {"name": "Vue.js", "color": "#42b883", "description": "Vue.js 框架相关技术"},
        {"name": "React", "color": "#61dafb", "description": "React 框架相关技术"},
        {"name": "TypeScript", "color": "#3178c6", "description": "TypeScript 语言"},
        {"name": "Python", "color": "#3776ab", "description": "Python 编程语言"},
        {"name": "FastAPI", "color": "#009688", "description": "FastAPI 框架"},
        {"name": "Docker", "color": "#2496ed", "description": "Docker 容器技术"},
        {"name": "数据库", "color": "#f29111", "description": "数据库相关技术"},
        {"name": "前端", "color": "#e34c26", "description": "前端开发"},
        {"name": "后端", "color": "#68a063", "description": "后端开发"},
        {"name": "架构设计", "color": "#5c2d91", "description": "系统架构设计"},
    ]

    tags = {}
    for tag_data in tags_data:
        existing = db.query(Tag).filter(Tag.name == tag_data["name"]).first()
        if existing:
            tags[tag_data["name"]] = existing
            print(f"Tag '{tag_data['name']}' already exists")
        else:
            tag = Tag(
                name=tag_data["name"],
                slug=make_slug(tag_data["name"]),
                color=tag_data["color"],
                description=tag_data["description"],
            )
            db.add(tag)
            db.flush()
            tags[tag_data["name"]] = tag
            print(f"Created tag: {tag_data['name']}")

    # 创建文章
    articles_data = [
        {
            "title": "Vue 3 + TypeScript 最佳实践",
            "summary": "深入探讨 Vue 3 与 TypeScript 结合使用的最佳实践，包括组合式 API、类型推断和项目配置。",
            "content": """# Vue 3 + TypeScript 最佳实践

Vue 3 与 TypeScript 的结合为前端开发带来了更好的类型安全和开发体验。本文将分享一些实用的最佳实践。

## 组合式 API 的类型定义

使用 `defineComponent` 和 `ref` 时，TypeScript 可以自动推断类型：

```typescript
import { defineComponent, ref } from 'vue'

export default defineComponent({
  setup() {
    const count = ref(0) // 自动推断为 Ref<number>
    const message = ref('Hello') // 自动推断为 Ref<string>

    return { count, message }
  }
})
```

## Props 类型定义

使用 `defineProps` 配合泛型可以获得完整的类型支持：

```typescript
<script setup lang="ts">
interface Props {
  title: string
  count?: number
  tags: string[]
}

const props = defineProps<Props>()
</script>
```

## Emit 事件类型

为事件定义明确的类型：

```typescript
<script setup lang="ts">
const emit = defineEmits<{
  (e: 'update', value: string): void
  (e: 'delete', id: number): void
}>()
</script>
```

## 总结

TypeScript 让 Vue 3 开发更加可靠和高效。合理使用类型系统可以在编译时发现潜在问题，提升代码质量。
""",
            "tags": ["Vue.js", "TypeScript", "前端"],
            "is_featured": True,
            "cover_image": None,
        },
        {
            "title": "FastAPI 异步编程实战",
            "summary": "学习如何在 FastAPI 中使用异步编程提升 API 性能，包括异步数据库操作、并发请求处理等。",
            "content": """# FastAPI 异步编程实战

FastAPI 原生支持异步编程，可以显著提升 API 的并发处理能力。

## 异步路由

定义异步路由非常简单：

```python
from fastapi import FastAPI

app = FastAPI()

@app.get("/items/{item_id}")
async def read_item(item_id: int):
    # 异步操作
    result = await fetch_item_from_db(item_id)
    return result
```

## 异步数据库操作

使用 SQLAlchemy 的异步支持：

```python
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession

engine = create_async_engine("postgresql+asyncpg://...")

async def get_user(user_id: int):
    async with AsyncSession(engine) as session:
        result = await session.execute(
            select(User).where(User.id == user_id)
        )
        return result.scalar_one_or_none()
```

## 并发请求

使用 `asyncio.gather` 并发处理多个请求：

```python
import asyncio

async def fetch_multiple_resources():
    results = await asyncio.gather(
        fetch_users(),
        fetch_posts(),
        fetch_comments()
    )
    return results
```

## 性能对比

在高并发场景下，异步 API 的性能提升可达 3-5 倍。

## 注意事项

- 避免在异步函数中使用阻塞操作
- 合理使用连接池
- 注意异常处理

异步编程是现代 Web 开发的重要技能，FastAPI 让它变得简单易用。
""",
            "tags": ["Python", "FastAPI", "后端"],
            "is_featured": True,
            "cover_image": None,
        },
        {
            "title": "Docker 容器化部署完整指南",
            "summary": "从零开始学习 Docker 容器化部署，包括 Dockerfile 编写、Docker Compose 多容器编排、生产环境最佳实践。",
            "content": """# Docker 容器化部署完整指南

Docker 已成为现代应用部署的标准方案。本文将介绍完整的容器化部署流程。

## Dockerfile 最佳实践

### 多阶段构建

减小镜像体积的关键技术：

```dockerfile
# 构建阶段
FROM node:20-alpine AS builder
WORKDIR /app
COPY package*.json ./
RUN npm ci
COPY . .
RUN npm run build

# 生产阶段
FROM nginx:alpine
COPY --from=builder /app/dist /usr/share/nginx/html
EXPOSE 80
```

### 优化层缓存

合理安排指令顺序，充分利用缓存：

```dockerfile
# 先复制依赖文件
COPY package*.json ./
RUN npm ci

# 再复制源码
COPY . .
RUN npm run build
```

## Docker Compose 编排

定义多容器应用：

```yaml
services:
  backend:
    build: ./backend
    environment:
      DATABASE_URL: postgresql://user:pass@db:5432/mydb
    depends_on:
      db:
        condition: service_healthy

  db:
    image: postgres:16-alpine
    volumes:
      - pgdata:/var/lib/postgresql/data
    healthcheck:
      test: ["CMD", "pg_isready"]
      interval: 5s

volumes:
  pgdata:
```

## 生产环境部署

### 安全加固

- 使用非 root 用户运行
- 扫描镜像漏洞
- 限制容器资源

### 日志管理

配置日志驱动：

```yaml
services:
  app:
    logging:
      driver: "json-file"
      options:
        max-size: "10m"
        max-file: "3"
```

## 总结

Docker 简化了应用部署流程，掌握容器化技术是现代开发者的必备技能。
""",
            "tags": ["Docker", "后端", "架构设计"],
            "is_featured": True,
            "cover_image": None,
        },
        {
            "title": "PostgreSQL 性能优化技巧",
            "summary": "分享 PostgreSQL 数据库性能优化的实用技巧，包括索引优化、查询优化、配置调优等。",
            "content": """# PostgreSQL 性能优化技巧

PostgreSQL 是功能强大的开源数据库，合理优化可以获得出色的性能。

## 索引优化

### 选择合适的索引类型

```sql
-- B-tree 索引（默认）
CREATE INDEX idx_user_email ON users(email);

-- GIN 索引用于全文搜索
CREATE INDEX idx_article_search ON articles
USING GIN(to_tsvector('english', content));

-- 部分索引
CREATE INDEX idx_active_users ON users(email)
WHERE is_active = true;
```

### 复合索引顺序

将选择性高的列放在前面：

```sql
-- 好的顺序
CREATE INDEX idx_user_status_created
ON users(status, created_at);

-- 不好的顺序（created_at 选择性低）
CREATE INDEX idx_user_created_status
ON users(created_at, status);
```

## 查询优化

### 使用 EXPLAIN ANALYZE

分析查询执行计划：

```sql
EXPLAIN ANALYZE
SELECT * FROM articles
WHERE status = 'published'
ORDER BY created_at DESC
LIMIT 10;
```

### 避免 N+1 查询

使用 JOIN 代替多次查询：

```sql
-- 不好：N+1 查询
SELECT * FROM articles;
-- 然后对每篇文章查询作者

-- 好：一次查询
SELECT a.*, u.username
FROM articles a
LEFT JOIN users u ON a.author_id = u.id;
```

## 配置调优

关键参数：

```ini
# 内存配置
shared_buffers = 256MB
effective_cache_size = 1GB
work_mem = 16MB

# 连接配置
max_connections = 100

# 检查点配置
checkpoint_completion_target = 0.9
```

## 监控与维护

定期执行 VACUUM 和 ANALYZE：

```sql
VACUUM ANALYZE articles;
```

性能优化是持续的过程，需要根据实际负载不断调整。
""",
            "tags": ["数据库", "后端"],
            "is_featured": False,
            "cover_image": None,
        },
        {
            "title": "React Hooks 深入理解",
            "summary": "深入理解 React Hooks 的工作原理，掌握 useState、useEffect、useCallback 等常用 Hooks 的最佳实践。",
            "content": """# React Hooks 深入理解

React Hooks 改变了我们编写组件的方式，让函数组件拥有了状态和生命周期。

## useState 的正确使用

### 函数式更新

当新状态依赖旧状态时，使用函数式更新：

```javascript
const [count, setCount] = useState(0);

// 不好
setCount(count + 1);

// 好
setCount(prev => prev + 1);
```

### 惰性初始化

避免每次渲染都执行昂贵的计算：

```javascript
const [data, setData] = useState(() => {
  return expensiveComputation();
});
```

## useEffect 的依赖管理

### 正确声明依赖

```javascript
useEffect(() => {
  fetchData(userId);
}, [userId]); // 依赖数组
```

### 清理副作用

```javascript
useEffect(() => {
  const timer = setInterval(() => {
    console.log('tick');
  }, 1000);

  return () => clearInterval(timer);
}, []);
```

## 性能优化 Hooks

### useMemo

缓存计算结果：

```javascript
const expensiveValue = useMemo(() => {
  return computeExpensiveValue(a, b);
}, [a, b]);
```

### useCallback

缓存函数引用：

```javascript
const handleClick = useCallback(() => {
  doSomething(a, b);
}, [a, b]);
```

## 自定义 Hooks

封装可复用逻辑：

```javascript
function useLocalStorage(key, initialValue) {
  const [value, setValue] = useState(() => {
    const item = localStorage.getItem(key);
    return item ? JSON.parse(item) : initialValue;
  });

  useEffect(() => {
    localStorage.setItem(key, JSON.stringify(value));
  }, [key, value]);

  return [value, setValue];
}
```

## 总结

Hooks 让 React 代码更简洁、更易维护。理解其工作原理是写好 React 应用的关键。
""",
            "tags": ["React", "TypeScript", "前端"],
            "is_featured": False,
            "cover_image": None,
        },
        {
            "title": "微服务架构设计原则",
            "summary": "探讨微服务架构的核心设计原则，包括服务拆分、通信方式、数据一致性等关键问题。",
            "content": """# 微服务架构设计原则

微服务架构已成为大型应用的主流架构模式。本文总结核心设计原则。

## 服务拆分原则

### 单一职责

每个服务只负责一个业务领域：

- 用户服务：用户管理、认证
- 订单服务：订单创建、查询
- 支付服务：支付处理、退款

### 高内聚低耦合

服务内部高度相关，服务之间松散耦合。

## 通信方式

### 同步通信

使用 REST API 或 gRPC：

```python
# REST API
@app.get("/orders/{order_id}")
async def get_order(order_id: int):
    return await order_service.get(order_id)
```

### 异步通信

使用消息队列（RabbitMQ、Kafka）：

```python
# 发布事件
await event_bus.publish("order.created", {
    "order_id": 123,
    "user_id": 456
})

# 订阅事件
@event_bus.subscribe("order.created")
async def handle_order_created(event):
    await send_notification(event["user_id"])
```

## 数据管理

### 数据库独立

每个服务拥有独立的数据库：

```
用户服务 -> 用户数据库
订单服务 -> 订单数据库
支付服务 -> 支付数据库
```

### 最终一致性

使用 Saga 模式处理分布式事务：

1. 订单服务创建订单
2. 发布 OrderCreated 事件
3. 库存服务扣减库存
4. 支付服务处理支付

## 服务发现与负载均衡

使用服务注册中心（Consul、Eureka）：

```yaml
services:
  order-service:
    instances:
      - host: 10.0.1.10
        port: 8001
      - host: 10.0.1.11
        port: 8001
```

## 监控与追踪

### 分布式追踪

使用 Jaeger 或 Zipkin 追踪请求链路。

### 日志聚合

集中收集和分析日志（ELK Stack）。

## 总结

微服务架构提供了灵活性和可扩展性，但也带来了复杂性。需要权衡利弊，选择合适的架构。
""",
            "tags": ["架构设计", "后端"],
            "is_featured": False,
            "cover_image": None,
        },
    ]

    # 计算阅读时间
    def calc_read_time(content):
        words = len(content.split())
        return max(1, round(words / 200))

    for i, article_data in enumerate(articles_data):
        existing = db.query(Article).filter(Article.title == article_data["title"]).first()
        if existing:
            print(f"Article '{article_data['title']}' already exists")
            continue

        article_tags = [tags[tag_name] for tag_name in article_data["tags"]]

        # 设置发布时间（从最近到最早）
        published_at = datetime.now(timezone.utc) - timedelta(days=i * 2)

        article = Article(
            title=article_data["title"],
            slug=make_slug(article_data["title"]),
            summary=article_data["summary"],
            content=article_data["content"],
            cover_image=article_data.get("cover_image"),
            author_id=admin.id,
            status="published",
            is_featured=article_data["is_featured"],
            read_time=calc_read_time(article_data["content"]),
            tags=article_tags,
            published_at=published_at,
            view_count=0,
        )
        db.add(article)
        print(f"Created article: {article_data['title']}")

    db.commit()
    print("\n✅ Database seeded successfully!")
    print(f"Created {len(tags_data)} tags and {len(articles_data)} articles")

except Exception as e:
    print(f"Error: {e}")
    db.rollback()
    raise
finally:
    db.close()
