import client from './client'
import type { Tag, TagCreate } from '@/types/tag'

export const tagsApi = {
  list: () =>
    client.get<Tag[]>('/tags'),

  getBySlug: (slug: string) =>
    client.get<Tag>(`/tags/${slug}`),

  create: (data: TagCreate) =>
    client.post<Tag>('/admin/tags', data),

  update: (id: number, data: Partial<TagCreate>) =>
    client.put<Tag>(`/admin/tags/${id}`, data),

  delete: (id: number) =>
    client.delete(`/admin/tags/${id}`),
}
