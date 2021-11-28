<template>
  <div id="app" class="container-fluid">
      <nav class="navbar navbar-expand-lg navbar-light bg-light">
        <div class="container-fluid">
          <router-link class="text-decoration-none" style="color:#222222;" :to="{ name: 'Main' }">
            <img src="@/assets/logo.png" alt="p!ck logo" width="75px" class="d-inline-block" style="vertical-align:-0.6em;"/> your taste
          </router-link>
          <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarNav" aria-controls="navbarNav" aria-expanded="false" aria-label="Toggle navigation">
            <span class="navbar-toggler-icon"></span>
          </button>
          <div class="collapse navbar-collapse" id="navbarNav">
            <ul class="navbar-nav ms-auto" v-if="isLoggedIn">
              <li class="nav-item mx-2 mt-2">
                <router-link class="nav-link" :to="{ name: 'Main' }">홈</router-link>
              </li>
              <li class="nav-item mx-2 mt-2">
                <router-link class="nav-link" :to="{ name: 'Movie' }">영화</router-link>
              </li>
              <li class="nav-item mx-2 mt-2">
                <router-link class="nav-link" :to="{ name: 'Basket' }">바스켓</router-link>
              </li>
              <li class="nav-item mx-2 mt-3">
                <router-link :to="{ name: 'MyProfile' }" style="color:#5a89cf;">{{ userInfo[userId].nickname }}</router-link> 님, 환영합니다!
              </li>
              <li class="nav-item dropdown mx-2">
                <a class="nav-link dropdown-toggle" href="#" id="navbarDropdownMenuLink" role="button" data-bs-toggle="dropdown" aria-expanded="false">
                  <b-avatar src="@/assets/profile-image.png"></b-avatar>
                </a>
                <ul class="dropdown-menu dropdown-menu-right" aria-labelledby="navbarDropdownMenuLink">
                  <li class="nav-item mx-3 my-2"><router-link style="color:#5a89cf;" :to="{ name: 'MyProfile' }">내 프로필</router-link></li>
                  <li class="nav-item mx-3 my-2"><router-link style="color:#5a89cf;" :to="{ name: 'Group' }">그룹 관리</router-link></li>
                  <li class="nav-item mx-3 my-2"><router-link style="color:#5a89cf;" @click.native="logout" to="#">로그아웃</router-link></li>
                </ul>
              </li>
            </ul>
            <ul class="navbar-nav ms-auto" v-else>
              <li class="nav-item mx-2 mt-3">
                <router-link style="color:#5a89cf;" :to="{ name: 'Login' }">[로그인 후 이용 부탁 드립니다.]</router-link>
              </li>
              <li class="nav-item dropdown mx-2">
                <a class="nav-link dropdown-toggle" href="#" id="navbarDropdownMenuLink" role="button" data-bs-toggle="dropdown" aria-expanded="false">
                  <b-avatar src="@/assets/profile-image.png"></b-avatar>
                </a>
                <ul class="dropdown-menu dropdown-menu-right" aria-labelledby="navbarDropdownMenuLink">
                  <li class="nav-item mx-3 my-2"><router-link style="color:#5a89cf;" :to="{ name: 'Signup' }">회원가입</router-link></li>
                  <li class="nav-item mx-3 my-2"><router-link style="color:#5a89cf;" :to="{ name: 'Login' }">로그인</router-link></li>
                </ul>
              </li>
            </ul>
          </div>
        </div>
      </nav>
      <img id="line" src="@/assets/navbar.png" width="vw" alt="line" class="wave-line m-0 p-0">
    <router-view/>
  </div>
</template>

<script>
import { mapGetters, mapActions, mapState } from 'vuex'

export default {
  name: 'App',
  methods: {
    ...mapActions([
      'logout',
      'getUserId',
      'setUserInfo',
      // 'getMovieData'
      ]),
    ...mapActions('accountStore', [
      'getProfile',
    ]),
    unLoadEvent: function (event) {
      if (this.canLeaveSite) return
      this.logout()
      event.preventDefault()
      event.returnValue = ''
    },
  },
  computed: {
    ...mapGetters([
      'isLoggedIn',
    ]),
   ...mapState({
      userId: state => state.userId, // 얘가 왜 계속 사라지는건가??
      userInfo: state => state.userInfo,
    })
  },
  created: function () {
    this.getUserId()
    this.setUserInfo()
  },
  mounted() {
    window.addEventListener('beforeunload', this.unLoadEvent);
  },
  beforeUnmount() {
    window.removeEventListener('beforeunload', this.unLoadEvent);
  },
}
</script>


<style>

#app {
  font-family: 'Gothic A1', sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #222222;
  background-color: #f9f9f9;
}

#nav {
  padding: 35px;
}

#nav a {
  font-size: 95%;
  font-weight: 600;
  color: #222222;
  margin: 30px;
}

#line {
  position: absolute;
  top: 50px; left: 0px;
  width: 100%;
  z-index: 10;
}

#nav a.router-link-exact-active {
  color: #5a89cf;
}

.strong-text {
  font-family: 'Hahmlet', serif;
  font-weight: 600;
  color: #5a89cf;
}

.pick-text {
  color: #5a89cf;
}

.action-button {
  font-family: 'Hahmlet', serif;
  font-weight: 500;
  color: #ffffff;
  background-color: #5a89cf !important;
  border-color: #5a89cf !important;
}

.action-button-transparent {
  font-family: 'Hahmlet', serif;
  font-weight: 500;
  color: #c4c4c4;
  background-color: transparent !important;
  border-color: #c4c4c4 !important;
}

.action-button-gray {
  font-family: 'Hahmlet', serif;
  font-weight: 500;
  color: #ffffff;
  background-color: #c4c4c4 !important;
  border-color: #c4c4c4 !important;
}

.mini-button {
  font-family: 'Gothic A1', sans-serif;
  font-weight: 500;
  color: #5a89cf !important;
  background-color: transparent !important;
  border-color: #5a89cf !important;
}

.pick-button {
  font-family: 'Hahmlet', serif;
  font-weight: 700;
  font-size: 1.1rem;
  color: #ffffff;
  background-color: #5a89cf !important;
  border-color: #5a89cf !important;
  width:60px;
  height:60px;
  border-radius:75px;
  text-align:center;
  margin:0 auto;
  vertical-align:middle;
  border: none;
}

.unpick-button {
  font-family: 'Hahmlet', serif;
  font-weight: 700;
  font-size: 1.1rem;
  color: #ffffff;
  background-color: #c4c4c4 !important;
  border-color: #c4c4c4 !important;
  width:60px;
  height:60px;
  border-radius:75px;
  text-align:center;
  margin:0 auto;
  vertical-align:middle;
  border: none;
}

b-modal {
  background-color: #ffffff;
}

.card-box {
  display: flex;
  justify-content: space-between;
  margin: 0 70px;
  margin-top: 65px;
  flex-wrap: wrap;
}

</style>
