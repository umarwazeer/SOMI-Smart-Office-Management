import { createStore } from 'vuex'
import AuthenticationService from 'src/pages/authentication/AuthenticationService'

export default createStore({
  state: {
    user: null,
    isLoading: false
  },

  getters: {
    currentUser: (state) => state.user,

    isAuthenticated: (state) => {
      return !!state.user && AuthenticationService.isAuthenticated()
    },

    hasToken: () => {
      return AuthenticationService.isAuthenticated()
    },

    userRole: (state) => {
      return String(state.user?.role || '').toUpperCase()
    },

    username: (state) => {
      return state.user?.username || ''
    },

    fullName: (state) => {
      if (!state.user) {
        return ''
      }

      const name = `${state.user.first_name || ''} ${state.user.last_name || ''}`.trim()

      return name || state.user.username || ''
    },

    email: (state) => {
      return state.user?.email || ''
    },

    isAdmin: (state) => {
      return String(state.user?.role || '').toUpperCase() === 'ADMIN'
    },

    isManager: (state) => {
      return String(state.user?.role || '').toUpperCase() === 'MANAGER'
    },

    isEmployee: (state) => {
      return String(state.user?.role || '').toUpperCase() === 'EMPLOYEE'
    },

    canManage: (state) => {
      const role = String(state.user?.role || '').toUpperCase()

      return role === 'ADMIN' || role === 'MANAGER'
    },

    canCreate: (state) => {
      const role = String(state.user?.role || '').toUpperCase()

      return role === 'ADMIN' || role === 'MANAGER'
    },

    canEdit: (state) => {
      const role = String(state.user?.role || '').toUpperCase()

      return role === 'ADMIN' || role === 'MANAGER'
    },

    canDelete: (state) => {
      return String(state.user?.role || '').toUpperCase() === 'ADMIN'
    }
  },

  mutations: {
    SET_USER (state, user) {
      state.user = user
    },

    CLEAR_USER (state) {
      state.user = null
    },

    SET_LOADING (state, value) {
      state.isLoading = value
    }
  },

  actions: {
    async fetchCurrentUser ({ commit }) {
      if (!AuthenticationService.isAuthenticated()) {
        commit('CLEAR_USER')
        return null
      }

      commit('SET_LOADING', true)

      try {
        const response = await AuthenticationService.getUserDetail()
        const user = response.data

        commit('SET_USER', user)

        return user
      } catch (error) {
        console.error('Failed to fetch current user:', error)

        if (error.response?.status === 401) {
          AuthenticationService.clearTokens()
          commit('CLEAR_USER')
        }

        throw error
      } finally {
        commit('SET_LOADING', false)
      }
    },

    setUser ({ commit }, user) {
      commit('SET_USER', user)
    },

    async logout ({ commit }) {
      try {
        await AuthenticationService.logout()
      } catch (error) {
        console.error('Logout request failed:', error)
      } finally {
        AuthenticationService.clearTokens()
        commit('CLEAR_USER')
      }
    },

    clearUser ({ commit }) {
      AuthenticationService.clearTokens()
      commit('CLEAR_USER')
    }
  }
})
