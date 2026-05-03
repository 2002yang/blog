import { defineStore } from 'pinia'
import { ref } from 'vue'
import { tagsApi } from '@/api/tags'
import type { Tag } from '@/types/tag'

export const useTagsStore = defineStore('tags', () => {
  const tags = ref<Tag[]>([])
  const loading = ref(false)

  async function fetchTags() {
    if (tags.value.length > 0) return
    loading.value = true
    try {
      const { data } = await tagsApi.list()
      tags.value = data
    } finally {
      loading.value = false
    }
  }

  function invalidate() {
    tags.value = []
  }

  return { tags, loading, fetchTags, invalidate }
})
