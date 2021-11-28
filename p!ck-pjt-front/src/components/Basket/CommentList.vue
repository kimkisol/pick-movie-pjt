<template>
  <div class="container">
    <comment-form></comment-form>
    <div v-if="showSpoilerOption">
      <div v-for="(comment, idx) in comments" :comment="comment" :key="'spoilered' + idx" class="mb-1">
        <span class="d-flex justify-content-between">
          <div class="d-flex">
            <p class="me-4" @click="getProfile(comment.author)" style="cursor:pointer; font-weight:600;">{{ userInfo[comment.author].nickname }}</p>
            <p>{{ comment.content }}</p>
          </div>
          <div class="d-flex">
            <p class="me-3">{{ comment.created_at.split('T')[0] }}</p>
            <button @click="deleteComment(comment)"
              v-show="comment.author === userId"
              class="mb-3 px-1 py-0"
              style="border: none; background-color: transparent; color: #5a89cf;"
            >x</button>
          </div>
        </span>
      </div>
    </div>
    <div v-else>
      <div v-for="(comment, idx) in comments" :comment="comment" :key="'notSpoilered' + idx" class="mb-1">
        <div v-if="comment.spoiler === true && comment.author !== userId"> <!--  && comment.author !== userId -->
          <span class="d-flex justify-content-between">
            <div class="d-flex">
              <p class="me-4" @click="getProfile(comment.author)" style="cursor:pointer; font-weight:600;">{{ userInfo[comment.author].nickname }}</p>
              <p>이 댓글은 스포일러가 포함된 댓글입니다.</p>
            </div>
            <div class="d-flex justify-content-end">
              <p class="me-0">{{ comment.created_at.split('T')[0] }}</p>
              <button class="mb-3 px-1 py-0"
                  style="border: none; background-color: transparent; color: transparent;"
                >x</button>
            </div>
          </span>
        </div>
        <div v-else>
          <span class="d-flex justify-content-between">
            <div class="d-flex">
              <p class="me-4" @click="getProfile(comment.author)" style="cursor:pointer; font-weight:600;">{{ userInfo[comment.author].nickname }}</p>
              <p>{{ comment.content }}</p>
            </div>
            <div class="d-flex">
              <p class="me-3">{{ comment.created_at.split('T')[0] }}</p>
              <button @click="deleteComment(comment)"
                v-show="comment.author === userId"
                class="mb-3 px-1 py-0"
                style="border: none; background-color: transparent; color: #5a89cf;"
              >x</button>
            </div>
          </span>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import CommentForm from '@/components/Basket/CommentForm.vue'

import { mapState, mapActions } from 'vuex'

export default {
  name: 'CommentList',
  components: {
    CommentForm,
  },
  methods: {
    ...mapActions('basketStore', [
      'getCommentList',
      'deleteComment'
    ]),
    ...mapActions('accountStore', [
      'getProfile',
    ])
  },
  computed: {
    ...mapState('basketStore', {
      comments: state => state.comments,
      noSpoilerComments: state => state.noSpoilerComments,
      showSpoilerOption: state => state.showSpoilerOption,
    }),
    ...mapState({
      userInfo: state => state.userInfo,
      userId: state => state.userId,
    }),
  },
  created: function () {
    this.getCommentList()
  },
  // updated: function () {
  //   this.getCommentList()
  // },
}
</script>

<style>

</style>