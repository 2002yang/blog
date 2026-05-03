<script setup lang="ts">
import { ref, onMounted, onUnmounted } from 'vue'
import { RouterLink, useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth'
import AppSearch from '@/components/common/AppSearch.vue'

const auth = useAuthStore()
const router = useRouter()
const scrolled = ref(false)
const mobileOpen = ref(false)

function onScroll() {
  scrolled.value = window.scrollY > 10
}

onMounted(() => window.addEventListener('scroll', onScroll))
onUnmounted(() => window.removeEventListener('scroll', onScroll))

async function handleLogout() {
  await auth.logout()
  router.push({ name: 'home' })
}
</script>

<template>
  <header
    class="sticky top-0 z-40 transition-all duration-200"
    :class="scrolled ? 'bg-white/90 backdrop-blur-md shadow-card border-b border-border/60' : 'bg-transparent'"
  >
    <div class="page-container">
      <div class="flex items-center h-16 gap-6">
        <!-- Logo -->
        <RouterLink to="/" class="flex items-center gap-2 font-bold text-title text-lg shrink-0">
          <span class="w-7 h-7 rounded-lg bg-primary flex items-center justify-center text-white text-sm font-bold">D</span>
          DevBlog
        </RouterLink>

        <!-- Nav -->
        <nav class="hidden md:flex items-center gap-1 ml-2">
          <RouterLink to="/articles" class="btn-ghost text-sm" active-class="text-primary bg-primary-light">文章</RouterLink>
          <RouterLink to="/tags" class="btn-ghost text-sm" active-class="text-primary bg-primary-light">标签</RouterLink>
        </nav>

        <div class="flex-1" />

        <!-- Right -->
        <div class="hidden md:flex items-center gap-3">
          <AppSearch />
          <template v-if="auth.isAuthenticated">
            <RouterLink v-if="auth.isAdmin" to="/admin" class="btn-secondary text-sm">后台</RouterLink>
            <button class="btn-ghost text-sm" @click="handleLogout">退出</button>
          </template>
          <RouterLink v-else to="/login" class="btn-primary text-sm">登录</RouterLink>
        </div>

        <!-- Mobile toggle -->
        <button class="md:hidden btn-ghost p-2" @click="mobileOpen = !mobileOpen">
          <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path v-if="!mobileOpen" stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 6h16M4 12h16M4 18h16" />
            <path v-else stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
          </svg>
        </button>
      </div>
    </div>

    <!-- Mobile menu -->
    <Transition
      enter-active-class="transition-all duration-200"
      enter-from-class="opacity-0 -translate-y-2"
      enter-to-class="opacity-100 translate-y-0"
      leave-active-class="transition-all duration-150"
      leave-from-class="opacity-100"
      leave-to-class="opacity-0"
    >
      <div v-if="mobileOpen" class="md:hidden bg-white border-t border-border px-4 py-4 space-y-2">
        <RouterLink to="/articles" class="block py-2 text-sm text-body hover:text-primary" @click="mobileOpen = false">文章</RouterLink>
        <RouterLink to="/tags" class="block py-2 text-sm text-body hover:text-primary" @click="mobileOpen = false">标签</RouterLink>
        <RouterLink to="/search" class="block py-2 text-sm text-body hover:text-primary" @click="mobileOpen = false">搜索</RouterLink>
        <div class="pt-2 border-t border-border">
          <template v-if="auth.isAuthenticated">
            <RouterLink v-if="auth.isAdmin" to="/admin" class="block py-2 text-sm text-primary font-medium" @click="mobileOpen = false">后台管理</RouterLink>
            <button class="block py-2 text-sm text-body" @click="handleLogout; mobileOpen = false">退出登录</button>
          </template>
          <RouterLink v-else to="/login" class="block py-2 text-sm text-primary font-medium" @click="mobileOpen = false">登录</RouterLink>
        </div>
      </div>
    </Transition>
  </header>
</template>
