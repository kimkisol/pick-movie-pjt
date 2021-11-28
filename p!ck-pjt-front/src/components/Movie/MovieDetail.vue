<template>
  <div id="detail-modal" class="container" style="background-color: white;">
    <b-card no-body class="overflow-hidden my-3" style="max-width:100vmax; background-color:#F9F9F9;" border-variant="light">
      <b-row g-1>
        <b-col md="3">
          <b-card-img :src="'https://image.tmdb.org/t/p/original/' + selectedMovieDetail.poster_path" alt="Poster"></b-card-img>
        </b-col>
        <b-col md="4">
          <p style="font-weight:600; font-size:1.8em;">{{ selectedMovieDetail.title }} ({{ selectedMovieDetail.release_date.split('-')[0] }})</p>
          <p style="font-weight:400; font-size:1.1em;">{{ selectedMovieDetail.runtime }}분</p>
          <div class="d-inline-block me-2" v-for="(genre, idx) in selectedMovieDetail.genres" :key="'genre' + idx">
            <p style="font-weight:400; font-size:1.1em;">{{ genre.name }}</p>
          </div><br>
          <div class="d-inline-block me-2" v-for="(actor, idx) in selectedMovieDetail.actors" :key="'actor' + idx">
            <p style="font-weight:400; font-size:1.1em;">{{ actor.name }}</p>
          </div>
        </b-col>
        <b-col md="5" class="mt-3 d-flex flex-column justify-content-between">
          <div>
            <p style="font-weight:500; font-size:1.2em;">⭐ {{ selectedMovieDetail.vote_average }}</p>
            <p style="font-weight:400; font-size:1em;">{{ selectedMovieDetail.overview }}</p>
          </div>
          <div>
            <div align="right">
              <div class="me-2">
                <p class="strong-text d-inline-block me-1">{{ likeCnt }}</p>
                <p class="d-inline-block">p!cks</p>
              </div>
              <button class="pick-button" v-show="likeButtonName === 'like'" @click="likeUnlike(selectedMovieDetail.id)">p!ck</button>
              <button class="unpick-button" v-show="likeButtonName === 'unlike'" @click="likeUnlike(selectedMovieDetail.id)">p!ck</button>
            </div>
          </div>
        </b-col>
      </b-row>
    </b-card>
    <hr>
    <p align="left" class="mt-2" style="font-weight:500; font-size:1.2em;">이 영화를 담고 있는 바스켓</p>
    <div class="row row-cols-3">
      <basket-list-item v-for="(basket, idx) in movieBaskets"
      :basket="basket"
      :key="'movieBaskets' + idx"
      class="mt-2"
      ></basket-list-item>
    </div>
    <!-- <p>{{ selectedMovieDetail }}</p> -->
    <!-- <p>좋아요 개수: {{ likeCnt }}</p>
    <button @click="likeUnlike(selectedMovieDetail.id)">{{ likeButtonName }}</button> -->
  </div>
</template>

<script>
import BasketListItem from '@/components/Basket/BasketListItem'

import { mapState, mapActions } from 'vuex'

export default {
  name: 'MovieDetail',
  components: {
    BasketListItem,
  },
  methods: {
    ...mapActions('movieStore', [
      'likeUnlike',
      'getLikeButtonName',
    ]),
  },
  computed: {
    ...mapState('movieStore', {
      selectedMovieDetail: state => state.selectedMovieDetail,
      likeButtonName: state => state.likeButtonName,
      likeCnt: state => state.likeCnt,
      movieBaskets: state => state.movieBaskets,
    })
  },
  created: function () {
    console.log('Movie getLikeButtonName')
    this.getLikeButtonName(this.selectedMovieDetail)
    console.log(this.LikeButtonName)
  }
}
</script>

<style>

template {
  background-color: #F9F9F9;
}

#detail-modal {
  font-family: 'Gothic A1', sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  color: #222222;
  background-color: #f9f9f9;
}

</style>