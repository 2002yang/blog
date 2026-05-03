import client from './client'
import type { Article, ArticleCreate, ArticleUpdate, ArticleListItem, PaginatedArticles } from '@/types/article'

export const articlesApi = {
  list: (params?: { page?: number; size?: number; tag?: string; q?: string }) =>
    client.get<PaginatedArticles>('/articles', { params }),

  featured: () =>
    client.get<ArticleListItem[]>('/articles/featured'),

  search: (q: string, page = 1) =>
    client.get<PaginatedArticles>('/articles/search', { params: { q, page } }),

  getBySlug: (slug: string) =>
    client.get<Article>(`/articles/${slug}`),

  incrementView: (id: number) =>
    client.post(`/articles/${id}/view`),

  // Admin
  adminList: (params?: { page?: number; size?: number; status?: string }) =>
    client.get<PaginatedArticles>('/admin/articles', { params }),

  create: (data: ArticleCreate) =>
    client.post<Article>('/admin/articles', data),

  update: (id: number, data: ArticleUpdate) =>
    client.put<Article>(`/admin/articles/${id}`, data),

  delete: (id: number) =>
    client.delete(`/admin/articles/${id}`),

  togglePublish: (id: number) =>
    client.patch<Article>(`/admin/articles/${id}/publish`),

  toggleFeature: (id: number) =>
    client.patch<Article>(`/admin/articles/${id}/feature`),
}
