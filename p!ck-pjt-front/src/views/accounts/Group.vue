<template>
  <div class="container mt-5"><br>
    <div>
      <p class="d-inline-block"
      style="font-family: 'Hahmlet', serif; font-weight: 600; font-size: 1.6rem; color: #222222;"
      >{{ userInfo[userId].nickname }}</p>
      <p class="d-inline-block ms-1">님의 팔로잉 그룹 관리</p>
    </div>
    <b-row class="mt-5">
      <b-col md="5">
        <create-group></create-group>
        <group-list></group-list>
      </b-col>
      <b-col md="7">
        <relationship-list></relationship-list>
      </b-col>
    </b-row>
  </div>
</template>

<script>
import CreateGroup from '../../components/Account/CreateGroup.vue'
import GroupList from '../../components/Account/GroupList.vue'
import RelationshipList from '../../components/Account/RelationshipList.vue'

import { mapState } from 'vuex'

export default {
  name: 'Group',
  components: { GroupList, RelationshipList, CreateGroup },
  computed: {
    ...mapState({
      userId: state => state.userId,
      userInfo: state => state.userInfo,
    })
  }
}
</script>

<style>

</style>