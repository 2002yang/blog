# 精选文章功能完整实现文档

## 📊 功能概述

精选文章功能允许管理员标记重要文章，并在首页优先展示。用户访问首页时，会看到最多 5 篇精选文章的卡片展示。

## 🔄 数据流向图

```
用户访问首页 (http://localhost:8080/)
    ↓
HomeView.vue 组件挂载
    ↓
调用 articlesApi.featured()
    ↓
发送 HTTP 请求: GET /api/v1/articles/featured
    ↓
Nginx 反向代理转发到 backend:8000
    ↓
FastAPI 路由匹配: featured_articles()
    ↓
数据库查询: SELECT * FROM articles WHERE status='published' AND is_featured=true
    ↓
SQLAlchemy ORM 对象 → Pydantic 模型 (ArticleListItem)
    ↓
返回 JSON 数组 (最多 5 篇文章)
    ↓
前端接收数据并存储到 featured.value
    ↓
Vue 渲染 ArticleCardFeatured 组件
    ↓
用户看到精选文章卡片
```

---

## 1️⃣ 后端实现

### 1.1 数据库模型

**文件**: `backend/app/models/article.py`

```python
from sqlalchemy import Column, Integer, String, Text, Boolean, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base

class Article(Base):
    __tablename__ = "articles"
    
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(200), nullable=False)
    slug = Column(String(250), unique=True, nullable=False, index=True)
    summary = Column(Text)
    content = Column(Text, nullable=False)
    cover_image = Column(String(500))
    
    # 关键字段：精选标记
    is_featured = Column(Boolean, default=False, nullable=False)
    
    # 状态字段
    status = Column(String(20), default="draft", index=True)  # draft 或 published
    
    # 统计字段
    view_count = Column(Integer, default=0)
    read_time = Column(Integer, default=1)
    
    # 时间字段
    published_at = Column(DateTime(timezone=True))
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # 关联字段
    author_id = Column(Integer, ForeignKey("users.id", ondelete="SET NULL"))
    author = relationship("User", back_populates="articles")
    tags = relationship("Tag", secondary="article_tags", back_populates="articles")
```

**数据库迁移**: `backend/alembic/versions/001_initial_schema.py`

```python
# 创建 articles 表时包含 is_featured 字段
sa.Column("is_featured", sa.Boolean, default=False, nullable=False),
```

### 1.2 响应模型 (Pydantic Schema)

**文件**: `backend/app/schemas/article.py`

```python
from pydantic import BaseModel
from datetime import datetime

class ArticleAuthor(BaseModel):
    id: int
    username: str
    avatar_url: str | None

class TagOut(BaseModel):
    id: int
    name: str
    slug: str
    color: str

class ArticleListItem(BaseModel):
    """文章列表项（用于列表页和精选文章）"""
    id: int
    title: str
    slug: str
    summary: str | None
    cover_image: str | None
    author: ArticleAuthor | None
    status: str
    is_featured: bool  # 是否精选
    view_count: int
    read_time: int
    tags: list[TagOut]
    published_at: datetime | None
    created_at: datetime
    
    class Config:
        from_attributes = True
```

### 1.3 API 路由

**文件**: `backend/app/routers/articles.py`

```python
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import Article
from app.schemas.article import ArticleListItem

router = APIRouter(prefix="/api/v1", tags=["articles"])

@router.get("/articles/featured", response_model=list[ArticleListItem])
def featured_articles(db: Session = Depends(get_db)):
    """
    获取精选文章列表
    
    - 只返回已发布的文章 (status='published')
    - 只返回标记为精选的文章 (is_featured=True)
    - 按发布时间倒序排列
    - 最多返回 5 篇
    - 无需认证，公开访问
    """
    return (
        db.query(Article)
        .filter(
            Article.status == "published",
            Article.is_featured == True
        )
        .order_by(Article.published_at.desc())
        .limit(5)
        .all()
    )
```

### 1.4 管理员设置精选

**文件**: `backend/app/routers/articles.py`

```python
from app.dependencies import require_admin

@router.patch("/admin/articles/{article_id}/feature", response_model=ArticleOut)
def toggle_feature(
    article_id: int,
    db: Session = Depends(get_db),
    _=Depends(require_admin)  # 需要管理员权限
):
    """
    切换文章的精选状态
    
    - 需要管理员权限
    - 切换 is_featured 字段的布尔值
    """
    article = db.get(Article, article_id)
    if not article:
        raise HTTPException(status_code=404, detail="Article not found")
    
    # 切换精选状态
    article.is_featured = not article.is_featured
    db.commit()
    db.refresh(article)
    
    return article
```

---

## 2️⃣ 前端实现

### 2.1 API 客户端

**文件**: `frontend/src/api/client.ts`

