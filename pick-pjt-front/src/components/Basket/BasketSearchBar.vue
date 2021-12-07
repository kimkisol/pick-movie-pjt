<template>
  <div class="searchbar-container">
    <b-input
      class="searchbar d-inline-block"
      placeholder="영화, 태그명, ... 등을 입력해주세요."
      @keypress.enter="getBasketSearchResult"
    />
    <!-- 돋보기 이모티콘 추가 -->
  </div>
</template>

<script>
import { mapState, mapActions } from 'vuex'

export default {
  name: 'BasketSearchBar',
  methods: {
    ...mapActions('basketStore', [
      'getBasketSearchResult',
    ])
  },
  computed: {
    ...mapState('basketStore', {
      baskets: state => state.baskets,
    })
  },
}
</script>

<style>

.searchbar-container {
  display: inline-block;
  width: 50%;
  padding: 35px;
}

</style>