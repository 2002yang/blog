# Vue 组件数据流动详解

## 📚 概述

本文档详细解释 Vue 3 中父组件如何通过 `ref` 变量和 `v-for` 指令将数据传递给子组件。

以首页的精选文章功能为例，展示从 API 获取数据到组件渲染的完整流程。

---

## 🔄 完整数据流动图

```
┌─────────────────────────────────────────────────────────────┐
│ 1. 组件挂载 (onMounted)                                      │
└─────────────────────────────────────────────────────────────┘
                            ↓
┌─────────────────────────────────────────────────────────────┐
│ 2. 调用后端 API                                              │
│    GET /api/v1/articles/featured                            │
└─────────────────────────────────────────────────────────────┘
                            ↓
┌─────────────────────────────────────────────────────────────┐
│ 3. 后端返回 JSON 数据                                        │
│    [                                                         │
│      { id: 1, title: "文章1", ... },                        │
│      { id: 2, title: "文章2", ... },                        │
│      { id: 3, title: "文章3", ... }                         │
│    ]                                                         │
└─────────────────────────────────────────────────────────────┘
                            ↓
┌─────────────────────────────────────────────────────────────┐
│ 4. 数据赋值给 ref 变量                                       │
│    featured.value = [文章1, 文章2, 文章3]                   │
└─────────────────────────────────────────────────────────────┘
                            ↓
┌─────────────────────────────────────────────────────────────┐
│ 5. Vue 模板渲染 (v-for 遍历)                                │
│    v-for="a in featured"                                    │
│    第1次循环: a = 文章1                                      │
│    第2次循环: a = 文章2                                      │
│    第3次循环: a = 文章3                                      │
└─────────────────────────────────────────────────────────────┘
                            ↓
┌─────────────────────────────────────────────────────────────┐
│ 6. 创建子组件实例并传递 props                                │
│    <ArticleCardFeatured :article="文章1" />                 │
│    <ArticleCardFeatured :article="文章2" />                 │
│    <ArticleCardFeatured :article="文章3" />                 │
└─────────────────────────────────────────────────────────────┘
                            ↓
┌─────────────────────────────────────────────────────────────┐
│ 7. 子组件接收 props 并渲染                                   │
│    props.article.title                                      │
│    props.article.summary                                    │
│    props.article.cover_image                                │
└─────────────────────────────────────────────────────────────┘
                            ↓
┌─────────────────────────────────────────────────────────────┐
│ 8. 用户看到页面                                              │
│    ┌──────────────────┐                                     │
│    │ 精选文章卡片 1   │                                     │
│    └──────────────────┘                                     │
│    ┌──────────────────┐                                     │
│    │ 精选文章卡片 2   │                                     │
│    └──────────────────┘                                     │
│    ┌──────────────────┐                                     │
│    │ 精选文章卡片 3   │                                     │
│    └──────────────────┘                                     │
└─────────────────────────────────────────────────────────────┘
```

---

## 📝 代码详解

### 第 1 步：定义响应式变量

**文件**: `frontend/src/views/HomeView.vue`

```typescript
import { ref } from 'vue'
import type { ArticleListItem } from '@/types/article'

// 定义两个响应式数组，初始值为空数组
const featured = ref<ArticleListItem[]>([])  // 存储精选文章
const recent = ref<ArticleListItem[]>([])    // 存储最新文章
```

**解释**：
- `ref()` 创建响应式变量
- `<ArticleListItem[]>` 是 TypeScript 类型注解，表示这是一个文章对象数组
- 初始值是空数组 `[]`，等待数据填充

**类型定义**：

```typescript
// frontend/src/types/article.ts
export interface ArticleListItem {
  id: number
  title: string
  slug: string
  summary: string | null
  cover_image: string | null
  author: ArticleAuthor | null
  status: string
  is_featured: boolean
  view_count: number
  read_time: number
  tags: Tag[]
  published_at: string | null
  created_at: string
}
```

---

