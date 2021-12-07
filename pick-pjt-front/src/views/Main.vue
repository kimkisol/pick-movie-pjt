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
      >ck</p>
      <p class="d-inline-block ms-2">your taste</p>
    </div>
    <br><br>
    <basket-list></basket-list>
    <movie-list></movie-list>
  </div>
</template>

<script>
import MovieList from '@/components/Movie/MovieList.vue'
import BasketList from '@/components/Basket/BasketList.vue'

import { mapState, mapActions } from 'vuex'

export default {
  name: 'Main',
  components: {
    MovieList,
    BasketList,
  },
  methods: {
    ...mapActions('movieStore', [
      'getMovieRecommendation',
      'resetMovies',
    ]),
    ...mapActions('basketStore', [
      'getBasketRecommendation',
      'resetBaskets',
    ]),
  },
  computed: {
    ...mapState('MovieStore', {
      recommendedMovies: state => state.recommendedMovies,
    }),
    ...mapState('basketStore', {
      recommendedBaskets: state => state.recommendedBaskets,
    }),
  },
  created: function () {
    if (this.$store.getters.isLoggedIn) {
      this.resetBaskets('recommended')
      this.resetMovies('recommended')
      this.getBasketRecommendation()
      this.getBasketRecommendation()
      this.getMovieRecommendation()
    }
  }
}
</script>

<style>

</style>