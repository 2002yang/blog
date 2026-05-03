<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { RouterLink } from 'vue-router'
import client from '@/api/client'
import { useHead } from '@vueuse/head'

useHead({ title: '后台概览 — DevBlog' })

interface Stats {
  total_articles: number
  published_articles: number
  draft_articles: number
  total_views: number
  total_tags: number
}

const stats = ref<Stats | null>(null)

onMounted(async () => {
  const { data } = await client.get<Stats>('/admin/stats')
  stats.value = data
})

const cards = [
  { key: 'total_articles', label: '全部文章', color: 'text-blue-600 bg-blue-50' },
  { key: 'published_articles', label: '已发布', color: 'text-primary bg-primary-light' },
  { key: 'draft_articles', label: '草稿', color: 'text-yellow-600 bg-yellow-50' },
  { key: 'total_views', label: '总阅读量', color: 'text-purple-600 bg-purple-50' },
]
</script>

<template>
  <div class="p-8">
    <div class="flex items-center justify-between mb-8">
      <h1 class="text-2xl font-bold text-title">概览</h1>
      <RouterLink to="/admin/articles/new" class="btn-primary">+ 新建文章</RouterLink>
    </div>

    <div class="grid grid-cols-2 lg:grid-cols-4 gap-4 mb-8">
      <div v-for="card in cards" :key="card.key" class="card p-5">
        <div class="text-3xl font-bold text-title mb-1">
          {{ stats ? (stats as any)[card.key].toLocaleString() : '—' }}
        </div>
        <div class="text-sm text-muted">{{ card.label }}</div>
      </div>
    </div>

    <div class="card p-6">
      <h2 class="text-base font-semibold text-title mb-4">快速操作</h2>
      <div class="flex flex-wrap gap-3">
        <RouterLink to="/admin/articles/new" class="btn-primary">写新文章</RouterLink>
        <RouterLink to="/admin/articles" class="btn-secondary">管理文章</RouterLink>
        <RouterLink to="/" target="_blank" class="btn-ghost">查看博客 ↗</RouterLink>
      </div>
    </div>
  </div>
</template>
