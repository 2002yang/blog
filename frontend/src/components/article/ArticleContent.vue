<script setup lang="ts">
defineProps<{ html: string }>()
</script>

<template>
  <div class="prose prose-base max-w-none" v-html="html" />
</template>
