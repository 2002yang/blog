<script setup lang="ts">
import { computed } from 'vue'

const props = withDefaults(defineProps<{
  total: number
  page: number
  size?: number
}>(), { size: 10 })

const emit = defineEmits<{ (e: 'change', page: number): void }>()

const pages = computed(() => Math.ceil(props.total / props.size))

const visiblePages = computed(() => {
  const p = props.page
  const last = pages.value
  if (last <= 7) return Array.from({ length: last }, (_, i) => i + 1)
  if (p <= 4) return [1, 2, 3, 4, 5, '...', last]
  if (p >= last - 3) return [1, '...', last - 4, last - 3, last - 2, last - 1, last]
  return [1, '...', p - 1, p, p + 1, '...', last]
})
</script>

<template>
  <div v-if="pages > 1" class="flex items-center justify-center gap-1">
    <button
      class="btn-ghost px-2 py-1.5 disabled:opacity-40 disabled:cursor-not-allowed"
      :disabled="page <= 1"
      @click="emit('change', page - 1)"
    >
      ←
    </button>
    <template v-for="p in visiblePages" :key="p">
      <span v-if="p === '...'" class="px-2 text-muted">…</span>
      <button
        v-else
        class="w-9 h-9 rounded-lg text-sm font-medium transition-colors"
        :class="p === page ? 'bg-primary text-white' : 'text-body hover:bg-bg'"
        @click="emit('change', p as number)"
      >
        {{ p }}
      </button>
    </template>
    <button
      class="btn-ghost px-2 py-1.5 disabled:opacity-40 disabled:cursor-not-allowed"
      :disabled="page >= pages"
      @click="emit('change', page + 1)"
    >
      →
    </button>
  </div>
</template>
