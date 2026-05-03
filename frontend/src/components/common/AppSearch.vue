<script setup lang="ts">
import { ref } from 'vue'
import { useRouter } from 'vue-router'

const router = useRouter()
const query = ref('')

function submit() {
  if (query.value.trim()) {
    router.push({ name: 'search', query: { q: query.value.trim() } })
    query.value = ''
  }
}
</script>

<template>
  <form class="relative" @submit.prevent="submit">
    <input
      v-model="query"
      type="search"
      placeholder="搜索文章..."
      class="input pl-9 pr-4 py-2 w-full sm:w-56 text-sm"
    />
    <svg class="absolute left-2.5 top-1/2 -translate-y-1/2 w-4 h-4 text-muted" fill="none" stroke="currentColor" viewBox="0 0 24 24">
      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" />
    </svg>
  </form>
</template>
