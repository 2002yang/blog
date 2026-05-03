import type { Tag } from './tag'
import type { User } from './auth'

export type ArticleStatus = 'draft' | 'published'

export interface Article {
  id: number
  title: string
  slug: string
  summary?: string
  content: string
  cover_image?: string
  author?: User
  status: ArticleStatus
  is_featured: boolean
  view_count: number
  read_time: number
  tags: Tag[]
  published_at?: string
  created_at: string
  updated_at: string
}

export interface ArticleListItem {
  id: number
  title: string
  slug: string
  summary?: string
  cover_image?: string
  author?: Pick<User, 'id' | 'username' | 'avatar_url'>
  status: ArticleStatus
  is_featured: boolean
  view_count: number
  read_time: number
  tags: Tag[]
  published_at?: string
  created_at: string
}

export interface ArticleCreate {
  title: string
  slug?: string
  summary?: string
  content: string
  cover_image?: string
  status?: ArticleStatus
  is_featured?: boolean
  tag_ids?: number[]
  published_at?: string
}

export interface ArticleUpdate extends Partial<ArticleCreate> {}

export interface PaginatedArticles {
  items: ArticleListItem[]
  total: number
  page: number
  size: number
  pages: number
}
