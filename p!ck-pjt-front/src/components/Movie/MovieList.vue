<template>
  <div class="container">
    <div v-for="(movieListData, idx) in recommendedMovies"
      :movieListData="movieListData"
      :key="'movies' + idx">
      <div align="left" class="mt-2">
        <p class="d-inline-block strong-text" style="font-size:1.1em;">{{ movieListData.recommended_name }}</p>
        <p class="d-inline-block mx-1">{{ recommendedTail[idx] }}</p>
      </div>
      <b-card-group class="row row-cols-3 row-cols-lg-6">
        <movie-list-item v-for="(movie, idx) in movieListData.movies"
          :movie="movie"
          :key="'movie' + idx"
        ></movie-list-item>
      </b-card-group>
    </div>
    <b-modal id="modal-xl" size="xl" hide-footer>
      <movie-detail></movie-detail>
    </b-modal>
  </div>
</template>

<script>
import MovieListItem from './MovieListItem.vue'
import MovieDetail from '@/components/Movie/MovieDetail'

import { mapState } from 'vuex'

export default {
  name: 'MovieList',
  components: {
    MovieDetail,
    MovieListItem,
  },
  computed: {
    ...mapState('movieStore', {
      recommendedMovies: state => state.recommendedMovies,
      recommendedTail: state => state.recommendedTail,
    })
  }
}
</script>

<style>

</style>