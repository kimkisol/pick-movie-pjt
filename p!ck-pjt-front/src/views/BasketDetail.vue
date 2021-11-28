<template>
  <div class="container my-5">
    <!-- 바스켓 소개 -->
    <div class="card border-light bg-light">
      <!-- 프로필, 바스켓삭제 -->
      <div class="d-flex justify-content-between mb-3">
        <div class="container d-flex align-items-center">
          <b-avatar src="@/assets/profile-image.png" size="4rem;"></b-avatar>
          <div class="ms-2" align="left">
            <p @click="getProfile(selectedBasketDetail.author)"
              class="mb-1"
              style="cursor:pointer; font-family:'Hahmlet', serif; font-weight:600; font-size: 1.1rem;"
            >{{ userInfo[selectedBasketDetail.author].nickname }}</p>
            <p class="mb-0" style="font-size: 0.9rem;">팔로워 {{ userInfo[selectedBasketDetail.author].fans.length }}명</p>
          </div>
        </div>
        <b-button @click="deleteBasket(selectedBasketDetail)"
          v-if="userId === selectedBasketDetail.author"
          style="width:10vw; font-size:0.95rem; border:none; color:#5a89cf; background-color:transparent; text-decoration:underline;"
        >바스켓 삭제</b-button>
      </div>
      <!-- 이미지 -->
      <div class="row">
        <div class="card col-6 border-light  bg-light" style="max-width: 400px;">
          <div v-if="selectedBasketDetail.movies.length > 3">
            <div class="container">
              <div class="row row-cols-2 m-0 p-0">
                <div class="imgContainer2 col m-0 p-0" v-for="(movie, idx) in selectedBasketDetail.movies.slice(0,4)" :key="'selectedMovie' + idx">
                  <img :src="'https://image.tmdb.org/t/p/original/' + movie.poster_path" alt="poster" class="image">
                </div>
              </div>
            </div>
          </div>
        </div>
        <div class="card col border-light bg-light d-flex justify-content-between" align="left">
          <div>
            <div v-if="selectedBasketDetail.public === true" class="public-button d-flex align-items-center justify-content-center">공개</div>
            <div v-else class="public-button d-flex align-items-center justify-content-center">비공개</div>
            <p class="my-2" style="font-weight:600; font-size:1.4em;">{{ selectedBasketDetail.title }}</p>
            <!-- 태그 -->
            <div class="d-flex">
              <div v-for="(basket_tag, idx) in selectedBasketDetail.baskets_tags"
                :key="'basket' + idx"
                class="tag-button d-flex align-items-center justify-content-center px-3 me-2"
              >{{ basket_tag.name }}</div>
            </div>
            <!-- 설명 -->
            <p class="my-3">{{ selectedBasketDetail.explanation }}</p>
            <!-- <div v-if="selectedBasketDetail.public === true">
              <p>이 바스켓을 좋아하는 {{ selectedBasketDetail.like_users.length }}명</p>
              <span v-for="(like_user, idx) in selectedBasketDetail.like_users" :key="'like_user' + idx">{{ userInfo[like_user.id].nickname }} </span>
            </div>
            <div v-else>
              <p>이 바스켓에 참여중인 {{ selectedBasketDetail.participants.length }}명</p>
              <div>
                <span v-for="(participant, idx) in selectedBasketDetail.participants" :key="'participant' + idx">{{ userInfo[participant.id].nickname }} </span>
              </div>
            </div> -->
          </div>
          <!-- p!ck 버튼 -->
          <div align="right">
            <div class="me-2">
              <p class="strong-text d-inline-block me-1 mb-1">{{ likeCnt }}</p>
              <p class="d-inline-block mb-1">p!cks</p>
            </div>
            <button class="pick-button" v-if="likeButtonName === 'like'" @click="likeUnlike(selectedBasketDetail.id)">p!ck</button>
            <button class="unpick-button" v-if="likeButtonName === 'unlike'" @click="likeUnlike(selectedBasketDetail.id)">p!ck</button>
          </div>
        </div>
      </div>
    </div>
    <!-- 영화 -->
    <br><hr>
    <div class="container mt-4">
      <div align="left">
        <p class="d-inline-block" style="font-size: 1.2rem;">이 바스켓의</p>
        <p class="d-inline-block ms-1"
        style="font-family: 'Hahmlet', serif; font-weight: 600; font-size: 1.2rem; color: #5a89cf;"
        >영화 리스트</p>
      </div>
      <b-card-group class="row row-cols-3 row-cols-lg-6">
        <movie-list-item
          v-for="(movie, idx) in selectedBasketDetail.movies"
          :movie="movie"
          :key="'movie' + idx"
        ></movie-list-item>
      </b-card-group>
      <b-modal id="modal-xl" size="xl" hide-footer>
        <movie-detail></movie-detail>
      </b-modal>
    </div>
    <!-- 테이스팅 홀 -->
    <br><hr class="mt-0">
    <div class="d-flex justify-content-between align-items-center">
      <div align="left">
        <p class="d-inline-block pt-3" style="font-size: 1.2rem;">영화와 취향 이야기를 나누는</p>
        <p class="d-inline-block ms-1"
        style="font-family: 'Hahmlet', serif; font-weight: 600; font-size: 1.2rem; color: #5a89cf;"
        >테이스팅 홀</p>
      </div>
      <b-form-checkbox @change="setSpoilerFilter(showSpoiler)" v-model="showSpoiler" name="spoiler-button" switch class="d-inline-block">
      스포일러 보기
      </b-form-checkbox>
    </div>
    <span class="card p-4 border-light">
      <comment-list></comment-list>
    </span>
  </div>
