<template>
  <div class="mt-5 container"><br>
    <div>
      <p class="d-inline-block"
      style="font-family: 'Hahmlet', serif; font-weight: 600; font-size: 1.6rem; color: #222222;"
      >p</p>
      <p class="d-inline-block"
      style="font-family: 'Hahmlet', serif; font-weight: 600; font-size: 1.6rem; color: #5a89cf;"
      >!</p>
      <p class="d-inline-block"
      style="font-family: 'Hahmlet', serif; font-weight: 600; font-size: 1.6rem; color: #222222;"
      >ck</p>
      <p class="d-inline-block ms-2">영화</p>
    </div>
    <!-- <movie-detail-modal v-if="isModalViewed" @close-modal="isModalViewed=false"></movie-detail-modal> -->
    <movie-search-bar class="mt-3"></movie-search-bar>
    <movie-search-result v-if="searchedMovies"></movie-search-result>
    <movie-list v-if="recommendedMovies"></movie-list>
  </div>
</template>

<script>
import MovieSearchBar from '@/components/Movie/MovieSearchBar.vue'
import MovieList from '@/components/Movie/MovieList.vue'
import MovieSearchResult from '@/components/Movie/MovieSearchResult.vue'

import { mapState, mapActions } from 'vuex'

export default {
  name: 'Movie',
  components: {
    MovieList,
    MovieSearchBar,
    MovieSearchResult,
  },
  methods: {
    ...mapActions('movieStore', [
      'resetMovies',
      'getMovieRecommendation',
      'resetMovies',
    ])
  },
  computed: {
    ...mapState('movieStore', {
      recommendedMovies: state => state.recommendedMovies,
      searchedMovies: state => state.searchedMovies,
    })
  },
  created: function () {
    if (this.$store.getters.isLoggedIn) {
      this.resetMovies('recommended')
      this.resetMovies('method')
      this.resetMovies('tail')
      for (let i = 0; i < 5; i++) {
        this.getMovieRecommendation()
      }
    }
  }
}
</script>

<style>

</style>