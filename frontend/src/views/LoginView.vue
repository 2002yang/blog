<script setup lang="ts">
import { ref } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { useAuthStore } from '@/stores/auth'
import { useUiStore } from '@/stores/ui'
import { useHead } from '@vueuse/head'

useHead({ title: '登录 — DevBlog' })

const auth = useAuthStore()
const ui = useUiStore()
const router = useRouter()
const route = useRoute()

const form = ref({ username: '', password: '' })
const loading = ref(false)

async function submit() {
  if (!form.value.username || !form.value.password) return
  loading.value = true
  try {
    await auth.login(form.value.username, form.value.password)
    const redirect = (route.query.redirect as string) || (auth.isAdmin ? '/admin' : '/')
    router.push(redirect)
  } catch {
    ui.toast.error('用户名或密码错误')
  } finally {
    loading.value = false
  }
}
</script>

<template>
  <div class="min-h-screen bg-bg flex items-center justify-center px-4">
    <div class="w-full max-w-sm">
      <div class="text-center mb-8">
        <div class="inline-flex w-12 h-12 rounded-2xl bg-primary items-center justify-center text-white text-xl font-bold mb-4">D</div>
        <h1 class="text-2xl font-bold text-title">欢迎回来</h1>
        <p class="text-muted text-sm mt-1">登录到 DevBlog 后台</p>
      </div>

      <form class="card p-6 space-y-4" @submit.prevent="submit">
        <div>
          <label class="block text-sm font-medium text-title mb-1.5">用户名</label>
          <input v-model="form.username" type="text" class="input" placeholder="输入用户名" autocomplete="username" required />
        </div>
        <div>
          <label class="block text-sm font-medium text-title mb-1.5">密码</label>
          <input v-model="form.password" type="password" class="input" placeholder="输入密码" autocomplete="current-password" required />
        </div>
        <button type="submit" class="btn-primary w-full justify-center py-2.5" :disabled="loading">
          <svg v-if="loading" class="w-4 h-4 animate-spin" fill="none" viewBox="0 0 24 24">
            <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4" />
            <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4z" />
          </svg>
          {{ loading ? '登录中...' : '登录' }}
        </button>
      </form>
    </div>
  </div>
</template>
