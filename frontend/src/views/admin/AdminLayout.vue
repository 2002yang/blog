<script setup lang="ts">
import { RouterView, RouterLink, useRoute } from 'vue-router'
import { useAuthStore } from '@/stores/auth'
import { useRouter } from 'vue-router'

const auth = useAuthStore()
const router = useRouter()
const route = useRoute()

async function logout() {
  await auth.logout()
  router.push({ name: 'home' })
}

const navItems = [
  { name: 'admin-dashboard', label: '概览', icon: '◈' },
  { name: 'admin-articles', label: '文章', icon: '◉' },
]
</script>

<template>
  <div class="min-h-screen bg-bg flex">
    <!-- Sidebar -->
    <aside class="w-56 shrink-0 bg-card border-r border-border flex flex-col">
      <div class="p-5 border-b border-border">
        <RouterLink to="/" class="flex items-center gap-2 font-bold text-title">
          <span class="w-7 h-7 rounded-lg bg-primary flex items-center justify-center text-white text-sm font-bold">D</span>
          DevBlog
        </RouterLink>
      </div>

      <nav class="flex-1 p-3 space-y-1">
        <RouterLink
          v-for="item in navItems"
          :key="item.name"
          :to="{ name: item.name }"
          class="flex items-center gap-3 px-3 py-2 rounded-lg text-sm font-medium transition-colors"
          :class="route.name === item.name ? 'bg-primary-light text-primary' : 'text-body hover:bg-bg'"
        >
          <span>{{ item.icon }}</span>
          {{ item.label }}
        </RouterLink>
      </nav>

      <div class="p-3 border-t border-border">
        <div class="flex items-center gap-3 px-3 py-2 mb-1">
          <div class="w-7 h-7 rounded-full bg-primary-light flex items-center justify-center text-primary text-xs font-bold">
            {{ auth.user?.username?.[0]?.toUpperCase() }}
          </div>
          <span class="text-sm font-medium text-title truncate">{{ auth.user?.username }}</span>
        </div>
        <button class="w-full flex items-center gap-3 px-3 py-2 rounded-lg text-sm text-muted hover:bg-bg hover:text-body transition-colors" @click="logout">
          ↩ 退出登录
        </button>
      </div>
    </aside>

    <!-- Content -->
    <div class="flex-1 min-w-0 overflow-auto">
      <RouterView />
    </div>
  </div>
</template>
