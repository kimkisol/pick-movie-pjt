import SERVER from '@/api/drf.js'
import router from '@/router/index.js'
import axios from 'axios'
import _ from 'lodash'


const basketStore = {
  namespaced: true,
  state: () => ({
    // userId: '',
    authToken: localStorage.getItem('jwt'),
    searchedBaskets: [],
    query: '',
    recommendedBaskets: [],
    recommendedMethod: [],
    recommendedTail: [],
    // 디테일
    selectedBasketDetail: '',
    // 좋아요
    likeButtonName: '',
    likeCnt: '',
    // COMMENT
    comments: [],
    noSpoilerComments: [],
    showSpoilerOption: false,
    // 유저, 영화별 바스켓
    // authorBaskets: [],
    // movieBaskets: [],
  }),
  getters: {
    isLoggedIn: function (state, getters, rootState, rootGetters) {
      return rootGetters.isLoggedIn
    },
    config: function (state, getters, rootState, rootGetters) {
      return rootGetters.config
    },
  },
  mutations: {
    SET_SEARCHED_BASKET_LIST: function (state, baskets) {
      state.searchedBaskets = baskets
      state.recommendedBaskets = []
    },
    SET_SEARCHED_QUERY: function (state, query) {
      state.query = query
    },
    SET_RECOMMENDED_BASKET_LIST: function (state, recommendedData) {
      state.recommendedBaskets.push({
        recommended_name: recommendedData.pop(3).recommended_name,
        baskets: recommendedData
      }) 
      state.searchedBaskets = []
    },
    SET_RECOMMENDED_METHOD_TAIL: function (state, methodTail) {
      state.recommendedMethod.push(methodTail.method)
      state.recommendedTail.push(methodTail.tail)
    },
    // 디테일
    SET_BASKET_DETAIL: function (state, basketDetail) {
      state.selectedBasketDetail = basketDetail
    },
    // 좋아요
    GET_LIKE_INFO: function (state, likeButtonName) {
      state.likeButtonName = likeButtonName
    },
    GET_LIKE_CNT: function (state, likeCnt) {
      state.likeCnt = likeCnt
    },
    RESET_BASKETS: function (state, type) {
      if (type === 'recommended') {
        state.recommendedBaskets = []
      } if (type === 'searched') {
        state.searchedBaskets = []
      }
      state.query = ''
      state.recommendedTail = []
      state.recommendedMethod = []
    },
    // COMMENT
    SET_COMMENTS: function (state, comments) {
      state.comments = comments
      const noSpoilerCommentList = []
      for (let comment of comments) {
        if (!comment.spoiler) {
          noSpoilerCommentList.push(comment)
        }
      }
      state.noSpoilerComments = noSpoilerCommentList
    },
    SET_SPOILER_FILTER: function (state, showSpoiler) {
      state.showSpoilerOption = showSpoiler
    },
    // 유저, 영화별 바스켓
    // GET_AUTHOR_BASKETS: function (state, authorBaskets) {
    //   state.authorBaskets = authorBaskets
    // },
    // GET_MOVIE_BASKETS: function (state, movieBaskets) {
    //   state.movieBaskets = movieBaskets
    // },
  },
  actions: {
    getBasketSearchResult: function ({ commit, getters }, event) {
      const headers = getters.config
      const query = event.target.value
      axios({
        method: 'get',
        url: `${SERVER.URL}/api/v1/baskets/search/${query}/`,
        headers,
      })
      .then((res) => {
        commit('SET_SEARCHED_BASKET_LIST', res.data)
        commit('SET_SEARCHED_QUERY', query)
      })
      .catch((err) => {
        console.log(err)
      })
    },
    getBasketRecommendation: function ({ commit, getters }) {
      const headers = getters.config
      const recommend_method = _.sample(['myinfo', 'movies', 'tags', 'friends'])

      const recommend_tail = {
        'myinfo': '사용자들이 p!ck한 바스켓',
        'movies': '영화가 들어있는 바스켓',
        'tags': '태그가 들어있는 바스켓',
        'friends': '님이 p!ck한 바스켓',
      }
      const methodTail = []

      axios({
        method: 'get',
        url: `${SERVER.URL}/api/v1/baskets/recommend/${recommend_method}`,
        headers,
      })
      .then((res) => {
        console.log(res.data[3])
        if (res.data[3].recommended_name === '지금 핫한') {
          const methodTailItem = {
            method: recommend_method,
            tail: '바스켓',
          }
          methodTail.push(methodTailItem)
        } else {
          const methodTailItem = {
            method: recommend_method,
            tail: recommend_tail[recommend_method],
          }
          methodTail.push(methodTailItem)
        }
        console.log(recommend_method)
        commit('SET_RECOMMENDED_BASKET_LIST', res.data)
        commit('SET_RECOMMENDED_METHOD_TAIL', methodTail[0])
      })
      .catch((err) => {
        console.log(err)
      })
    },
    // 디테일
    getBasketDetail: function ({ commit, getters }, selectedBasket) {
      const headers = getters.config
      const basket_pk = selectedBasket.id
      axios({
        method: 'get',
        url: `${SERVER.URL}/api/v1/baskets/${basket_pk}/`,
        headers,
      })
      .then((res) => {
        commit('SET_BASKET_DETAIL', res.data)
        commit('GET_LIKE_CNT', res.data.like_users.length)
        router.push({ name: 'BasketDetail' })
      })
      .catch((err) => {
        console.log(err)
      })
    },
    // 생성 관련
    showBasketForm: function () {
      router.push({ name: 'BasketForm' })
    },
    // 좋아요
    getLikeButtonName: function ({ state, commit, rootState }) {
      let flag = false
      for (let like_user of state.selectedBasketDetail.like_users) {
        if (rootState.userId === like_user['id']) {
          commit('GET_LIKE_INFO', 'unlike')
          flag = true
        }
      }
      if (flag === false) {
        commit('GET_LIKE_INFO', 'like')
      }
    },
    likeUnlike: function ({ state, commit, dispatch, getters, rootGetters }, basketId) {
      console.log(getters.config)
      console.log(rootGetters.config)
      axios({
        method: 'post',
        url: `${SERVER.URL}/api/v1/baskets/${basketId}/like/`,
        headers: getters.config
      })
      .then((res) => {
        console.log('likeUnlike', res)
        dispatch('getBasketDetail', state.selectedBasketDetail)
        if (res.data.liked) {
          commit('GET_LIKE_INFO', 'unlike')
        } else {
          commit('GET_LIKE_INFO', 'like')
        }
        commit('GET_LIKE_CNT', res.data.cnt_likes)
      })
      .catch((err) => {
        console.log(err)
      })
    },
    // 초기화
    resetBaskets: function ({ commit }, type) {
      commit('RESET_BASKETS', type)
    },
    // COMMENT
    getCommentList: function ({ state, commit, getters }) {
      const headers = getters.config
      const basket_id = state.selectedBasketDetail.id
      // console.log(basket_id)
      axios({
        url: `${SERVER.URL}/api/v1/baskets/${basket_id}/comment/`,
        method: 'get',
        headers,
      })
      .then((res) => {
        commit('SET_COMMENTS', res.data)
      })
      .catch((err) => {
        console.log(err)
      })
    },
    createComment: function ({ state, getters, dispatch }, { content, spoiler }) {
      const headers = getters.config
      const basket_id = state.selectedBasketDetail.id
      const commentItem = {
        content,
        spoiler,
      }

      if (commentItem.content) {
        axios({
          url: `${SERVER.URL}/api/v1/baskets/${basket_id}/comment/`,
          method: 'post',
          data: commentItem,
          headers,
        })
        .then(() => {
          dispatch('getCommentList')
        })
        .catch((err) => {
          console.log(err)
        })
      }
    },
    deleteComment: function ({ getters, dispatch }, comment) {
      const headers = getters.config
      const comment_pk = comment.id
      axios({
        url: `${SERVER.URL}/api/v1/baskets/comment/${comment_pk}/`,
        method: 'delete',
        headers,
      })
      .then(() => {
        dispatch('getCommentList')
      })
      .catch((err) => {
        console.log(err)
      })
    },
    setSpoilerFilter: function ({ commit }, showSpoiler) {
      commit('SET_SPOILER_FILTER', showSpoiler)
    },
    // 바스켓 CD
    createBasket: function ({ getters, dispatch }, basketInfo) {
      const headers = getters.config
      console.log(basketInfo)
      axios({
        url: `${SERVER.URL}/api/v1/baskets/`,
        method: 'post',
        data: basketInfo,
        headers,
      })
      .then((res) => {
        console.log(res)
        dispatch('getBasketDetail', res.data)
      })
      .catch((err) => {
        console.log(err)
      })
    },
    deleteBasket: function ({ getters }, basket) {
      const headers = getters.config
      axios({
        url: `${SERVER.URL}/api/v1/baskets/${basket.id}/`,
        method: 'delete',
        headers,
      })
      .then(() => {
        alert('해당 바스켓이 삭제되었습니다.')
        router.push({ name: 'Main' })
      })
      .catch((err) => {
        console.log(err)
      })
    },
  },
}
export default basketStore