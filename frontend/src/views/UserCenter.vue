<template>
  <blog-header ref="header" />
  <div id="user-center">
    <h3>更新资料信息</h3>
    <form>
      <div class="form-elem">
        <span>用户名：</span>
        <input type="text" v-model="username" placeholder="输入用户名">
      </div>
      <div class="form-elem">
        <span>新密码：</span>
        <input type="password" v-model="password" placeholder="输入密码">
      </div>
      <div class="form-elem">
        <button @click.prevent="changeInfo">更新</button>
      </div>
      <div class="form-elem">
        <button @click.prevent="showingDeleteAlert = true" class="delete-btn">删除用户</button>
        <div :class="{ shake: showingDeleteAlert }">
          <button v-if="showingDeleteAlert" class="confirm-btn" @click.prevent="confirmDelete">
            确定？
          </button>
        </div>
      </div>
    </form>
  </div>
  <blog-footer />
</template>

<script>
import axios from 'axios'
import BlogHeader from '@/components/BlogHeader.vue';
import BlogFooter from '@/components/BlogFooter.vue';
import authorization from '@/utils/authorization'

const storage = localStorage

export default {
  name: 'UserCenter',
  components: {
    BlogHeader,
    BlogFooter
  },
  data() {
    return {
      username: '',
      password: '',
      token: '',
      showingDeleteAlert: false
    }
  },
  mounted() {
    this.username = storage.getItem('username.myblog')
  },
  methods: {
    changeInfo() {
      authorization().then((resoponse) => {
        if (!resoponse[0]) {
          alert('登录已过期，请重新登录')
          return
        }
        console.log('Change info start')
        if (this.password.length > 0 && this.password.length < 6) {
          alert('Password too short')
          return
        }
        const oldName = storage.getItem('username.myblog')
        let data = {}
        if (this.username !== '') {
          data.username = this.username
        }
        if (this.password !== '') {
          data.password = this.password
        }
        this.token = storage.getItem('access.myblog')
        axios.patch('/api/user/' + oldName + '/', data, { headers: { Authorization: 'Bearer ' + this.token } }).then((response) => {
          const name = response.data.username
          storage.setItem('username.myblog', name)
          this.$router.push({ name: 'UserCenter', params: { username: name } })
          this.$refs.header.refresh()
        })
      })
    },
    confirmDelete() {
      authorization().then((response) => {
        if (response[0]) {
          this.token = storage.getItem('access.myblog')
          axios.delete('/api/user/' + this.username + '/', { headers: { Authorization: 'Bearer ' + this.token } }).then(() => {
            storage.clear()
            this.$router.push({ name: 'Home' })
          })
        }
      })
    }
  }
}

</script>

<style scoped>
#user-center {
  text-align: center;
}

.form-elem {
  padding: 10px;
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
  width: 200px;
}

.confirm-btn {
  width: 80px;
  background-color: darkorange;
}

.delete-btn {
  background-color: darkred;
  margin-bottom: 10px;
}

.shake {
  animation: shake 0.82s cubic-bezier(0.36, 0.07, 0.19, 0.97) both;
  transform: translate3d(0, 0, 0);
  backface-visibility: hidden;
  perspective: 1000px;
}

@keyframes shake {

  10%,
  90% {
    transform: translate3d(-1px, 0, 0);
  }

  20%,
  80% {
    transform: translate3d(2px, 0, 0);
  }

  30%,
  50%,
  70% {
    transform: translate3d(-4px, 0, 0);
  }

  40%,
  60% {
    transform: translate3d(4px, 0, 0);
  }
}
</style>
