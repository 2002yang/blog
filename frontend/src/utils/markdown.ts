import { marked, type Renderer } from 'marked'
import { markedHighlight } from 'marked-highlight'
import hljs from 'highlight.js'
import DOMPurify from 'dompurify'

marked.use(
  markedHighlight({
    langPrefix: 'hljs language-',
    highlight(code, lang) {
      const language = hljs.getLanguage(lang) ? lang : 'plaintext'
      return hljs.highlight(code, { language }).value
    },
  }),
)

const renderer: Partial<Renderer> = {
  heading({ tokens, depth }) {
    const text = tokens.map((t) => ('text' in t ? t.text : '')).join('')
    const id = text.toLowerCase().replace(/[^\w一-龥]+/g, '-').replace(/^-|-$/g, '')
    const tag = `h${depth}`
    return `<${tag} id="${id}">${text}</${tag}>\n`
  },
  link({ href, title, tokens }) {
    const text = tokens.map((t) => ('text' in t ? t.text : '')).join('')
    const isExternal = href?.startsWith('http')
    const attrs = isExternal ? ` target="_blank" rel="noopener noreferrer"` : ''
    const titleAttr = title ? ` title="${title}"` : ''
    return `<a href="${href}"${titleAttr}${attrs}>${text}</a>`
  },
}

marked.use({ renderer })

export function renderMarkdown(content: string): string {
  const raw = marked.parse(content) as string
  return DOMPurify.sanitize(raw, {
    ADD_TAGS: ['iframe'],
    ADD_ATTR: ['allow', 'allowfullscreen', 'frameborder', 'scrolling', 'target'],
  })
}

export interface TocItem {
  id: string
  text: string
  level: number
}

export function extractToc(content: string): TocItem[] {
  const headingRegex = /^#{1,4}\s+(.+)$/gm
  const items: TocItem[] = []
  let match
  while ((match = headingRegex.exec(content)) !== null) {
    const level = match[0].match(/^#+/)![0].length
    const text = match[1].trim()
    const id = text.toLowerCase().replace(/[^\w一-龥]+/g, '-').replace(/^-|-$/g, '')
    items.push({ id, text, level })
  }
  return items
}
