<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { RouterLink } from 'vue-router'
import { articlesApi } from '@/api/articles'
import { useUiStore } from '@/stores/ui'
import type { ArticleListItem, PaginatedArticles } from '@/types/article'
import AppPagination from '@/components/common/AppPagination.vue'
import { formatDateShort } from '@/utils/date'
import { useHead } from '@vueuse/head'

useHead({ title: '文章管理 — DevBlog' })

const ui = useUiStore()
const data = ref<PaginatedArticles | null>(null)
const page = ref(1)
const loading = ref(true)

async function fetchArticles() {
  loading.value = true
  try {
    const { data: res } = await articlesApi.adminList({ page: page.value, size: 15 })
    data.value = res
  } finally {
    loading.value = false
  }
}

onMounted(fetchArticles)

async function togglePublish(article: ArticleListItem) {
  try {
    await articlesApi.togglePublish(article.id)
    await fetchArticles()
    ui.toast.success(article.status === 'published' ? '已取消发布' : '已发布')
  } catch {
    ui.toast.error('操作失败')
  }
}

async function deleteArticle(article: ArticleListItem) {
  if (!confirm(`确认删除「${article.title}」？此操作不可撤销。`)) return
  try {
    await articlesApi.delete(article.id)
    await fetchArticles()
    ui.toast.success('已删除')
  } catch {
    ui.toast.error('删除失败')
  }
}
</script>

<template>
  <div class="p-8">
    <div class="flex items-center justify-between mb-8">
      <h1 class="text-2xl font-bold text-title">文章管理</h1>
      <RouterLink to="/admin/articles/new" class="btn-primary">+ 新建文章</RouterLink>
    </div>

    <div class="card overflow-hidden">
      <table class="w-full text-sm">
        <thead class="bg-bg border-b border-border">
          <tr>
            <th class="text-left px-5 py-3 font-medium text-muted">标题</th>
            <th class="text-left px-4 py-3 font-medium text-muted hidden md:table-cell">标签</th>
            <th class="text-left px-4 py-3 font-medium text-muted hidden lg:table-cell">日期</th>
            <th class="text-left px-4 py-3 font-medium text-muted">状态</th>
            <th class="text-right px-5 py-3 font-medium text-muted">操作</th>
          </tr>
        </thead>
        <tbody>
          <tr v-if="loading">
            <td colspan="5" class="px-5 py-8 text-center text-muted">加载中...</td>
          </tr>
          <tr
            v-for="article in data?.items"
            :key="article.id"
            class="border-b border-border/60 hover:bg-bg/50 transition-colors"
          >
            <td class="px-5 py-3.5">
              <RouterLink
                :to="{ name: 'article-detail', params: { slug: article.slug } }"
                target="_blank"
                class="font-medium text-title hover:text-primary line-clamp-1"
              >
                {{ article.title }}
              </RouterLink>
            </td>
            <td class="px-4 py-3.5 hidden md:table-cell">
              <div class="flex flex-wrap gap-1">
                <span v-for="tag in article.tags.slice(0, 2)" :key="tag.id" class="badge-primary text-xs">{{ tag.name }}</span>
              </div>
            </td>
            <td class="px-4 py-3.5 text-muted hidden lg:table-cell">{{ formatDateShort(article.created_at) }}</td>
            <td class="px-4 py-3.5">
              <span
                class="badge text-xs"
                :class="article.status === 'published' ? 'bg-green-50 text-green-700' : 'bg-yellow-50 text-yellow-700'"
              >
                {{ article.status === 'published' ? '已发布' : '草稿' }}
              </span>
            </td>
            <td class="px-5 py-3.5 text-right">
              <div class="flex items-center justify-end gap-2">
                <RouterLink :to="{ name: 'admin-article-edit', params: { id: article.id } }" class="btn-ghost text-xs px-2 py-1">编辑</RouterLink>
                <button class="btn-ghost text-xs px-2 py-1" @click="togglePublish(article)">
                  {{ article.status === 'published' ? '取消发布' : '发布' }}
                </button>
                <button class="btn-ghost text-xs px-2 py-1 text-red-500 hover:bg-red-50" @click="deleteArticle(article)">删除</button>
              </div>
            </td>
          </tr>
        </tbody>
      </table>
    </div>

    <div class="mt-6">
      <AppPagination v-if="data" :total="data.total" :page="page" :size="15" @change="(p) => { page = p; fetchArticles() }" />
    </div>
  </div>
</template>
