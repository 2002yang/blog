<script setup lang="ts">
import { ref } from 'vue'
import { uploadApi } from '@/api/upload'
import { useUiStore } from '@/stores/ui'

const emit = defineEmits<{ (e: 'uploaded', url: string): void }>()
const ui = useUiStore()
const uploading = ref(false)
const fileInput = ref<HTMLInputElement>()

async function handleFile(file: File) {
  if (!file.type.startsWith('image/')) {
    ui.toast.error('只支持图片文件')
    return
  }
  if (file.size > 5 * 1024 * 1024) {
    ui.toast.error('图片大小不能超过 5MB')
    return
  }
  uploading.value = true
  try {
    const { data } = await uploadApi.image(file)
    emit('uploaded', data.url)
    ui.toast.success('图片上传成功')
  } catch {
    ui.toast.error('上传失败，请重试')
  } finally {
    uploading.value = false
  }
}

function onFileChange(e: Event) {
  const file = (e.target as HTMLInputElement).files?.[0]
  if (file) handleFile(file)
}

function onDrop(e: DragEvent) {
  e.preventDefault()
  const file = e.dataTransfer?.files?.[0]
  if (file) handleFile(file)
}
</script>

<template>
  <div
    class="border-2 border-dashed border-border rounded-xl p-6 text-center cursor-pointer hover:border-primary hover:bg-primary-light/30 transition-colors"
    :class="{ 'opacity-60 pointer-events-none': uploading }"
    @click="fileInput?.click()"
    @dragover.prevent
    @drop="onDrop"
  >
    <input ref="fileInput" type="file" accept="image/*" class="hidden" @change="onFileChange" />
    <div v-if="uploading" class="flex items-center justify-center gap-2 text-primary">
      <svg class="w-5 h-5 animate-spin" fill="none" viewBox="0 0 24 24">
        <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4" />
        <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4z" />
      </svg>
      上传中...
    </div>
    <div v-else class="text-muted text-sm">
      <p class="font-medium text-body mb-1">点击或拖拽上传图片</p>
      <p>支持 JPG、PNG、WebP、GIF，最大 5MB</p>
    </div>
  </div>
</template>
