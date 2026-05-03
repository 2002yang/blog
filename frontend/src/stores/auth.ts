import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import { authApi } from '@/api/auth'
import type { User } from '@/types/auth'

export const useAuthStore = defineStore('auth', () => {
  const user = ref<User | null>(null)
  const accessToken = ref<string | null>(null)
  const loading = ref(false)

  const isAuthenticated = computed(() => !!accessToken.value && !!user.value)
  const isAdmin = computed(() => user.value?.is_admin ?? false)

  function setAccessToken(token: string) {
    accessToken.value = token
  }

  async function login(username: string, password: string) {
    loading.value = true
    try {
      const { data } = await authApi.login({ username, password })
      accessToken.value = data.access_token
      user.value = data.user
      return data
    } finally {
      loading.value = false
    }
  }

  async function fetchMe() {
    try {
      const { data } = await authApi.me()
      user.value = data
    } catch {
      user.value = null
      accessToken.value = null
    }
  }

  async function restoreSession() {
    try {
      const { data } = await authApi.refresh()
      accessToken.value = data.access_token
      await fetchMe()
    } catch {
      // no valid session
    }
  }

  async function logout() {
    try {
      await authApi.logout()
    } catch {
      // ignore
    } finally {
      user.value = null
      accessToken.value = null
    }
  }

  return { user, accessToken, loading, isAuthenticated, isAdmin, setAccessToken, login, fetchMe, restoreSession, logout }
})
