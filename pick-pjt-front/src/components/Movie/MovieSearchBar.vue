<template>
  <div class="searchbar-container">
    <b-input
      class="searchbar d-inline-block"
      placeholder="영화 제목, 장르, 배우명을 검색해주세요."
      @keypress.enter="getMovieSearchResult"
    />
    <!-- 돋보기 이모티콘 추가 -->
  </div>
</template>

<script>
import { mapState, mapActions } from 'vuex'

export default {
  name: 'MovieSearchBar',
  methods: {
    ...mapActions('movieStore', [
      'getMovieSearchResult',
    ])
  },
  computed: {
    ...mapState('movieStore', [
      'userInput',
      'movies',
    ])
  },
}
</script>

<style>

</style>