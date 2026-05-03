<script setup lang="ts">
import { RouterLink } from 'vue-router'
import type { ArticleListItem } from '@/types/article'
import { formatDate } from '@/utils/date'

defineProps<{ article: ArticleListItem }>()
</script>

<template>
  <RouterLink :to="{ name: 'article-detail', params: { slug: article.slug } }" class="block group">
    <article class="card-hover p-6 md:p-8 flex flex-col md:flex-row gap-6">
      <!-- Cover -->
      <div v-if="article.cover_image" class="md:w-72 md:shrink-0 aspect-video md:aspect-auto rounded-xl overflow-hidden bg-bg">
        <img :src="article.cover_image" :alt="article.title" class="w-full h-full object-cover group-hover:scale-105 transition-transform duration-300" />
      </div>

      <div class="flex flex-col gap-3 flex-1 min-w-0">
        <!-- Featured badge + tags -->
        <div class="flex flex-wrap items-center gap-2">
          <span class="badge bg-primary text-white text-xs">精选</span>
          <span
            v-for="tag in article.tags.slice(0, 3)"
            :key="tag.id"
            class="badge-primary text-xs"
          >
            {{ tag.name }}
          </span>
        </div>

        <h2 class="text-xl md:text-2xl font-bold text-title group-hover:text-primary transition-colors line-clamp-2 leading-snug">
          {{ article.title }}
        </h2>

        <p v-if="article.summary" class="text-body line-clamp-3 flex-1">
          {{ article.summary }}
        </p>

        <div class="flex items-center gap-3 text-sm text-muted mt-auto">
          <span>{{ formatDate(article.published_at || article.created_at) }}</span>
          <span>·</span>
          <span>{{ article.read_time }} 分钟阅读</span>
        </div>
      </div>
    </article>
  </RouterLink>
</template>
