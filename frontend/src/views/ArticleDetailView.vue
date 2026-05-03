<script setup lang="ts">
import { ref, onMounted, watch } from 'vue'
import { useRoute, RouterLink } from 'vue-router'
import AppHeader from '@/components/layout/AppHeader.vue'
import AppFooter from '@/components/layout/AppFooter.vue'
import ArticleContent from '@/components/article/ArticleContent.vue'
import ArticleToc from '@/components/article/ArticleToc.vue'
import AppSkeleton from '@/components/common/AppSkeleton.vue'
import { articlesApi } from '@/api/articles'
import type { Article } from '@/types/article'
import { renderMarkdown, extractToc, type TocItem } from '@/utils/markdown'
import { formatDate } from '@/utils/date'
import { useHead } from '@vueuse/head'
import { computed } from 'vue'

const route = useRoute()
const article = ref<Article | null>(null)
const html = ref('')
const toc = ref<TocItem[]>([])
const loading = ref(true)
const error = ref(false)

useHead(computed(() => ({
  title: article.value ? `${article.value.title} — DevBlog` : 'DevBlog',
  meta: [
    { name: 'description', content: article.value?.summary ?? '' },
    { property: 'og:title', content: article.value?.title ?? '' },
    { property: 'og:description', content: article.value?.summary ?? '' },
    { property: 'og:image', content: article.value?.cover_image ?? '' },
    { property: 'og:type', content: 'article' },
  ],
})))

async function fetchArticle() {
  loading.value = true
  error.value = false
  try {
    const { data } = await articlesApi.getBySlug(route.params.slug as string)
    article.value = data
    html.value = renderMarkdown(data.content)
    toc.value = extractToc(data.content)
    articlesApi.incrementView(data.id).catch(() => {})
  } catch {
    error.value = true
  } finally {
    loading.value = false
  }
}

onMounted(fetchArticle)
watch(() => route.params.slug, fetchArticle)
</script>

<template>
  <div class="min-h-screen flex flex-col">
    <AppHeader />
    <main class="flex-1 page-container py-12">
      <!-- Loading -->
      <div v-if="loading" class="max-w-3xl mx-auto">
        <AppSkeleton :lines="2" class="mb-6" />
        <div class="h-64 bg-border rounded-xl animate-pulse mb-8" />
        <AppSkeleton :lines="8" />
      </div>

      <!-- Error -->
      <div v-else-if="error" class="text-center py-20">
        <p class="text-2xl font-bold text-title mb-2">文章不存在</p>
        <p class="text-muted mb-6">该文章可能已被删除或链接有误</p>
        <RouterLink to="/articles" class="btn-primary">返回文章列表</RouterLink>
      </div>

      <!-- Content -->
      <div v-else-if="article" class="flex gap-12">
        <article class="flex-1 min-w-0 max-w-3xl">
          <!-- Tags -->
          <div class="flex flex-wrap gap-2 mb-4">
            <RouterLink
              v-for="tag in article.tags"
              :key="tag.id"
              :to="{ name: 'tag-articles', params: { slug: tag.slug } }"
              class="badge-primary text-xs hover:bg-primary hover:text-white transition-colors"
            >
              {{ tag.name }}
            </RouterLink>
          </div>

          <!-- Title -->
          <h1 class="text-3xl md:text-4xl font-bold text-title leading-tight mb-4">
            {{ article.title }}
          </h1>

          <!-- Meta -->
          <div class="flex flex-wrap items-center gap-3 text-sm text-muted mb-8 pb-8 border-b border-border">
            <span v-if="article.author" class="flex items-center gap-1.5">
              <img v-if="article.author.avatar_url" :src="article.author.avatar_url" class="w-5 h-5 rounded-full" />
              <span>{{ article.author.username }}</span>
            </span>
            <span>{{ formatDate(article.published_at || article.created_at) }}</span>
            <span>·</span>
            <span>{{ article.read_time }} 分钟阅读</span>
            <span>·</span>
            <span>{{ article.view_count }} 次阅读</span>
          </div>

          <!-- Cover -->
          <div v-if="article.cover_image" class="rounded-xl overflow-hidden mb-8">
            <img :src="article.cover_image" :alt="article.title" class="w-full" />
          </div>

          <!-- Body -->
          <ArticleContent :html="html" />
        </article>

        <!-- TOC sidebar -->
        <aside v-if="toc.length" class="hidden xl:block w-56 shrink-0">
          <div class="sticky top-24">
            <ArticleToc :items="toc" />
          </div>
        </aside>
      </div>
    </main>
    <AppFooter />
  </div>
</template>
