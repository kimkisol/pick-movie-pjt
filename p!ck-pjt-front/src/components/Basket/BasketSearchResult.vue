<template>
  <div>
    <div class="mt-2 mb-5" v-if="query">
      <span class="strong-text fs-5">[{{ query }}]</span>
      <span class="ms-1 fs-6">검색어를 포함하는 </span>
      <span class="strong-text fs-5">{{ searchedBaskets.length }}</span>
      <span class="fs-6">개의 바스켓이 있습니다.</span>
    </div>
    <div class="basket-search-result row row-cols-3">
      <basket-list-item
        v-for="(basket, idx) in searchedBaskets"
        :basket="basket"
        :key="idx"
      ></basket-list-item>
    </div>
  </div>
</template>

<script>
import BasketListItem from '@/components/Basket/BasketListItem.vue'

import { mapState } from 'vuex'

export default {
  name: 'BasketSearchResult',
  components: {
    BasketListItem,
  },
  computed: {
    ...mapState('basketStore', {
      searchedBaskets: state => state.searchedBaskets,
      query: state => state.query,
    })
  },
}
</script>

<style>

</style>