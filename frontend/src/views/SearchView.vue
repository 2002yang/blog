<script setup lang="ts">
import { ref, watch, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import AppHeader from '@/components/layout/AppHeader.vue'
import AppFooter from '@/components/layout/AppFooter.vue'
import ArticleCard from '@/components/article/ArticleCard.vue'
import AppPagination from '@/components/common/AppPagination.vue'
import AppSkeleton from '@/components/common/AppSkeleton.vue'
import { articlesApi } from '@/api/articles'
import type { PaginatedArticles } from '@/types/article'
import { useHead } from '@vueuse/head'

useHead({ title: '搜索 — DevBlog' })

const route = useRoute()
const router = useRouter()
const query = ref((route.query.q as string) ?? '')
const inputVal = ref(query.value)
const page = ref(1)
const data = ref<PaginatedArticles | null>(null)
const loading = ref(false)
const searched = ref(false)

async function doSearch() {
  if (!query.value.trim()) return
  loading.value = true
  searched.value = true
  try {
    const { data: res } = await articlesApi.search(query.value, page.value)
    data.value = res
  } finally {
    loading.value = false
  }
}

function submit() {
  query.value = inputVal.value.trim()
  page.value = 1
  router.replace({ query: { q: query.value } })
}

onMounted(() => { if (query.value) doSearch() })
watch([query, page], doSearch)
watch(() => route.query.q, (q) => {
  query.value = (q as string) ?? ''
  inputVal.value = query.value
})
</script>

<template>
  <div class="min-h-screen flex flex-col">
    <AppHeader />
    <main class="flex-1 page-container py-12">
      <h1 class="section-title mb-8">搜索</h1>

      <form class="relative max-w-xl mb-10" @submit.prevent="submit">
        <input
          v-model="inputVal"
          type="search"
          placeholder="输入关键词搜索文章..."
          class="input pl-11 pr-4 py-3 text-base"
          autofocus
        />
        <svg class="absolute left-3.5 top-1/2 -translate-y-1/2 w-5 h-5 text-muted" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" />
        </svg>
      </form>

      <div v-if="loading" class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-5">
        <div v-for="i in 6" :key="i" class="card p-6"><AppSkeleton :lines="5" /></div>
      </div>
      <template v-else-if="searched">
        <p class="text-sm text-muted mb-6">
          找到 <span class="text-title font-medium">{{ data?.total ?? 0 }}</span> 篇关于 "<span class="text-primary">{{ query }}</span>" 的文章
        </p>
        <div v-if="data?.items.length" class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-5">
          <ArticleCard v-for="a in data.items" :key="a.id" :article="a" />
        </div>
        <div v-else class="text-center py-16 text-muted">未找到相关文章</div>
        <div class="mt-10">
          <AppPagination v-if="data" :total="data.total" :page="page" :size="9" @change="(p) => { page = p }" />
        </div>
      </template>
    </main>
    <AppFooter />
  </div>
</template>