```typescript
import axios from 'axios'

const client = axios.create({
  baseURL: '/api/v1',  // 自动添加前缀
  timeout: 15000,
  headers: { 'Content-Type': 'application/json' },
})

export default client
```

**文件**: `frontend/src/api/articles.ts`

```typescript
import client from './client'
import type { ArticleListItem } from '@/types/article'

export const articlesApi = {
  // 获取精选文章
  featured: () => 
    client.get<ArticleListItem[]>('/articles/featured'),
  
  // 其他接口...
  list: (params: { page: number; size: number; tag?: string }) =>
    client.get('/articles', { params }),
}
```

### 2.2 TypeScript 类型定义

**文件**: `frontend/src/types/article.ts`

```typescript
export interface ArticleAuthor {
  id: number
  username: string
  avatar_url: string | null
}

export interface Tag {
  id: number
  name: string
  slug: string
  color: string
}

export interface ArticleListItem {
  id: number
  title: string
  slug: string
  summary: string | null
  cover_image: string | null
  author: ArticleAuthor | null
  status: string
  is_featured: boolean  // 是否精选
  view_count: number
  read_time: number
  tags: Tag[]
  published_at: string | null
  created_at: string
}
```

### 2.3 首页组件

**文件**: `frontend/src/views/HomeView.vue`

```vue
<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { articlesApi } from '@/api/articles'
import ArticleCardFeatured from '@/components/article/ArticleCardFeatured.vue'
import type { ArticleListItem } from '@/types/article'

const featured = ref<ArticleListItem[]>([])
const recent = ref<ArticleListItem[]>([])
const loading = ref(true)

onMounted(async () => {
  try {
    // 并行请求精选文章和最新文章
    const [featuredRes, recentRes] = await Promise.all([
      articlesApi.featured(),
      articlesApi.list({ page: 1, size: 6 }),
    ])
    
    featured.value = featuredRes.data
    recent.value = recentRes.data.items
  } catch (error) {
    console.error('Failed to load articles:', error)
  } finally {
    loading.value = false
  }
})
</script>

<template>
  <div class="max-w-6xl mx-auto px-4 py-12">
    <!-- Hero 区域 -->
    <section class="mb-16 text-center">
      <h1 class="text-5xl font-bold text-title mb-4">技术博客</h1>
      <p class="text-xl text-body">分享技术见解，记录成长历程</p>
    </section>

    <!-- 精选文章区域 -->
    <section v-if="featured.length" class="mb-16">
      <h2 class="text-2xl font-bold text-title mb-6">精选文章</h2>
      <div class="grid gap-6 md:grid-cols-2">
        <ArticleCardFeatured 
          v-for="article in featured" 
          :key="article.id" 
          :article="article" 
        />
      </div>
    </section>

    <!-- 最新文章区域 -->
    <section>
      <h2 class="text-2xl font-bold text-title mb-6">最新文章</h2>
      <div class="grid gap-6 md:grid-cols-3">
        <ArticleCard 
          v-for="article in recent" 
          :key="article.id" 
          :article="article" 
        />
      </div>
    </section>
  </div>
</template>
```

### 2.4 精选文章卡片组件

**文件**: `frontend/src/components/article/ArticleCardFeatured.vue`

```vue
<script setup lang="ts">
import { computed } from 'vue'
import { RouterLink } from 'vue-router'
import type { ArticleListItem } from '@/types/article'
import { formatDate } from '@/utils/date'

const props = defineProps<{ article: ArticleListItem }>()

const coverImage = computed(() => 
  props.article.cover_image || '/default-cover.jpg'
)
</script>

<template>
  <RouterLink 
    :to="`/articles/${article.slug}`"
    class="group block bg-card rounded-xl overflow-hidden shadow-sm hover:shadow-md transition-all"
  >
    <!-- 封面图片 -->
    <div class="relative h-48 overflow-hidden">
      <img 
        :src="coverImage" 
        :alt="article.title"
        class="w-full h-full object-cover group-hover:scale-105 transition-transform duration-300"
      />
      <!-- 精选徽章 -->
      <div class="absolute top-4 left-4 bg-primary text-white px-3 py-1 rounded-full text-sm font-medium">
        精选
      </div>
    </div>

    <!-- 文章信息 -->
    <div class="p-6">
      <!-- 标题 -->
      <h3 class="text-xl font-bold text-title mb-2 group-hover:text-primary transition-colors">
        {{ article.title }}
      </h3>

      <!-- 摘要 -->
      <p v-if="article.summary" class="text-body text-sm mb-4 line-clamp-2">
        {{ article.summary }}
      </p>

      <!-- 标签 -->
      <div class="flex flex-wrap gap-2 mb-4">
        <span 
          v-for="tag in article.tags" 
          :key="tag.id"
          class="px-2 py-1 rounded text-xs"
          :style="{ backgroundColor: tag.color + '20', color: tag.color }"
        >
          {{ tag.name }}
        </span>
      </div>

      <!-- 元信息 -->
      <div class="flex items-center gap-4 text-sm text-muted">
        <span v-if="article.author">{{ article.author.username }}</span>
        <span>{{ formatDate(article.published_at) }}</span>
        <span>{{ article.read_time }} 分钟阅读</span>
      </div>
    </div>
  </RouterLink>
</template>
```

