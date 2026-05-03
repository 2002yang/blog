<script setup lang="ts">
import { ref, onMounted, onUnmounted, watch } from 'vue'
import { EditorView, keymap, lineNumbers, highlightActiveLine } from '@codemirror/view'
import { EditorState } from '@codemirror/state'
import { markdown } from '@codemirror/lang-markdown'
import { oneDark } from '@codemirror/theme-one-dark'
import { defaultKeymap, history, historyKeymap } from '@codemirror/commands'
import { renderMarkdown } from '@/utils/markdown'

const props = defineProps<{ modelValue: string }>()
const emit = defineEmits<{ (e: 'update:modelValue', v: string): void }>()

const editorEl = ref<HTMLElement>()
const previewHtml = ref('')
let view: EditorView | null = null
let autoSaveTimer: ReturnType<typeof setInterval>

function updatePreview(content: string) {
  previewHtml.value = renderMarkdown(content)
}

onMounted(() => {
  const state = EditorState.create({
    doc: props.modelValue,
    extensions: [
      lineNumbers(),
      highlightActiveLine(),
      history(),
      keymap.of([...defaultKeymap, ...historyKeymap]),
      markdown(),
      oneDark,
      EditorView.updateListener.of((update) => {
        if (update.docChanged) {
          const content = update.state.doc.toString()
          emit('update:modelValue', content)
          updatePreview(content)
        }
      }),
      EditorView.theme({
        '&': { height: '100%', fontSize: '14px' },
        '.cm-scroller': { fontFamily: "'JetBrains Mono', monospace", overflow: 'auto' },
        '.cm-content': { padding: '16px' },
      }),
    ],
  })

  view = new EditorView({ state, parent: editorEl.value! })
  updatePreview(props.modelValue)

  // Auto-save to localStorage
  autoSaveTimer = setInterval(() => {
    const content = view?.state.doc.toString()
    if (content) localStorage.setItem('editor_autosave', content)
  }, 30000)
})

onUnmounted(() => {
  view?.destroy()
  clearInterval(autoSaveTimer)
})

watch(() => props.modelValue, (val) => {
  if (view && view.state.doc.toString() !== val) {
    view.dispatch({ changes: { from: 0, to: view.state.doc.length, insert: val } })
    updatePreview(val)
  }
})
</script>

<template>
  <div class="flex h-full border border-border rounded-xl overflow-hidden">
    <!-- Editor -->
    <div class="flex-1 min-w-0 border-r border-border">
      <div class="px-4 py-2 bg-bg border-b border-border text-xs text-muted font-medium">编辑</div>
      <div ref="editorEl" class="h-full" style="height: calc(100% - 33px)" />
    </div>

    <!-- Preview -->
    <div class="flex-1 min-w-0 overflow-auto">
      <div class="px-4 py-2 bg-bg border-b border-border text-xs text-muted font-medium">预览</div>
      <div class="p-6 prose prose-base max-w-none" v-html="previewHtml" />
    </div>
  </div>
</template>
