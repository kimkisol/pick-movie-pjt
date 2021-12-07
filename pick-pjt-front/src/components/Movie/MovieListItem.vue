<template>
  <div v-b-modal.modal-xl class="col" @click="getMovieDetail(movie)" style="cursor:pointer">
    <div class="card border-0" style="background-color:#F9F9F9;">
      <img class="card-img-top" :src="'https://image.tmdb.org/t/p/original/' + movie.poster_path" alt="poster">
      <div class="card-body px-0">
        <p class="fw-bold" align="left">{{ movie.title }}</p>
        <div class="d-flex justify-content-between">
          <p>{{ year }}</p>
          <p>⭐ {{ movie.vote_average }}</p>
        </div>
      </div>
    </div>
  </div>
</template>

<script>

import { mapActions, mapState } from 'vuex'

export default {
  name: 'MovieListItem',
  props: {
    movie: {
      type: Object,
    },
  },
  data: function () {
    return {
      year: this.movie.release_date.split('-')[0]
    } 
  },
  methods: {
    ...mapActions('movieStore', [
      'getMovieDetail',
      // 'checkPickedMovies',
    ])
  },
  computed: {
    ...mapState('movieStore', {
      pickedMovies: state => state.pickedMovies
    })
  }
}
</script>

<style>

.card-img-top {
  height: 15rem;
  object-fit: cover;
}

</style>