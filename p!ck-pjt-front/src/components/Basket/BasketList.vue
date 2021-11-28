<template>
  <div class="container">
    <div v-for="(basketListData, idx) in recommendedBaskets"
      :basketListData="basketListData"
      :key="'baskets' + idx">
      <div align="left" class="mt-2">
        <p class="d-inline-block strong-text" style="font-size:1.1em;">{{ basketListData.recommended_name }}</p>
        <p class="d-inline-block mx-1">{{ recommendedTail[idx] }}</p>
      </div>
      <div>
        <div class="basket-search-result row row-cols-1 row-cols-md-2 row-cols-xl-3">
          <basket-list-item v-for="(basket, idx) in basketListData.baskets"
            :basket="basket"
            :key="'basket' + idx"
            class=""
          ></basket-list-item>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { mapState } from 'vuex'
import BasketListItem from './BasketListItem.vue'

export default {
  components: { BasketListItem },
  name: 'BasketList',
  computed: {
    ...mapState('basketStore', {
      recommendedBaskets: state => state.recommendedBaskets,
      recommendedTail: state => state.recommendedTail,
    })
  }
}
</script>

<style>

</style>
