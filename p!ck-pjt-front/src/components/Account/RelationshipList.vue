<template>
  <div>
    <ul>
      <b-row>
        <b-col md="7" align="right">
          <p class="mt-3 mb-0" style="font-size:0.8rem; color:#c4c4c4">선택한 친구를 이동시킬 그룹</p>
        </b-col>
        <b-col md="3" class="px-0">
          <b-form-select v-model="selectedGroup">
            <option disabled value="">선택</option>
            <option v-for="(group, idx) in groups" :key="idx" :value="group.id">{{ group.name }}</option>
          </b-form-select>
        </b-col>
        <b-col md="2" class="px-0">
          <b-button pill class="mini-button" @click="changeRelationshipGroup({ selectedRelationships, selectedGroup })">그룹 이동</b-button>
        </b-col>
      </b-row>
      <div class="mt-4">
        <b-table-simple small responsive>
          <b-thead>
            <b-tr>
              <b-th>✔</b-th>
              <b-th>닉네임</b-th>
              <b-th>그룹</b-th>
            </b-tr>
          </b-thead>
          <b-tbody style="font-size: 0.9rem;">
            <b-tr v-for="(relationship, idx) in filterRelationshipList(relationshipList, groupFilterId)" :key="idx">
              <b-td><input type="checkbox" :value="relationship.id" v-model="selectedRelationships"></b-td>
              <b-td>{{relationship.star.nickname}}</b-td>
              <b-td>{{relationship.group.name}}</b-td>
            </b-tr>
          </b-tbody>
        </b-table-simple>
      </div>
    </ul>
  </div>
</template>

<script>
import { mapState, mapActions } from 'vuex'

export default {
  name: 'RelationshipList',
  data: function () {
    return {
      selectedRelationships: [],
      selectedGroup: '',
    }
  },
  methods: {
    ...mapActions('accountStore', [
      'changeRelationshipGroup',
    ]),
    filterRelationshipList: function (relationshipList, groupFilterId) {
      return relationshipList.filter(relationship => {
        console.log(relationship.id)
        console.log(relationship.id === this.groupFilterId)
        if (groupFilterId === '전체') {
          return relationship
        } else {
          return relationship.group.id === this.groupFilterId
        }
      })
    }
  },
  computed: {
    ...mapState('accountStore', {
      relationshipList: state => state.relationshipList,
      groupFilterId: state => state.groupFilterId,
      groups: state => state.groups,
    })
  },
}
</script>

<style scoped>
  .group-btn {
    margin-left: 10px;
  }
</style>