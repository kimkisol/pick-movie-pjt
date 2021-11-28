<template>
  <div class="mb-5">
    <div class="text-start d-flex align-items-center mt-2">
      <span class="me-2" style="color: #5a89cf; font-size: 0.8rem;">스포일러를 포함하기</span>
      <b-form-checkbox v-model="spoiler"></b-form-checkbox>
      <!-- <input type="checkbox" name="spoiler" style="border-color: #5a89cf;" v-model="spoiler"><br> -->
    </div>
    <b-row>
      <b-col md="10" class="me-0">
        <b-form-input v-model.trim="content"
          placeholder="댓글을 입력해주세요."
        ></b-form-input>
      </b-col>
      <b-col md="2" class="m-0" align="right">
        <b-button class="action-button px-3"
        @click="createAndErase({ content, spoiler })">등록</b-button>
      </b-col>
    </b-row>
      <!-- <button @click="createAndErase({ content, spoiler })" class="mb-3">등록하기</button> -->
  </div>
</template>

<script>
import { mapActions } from 'vuex'

export default {
  name: 'CommentForm',
  data: function () {
    return {
      content: '',
      spoiler: false,
    }
  },
  methods: {
    createAndErase: function ({ content, spoiler }) {
      this.createComment({ content, spoiler })
      this.content = ''
      this.spoiler = false
    },
    ...mapActions('basketStore', [
      'createComment',
    ]),
  },
}
</script>

<style>

</style>