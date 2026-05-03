<script setup lang="ts">
defineProps<{
  lines?: number
  class?: string
}>()
</script>

<template>
  <div class="animate-pulse space-y-3" :class="$props.class">
    <div v-for="i in (lines ?? 3)" :key="i" class="h-4 bg-border rounded-full" :style="{ width: i === (lines ?? 3) ? '60%' : '100%' }" />
  </div>
</template>