### 2.5 管理员编辑页面

**文件**: `frontend/src/views/admin/AdminArticleEditView.vue`

```vue
<script setup lang="ts">
import { ref } from 'vue'

const form = ref({
  title: '',
  slug: '',
  summary: '',
  content: '',
  cover_image: '',
  is_featured: false,  // 精选开关
  status: 'draft',
  tags: [] as number[],
})

async function handleSave() {
  // 保存文章时，is_featured 会一起提交到后端
  const payload = {
    ...form.value,
    is_featured: form.value.is_featured,
  }
  
  await articlesApi.create(payload)
}
</script>

<template>
  <div class="max-w-4xl mx-auto p-6">
    <h1 class="text-2xl font-bold mb-6">编辑文章</h1>

    <form @submit.prevent="handleSave">
      <!-- 标题 -->
      <div class="mb-4">
        <label class="block text-sm font-medium mb-2">标题</label>
        <input 
          v-model="form.title" 
          type="text" 
          class="w-full px-4 py-2 border rounded-lg"
          required
        />
      </div>

      <!-- 精选开关 -->
      <div class="mb-4 flex items-center gap-3">
        <label class="text-sm font-medium">设为精选</label>
        <input 
          v-model="form.is_featured" 
          type="checkbox"
          class="w-5 h-5 text-primary rounded"
        />
        <span class="text-sm text-muted">
          精选文章会在首页优先展示
        </span>
      </div>

      <!-- 其他表单字段... -->

      <div class="flex gap-4">
        <button type="submit" class="px-6 py-2 bg-primary text-white rounded-lg">
          保存
        </button>
      </div>
    </form>
  </div>
</template>
```

---

## 3️⃣ Nginx 配置

**文件**: `nginx.conf`

```nginx
upstream backend {
    server backend:8000;
}

upstream frontend {
    server frontend:80;
}

server {
    listen 80;

    # API 请求转发到后端
    location /api/ {
        proxy_pass http://backend;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
    }

    # 前端 SPA
    location / {
        proxy_pass http://frontend;
        proxy_set_header Host $host;
    }
}
```

---

## 4️⃣ 测试验证

### 4.1 后端 API 测试

```bash
# 获取精选文章
curl http://localhost:8080/api/v1/articles/featured

# 预期响应
[
  {
    "id": 1,
    "title": "Vue 3 + TypeScript 最佳实践",
    "slug": "vue-3-typescript-best-practices",
    "summary": "深入探讨 Vue 3 与 TypeScript 结合使用的最佳实践...",
    "cover_image": null,
    "author": {
      "id": 3,
      "username": "admin",
      "avatar_url": null
    },
    "status": "published",
    "is_featured": true,
    "view_count": 7,
    "read_time": 5,
    "tags": [
      {
        "id": 1,
        "name": "Vue.js",
        "slug": "vuejs",
        "color": "#42b883"
      }
    ],
    "published_at": "2026-05-02T04:22:17.053364+00:00",
    "created_at": "2026-05-02T04:22:17.053364+00:00"
  }
]
```

### 4.2 前端页面测试

1. 访问首页：http://localhost:8080/
2. 应该看到"精选文章"区域
3. 最多显示 5 篇精选文章
4. 每篇文章卡片显示"精选"徽章

### 4.3 管理员功能测试

1. 登录管理后台：http://localhost:8080/admin
2. 进入文章编辑页面
3. 勾选"设为精选"开关
4. 保存文章
5. 返回首页，应该看到该文章出现在精选区域

---

## 5️⃣ 数据库查询示例

```sql
-- 查看所有精选文章
SELECT id, title, is_featured, status, published_at 
FROM articles 
WHERE is_featured = true 
ORDER BY published_at DESC;

-- 设置文章为精选
UPDATE articles 
SET is_featured = true 
WHERE id = 1;

-- 取消精选
UPDATE articles 
SET is_featured = false 
WHERE id = 1;

-- 统计精选文章数量
SELECT COUNT(*) 
FROM articles 
WHERE is_featured = true AND status = 'published';
```

---

## 6️⃣ 关键文件清单

