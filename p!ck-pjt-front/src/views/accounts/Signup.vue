<template>
  <div class="container mt-5">
    <div><br>
      <p class="d-inline-block"
      style="font-family: 'Hahmlet', serif; font-weight: 600; font-size: 1.6rem; color: #222222;"
      >회원가입</p>
    </div>
    <div class="input-signup">
      <label for="username" class="d-flex">아이디</label>
      <b-form-input
        id="username"
        type="text"
        v-model="credentials.username"
        placeholder="아이디를 입력해주세요."></b-form-input>
      <b-alert show variant="warning" style="text-align:start;"
        v-if="isInvalid && isDuplicatedId && credentials.username === duplicatedId">
        이 아이디는 중복된 아이디입니다.</b-alert>
      <b-alert show variant="warning" style="text-align:start;"
        v-if="isInvalid && credentials.username === ''">
        아이디는 필수 값입니다.</b-alert>
    </div>
    <div class="input-signup">
      <label for="password" class="d-flex">비밀번호</label>
      <b-form-input
        id="password"
        type="password"
        v-model="credentials.password"
        placeholder="비밀번호를 입력해주세요."></b-form-input>
    </div>
    <div class="input-signup">
      <label for="passwordConfirmation" class="d-flex">비밀번호 확인</label>
      <b-form-input
        id="passwordConfirmation"
        type="password"
        v-model="credentials.passwordConfirmation"
        placeholder="비밀번호를 다시 입력해주세요."></b-form-input>
      <b-alert show variant="warning" style="text-align:start;"
        v-if="credentials.passwordConfirmation && (credentials.password != credentials.passwordConfirmation)">
        비밀번호가 일치하지 않습니다. 다시 입력해주세요.</b-alert>
    </div>
    <div class="input-signup">
      <label for="nickname" class="d-flex">닉네임</label>
      <b-form-input
        id="nickname"
        type="text"
        v-model="credentials.nickname"
        placeholder="서비스 내에서 사용할 닉네임을 입력해주세요."></b-form-input>
      <b-alert show variant="warning" style="text-align:start;"
        v-if="isInvalid && isDuplicatedNickname && credentials.nickname === duplicatedNickname">
        이 아이디는 중복된 닉네임입니다.</b-alert>
      <b-alert show variant="warning" style="text-align:start;"
        v-if="isInvalid && credentials.nickname === ''">
        닉네임은 필수 값입니다.</b-alert>
    </div>
    <div class="input-signup">
      <label for="birthdate" class="d-flex">생년월일</label>
      <b-form-input id="birthdate" type="date" v-model="credentials.birthdate" class="mb-2"></b-form-input>
      <b-alert show variant="warning" style="text-align:start;"
        v-if="isInvalid && credentials.birthdate === ''">
        생년월일은 필수 값입니다.</b-alert>
    </div>
    <div class="input-signup">
      <b-form-group label="성별" align="left" style="font-weight:600;">
        <b-form-radio-group
          v-model="credentials.gender"
          buttons
          button-variant="outline-secondary"
          class="mx-n1"
          align="left"
        ><template v-for="genderOption in genderOptions">
            <b-form-radio :value="genderOption.value" :key="genderOption.text" class="rounded-pill mx-1">
              {{ genderOption.text }}
            </b-form-radio>
          </template>
        </b-form-radio-group>
      </b-form-group>
      <b-alert show variant="warning" style="text-align:start;"
       v-if="isInvalid && credentials.gender === ''">
        성별은 필수 값입니다.</b-alert>
    </div>
    <b-button class="action-button m-4" @click="check">가입하기</b-button>
  </div>
</template>

<script>
import { mapActions, mapState } from 'vuex'

export default {
  name: 'Signup',
  data: function () {
    return {
      genderOptions: [
        { text: '남', value: 1 },
        { text: '여', value: 2 },
      ],
      credentials: {
        username: '',
        password: '',
        passwordConfirmation: '',
        nickname: '',
        birthdate: '',
        gender: '',
      },
      isInvalid: false,
      isDuplicatedId: false,
      duplicatedId: '',
      isDuplicatedNickname: false,
      duplicatedNickname: '',
    }
  },
  methods: {
    ...mapActions([
      'signup',
    ]),
    check: function () {
      this.signup(this.credentials)
      this.isInvalid = true
      let flag1 = false
      let flag2 = false
      for (let i of Object.keys(this.userInfo)) {
        if (this.userInfo[i].username === this.credentials.username) {
          this.isDuplicatedId = true
          flag1 = true
          this.duplicatedId = this.credentials.username
        }
        if (this.userInfo[i].nickname === this.credentials.nickname) {
          this.isDuplicatedNickname = true
          flag2 = true
          this.duplicatedNickname = this.credentials.nickname
        }
      }
      if (flag1 === false) {
        this.isDuplicatedId = false
      }
      if (flag2 === false) {
        this.isDuplicatedNickname = false
      }
    }
  },
  computed: {
    ...mapState([
      'userInfo'
    ])
  }
}
</script>

<style>

.input-signup {
  display: block;
  padding: 35px;
}

.input-signup label {
  font-weight: 600;
}

</style>