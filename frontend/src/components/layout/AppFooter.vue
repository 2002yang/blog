<script setup lang="ts">
import { RouterLink } from 'vue-router'
</script>

<template>
  <footer class="border-t border-border mt-20">
    <div class="page-container py-12">
      <div class="flex flex-col md:flex-row items-center justify-between gap-4">
        <div class="flex items-center gap-2 text-title font-semibold">
          <span class="w-6 h-6 rounded-md bg-primary flex items-center justify-center text-white text-xs font-bold">D</span>
          DevBlog
        </div>
        <nav class="flex items-center gap-6 text-sm text-muted">
          <RouterLink to="/articles" class="hover:text-primary transition-colors">文章</RouterLink>
          <RouterLink to="/tags" class="hover:text-primary transition-colors">标签</RouterLink>
          <RouterLink to="/search" class="hover:text-primary transition-colors">搜索</RouterLink>
        </nav>
        <p class="text-sm text-muted">© {{ new Date().getFullYear() }} DevBlog. Built with Vue3 + FastAPI.</p>
      </div>
    </div>
  </footer>
</template>
