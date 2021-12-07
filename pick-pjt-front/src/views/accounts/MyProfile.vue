<template>
  <div class="mt-5 container">
    <div><br>
      <p class="d-inline-block"
      style="font-family: 'Hahmlet', serif; font-weight: 600; font-size: 1.6rem; color: #222222;"
      >p</p>
      <p class="d-inline-block"
      style="font-family: 'Hahmlet', serif; font-weight: 600; font-size: 1.6rem; color: #5a89cf;"
      >!</p>
      <p class="d-inline-block"
      style="font-family: 'Hahmlet', serif; font-weight: 600; font-size: 1.6rem; color: #222222;"
      >cker</p>
      <p class="d-inline-block ms-2 fs-5 fw-bold">{{ profileInfo.nickname }}</p>
    </div>
    <div class="d-flex flex-column align-items-start container">
      <div class="">
        <!-- 태그 -->
        <div class="d-flex my-3">
          <div v-for="(tag, idx) in tags"
            :key="'tags' + idx"
            class="tag-button d-flex align-items-center justify-content-center px-3 me-2"
          >{{ tag }}</div>
        </div>
      </div>
      <div md="1" class="d-flex align-items-center mb-3">
        <b-avatar src="@/assets/profile-image.png"></b-avatar>
        <span class="ms-3 fs-5" style="font-weight:600;">{{ profileInfo.nickname }}</span>
      </div>
      <div>
        <span>팔로워</span>
        <span class="pick-text ms-1">{{ profileInfo.fans.length }}</span>
        <span class="ms-3">팔로잉</span>
        <span class="pick-text ms-1 me-3">{{ profileInfo.stars.length }}</span>
        <!-- <b-button @click="followUnfollow" v-if="userId !== profileInfo.id && followButtonName == '팔로우'" class="action-button d-inline-block ms-2">{{ followButtonName }}</b-button>
        <b-button @click="followUnfollow" v-if="userId !== profileInfo.id && followButtonName == '언팔로우'" class="action-button-gray d-inline-block ms-2 unfollow">{{ followButtonName }}</b-button> -->
      </div>
    </div><br><hr>
    <div>
      <div class="container">
        <div align="left">
          <p class="d-inline-block ms-1"
          style="font-family: 'Hahmlet', serif; font-weight: 600; font-size: 1.2rem; color: #5a89cf;"
          >{{ profileInfo.nickname }}</p>
          <p class="d-inline-block" style="font-size: 1.2rem;">님이 생성한 바스켓</p>
        </div>
        <div class="basket-search-result row row-cols-1 row-cols-md-2 row-cols-xl-3">
          <basket-list-item v-for="(basket, idx) in authorBaskets"       
            :key="'author_baskets' + idx"
            :basket="basket"
          ></basket-list-item>
        </div>
      </div><br><hr>
      <div class="container">
        <div align="left">
          <p class="d-inline-block ms-1"
          style="font-family: 'Hahmlet', serif; font-weight: 600; font-size: 1.2rem; color: #5a89cf;"
          >{{ profileInfo.nickname }}</p>
          <p class="d-inline-block" style="font-size: 1.2rem;">님이 좋아하는 바스켓</p>
        </div>
        <div class="basket-search-result row row-cols-1 row-cols-md-2 row-cols-xl-3">
          <basket-list-item v-for="(basket, idx) in likeBaskets"       
            :key="'like_baskets' + idx"
            :basket="basket"
          ></basket-list-item>
        </div>
      </div><br><hr>
      <div class="container">
        <div align="left">
          <p class="d-inline-block ms-1"
          style="font-family: 'Hahmlet', serif; font-weight: 600; font-size: 1.2rem; color: #5a89cf;"
          >{{ profileInfo.nickname }}</p>
          <p class="d-inline-block" style="font-size: 1.2rem;">님이 좋아하는 영화</p>
        </div>
        <b-card-group class="row row-cols-3 row-cols-lg-6">
          <movie-list-item v-for="(movie, idx) in likeMovies"
            :movie="movie"
            :key="'movie' + idx"
          ></movie-list-item>
        </b-card-group>
        <b-modal id="modal-xl" size="xl" hide-footer>
          <movie-detail></movie-detail>
        </b-modal>
      </div>
    </div>
  </div>
</template>

<script>
import { mapState, mapActions } from 'vuex'
import BasketListItem from '../../components/Basket/BasketListItem.vue'
import MovieListItem from '../../components/Movie/MovieListItem.vue'
// import axios from 'axios'
// import SERVER from '@/api/drf.js'
// import SERVER from '@/api/drf.js'

export default {
  components: { BasketListItem, MovieListItem },
  name: 'MyProfile',
  data: function() {
    return {
      profileId: '',
    }
  },
  methods: {
    ...mapActions('accountStore', [
      'getProfile',
      'follow',
      'unfollow',
      'getFollowButtonName',
    ]),
    // ...mapGetters([
    //   'config'
    // ]),
    // followUnfollow: function() {
    //   if (this.followButtonName === '팔로우') {
    //     this.follow(this.profileInfo.id)
    //   } else {
    //     this.unfollow(this.profileInfo.id)
    //   }
    //   console.log('getFollowButtonName', this.profileInfo)
    //   this.getFollowButtonName(this.profileInfo)
    // },
  },
  computed: {
    ...mapState('accountStore', {
      profileInfo: state => state.profileInfo,
      tags: state => state.tags,
      followButtonName: state => state.followButtonName,
      authorBaskets: state => state.authorBaskets,
      likeBaskets: state => state.likeBaskets,
      likeMovies: state => state.likeMovies,
    }),
    ...mapState({
      userId: state => state.userId,
    })
  },
  created: function () {
    this.getProfile(this.userId) // 나중에 다른 회원 정보랑 분리해야됨
    // this.getFollowButtonName(this.profileInfo)
    // console.log(this.$route.params.userId)
    // console.log(this.userId)
    // if (this.$route.params.userId === this.userId) {
    //   this.getProfile(this.$route.params.userId)
    // }
    // this.profileId = this.$route.userId
    // this.getAuthorBaskets(this.$route.userId)
    this.profileId = this.userId
  }
}
</script>

<style>

</style>