### 第 2 步：组件挂载时获取数据

```typescript
import { onMounted } from 'vue'
import { articlesApi } from '@/api/articles'

onMounted(async () => {
  try {
    // 并行请求两个接口
    const [featuredRes, recentRes] = await Promise.all([
      articlesApi.featured(),              // 获取精选文章
      articlesApi.list({ page: 1, size: 6 }), // 获取最新文章
    ])
    
    // 把后端返回的数据赋值给 ref 变量
    featured.value = featuredRes.data      // 数组赋值
    recent.value = recentRes.data.items    // 数组赋值
  } catch (error) {
    console.error('Failed to load articles:', error)
  } finally {
    loading.value = false
  }
})
```

**关键点**：
1. `onMounted` 是 Vue 3 生命周期钩子，组件挂载后执行
2. `Promise.all` 并行请求两个接口，提高性能
3. `featuredRes.data` 是后端返回的文章数组
4. 必须使用 `.value` 访问 ref 的值

**API 调用**：

```typescript
// frontend/src/api/articles.ts
export const articlesApi = {
  featured: () => 
    client.get<ArticleListItem[]>('/articles/featured'),
}
```

**后端响应示例**：

```json
// GET /api/v1/articles/featured 返回
[
  {
    "id": 1,
    "title": "Vue 3 + TypeScript 最佳实践",
    "slug": "vue-3-typescript",
    "summary": "深入探讨 Vue 3 与 TypeScript 结合使用的最佳实践...",
    "cover_image": "/uploads/2026/05/xxx.jpg",
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
  },
  {
    "id": 2,
    "title": "FastAPI 异步编程实战",
    "slug": "fastapi-async",
    "summary": "学习如何在 FastAPI 中使用异步编程提升 API 性能...",
    "cover_image": "/uploads/2026/05/yyy.jpg",
    "is_featured": true,
    "view_count": 2,
    "read_time": 8,
    "tags": [
      {
        "id": 4,
        "name": "Python",
        "slug": "python",
        "color": "#3776ab"
      }
    ],
    "published_at": "2026-04-30T04:22:17.054159+00:00"
  }
]
```

---

### 第 3 步：模板中遍历数据

```vue
<template>
  <div>
    <!-- 精选文章区域 -->
    <section v-if="loading || featured.length" class="page-container pb-16">
      <h2 class="section-title mb-6">精选文章</h2>
      
      <!-- 加载状态 -->
      <div v-if="loading" class="space-y-4">
        <div v-for="i in 2" :key="i" class="card p-6 md:p-8">
          <AppSkeleton :lines="4" />
        </div>
      </div>
      
      <!-- 数据加载完成后渲染 -->
      <div v-else class="space-y-4">
        <!-- 关键代码：v-for 遍历 featured 数组 -->
        <ArticleCardFeatured 
          v-for="a in featured" 
          :key="a.id" 
          :article="a" 
        />
      </div>
    </section>
  </div>
</template>
```

**v-for 指令详解**：

```vue
<ArticleCardFeatured v-for="a in featured" :key="a.id" :article="a" />
```

这行代码等价于：

```javascript
// 伪代码展示 v-for 的工作原理
featured.value.forEach((a) => {
  // 创建一个 ArticleCardFeatured 组件实例
  createComponent(ArticleCardFeatured, {
    key: a.id,      // 唯一标识
    article: a      // 传递 props
  })
})
```

**实际渲染结果**（假设有 3 篇文章）：

```vue
<!-- Vue 会将 v-for 展开成多个组件 -->
<ArticleCardFeatured :key="1" :article="文章1对象" />
<ArticleCardFeatured :key="2" :article="文章2对象" />
<ArticleCardFeatured :key="3" :article="文章3对象" />
```

**v-for 语法说明**：

