<template>
  <div>
    <b-row>
      <b-col md="9" class="pe-0">
        <b-form-input
          type="text"
          v-model.trim="name"
          placeholder="생성할 그룹명을 입력해주세요."
          @keypress.enter="callCreateGroup"
        ></b-form-input>
      </b-col>
      <b-col md="3" class="px-0">
        <b-button pill class="mini-button" @click="callCreateGroup">그룹 생성</b-button>
      </b-col>
    </b-row>
  </div>
</template>

<script>
import { mapActions } from 'vuex'

export default {
  name: 'CreateGroup',
  data: function () {
    return {
      name: '',
    }
  },
  methods: {
    ...mapActions('accountStore', [
      'createGroup',
    ]),
    callCreateGroup: function() {
      this.createGroup(this.name)
      this.name = ''
    }
  }
}
</script>