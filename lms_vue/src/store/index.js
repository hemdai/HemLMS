import { createStore } from 'vuex'

export default createStore({
  state: {
    user: {
      token: '',
      isAuthenticated: false,
      first_name: ''
    }
  },
  mutations: {
    initializeStore (state) {
      if (localStorage.getItem('token')) {
        state.user.token = localStorage.getItem('token')
        state.user.isAuthinticated = true
      }
      else {
        state.user.token = ''
        state.user.isAuthinticated = false
      }
    },
    setToken(state, token) {
      state.user.token = token
      state.user.isAuthenticated = true
    },
    setUserName(state, first_name) {
      state.user.first_name = first_name
    },
    removeUserName(state) {
      state.user.first_name = ''
    },
    removeToken(state) {
      state.user.token = ''
      state.user.isAuthenticated = false
    },
  },
  actions: {
  },
  modules: {
  }
})
