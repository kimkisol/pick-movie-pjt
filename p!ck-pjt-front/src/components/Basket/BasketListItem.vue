<template>
  <div class="container mb-4 col">
    <div class="card p-3 bg-light h-100">
      <div class="row">
        <div class="card col-6 border-light bg-light p-0" style="max-width: 230px; cursor:pointer;" @click="getBasketDetail(basket)">
          <div v-if="basket.movies.length > 3">
            <div class="container pe-0">
              <div class="row row-cols-2 m-0 p-0">
                <div class="imgContainer col m-0 p-0" v-for="(movie, idx) in basket.movies.slice(0,4)" :key="idx">
                  <img :src="'https://image.tmdb.org/t/p/original/' + movie.poster_path" alt="poster" class="image">
                </div>
              </div>
            </div>
          </div>
        </div>
        <div class="card col d-flex d-column justify-content-between me-1 border-light bg-light px-3" align="left">
          <div class="ms-2">
            <span @click="getBasketDetail(basket)" style="cursor:pointer; font-size:1.1rem;" class="fw-bold">{{ basket.title }}</span><br>
            <span @click="getProfile(basket.author)" style="cursor:pointer; color:grey;">{{ userInfo[basket.author].nickname }}</span>
            <!-- 태그 -->
            <!-- <div class="d-flex">
              <div v-for="(basket_tag, idx) in basket.baskets_tags"  :key="'basket' + idx" class="">{{ basket_tag.name }}</div>
            </div> -->
            <div class="container">
              <div class="card row border-light bg-light pick-text">
                <div v-for="(basket_tag, idx) in basket.baskets_tags.slice(0,3)"
                  :key="'basket' + idx"
                  class="col p-0"
                >
                #{{ basket_tag.name }}
                </div>
              </div>
            </div>
          </div>
          <div align="right">
            <div class="">
              <span class="strong-text d-inline-block me-1">{{ basket.like_users.length }}</span>
              <span class="d-inline-block">p!cks</span>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { mapActions, mapState } from 'vuex'

export default {
  name: 'BasketListItem',
  props: {
    basket: {
      type: Object,
    },
  },
  methods: {
    ...mapActions('basketStore', [
      'getBasketDetail',
    ]),
    ...mapActions('accountStore', [
      'getProfile',
    ]),
  },
  computed: {
    ...mapState({
      userInfo: state => state.userInfo
    })
  }
}
</script>

<style>
/* * {
  background: grey;
} */

.imgContainer {
  width: 100px;
  height: 100px;
  overflow: hidden;
}
.imgContainer > img {
  width: 100%;
  object-fit: fill;
  /* height: 200px; */
}
</style>