</template>

<script>
import CommentList from '@/components/Basket/CommentList.vue'


import { mapState, mapActions } from 'vuex'
import MovieDetail from '@/components/Movie/MovieDetail'
import MovieListItem from '../components/Movie/MovieListItem.vue'

export default {
  name: 'BasketDetail',
  data: function () {
    return {
      showSpoiler: false,
    }
  },
  components: {
    CommentList,
    MovieDetail,
    MovieListItem,
  },
  methods: {
    ...mapActions('basketStore', [
      'setSpoilerFilter',
      'likeUnlike',
      'getLikeButtonName',
      'updateBasket',
      'deleteBasket',
    ]),
    ...mapActions('accountStore', [
      'getProfile',
    ]),
  },
  computed: {
    ...mapState('basketStore', {
      selectedBasketDetail: state => state.selectedBasketDetail,
      showSpoilerOption: state => state.showSpoilerOption,
      likeButtonName: state => state.likeButtonName,
      likeCnt: state => state.likeCnt,
    }),
    ...mapState({
      userId: state => state.userId,
      userInfo: state => state.userInfo
    })
  },
  created: function () {
    this.getLikeButtonName(this.selectedBasketDetail)
  },
}
</script>

<style>
hr {
  height: 5px;
  background-color:#5a89cf;
  border: 0px;
}

.imgContainer2 {
  width: 200px;
  height: 200px;
  overflow: hidden;
}
.imgContainer2 > img {
  width: 100%;
  object-fit: fill;
  /* height: 200px; */
}

.public-button {
  width: 65px;
  height: 25px;
  color: #ffffff;
  background-color: #5a89cf;
  border-color: #5a89cf;
  font-weight: 600;
  font-size: 0.8rem;
  /* text-align: center;
  vertical-align:middle; */
  border-radius: 75px;
}

.tag-button {
  height: 25px;
  color: #5a89cf;
  display: inline-block;
  background-color: transparent;
  border-style: solid;
  border-width: 1px;
  border-color: #5a89cf;
  font-weight: 600;
  font-size: 0.8rem;
  border-radius: 75px;
}

</style>