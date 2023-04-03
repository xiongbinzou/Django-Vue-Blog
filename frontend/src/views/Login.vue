<template>
  <blog-header />

  <div id="grid">
    <div id="signup">
      <h3>注册账号</h3>
      <form>
        <div class="form-elem">
          <span class="label">账号：</span>
          <input type="text" v-model="signupName" placeholder="输入用户名">
        </div>
        <div class="form-elem">
          <span class="label">密码：</span>
          <input type="password" v-model="signupPwd" placeholder="输入密码">
        </div>
        <div class="form-elem">
          <span class="label">确认密码：</span>
          <input type="password" v-model="signupPwdConfirm" placeholder="再次输入密码">
        </div>
        <div class="form-elem">
          <button @click.prevent="signup">提交</button>
        </div>
      </form>
    </div>
    <div id="signin">
      <h3>登录账号</h3>
      <form>
        <div class="form-elem">
          <span class="label">账号：</span>
          <input type="text" v-model="signinName" placeholder="输入用户名">
        </div>
        <div class="form-elem">
          <span class="label">密码：</span>
          <input type="password" v-model="signinPwd" placeholder="输入密码">
        </div>
        <div class="form-elem">
          <button @click.prevent="signin">登录</button>
        </div>
      </form>
    </div>
  </div>

  <blog-footer />
</template>


<script>
import axios from 'axios'
import BlogHeader from '@/components/BlogHeader.vue';
import BlogFooter from '@/components/BlogFooter.vue';

export default {
  name: "Login",
  components: { BlogHeader, BlogFooter },
  data() {
    return {
      signupName: '',
      signupPwd: '',
      signupPwdConfirm: '',
      signinName: '',
      signinPwd: '',
      signupResponse: null,
    }
  },
  methods: {
    signup() {
      if (this.signupPwd !== this.signupPwdConfirm) {
        alert("两次密码不一致，请重新输入!")
        return
      }
      axios.post('/api/user/', {
        username: this.signupName,
        password: this.signupPwd,
      }).then((response) => {
        this.signupResponse = response.data
        alert('用户注册成功')
      }).catch((error) => {
        alert('用户注册失败:', error.message)
      })
    },
    signin() {
      axios.post('/api/token/', {
        username: this.signinName,
        password: this.signinPwd,
      }).then((response) => {
        const storage = localStorage
        const expiredTime = Date.parse(response.headers.date) + 10800000
        storage.setItem('access.myblog', response.data.access)
        storage.setItem('refresh.myblog', response.data.refresh)
        storage.setItem('expiredTime.myblog', expiredTime)
        storage.setItem('username.myblog', this.signinName)
        axios.get('/api/user/' + this.signinName + '/').then((response) => {
          storage.setItem('isSuperuser.myblog', response.data.is_superuser)
          this.$router.push({ name: 'Home' })
        })
      }).catch((error) => {
        alert('用户登录失败:', error.message)
      })
    }
  }
}

</script>

<style scoped>
#grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
}

#signup {
  text-align: center;
}

#signin {
  text-align: center;
}

.form-elem {
  padding: 10px;
}

.label {
  display: inline-block;
  width: 80px;
  text-align: justify;
  text-align-last: justify;
  margin-right: 1px;
}

input {
  height: 25px;
  padding-left: 10px;
}

button {
  height: 35px;
  cursor: pointer;
  border: none;
  outline: none;
  background: gray;
  color: whitesmoke;
  border-radius: 5px;
  width: 60px;
}
</style>
