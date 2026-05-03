export interface Tag {
  id: number
  name: string
  slug: string
  color: string
  description?: string
  article_count?: number
  created_at: string
}

export interface TagCreate {
  name: string
  slug?: string
  color?: string
  description?: string
}
