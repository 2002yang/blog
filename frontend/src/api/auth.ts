import client from './client'
import type { LoginRequest, LoginResponse, User } from '@/types/auth'

export const authApi = {
  login: (data: LoginRequest) =>
    client.post<LoginResponse>('/auth/login', data),

  refresh: () =>
    client.post<{ access_token: string }>('/auth/refresh', {}, { withCredentials: true }),

  me: () =>
    client.get<User>('/auth/me'),

  updateMe: (data: Partial<Pick<User, 'username' | 'bio' | 'avatar_url'>>) =>
    client.put<User>('/auth/me', data),

  logout: () =>
    client.post('/auth/logout', {}, { withCredentials: true }),
}