| 语法部分 | 说明 | 示例值 |
|---------|------|--------|
| `v-for="a in featured"` | 遍历 featured 数组，每次循环 a 代表当前文章 | a = { id: 1, title: "...", ... } |
| `:key="a.id"` | 为每个组件提供唯一标识，用于 Vue 的 diff 算法 | key = 1, 2, 3 |
| `:article="a"` | 将当前文章对象作为 props 传递给子组件 | article = { id: 1, title: "...", ... } |

---

### 第 4 步：子组件接收 props

**文件**: `frontend/src/components/article/ArticleCardFeatured.vue`

```vue
<script setup lang="ts">
import { RouterLink } from 'vue-router'
import type { ArticleListItem } from '@/types/article'
import { formatDate } from '@/utils/date'

// 定义组件接收的 props
defineProps<{ article: ArticleListItem }>()
</script>

<template>
  <RouterLink 
    :to="{ name: 'article-detail', params: { slug: article.slug } }" 
    class="block group"
  >
    <article class="card-hover p-6 md:p-8 flex flex-col md:flex-row gap-6">
      <!-- 封面图片 -->
      <div 
        v-if="article.cover_image" 
        class="md:w-72 md:shrink-0 aspect-video md:aspect-auto rounded-xl overflow-hidden bg-bg"
      >
        <img 
          :src="article.cover_image" 
          :alt="article.title" 
          class="w-full h-full object-cover group-hover:scale-105 transition-transform duration-300" 
        />
      </div>

      <div class="flex flex-col gap-3 flex-1 min-w-0">
        <!-- 精选徽章 + 标签 -->
        <div class="flex flex-wrap items-center gap-2">
          <span class="badge bg-primary text-white text-xs">精选</span>
          <span 
            v-for="tag in article.tags" 
            :key="tag.id"
            class="badge text-xs"
            :style="{ backgroundColor: tag.color + '20', color: tag.color }"
          >
            {{ tag.name }}
          </span>
        </div>

        <!-- 标题 -->
        <h3 class="text-xl md:text-2xl font-bold text-title group-hover:text-primary transition-colors line-clamp-2">
          {{ article.title }}
        </h3>

        <!-- 摘要 -->
        <p v-if="article.summary" class="text-body text-sm md:text-base line-clamp-2 flex-1">
          {{ article.summary }}
        </p>

        <!-- 元信息 -->
        <div class="flex items-center gap-3 text-sm text-muted mt-auto">
          <span v-if="article.author" class="flex items-center gap-1.5">
            <svg class="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z" />
            </svg>
            {{ article.author.username }}
          </span>
          <span class="flex items-center gap-1.5">
            <svg class="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 7V3m8 4V3m-9 8h10M5 21h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z" />
            </svg>
            {{ formatDate(article.published_at) }}
          </span>
          <span class="flex items-center gap-1.5">
            <svg class="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z" />
            </svg>
            {{ article.read_time }} 分钟
          </span>
        </div>
      </div>
    </article>
  </RouterLink>
</template>
```

**Props 接收说明**：

```typescript
defineProps<{ article: ArticleListItem }>()
```

这行代码的作用：
1. 定义组件接收一个名为 `article` 的 prop
2. 类型是 `ArticleListItem`（单篇文章对象）
3. 在模板中可以直接使用 `article.xxx` 访问属性

**在模板中使用 props**：

```vue
<!-- 直接访问 article 的属性 -->
{{ article.title }}           <!-- 文章标题 -->
{{ article.summary }}         <!-- 文章摘要 -->
{{ article.cover_image }}     <!-- 封面图片 URL -->
{{ article.author.username }} <!-- 作者用户名 -->
{{ article.read_time }}       <!-- 阅读时间 -->
```

---

## 🎯 核心概念总结

### 1. ref 响应式变量

```typescript
const featured = ref<ArticleListItem[]>([])
```

**作用**：
- 创建响应式数据容器
- 数据变化时，Vue 自动更新视图
- 必须通过 `.value` 访问和修改值

**示例**：

```typescript
// 读取
console.log(featured.value)  // [文章1, 文章2, ...]

// 修改
featured.value = [新文章1, 新文章2]  // 触发视图更新

// 添加
featured.value.push(新文章)  // 触发视图更新
```

