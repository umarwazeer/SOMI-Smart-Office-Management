import api from 'src/services/api'

class AuthenticationService {
  register (user) {
    return api.post('/auth/register/', user)
  }

  login (credentials) {
    return api.post('/auth/login/', credentials)
  }

  async refreshToken () {
    const refreshToken = this.getRefreshToken()

    if (!refreshToken) {
      throw new Error('No refresh token available')
    }

    try {
      const response = await api.post('/auth/token/refresh/', {
        refresh: refreshToken
      })

      const newAccessToken = response.data.access

      if (!newAccessToken) {
        throw new Error('No access token returned by server')
      }

      this.setToken(newAccessToken)

      return newAccessToken
    } catch (error) {
      this.clearTokens()
      throw error
    }
  }

  async refreshAccessToken (refreshToken) {
    if (!refreshToken) {
      throw new Error('No refresh token available')
    }

    try {
      const response = await api.post('/auth/token/refresh/', {
        refresh: refreshToken
      })

      const newAccessToken = response.data.access

      if (!newAccessToken) {
        throw new Error('No access token returned by server')
      }

      this.setToken(newAccessToken)

      return newAccessToken
    } catch (error) {
      this.clearTokens()
      throw error
    }
  }

  getUserDetail () {
    return api.get('/auth/me/')
  }

  async logout () {
    try {
      await api.post('/auth/logout/')
    } catch (error) {
      console.warn('Logout API request failed:', error)
    } finally {
      this.clearTokens()
    }
  }

  getToken () {
    return localStorage.getItem('access_token')
  }

  getRefreshToken () {
    return localStorage.getItem('refresh_token')
  }

  setToken (token) {
    localStorage.setItem('access_token', token)
  }

  setRefreshToken (token) {
    localStorage.setItem('refresh_token', token)
  }

  clearTokens () {
    localStorage.removeItem('access_token')
    localStorage.removeItem('refresh_token')
  }

  isAuthenticated () {
    return !!this.getToken()
  }

  async apiRequestWithAuth (url, method = 'GET', data = null) {
    try {
      const response = await api({
        url,
        method,
        data
      })

      return response.data
    } catch (error) {
      if (error.response && error.response.status === 401) {
        try {
          await this.refreshToken()

          const response = await api({
            url,
            method,
            data
          })

          return response.data
        } catch (refreshError) {
          this.clearTokens()
          throw new Error('Your session has expired. Please log in again.')
        }
      }

      throw error
    }
  }

  async getEmployees () {
    return this.apiRequestWithAuth('/employees/', 'GET')
  }

  protectedRouteExample () {
    return this.apiRequestWithAuth('/auth/me/', 'GET')
  }
}

export default new AuthenticationService()
