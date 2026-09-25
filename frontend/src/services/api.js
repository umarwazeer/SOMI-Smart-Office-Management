import axios from 'axios'

const API_BASE_URL = 'http://127.0.0.1:8000/api'

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json'
  }
})

api.interceptors.request.use(
  (config) => {
    const accessToken = localStorage.getItem('access_token')

    if (accessToken) {
      config.headers.Authorization = `Bearer ${accessToken}`
    }

    return config
  },
  (error) => {
    return Promise.reject(error)
  }
)

let isRefreshing = false
let refreshSubscribers = []

const subscribeTokenRefresh = (callback) => {
  refreshSubscribers.push(callback)
}

const onRefreshed = (newAccessToken) => {
  refreshSubscribers.forEach((callback) => callback(newAccessToken))
  refreshSubscribers = []
}

const onRefreshFailed = (error) => {
  refreshSubscribers.forEach((callback) => callback(null, error))
  refreshSubscribers = []
}

api.interceptors.response.use(
  (response) => {
    return response
  },
  async (error) => {
    const originalRequest = error.config

    if (
      error.response?.status !== 401 ||
      originalRequest?._retry ||
      originalRequest?.url?.includes('/auth/token/refresh/')
    ) {
      return Promise.reject(error)
    }

    originalRequest._retry = true

    const refreshToken = localStorage.getItem('refresh_token')

    if (!refreshToken) {
      localStorage.removeItem('access_token')
      localStorage.removeItem('refresh_token')

      return Promise.reject(error)
    }

    if (isRefreshing) {
      return new Promise((resolve, reject) => {
        subscribeTokenRefresh((newAccessToken, refreshError) => {
          if (refreshError || !newAccessToken) {
            reject(refreshError || error)
            return
          }

          originalRequest.headers.Authorization = `Bearer ${newAccessToken}`

          resolve(api(originalRequest))
        })
      })
    }

    isRefreshing = true

    try {
      const response = await axios.post(
        `${API_BASE_URL}/auth/token/refresh/`,
        {
          refresh: refreshToken
        }
      )

      const newAccessToken = response.data?.access

      if (!newAccessToken) {
        throw new Error('No access token returned by server')
      }

      localStorage.setItem('access_token', newAccessToken)

      onRefreshed(newAccessToken)

      originalRequest.headers.Authorization = `Bearer ${newAccessToken}`

      return api(originalRequest)
    } catch (refreshError) {
      onRefreshFailed(refreshError)

      localStorage.removeItem('access_token')
      localStorage.removeItem('refresh_token')

      return Promise.reject(refreshError)
    } finally {
      isRefreshing = false
    }
  }
)

export default api
