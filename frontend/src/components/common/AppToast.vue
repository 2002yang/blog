<script setup lang="ts">
import { useUiStore, type Toast } from '@/stores/ui'
import { TransitionGroup } from 'vue'

const ui = useUiStore()

const icons: Record<Toast['type'], string> = {
  success: '✓',
  error: '✕',
  info: 'ℹ',
  warning: '⚠',
}

const colors: Record<Toast['type'], string> = {
  success: 'bg-green-50 border-green-200 text-green-800',
  error: 'bg-red-50 border-red-200 text-red-800',
  info: 'bg-blue-50 border-blue-200 text-blue-800',
  warning: 'bg-yellow-50 border-yellow-200 text-yellow-800',
}
</script>

<template>
  <div class="fixed bottom-6 right-6 z-50 flex flex-col gap-2 pointer-events-none">
    <TransitionGroup
      enter-active-class="transition-all duration-300 ease-out"
      enter-from-class="opacity-0 translate-y-2 scale-95"
      enter-to-class="opacity-100 translate-y-0 scale-100"
      leave-active-class="transition-all duration-200 ease-in"
      leave-from-class="opacity-100"
      leave-to-class="opacity-0 scale-95"
    >
      <div
        v-for="toast in ui.toasts"
        :key="toast.id"
        class="pointer-events-auto flex items-center gap-3 px-4 py-3 rounded-xl border shadow-card-lg text-sm font-medium min-w-64 max-w-sm"
        :class="colors[toast.type]"
      >
        <span class="text-base leading-none">{{ icons[toast.type] }}</span>
        <span>{{ toast.message }}</span>
        <button class="ml-auto opacity-60 hover:opacity-100" @click="ui.removeToast(toast.id)">✕</button>
      </div>
    </TransitionGroup>
  </div>
</template>
