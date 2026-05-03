<script setup lang="ts">
import { RouterLink } from 'vue-router'
import { useHead } from '@vueuse/head'

useHead({ title: '404 — DevBlog' })
</script>

<template>
  <div class="min-h-screen bg-bg flex flex-col items-center justify-center text-center px-4">
    <div class="text-8xl font-bold text-border mb-4">404</div>
    <h1 class="text-2xl font-bold text-title mb-2">页面不存在</h1>
    <p class="text-muted mb-8">你访问的页面已被删除或从未存在过</p>
    <RouterLink to="/" class="btn-primary">返回首页</RouterLink>
  </div>
</template>
