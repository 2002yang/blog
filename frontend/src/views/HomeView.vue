<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { RouterLink } from 'vue-router'
import AppHeader from '@/components/layout/AppHeader.vue'
import AppFooter from '@/components/layout/AppFooter.vue'
import ArticleCardFeatured from '@/components/article/ArticleCardFeatured.vue'
import ArticleCard from '@/components/article/ArticleCard.vue'
import AppSkeleton from '@/components/common/AppSkeleton.vue'
import { articlesApi } from '@/api/articles'
import type { ArticleListItem } from '@/types/article'
import { useHead } from '@vueuse/head'

useHead({ title: 'DevBlog — 技术博客' })

const featured = ref<ArticleListItem[]>([])
const recent = ref<ArticleListItem[]>([])
const loading = ref(true)

onMounted(async () => {
  try {
    const [featuredRes, recentRes] = await Promise.all([
      articlesApi.featured(),
      articlesApi.list({ page: 1, size: 6 }),
    ])
    featured.value = featuredRes.data
    recent.value = recentRes.data.items
  } finally {
    loading.value = false
  }
})
</script>

<template>
  <div class="min-h-screen flex flex-col">
    <AppHeader />

    <main class="flex-1">
      <!-- Hero -->
      <section class="page-container pt-20 pb-16 text-center">
        <div class="inline-flex items-center gap-2 px-3 py-1.5 rounded-full bg-primary-light text-primary text-sm font-medium mb-6">
          <span class="w-1.5 h-1.5 rounded-full bg-primary animate-pulse" />
          持续更新中
        </div>
        <h1 class="text-4xl md:text-5xl lg:text-6xl font-bold text-title tracking-tight mb-6 leading-tight">
          记录技术，<br class="sm:hidden" />
          <span class="text-primary">分享思考</span>
        </h1>
        <p class="text-lg text-body max-w-xl mx-auto mb-8">
          一个独立开发者的技术博客，专注于 Web 开发、系统设计与工程实践。
        </p>
        <div class="flex items-center justify-center gap-3">
          <RouterLink to="/articles" class="btn-primary px-6 py-2.5">浏览文章</RouterLink>
          <RouterLink to="/tags" class="btn-secondary px-6 py-2.5">探索标签</RouterLink>
        </div>
      </section>

      <!-- Featured -->
      <section v-if="loading || featured.length" class="page-container pb-16">
        <h2 class="section-title mb-6">精选文章</h2>
        <div v-if="loading" class="space-y-4">
          <div v-for="i in 2" :key="i" class="card p-6 md:p-8">
            <AppSkeleton :lines="4" />
          </div>
        </div>
        <div v-else class="space-y-4">
          <ArticleCardFeatured v-for="a in featured" :key="a.id" :article="a" />
        </div>
      </section>

      <!-- Recent -->
      <section class="page-container pb-20">
        <div class="flex items-center justify-between mb-6">
          <h2 class="section-title">最新文章</h2>
          <RouterLink to="/articles" class="text-sm text-primary hover:text-primary-hover font-medium">查看全部 →</RouterLink>
        </div>
        <div v-if="loading" class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-5">
          <div v-for="i in 6" :key="i" class="card p-6">
            <AppSkeleton :lines="5" />
          </div>
        </div>
        <div v-else-if="recent.length" class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-5">
          <ArticleCard v-for="a in recent" :key="a.id" :article="a" />
        </div>
        <div v-else class="text-center py-16 text-muted">
          <p class="text-lg">暂无文章</p>
        </div>
      </section>
    </main>

    <AppFooter />
  </div>
</template>
