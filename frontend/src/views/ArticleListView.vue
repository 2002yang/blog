<script setup lang="ts">
import { ref, watch, onMounted, computed } from 'vue'
import { useRoute, RouterLink } from 'vue-router'
import AppHeader from '@/components/layout/AppHeader.vue'
import AppFooter from '@/components/layout/AppFooter.vue'
import ArticleCard from '@/components/article/ArticleCard.vue'
import AppPagination from '@/components/common/AppPagination.vue'
import AppSkeleton from '@/components/common/AppSkeleton.vue'
import { articlesApi } from '@/api/articles'
import { tagsApi } from '@/api/tags'
import type { ArticleListItem, PaginatedArticles } from '@/types/article'
import type { Tag } from '@/types/tag'
import { useHead } from '@vueuse/head'

const route = useRoute()
const tagSlug = computed(() => route.params.slug as string | undefined)
const page = ref(1)
const data = ref<PaginatedArticles | null>(null)
const currentTag = ref<Tag | null>(null)
const tags = ref<Tag[]>([])
const loading = ref(true)

useHead(computed(() => ({
  title: currentTag.value ? `${currentTag.value.name} — DevBlog` : '文章列表 — DevBlog',
})))

async function fetchData() {
  loading.value = true
  try {
    const [articlesRes, tagsRes] = await Promise.all([
      articlesApi.list({ page: page.value, size: 9, tag: tagSlug.value }),
      tagsApi.list(),
    ])
    data.value = articlesRes.data
    tags.value = tagsRes.data
    if (tagSlug.value) {
      currentTag.value = tags.value.find((t) => t.slug === tagSlug.value) ?? null
    } else {
      currentTag.value = null
    }
  } finally {
    loading.value = false
  }
}

onMounted(fetchData)
watch([() => route.params.slug, page], fetchData)

function onPageChange(p: number) {
  page.value = p
  window.scrollTo({ top: 0, behavior: 'smooth' })
}
</script>

<template>
  <div class="min-h-screen flex flex-col">
    <AppHeader />
    <main class="flex-1 page-container py-12">
      <div class="flex flex-col lg:flex-row gap-10">
        <!-- Main -->
        <div class="flex-1 min-w-0">
          <div class="mb-8">
            <h1 class="section-title">
              <template v-if="currentTag">
                <span class="text-primary">#{{ currentTag.name }}</span> 文章
              </template>
              <template v-else>全部文章</template>
            </h1>
            <p v-if="data" class="text-sm text-muted mt-1">共 {{ data.total }} 篇</p>
          </div>

          <div v-if="loading" class="grid grid-cols-1 md:grid-cols-2 gap-5">
            <div v-for="i in 6" :key="i" class="card p-6"><AppSkeleton :lines="5" /></div>
          </div>
          <div v-else-if="data?.items.length" class="grid grid-cols-1 md:grid-cols-2 gap-5">
            <ArticleCard v-for="a in data.items" :key="a.id" :article="a" />
          </div>
          <div v-else class="text-center py-20 text-muted">暂无文章</div>

          <div class="mt-10">
            <AppPagination v-if="data" :total="data.total" :page="page" :size="9" @change="onPageChange" />
          </div>
        </div>

        <!-- Sidebar -->
        <aside class="lg:w-60 shrink-0">
          <div class="card p-5 sticky top-24">
            <h3 class="text-sm font-semibold text-title mb-4">标签</h3>
            <div class="flex flex-wrap gap-2">
              <RouterLink
                to="/articles"
                class="badge text-xs transition-colors"
                :class="!tagSlug ? 'bg-primary text-white' : 'bg-bg text-body hover:bg-primary-light hover:text-primary'"
              >
                全部
              </RouterLink>
              <RouterLink
                v-for="tag in tags"
                :key="tag.id"
                :to="{ name: 'tag-articles', params: { slug: tag.slug } }"
                class="badge text-xs transition-colors"
                :class="tagSlug === tag.slug ? 'bg-primary text-white' : 'bg-bg text-body hover:bg-primary-light hover:text-primary'"
              >
                {{ tag.name }}
                <span v-if="tag.article_count" class="ml-1 opacity-70">{{ tag.article_count }}</span>
              </RouterLink>
            </div>
          </div>
        </aside>
      </div>
    </main>
    <AppFooter />
  </div>
</template>
