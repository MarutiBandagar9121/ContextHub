import axios from 'axios'
import useAuthStore from '../store/authStore'

const client = axios.create({
  withCredentials: true, // send the httpOnly refresh token cookie on every request
})

client.interceptors.request.use((config) => {
  const token = useAuthStore.getState().accessToken
  if (token) {
    config.headers.Authorization = `Bearer ${token}`
  }
  return config
})

let isRefreshing = false
let refreshQueue = []

const processQueue = (error, token = null) => {
  refreshQueue.forEach((cb) => (error ? cb.reject(error) : cb.resolve(token)))
  refreshQueue = []
}

client.interceptors.response.use(
  (response) => response,
  async (error) => {
    const original = error.config

    if (error.response?.status !== 401 || original._retry) {
      return Promise.reject(error)
    }

    if (isRefreshing) {
      return new Promise((resolve, reject) => {
        refreshQueue.push({ resolve, reject })
      }).then((token) => {
        original.headers.Authorization = `Bearer ${token}`
        return client(original)
      })
    }

    original._retry = true
    isRefreshing = true

    try {
      const { data } = await axios.post(
        '/api/v1/auth/refresh',
        {},
        { withCredentials: true }
      )
      const newToken = data.access_token
      useAuthStore.getState().setAccessToken(newToken)
      processQueue(null, newToken)
      original.headers.Authorization = `Bearer ${newToken}`
      return client(original)
    } catch (refreshError) {
      processQueue(refreshError, null)
      useAuthStore.getState().clearAuth()
      window.location.href = '/login'
      return Promise.reject(refreshError)
    } finally {
      isRefreshing = false
    }
  }
)

export default client
