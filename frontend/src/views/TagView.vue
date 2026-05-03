<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { RouterLink } from 'vue-router'
import AppHeader from '@/components/layout/AppHeader.vue'
import AppFooter from '@/components/layout/AppFooter.vue'
import { tagsApi } from '@/api/tags'
import type { Tag } from '@/types/tag'
import { useHead } from '@vueuse/head'

useHead({ title: '标签 — DevBlog' })

const tags = ref<Tag[]>([])
const loading = ref(true)

onMounted(async () => {
  try {
    const { data } = await tagsApi.list()
    tags.value = data
  } finally {
    loading.value = false
  }
})
</script>

<template>
  <div class="min-h-screen flex flex-col">
    <AppHeader />
    <main class="flex-1 page-container py-12">
      <h1 class="section-title mb-2">标签</h1>
      <p class="text-muted mb-10">按主题浏览文章</p>

      <div v-if="loading" class="flex flex-wrap gap-3">
        <div v-for="i in 12" :key="i" class="h-9 w-20 bg-border rounded-full animate-pulse" />
      </div>
      <div v-else class="flex flex-wrap gap-3">
        <RouterLink
          v-for="tag in tags"
          :key="tag.id"
          :to="{ name: 'tag-articles', params: { slug: tag.slug } }"
          class="flex items-center gap-2 px-4 py-2 rounded-full border border-border bg-card hover:border-primary hover:text-primary hover:bg-primary-light transition-all text-sm font-medium text-body"
        >
          <span class="w-2 h-2 rounded-full" :style="{ backgroundColor: tag.color }" />
          {{ tag.name }}
          <span v-if="tag.article_count" class="text-xs text-muted">({{ tag.article_count }})</span>
        </RouterLink>
      </div>
    </main>
    <AppFooter />
  </div>
</template>