| 层级 | 文件路径 | 作用 |
|------|---------|------|
| **后端** | | |
| 数据模型 | `backend/app/models/article.py` | 定义 Article 模型，包含 is_featured 字段 |
| 响应模型 | `backend/app/schemas/article.py` | 定义 ArticleListItem 响应格式 |
| API 路由 | `backend/app/routers/articles.py` | 定义 `/articles/featured` 端点 |
| 数据库迁移 | `backend/alembic/versions/001_initial_schema.py` | 创建 articles 表结构 |
| **前端** | | |
| API 客户端 | `frontend/src/api/articles.ts` | 封装精选文章 API 调用 |
| 类型定义 | `frontend/src/types/article.ts` | TypeScript 类型定义 |
| 首页组件 | `frontend/src/views/HomeView.vue` | 展示精选文章的页面 |
| 卡片组件 | `frontend/src/components/article/ArticleCardFeatured.vue` | 精选文章卡片样式 |
| 管理页面 | `frontend/src/views/admin/AdminArticleEditView.vue` | 设置精选状态 |
| **配置** | | |
| Nginx | `nginx.conf` | 反向代理配置 |
| Docker | `docker-compose.yml` | 容器编排 |

---

## 7️⃣ 常见问题

### Q1: 为什么精选文章不显示？

**检查清单**：
1. 文章的 `status` 是否为 `"published"`
2. 文章的 `is_featured` 是否为 `true`
3. 文章是否有 `published_at` 时间
4. 数据库中是否有符合条件的文章

```sql
-- 检查精选文章
SELECT id, title, status, is_featured, published_at 
FROM articles 
WHERE is_featured = true;
```

### Q2: 如何修改精选文章数量？

修改后端路由中的 `.limit(5)` 参数：

```python
# backend/app/routers/articles.py
@router.get("/articles/featured")
def featured_articles(db: Session = Depends(get_db)):
    return (
        db.query(Article)
        .filter(Article.status == "published", Article.is_featured == True)
        .order_by(Article.published_at.desc())
        .limit(10)  # 改为 10 篇
        .all()
    )
```

### Q3: 如何批量设置精选？

```python
# 在 Python shell 或脚本中
from app.database import SessionLocal
from app.models import Article

db = SessionLocal()

# 批量设置前 5 篇文章为精选
articles = db.query(Article).filter(Article.status == "published").limit(5).all()
for article in articles:
    article.is_featured = True

db.commit()
```

---

## 8️⃣ 性能优化建议

### 8.1 数据库索引

```sql
-- 为 is_featured 和 status 创建复合索引
CREATE INDEX idx_articles_featured_status 
ON articles(is_featured, status, published_at DESC);
```

### 8.2 前端缓存

```typescript
// 使用 Pinia 缓存精选文章
import { defineStore } from 'pinia'

export const useArticlesStore = defineStore('articles', {
  state: () => ({
    featured: [] as ArticleListItem[],
    featuredLoaded: false,
  }),
  
  actions: {
    async loadFeatured() {
      if (this.featuredLoaded) return this.featured
      
      const { data } = await articlesApi.featured()
      this.featured = data
      this.featuredLoaded = true
      
      return data
    }
  }
})
```

### 8.3 CDN 缓存

在 Nginx 中为精选文章 API 添加缓存：

```nginx
location /api/v1/articles/featured {
    proxy_pass http://backend;
    proxy_cache_valid 200 5m;  # 缓存 5 分钟
    add_header X-Cache-Status $upstream_cache_status;
}
```

---

## 9️⃣ 扩展功能建议

### 9.1 精选文章排序

添加 `featured_order` 字段，允许管理员自定义精选文章的显示顺序：

```python
# 数据库模型
featured_order = Column(Integer, default=0)

# API 查询
.order_by(Article.featured_order.desc(), Article.published_at.desc())
```

### 9.2 精选文章分类

添加 `featured_category` 字段，支持多个精选分类：

```python
featured_category = Column(String(50))  # 'tech', 'tutorial', 'news'
```

### 9.3 精选文章过期

添加 `featured_until` 字段，自动取消过期的精选：

```python
featured_until = Column(DateTime(timezone=True))

# 查询时过滤
.filter(
    Article.is_featured == True,
    or_(Article.featured_until.is_(None), Article.featured_until > datetime.now())
)
```

---

## 🎉 总结

精选文章功能通过以下关键点实现：

1. **数据库字段**：`is_featured` 布尔字段标记精选状态
2. **后端 API**：`GET /api/v1/articles/featured` 返回精选文章列表
3. **前端展示**：首页使用 `ArticleCardFeatured` 组件展示
4. **管理功能**：管理员可通过编辑页面设置精选状态
5. **性能优化**：数据库索引 + 前端缓存 + CDN 缓存

完整的实现涵盖了从数据库到前端展示的所有环节，确保功能稳定可靠。
