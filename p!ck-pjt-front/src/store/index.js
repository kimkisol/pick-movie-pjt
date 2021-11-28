import Vue from 'vue'
import Vuex from 'vuex'
import createPersistedState from "vuex-persistedstate"
import router from '@/router/index.js'
import axios from 'axios'
import SERVER from '@/api/drf.js'


Vue.use(Vuex)

import accountStore from '@/store/modules/accountStore.js'
import basketStore from '@/store/modules/basketStore.js'
import movieStore from '@/store/modules/movieStore.js'


const store = new Vuex.Store({
  modules: {
    accountStore: accountStore,
    basketStore: basketStore,
    movieStore: movieStore,
  },
  state: {
    authToken: localStorage.getItem('jwt'),
    userId: '',
    userInfo: '',
  },
  getters: {
    isLoggedIn: function (state) {
      return state.authToken ? true: false
    },
    config: function (state) {
      return {
        Authorization: `JWT ${state.authToken}`
      }
    },
  },
  mutations: {
    // 로그인
    SET_TOKEN: function (state, token) {
      state.authToken = token
      localStorage.setItem('jwt', token)
    },
    REMOVE_TOKEN: function (state) {
      localStorage.removeItem('jwt')
      state.authToken = ''
    },
    // 프로필
    SET_USER_ID: function (state, userId) {
      state.userId = userId
      console.log(state.userId)
    },
    // 모든 유저 정보
    SET_USER_INFO: function (state, userInfo) {
      state.userInfo = userInfo
    }
  },
  actions: {
    // 로그인
    login: function ({ commit, dispatch }, credentials) {
      axios({
        url: SERVER.URL + SERVER.ROUTES.login,
        method: 'post',
        data: credentials,
      })
      .then((res) => {
        commit('SET_TOKEN', res.data.token)
        router.push({ name: 'Main' })
        dispatch('getUserId')
        dispatch('setUserInfo')
      })
      .catch((err) => {
        console.log(err)
      })
    },
    logout: function ({ commit }) {
      commit('REMOVE_TOKEN')
      router.push({ name: 'Login' })
    },
    signup: function (context, credentials) {
      axios({
        url: SERVER.URL + SERVER.ROUTES.signup,
        method: 'post',
        data: credentials,
      })
      .then(() => {
        console.log(SERVER.URL + SERVER.ROUTES.signup)
        router.push({ name: 'Login' })
      })
      .catch((err) => {
        console.log(err)
      })
    },
    // 프로필
    getUserId: function ({ commit, getters }) {
      axios({
        url: SERVER.URL + '/api/v1/accounts/login/',
        method: 'get',
        headers: getters.config
      })
      .then((res) => {
        commit('SET_USER_ID', res.data.userId)
      })
      .catch((err) => {
        console.log(err)
      })
    },
    // 모든 유저 정보
    setUserInfo: function ({ commit, getters }) {
      axios({
        url: SERVER.URL + '/api/v1/accounts/user_info/',
        method: 'get',
        headers: getters.config
      })
      .then((res) => {
        console.log('유저정보', res)
        const userInfo = {}
        for (let data of res.data) {
          // const obj = {
          //   [data.id]: data
          // }
          // userInfo.push(obj)
          userInfo[data.id] = data
        }
        console.log(userInfo)
        commit('SET_USER_INFO', userInfo)
      })
      .catch((err) => {
        console.log(err)
      })
    },
    // getUserInfo: function (userId) {
    //   // return this.userInfo.find((user) => {
    //   //   return user.id === userId
    //   // })
    //   return this.userInfo.find(userId)
    // }
  },
  plugins: [createPersistedState()]
})

export default store