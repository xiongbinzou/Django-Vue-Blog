<template>
  <div id="header">
    <div class="grid">
      <div></div>
      <h1>My Django REST framework-Vue Blog</h1>
      <search-button />
    </div>
    <hr>
    <div class="login">
      <div v-if="hasLogin">
        <div class="dropdown">
          <button class="dropbtn">欢迎，{{ username }}</button>
          <div class="dropdown-content">
            <router-link :to="{ name: 'UserCenter', params: { username: username } }">用户中心</router-link>
            <router-link :to="{ name: 'ArticleCreate' }" v-if="isSuperuser">发布文章</router-link>
            <router-link @click.prevent="logout()" :to="{ name: 'Home' }">注销</router-link>
          </div>
        </div>
      </div>
      <div v-else>
        <router-link to="/login" class="login-link">登录</router-link>
      </div>
    </div>
  </div>
</template>

<script>
import SearchButton from '@/components/SearchButton.vue'
import authorization from '@/utils/authorization'

export default {
  name: 'BlogHeader',
  data() {
    return {
      username: '',
      hasLogin: false,
      isSuperuser: JSON.parse(localStorage.getItem('isSuperuser.myblog'))
    }
  },
  components: {
    SearchButton
  },
  mounted() {
    authorization().then((data) => [this.hasLogin, this.username] = data)
  },
  methods: {
    logout() {
      localStorage.clear()
      window.location.reload(false)
    },
    refresh() {
      this.username = localStorage.getItem('username.myblog')
    }
  }
}
</script>

<style scoped>
#header {
  text-align: center;
  margin-top: 20px;
}

.grid {
  display: grid;
  grid-template-columns: 1fr 4fr 1fr;
}

.login {
  text-align: right;
  padding-right: 5px;
}

.dropbtn {
  background-color: mediumaquamarine;
  color: white;
  padding: 8px 8px 30px 8px;
  font-size: 16px;
  border: none;
  cursor: pointer;
  height: 16px;
  border-radius: 5px;
}

.dropdown {
  position: relative;
  display: inline-block;
}

.dropdown-content {
  display: none;
  position: absolute;
  background-color: #f9f9f9;
  min-width: 120px;
  box-shadow: 0 8px 16px 0 rgb(0, 0, 0, 0.2);
  text-align: center;
}

.dropdown-content a {
  color: black;
  padding: 12px 16px;
  text-decoration: none;
  display: block;
}

.dropdown-content a:hover {
  background-color: #f1f1f1;
}

.dropdown:hover .dropdown-content {
  display: block;
}

.dropdown:hover .dropbtn {
  background-color: darkslateblue;
}
</style>