### 2. v-for 列表渲染

```vue
<ArticleCardFeatured v-for="a in featured" :key="a.id" :article="a" />
```

**作用**：
- 遍历数组，为每个元素创建一个组件实例
- `:key` 提供唯一标识，优化渲染性能
- 每次循环将当前元素传递给子组件

**等价代码**：

```javascript
// 伪代码
featured.value.forEach((article) => {
  render(<ArticleCardFeatured article={article} key={article.id} />)
})
```

### 3. Props 数据传递

```vue
<!-- 父组件 -->
<ArticleCardFeatured :article="a" />

<!-- 子组件 -->
<script setup>
defineProps<{ article: ArticleListItem }>()
</script>
```

**作用**：
- 父组件通过 props 向子组件传递数据
- 子组件通过 `defineProps` 接收数据
- 数据流是单向的：父 → 子

---

## 🔍 数据流动实例

假设后端返回 2 篇精选文章：

### 步骤 1：API 返回数据

```json
[
  {
    "id": 1,
    "title": "Vue 3 最佳实践",
    "slug": "vue-3-best-practices",
    "summary": "学习 Vue 3 的最佳实践...",
    "cover_image": "/uploads/2026/05/vue.jpg",
    "tags": [{ "id": 1, "name": "Vue.js", "color": "#42b883" }],
    "author": { "id": 3, "username": "admin" },
    "read_time": 5
  },
  {
    "id": 2,
    "title": "TypeScript 进阶",
    "slug": "typescript-advanced",
    "summary": "深入理解 TypeScript...",
    "cover_image": "/uploads/2026/05/ts.jpg",
    "tags": [{ "id": 3, "name": "TypeScript", "color": "#3178c6" }],
    "author": { "id": 3, "username": "admin" },
    "read_time": 8
  }
]
```

### 步骤 2：数据赋值

```typescript
featured.value = [文章1对象, 文章2对象]
```

### 步骤 3：模板渲染

```vue
<!-- v-for 第 1 次循环 -->
<ArticleCardFeatured 
  :key="1" 
  :article="{
    id: 1,
    title: 'Vue 3 最佳实践',
    slug: 'vue-3-best-practices',
    summary: '学习 Vue 3 的最佳实践...',
    cover_image: '/uploads/2026/05/vue.jpg',
    tags: [{ id: 1, name: 'Vue.js', color: '#42b883' }],
    author: { id: 3, username: 'admin' },
    read_time: 5
  }" 
/>

<!-- v-for 第 2 次循环 -->
<ArticleCardFeatured 
  :key="2" 
  :article="{
    id: 2,
    title: 'TypeScript 进阶',
    slug: 'typescript-advanced',
    summary: '深入理解 TypeScript...',
    cover_image: '/uploads/2026/05/ts.jpg',
    tags: [{ id: 3, name: 'TypeScript', color: '#3178c6' }],
    author: { id: 3, username: 'admin' },
    read_time: 8
  }" 
/>
```

### 步骤 4：子组件渲染

每个 `ArticleCardFeatured` 组件内部：

```vue
<!-- 第 1 个组件 -->
<article>
  <img src="/uploads/2026/05/vue.jpg" alt="Vue 3 最佳实践" />
  <h3>Vue 3 最佳实践</h3>
  <p>学习 Vue 3 的最佳实践...</p>
  <span>Vue.js</span>
  <span>admin</span>
  <span>5 分钟</span>
</article>

<!-- 第 2 个组件 -->
<article>
  <img src="/uploads/2026/05/ts.jpg" alt="TypeScript 进阶" />
  <h3>TypeScript 进阶</h3>
  <p>深入理解 TypeScript...</p>
  <span>TypeScript</span>
  <span>admin</span>
  <span>8 分钟</span>
</article>
```

---

## 🎨 可视化对比

### 传统方式（不使用 v-for）

