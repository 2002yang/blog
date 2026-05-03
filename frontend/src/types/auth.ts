export interface User {
  id: number
  username: string
  email: string
  is_admin: boolean
  avatar_url?: string
  bio?: string
  created_at: string
}

export interface LoginRequest {
  username: string
  password: string
}

export interface LoginResponse {
  access_token: string
  token_type: string
  user: User
}
