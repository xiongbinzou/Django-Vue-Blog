<template>
  <blog-header />
  <div id="article-create">
    <h3>更新文章</h3>
    <form>
      <div class="form-elem">
        <span>标题：</span>
        <input type="text" v-model="title" placeholder="输入标题">
      </div>
      <div class="form-elem">
        <span>分类：</span>
        <span v-for="category in categories" :key="category.id">
          <button class="category-btn" :style="categoryStyle(category)" @click.prevent="chooseCategory(category)">
            {{ category.title }}
          </button>
        </span>
      </div>
      <div class="form-elem">
        <span>标签：</span>
        <input type="text" v-model="tags" placeholder="输入标签，用逗号分隔">
      </div>
      <div class="form-elem">
        <span>正文：</span>
        <textarea v-model="body" placeholder="输入正文" cols="80" rows="20"></textarea>
      </div>
      <div class="form-elem">
        <button @click.prevent="submit">提交</button>
      </div>
      <div class="form-elem">
        <button @click.prevent="deleteArticle" style="background-color: darkred;">删除</button>
      </div>
    </form>
  </div>
  <blog-footer />
</template>


<script>
import BlogHeader from '@/components/BlogHeader.vue'
import BlogFooter from '@/components/BlogFooter.vue'
import axios from 'axios'
import authorization from '@/utils/authorization'

export default {
  name: 'ArticleEdit',
  components: {
    BlogHeader,
    BlogFooter,
  },
  data() {
    return {
      title: '',
      body: '',
      categories: [],
      selectedCategory: null,
      tags: '',
      articleID: null,
    }
  },
  mounted() {
    axios.get('/api/category/').then(response => this.categories = response.data)
    axios.get('/api/article/' + this.$route.params.id + '/').then((response) => {
      this.title = response.data.title
      this.body = response.data.body
      this.selectedCategory = response.data.category
      this.tags = response.data.tags.join(',')
      this.articleID = response.data.id
    })
  },
  methods: {
    categoryStyle(category) {
      if (this.selectedCategory !== null && category.id === this.selectedCategory.id) {
        return {
          backgroundColor: 'black',
        }
      }
      return {
        backgroundColor: 'lightgrey',
        color: 'black'
      }
    },
    chooseCategory(category) {
      if (this.selectedCategory !== null && category.id == this.selectedCategory.id) {
        this.selectedCategory = null
      } else {
        this.selectedCategory = category
      }
    },
    submit() {
      authorization().then((response) => {
        if (response[0]) {
          let data = {
            title: this.title,
            body: this.body
          }

          data.category_id = this.selectedCategory ? this.selectedCategory.id : null
          data.tags = this.tags.split(/[,，]/).map(x => x.trim()).filter(x => x.charAt(0) !== '')
          const token = localStorage.getItem('access.myblog')
          axios.put('/api/article/' + this.articleID + '/', data, { headers: { Authorization: 'Bearer ' + token } }).then((response) => {
            this.$router.push({ name: 'ArticleDetail', params: { id: response.data.id } })
          })
        } else {
          alert('令牌过期，请重新登录')
        }
      })
    },
    deleteArticle() {
      const token = localStorage.getItem('access.myblog')
      authorization().then((response) => {
        if (response[0]) {
          axios.delete('/api/article/' + this.articleID + '/', { headers: { Authorization: 'Bearer ' + token } }).then((response) => {
            this.$router.push({ name: 'Home' })
          })
        } else {
          alert('令牌过期，请重新登录')
        }
      })
    }
  }
}

</script>

<style scoped>
.category-btn {
  margin-right: 10px;
}

#article-create {
  text-align: center;
  font-size: large;
}

form {
  text-align: left;
  padding-left: 100px;
  padding-right: 10px;
}

.form-elem {
  padding: 10px;
}

input {
  height: 25px;
  padding-left: 10px;
  width: 50%;
}

button {
  height: 35px;
  cursor: pointer;
  border: none;
  outline: none;
  background: steelblue;
  color: whitesmoke;
  border-radius: 5px;
  width: 60px;
}
</style>