```vue
<!-- 需要手动写多个组件 -->
<ArticleCardFeatured :article="featured[0]" />
<ArticleCardFeatured :article="featured[1]" />
<ArticleCardFeatured :article="featured[2]" />
<!-- 如果有 100 篇文章，需要写 100 行... -->
```

### 使用 v-for（推荐）

```vue
<!-- 一行代码搞定，自动适应数组长度 -->
<ArticleCardFeatured v-for="a in featured" :key="a.id" :article="a" />
```

---

## 🚀 常见问题

### Q1: 为什么要用 `.value`？

```typescript
// ❌ 错误：直接赋值不会触发响应式更新
featured = [新数据]

// ✅ 正确：通过 .value 赋值才会触发更新
featured.value = [新数据]
```

**原因**：`ref()` 返回的是一个包装对象，真正的值存储在 `.value` 属性中。

### Q2: 为什么需要 `:key`？

```vue
<!-- ❌ 没有 key，Vue 无法高效追踪元素 -->
<ArticleCardFeatured v-for="a in featured" :article="a" />

<!-- ✅ 有 key，Vue 可以精确识别每个元素 -->
<ArticleCardFeatured v-for="a in featured" :key="a.id" :article="a" />
```

**原因**：`:key` 帮助 Vue 识别哪些元素改变了、添加了或删除了，提高渲染性能。

### Q3: `:article="a"` 和 `article="a"` 有什么区别？

```vue
<!-- ❌ 错误：传递字符串 "a" -->
<ArticleCardFeatured article="a" />

<!-- ✅ 正确：传递变量 a 的值 -->
<ArticleCardFeatured :article="a" />
```

**原因**：`:` 是 `v-bind:` 的缩写，表示绑定 JavaScript 表达式。

### Q4: 如何在子组件中修改 props？

```vue
<!-- ❌ 错误：不能直接修改 props -->
<script setup>
const props = defineProps<{ article: ArticleListItem }>()
props.article.title = "新标题"  // 报错！
</script>

<!-- ✅ 正确：通过 emit 通知父组件修改 -->
<script setup>
const props = defineProps<{ article: ArticleListItem }>()
const emit = defineEmits<{ update: [article: ArticleListItem] }>()

function updateTitle() {
  emit('update', { ...props.article, title: "新标题" })
}
</script>
```

**原因**：Vue 遵循单向数据流，子组件不能直接修改 props。

---

## 📚 相关文件清单

| 文件路径 | 作用 |
|---------|------|
| `frontend/src/views/HomeView.vue` | 父组件，定义 ref 变量，调用 API，使用 v-for |
| `frontend/src/components/article/ArticleCardFeatured.vue` | 子组件，接收 props，渲染卡片 |
| `frontend/src/api/articles.ts` | API 客户端，封装 HTTP 请求 |
| `frontend/src/types/article.ts` | TypeScript 类型定义 |
| `backend/app/routers/articles.py` | 后端 API 路由 |
| `backend/app/models/article.py` | 数据库模型 |

---

## 🎓 学习建议

1. **理解响应式原理**：学习 Vue 3 的 `ref` 和 `reactive`
2. **掌握列表渲染**：熟练使用 `v-for` 和 `:key`
3. **理解组件通信**：父子组件通过 props 和 emit 通信
4. **TypeScript 类型**：使用类型注解提高代码质量
5. **实践项目**：通过实际项目加深理解

---

## 🔗 参考资源

- [Vue 3 官方文档 - 列表渲染](https://cn.vuejs.org/guide/essentials/list.html)
- [Vue 3 官方文档 - 响应式基础](https://cn.vuejs.org/guide/essentials/reactivity-fundamentals.html)
- [Vue 3 官方文档 - 组件基础](https://cn.vuejs.org/guide/essentials/component-basics.html)
- [TypeScript 官方文档](https://www.typescriptlang.org/docs/)

---

**文档版本**: 1.0  
**最后更新**: 2026-05-03  
**作者**: Claude Code
