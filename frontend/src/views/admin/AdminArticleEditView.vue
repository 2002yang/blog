<script setup lang="ts">
import { ref, onMounted, computed } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import MarkdownEditor from '@/components/editor/MarkdownEditor.vue'
import ImageUploader from '@/components/editor/ImageUploader.vue'
import { articlesApi } from '@/api/articles'
import { tagsApi } from '@/api/tags'
import { useUiStore } from '@/stores/ui'
import type { Tag } from '@/types/tag'
import type { Article } from '@/types/article'
import { useHead } from '@vueuse/head'

const route = useRoute()
const router = useRouter()
const ui = useUiStore()

const isEdit = computed(() => !!route.params.id)
useHead(computed(() => ({ title: isEdit.value ? '编辑文章 — DevBlog' : '新建文章 — DevBlog' })))

const article = ref<Article | null>(null)
const allTags = ref<Tag[]>([])
const saving = ref(false)
const publishing = ref(false)

const form = ref({
  title: '',
  slug: '',
  summary: '',
  content: '',
  cover_image: '',
  is_featured: false,
  tag_ids: [] as number[],
  status: 'draft' as 'draft' | 'published',
})

function autoSlug(title: string) {
  return title.toLowerCase().replace(/[\s一-龥]+/g, '-').replace(/[^\w-]/g, '').replace(/^-|-$/g, '').slice(0, 80)
}

onMounted(async () => {
  const [tagsRes] = await Promise.all([tagsApi.list()])
  allTags.value = tagsRes.data

  if (isEdit.value) {
    const { data } = await articlesApi.adminList({ page: 1, size: 100 })
    const found = data.items.find((a) => a.id === Number(route.params.id))
    if (found) {
      const { data: full } = await articlesApi.getBySlug(found.slug)
      article.value = full
      form.value = {
        title: full.title,
        slug: full.slug,
        summary: full.summary ?? '',
        content: full.content,
        cover_image: full.cover_image ?? '',
        is_featured: full.is_featured,
        tag_ids: full.tags.map((t) => t.id),
        status: full.status,
      }
    }
  } else {
    const saved = localStorage.getItem('editor_autosave')
    if (saved) form.value.content = saved
  }
})

function toggleTag(id: number) {
  const idx = form.value.tag_ids.indexOf(id)
  if (idx === -1) form.value.tag_ids.push(id)
  else form.value.tag_ids.splice(idx, 1)
}

async function save(status?: 'draft' | 'published') {
  if (!form.value.title.trim()) { ui.toast.error('请输入文章标题'); return }
  if (!form.value.slug) form.value.slug = autoSlug(form.value.title)

  const payload = { ...form.value, status: status ?? form.value.status }
  if (status) publishing.value = true
  else saving.value = true

  try {
    if (isEdit.value && article.value) {
      await articlesApi.update(article.value.id, payload)
    } else {
      const { data } = await articlesApi.create(payload)
      localStorage.removeItem('editor_autosave')
      router.replace({ name: 'admin-article-edit', params: { id: data.id } })
    }
    form.value.status = payload.status
    ui.toast.success(status === 'published' ? '已发布' : '已保存')
  } catch {
    ui.toast.error('保存失败')
  } finally {
    saving.value = false
    publishing.value = false
  }
}

function onImageUploaded(url: string) {
  form.value.content += `\n\n![图片](${url})\n`
}
</script>

<template>
  <div class="flex flex-col h-screen">
    <!-- Top bar -->
    <div class="flex items-center gap-4 px-6 py-3 border-b border-border bg-card shrink-0">
      <input
        v-model="form.title"
        type="text"
        placeholder="文章标题..."
        class="flex-1 text-xl font-bold text-title bg-transparent outline-none placeholder:text-muted"
        @blur="() => { if (!form.slug) form.slug = autoSlug(form.title) }"
      />
      <span class="badge text-xs" :class="form.status === 'published' ? 'bg-green-50 text-green-700' : 'bg-yellow-50 text-yellow-700'">
        {{ form.status === 'published' ? '已发布' : '草稿' }}
      </span>
      <button class="btn-secondary text-sm" :disabled="saving" @click="save()">
        {{ saving ? '保存中...' : '保存草稿' }}
      </button>
      <button class="btn-primary text-sm" :disabled="publishing" @click="save('published')">
        {{ publishing ? '发布中...' : (form.status === 'published' ? '更新' : '发布') }}
      </button>
    </div>

    <div class="flex flex-1 min-h-0">
      <!-- Editor -->
      <div class="flex-1 min-w-0 p-4">
        <MarkdownEditor v-model="form.content" class="h-full" @image-uploaded="onImageUploaded" />
      </div>

      <!-- Sidebar -->
      <aside class="w-72 shrink-0 border-l border-border overflow-y-auto p-5 space-y-6">
        <!-- Slug -->
        <div>
          <label class="block text-xs font-semibold text-muted uppercase tracking-wider mb-2">URL Slug</label>
          <input v-model="form.slug" type="text" class="input text-sm" placeholder="auto-generated" />
        </div>

        <!-- Summary -->
        <div>
          <label class="block text-xs font-semibold text-muted uppercase tracking-wider mb-2">摘要</label>
          <textarea v-model="form.summary" rows="3" class="input text-sm resize-none" placeholder="文章简介..." />
        </div>

        <!-- Tags -->
        <div>
          <label class="block text-xs font-semibold text-muted uppercase tracking-wider mb-2">标签</label>
          <div class="flex flex-wrap gap-2">
            <button
              v-for="tag in allTags"
              :key="tag.id"
              type="button"
              class="badge text-xs transition-colors cursor-pointer"
              :class="form.tag_ids.includes(tag.id) ? 'bg-primary text-white' : 'bg-bg text-body hover:bg-primary-light hover:text-primary'"
              @click="toggleTag(tag.id)"
            >
              {{ tag.name }}
            </button>
          </div>
        </div>

        <!-- Cover image -->
        <div>
          <label class="block text-xs font-semibold text-muted uppercase tracking-wider mb-2">封面图片</label>
          <input v-model="form.cover_image" type="text" class="input text-sm mb-3" placeholder="图片 URL" />
          <ImageUploader @uploaded="(url) => form.cover_image = url" />
          <div v-if="form.cover_image" class="mt-3 rounded-lg overflow-hidden">
            <img :src="form.cover_image" alt="封面预览" class="w-full h-32 object-cover" />
          </div>
        </div>

        <!-- Featured -->
        <div class="flex items-center justify-between">
          <label class="text-sm font-medium text-title">精选文章</label>
          <button
            type="button"
            class="relative inline-flex h-5 w-9 rounded-full transition-colors"
            :class="form.is_featured ? 'bg-primary' : 'bg-border'"
            @click="form.is_featured = !form.is_featured"
          >
            <span
              class="inline-block w-4 h-4 rounded-full bg-white shadow transform transition-transform mt-0.5"
              :class="form.is_featured ? 'translate-x-4' : 'translate-x-0.5'"
            />
          </button>
        </div>
      </aside>
    </div>
  </div>
</template>
