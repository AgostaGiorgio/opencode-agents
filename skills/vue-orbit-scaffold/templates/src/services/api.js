import axios from 'axios'

// Single axios instance for the whole app. Base URL comes from the build-time
// env var (see .env.example / Dockerfile).
const apiClient = axios.create({
  baseURL: import.meta.env.VITE_API_BASE_URL,
  timeout: 10000,
  headers: {
    'Content-Type': 'application/json',
  },
})

// Add one method per backend endpoint, grouped by resource. Components never
// call axios directly — they use `api`.
export const api = {
  // Example: GET /api/v1/items
  async getItems() {
    const { data } = await apiClient.get('/api/v1/items')
    return data
  },
}

export default api
