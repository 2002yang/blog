import client from './client'

export interface UploadResponse {
  url: string
  filename: string
}

export const uploadApi = {
  image: (file: File) => {
    const form = new FormData()
    form.append('file', file)
    return client.post<UploadResponse>('/upload/image', form, {
      headers: { 'Content-Type': 'multipart/form-data' },
    })
  },
}
