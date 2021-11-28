<template>
  <div>
    <!-- <p>고른 영화: {{ pickedMovies }}</p>
    <b-button v-b-modal.modal-xl variant="primary">검색하기</b-button>
    <b-modal id="modal-xl" size="xl" title="p!ck movies">
      <movie-search-bar></movie-search-bar>
      <movie-search-result></movie-search-result>
    </b-modal> -->
    <movie-search-bar></movie-search-bar>
    <movie-search-result></movie-search-result>
  </div>
</template>

<script>
import MovieSearchBar from '@/components/Movie/MovieSearchBar'
import MovieSearchResult from '@/components/Movie/MovieSearchResult'

import { mapState } from 'vuex'

export default {
  name: 'SetMovieTaste',
  // data: function () {
  //   return {
  //     pickedMovies: []
  //   }
  // },
  components: {
    MovieSearchBar,
    MovieSearchResult,
  },
  computed: {
    ...mapState('movieStore', {
      pickedMovies: state => state.pickedMovies
    })
  },
}
</script>

<style>

</style>