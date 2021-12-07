<template>
  <div class="container">
    <div class="mt-2 mb-5" v-if="query">
      <span class="strong-text fs-5">[{{ query }}]</span>
      <span class="ms-1 fs-6">검색어를 포함하는 </span>
      <span class="strong-text fs-5">{{ searchedMovies.length }}</span>
      <span class="fs-6">개의 영화가 있습니다.</span>
    </div>
    <div class="row row-cols-3 row-cols-sm-6">
      <movie-list-item
        v-for="(movie, idx) in searchedMovies"
        :movie="movie"
        :key="idx"
      ></movie-list-item>
    </div>
  </div>
</template>

<script>
import { mapState } from 'vuex'
import MovieListItem from '@/components/Movie/MovieListItem.vue'

export default {
  name: 'MovieSearchResult',
  components: {
    MovieListItem,
  },
  computed: {
    ...mapState('movieStore', {
      searchedMovies: state => state.searchedMovies,
      query: state => state.query,
    })
  },
}
</script>

<style>

</style>