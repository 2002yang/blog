<script setup lang="ts">
import { onMounted, ref } from 'vue'
import type { TocItem } from '@/utils/markdown'

const props = defineProps<{ items: TocItem[] }>()
const activeId = ref('')

onMounted(() => {
  const observer = new IntersectionObserver(
    (entries) => {
      for (const entry of entries) {
        if (entry.isIntersecting) {
          activeId.value = entry.target.id
        }
      }
    },
    { rootMargin: '-80px 0px -60% 0px' },
  )
  props.items.forEach(({ id }) => {
    const el = document.getElementById(id)
    if (el) observer.observe(el)
  })
  return () => observer.disconnect()
})
</script>

<template>
  <nav v-if="items.length" class="space-y-1">
    <p class="text-xs font-semibold text-muted uppercase tracking-wider mb-3">目录</p>
    <a
      v-for="item in items"
      :key="item.id"
      :href="`#${item.id}`"
      class="block text-sm py-1 transition-colors truncate"
      :class="{
        'pl-0': item.level === 1,
        'pl-3': item.level === 2,
        'pl-6': item.level === 3,
        'pl-9': item.level === 4,
        'text-primary font-medium': activeId === item.id,
        'text-muted hover:text-body': activeId !== item.id,
      }"
    >
      {{ item.text }}
    </a>
  </nav>
</template>
