<script setup lang="ts">
import { RouterLink } from 'vue-router'
import type { ArticleListItem } from '@/types/article'
import { formatDate } from '@/utils/date'

defineProps<{ article: ArticleListItem }>()
</script>

<template>
  <RouterLink :to="{ name: 'article-detail', params: { slug: article.slug } }" class="block group">
    <article class="card-hover p-6 h-full flex flex-col gap-4">
      <!-- Cover -->
      <div v-if="article.cover_image" class="aspect-video rounded-lg overflow-hidden bg-bg">
        <img :src="article.cover_image" :alt="article.title" class="w-full h-full object-cover group-hover:scale-105 transition-transform duration-300" />
      </div>

      <!-- Tags -->
      <div v-if="article.tags.length" class="flex flex-wrap gap-1.5">
        <span
          v-for="tag in article.tags.slice(0, 3)"
          :key="tag.id"
          class="badge-primary text-xs"
        >
          {{ tag.name }}
        </span>
      </div>

      <!-- Title -->
      <h2 class="text-lg font-semibold text-title group-hover:text-primary transition-colors line-clamp-2 leading-snug">
        {{ article.title }}
      </h2>

      <!-- Summary -->
      <p v-if="article.summary" class="text-sm text-body line-clamp-2 flex-1">
        {{ article.summary }}
      </p>

      <!-- Meta -->
      <div class="flex items-center gap-3 text-xs text-muted mt-auto pt-2 border-t border-border/60">
        <span>{{ formatDate(article.published_at || article.created_at) }}</span>
        <span>·</span>
        <span>{{ article.read_time }} 分钟阅读</span>
        <span>·</span>
        <span>{{ article.view_count }} 次阅读</span>
      </div>
    </article>
  </RouterLink>
</template>
