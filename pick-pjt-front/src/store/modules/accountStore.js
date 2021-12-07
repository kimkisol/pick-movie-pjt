import SERVER from '@/api/drf.js'
import router from '@/router/index.js'
import axios from 'axios'

const accountStore = {
  namespaced: true,

  state: () => ({
    // 로그인
    profileInfo: '',
    tags: [],
    followButtonName: '',
    // 유저, 영화별 바스켓
    authorBaskets: [],
    likeBaskets: [],
    likeMovies: [],
    // 그룹
    groups: [],
    relationshipList: [],
    groupFilterId: '전체',
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
    RESET_PROFILE: function (state) {
      state.profileInfo = ''
      // state.followButtonName = ''
    },
    GET_PROFILE: function (state, userData) {
      state.profileInfo = userData
    },
    GET_TAGS: function (state, userData) {
      state.tags = userData.liked_baskets_tags
    },
    // 유저, 영화별 바스켓
    GET_AUTHOR_BASKETS: function (state, authorBaskets) {
      state.authorBaskets = authorBaskets
    },
    GET_LIKE_BASKETS: function (state, likeBaskets) {
      state.likeBaskets = likeBaskets
    },
    GET_LIKE_MOVIES: function (state, likeMovies) {
      state.likeMovies = likeMovies
    },
    // 팔로우
    GET_FOLLOW_INFO: function (state, followButtonName) {
      state.followButtonName = followButtonName
    },
    // 그룹
    SET_GROUPS: function (state, groups) {
      state.groups = groups
    },
    // Relationship
    SET_RELATIONSHIP_LIST: function (state, relationshipList) {
      state.relationshipList = relationshipList
    },
    SET_GROUP_FILTER_ID: function (state, groupFilterId) {
      state.groupFilterId = groupFilterId
    },
  },

  actions: {
    getProfile: function ({ commit, getters, dispatch }, userId) {
      console.log('getProfile', userId)
      dispatch('getProfileTags', userId)
      dispatch('addProfileInfo', userId)
      
      axios({
        method: 'get',
        url: `${SERVER.URL}/api/v1/accounts/profile/${userId}/`,
        headers: getters.config // getters.config
      })
      .then((res) => {
        const userData = res.data
        commit('GET_PROFILE', userData)
        // dispatch('getFollowButtonName')
        console.log('name: Profile, userId: ', userId)
        router.push({ name: 'Profile', params: { userId: userId } })
      })
      .catch((err) => {
        console.log(err)
      })
      dispatch('getProfileTags', userId)
      dispatch('addProfileInfo', userId)
      // dispatch('getFollowButtonName', state.profileInfo)
    },
    getProfileTags: function ({ commit, getters }, userId) {
      console.log('getProfileTags', userId)
      axios({
        method: 'get',
        url: `${SERVER.URL}/api/v1/accounts/liked_baskets_tags/${userId}/`,
        headers: getters.config
      })
      .then((res) => {
        const userData = res.data
        commit('GET_TAGS', userData)
      })
      .catch((err) => {
        console.log(err)
      })
    },
    // 유저별로 작성한 바스켓, 좋아요한 바스켓, 좋아요한 영화 가져오기
    addProfileInfo: function ({ commit, getters }, userId) {
      const headers = getters.config
      axios({
        url: `${SERVER.URL}/api/v1/accounts/add_profile_info/${userId}/write/basket/`,
        method: 'get',
        headers,
      })
      .then((res) => {
        // console.log('유저 바스켓', res.data)
        commit('GET_AUTHOR_BASKETS', res.data)
      })
      .catch((err) => {
        console.log(err)
      })
      axios({
        url: `${SERVER.URL}/api/v1/accounts/add_profile_info/${userId}/like/basket/`,
        method: 'get',
        headers,
      })
      .then((res) => {
        commit('GET_LIKE_BASKETS', res.data)
      })
      .catch((err) => {
        console.log(err)
      })
      axios({
        url: `${SERVER.URL}/api/v1/accounts/add_profile_info/${userId}/like/movie/`,
        method: 'get',
        headers,
      })
      .then((res) => {
        commit('GET_LIKE_MOVIES', res.data)
      })
      .catch((err) => {
        console.log(err)
      })
    },
    //팔로우
    getFollowButtonName: function ({ state, commit, rootState }) {
      // console.log('profileInfo', profileInfo)
      // console.log('rootState.userId in profileInfo.fans', rootState.userId in state.profileInfo.fans)
      // console.log('getFollowButtonName', rootState.userId)
      // console.log(typeof(rootState.userId))
      // console.log('getFollowButtonName', state.profileInfo.fans)
      // console.log(typeof(state.profileInfo.fans))
      // console.log(rootState.userId in state.profileInfo.fans)
      // if (rootState.userId in state.profileInfo.fans) {
      //   commit('GET_FOLLOW_INFO', '언팔로우')
      // } else {
      //   commit('GET_FOLLOW_INFO', '팔로우')
      // }
      let flag = false
      for (let fan of state.profileInfo.fans) {
        if (fan === rootState.userId) {
          commit('GET_FOLLOW_INFO', '언팔로우')
          flag = true
        }
      }
      if (flag === false) {
        commit('GET_FOLLOW_INFO', '팔로우')
      }
    },
    follow: function ({ commit, getters }, starId) {
      axios({
        method: 'post',
        url: `${SERVER.URL}/api/v1/accounts/relationship/star/${starId}/`,
        headers: getters.config
      })
      .then(() => {
        // dispatch('getFollowButtonName', starId)
        commit('GET_FOLLOW_INFO', '언팔로우')
      })
      .catch((err) => {
        console.log(err)
      })
    },
    unfollow: function ({ commit, getters }, starId) {
      axios({
        method: 'delete',
        url: `${SERVER.URL}/api/v1/accounts/relationship/star/${starId}/`,
        headers: getters.config
      })
      .then(() => {
        // dispatch('getProfile', starId)
        commit('GET_FOLLOW_INFO', '팔로우')
      })
      .catch((err) => {
        console.log(err)
      })
    },
    // 그룹
    getGroups: function ({ commit, getters }) {
      const headers = getters.config
      axios({
        url: `${SERVER.URL}/api/v1/accounts/group/`,
        method: 'get',
        headers,
      })
      .then((res) => {
        commit('SET_GROUPS', res.data)
      })
      .catch((err) => {
        console.log(err)
      })
    },
    createGroup: function ({ dispatch, getters }, name) {
      const headers = getters.config

      const group = {
        name,
      }
      if (group.name) {
        axios({
          url: `${SERVER.URL}/api/v1/accounts/group/`,
          method: 'post',
          data: group,
          headers,
        })
        .then(() => {
          dispatch('getGroups')
          router.push({ name: 'Group' })
        })
        .catch((err) => {
          console.log(err)
        })
      }
    },
    deleteGroup: function ({ dispatch, getters }, groupId) {
      const headers = getters.config

      axios({
        url: `${SERVER.URL}/api/v1/accounts/group/${groupId}/`,
        method: 'delete',
        headers,
      })
      .then(() => {
        dispatch('getGroups')
        dispatch('getGroupRelationshipList')
      })
      .catch((err) => {
        console.log(err)
      })
    },
    // Relationship (그룹관리)
    getGroupRelationshipList: function ({ commit, getters }) {
      const headers = getters.config
      axios({
        url: `${SERVER.URL}/api/v1/accounts/relationship/`,
        method: 'get',
        headers,
      })
      .then((res) => {
        commit('SET_RELATIONSHIP_LIST', res.data)
      })
      .catch((err) => {
        console.log(err)
      })
    },
    setGroupFilterId: function ({ commit }, groupFilterId) {
      commit('SET_GROUP_FILTER_ID', groupFilterId)
    },
    changeRelationshipGroup: function ({ dispatch, getters }, { selectedRelationships, selectedGroup }) {
      const headers = getters.config
      console.log(selectedGroup)
      for (let selectedRelationship of selectedRelationships) {
        axios({
          url: `${SERVER.URL}/api/v1/accounts/relationship/${selectedRelationship}/group/${selectedGroup}/`,
          method: 'put',
          headers,
        })
        .then(() => {
          dispatch('getGroupRelationshipList')
          router.push({ name: 'Group' })
        })
        .catch((err) => {
          console.log(err)
        })
      }
    },
  }
}
export default accountStore