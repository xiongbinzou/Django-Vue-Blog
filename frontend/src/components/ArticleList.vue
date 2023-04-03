<template>
  <div v-for="article in info.results" :key="article.url" id="articles">
    <div class="grid" :style="gridStyle(article)">
      <div class="image-container">
        <img :src="imageIfExists(article)" alt="" class="image" accept="image/gif, image/jpeg">
      </div>
      <div>
        <div>
          <span v-if="article.category !== null" class="category">{{ article.category.title }}</span>
          <span v-for="tag in article.tags" :key="tag" class="tag">
            {{ tag }}
          </span>
        </div>
        <router-link :to="{ name: 'ArticleDetail', params: { id: article.id } }" class="article-title">
          {{ article.title }}
        </router-link>
        <div>{{ formatted_time(article.created) }}</div>
      </div>
    </div>
  </div>
  <div id="paginator">
    <span v-if="is_page_exists('previous')">
      <router-link :to="get_path('previous')">
        Prev
      </router-link>
    </span>
    <span class="current-page">
      {{ get_page_param('current') }}
    </span>
    <span v-if="is_page_exists('next')">
      <router-link :to="get_path('next')">
        Next
      </router-link>
    </span>
  </div>
</template>

<script>
import axios from 'axios'

export default {
  name: 'ArticleList',
  data() {
    return {
      info: '',
    }
  },
  mounted() {
    this.get_article_data()
  },
  methods: {
    // 判断标题图是否存在并返回图像
    imageIfExists(article) {
      if (article.avatar) {
        return article.avatar.content
      }
    },
    // 修改grid样式
    gridStyle(article) {
      if (article.avatar) {
        return {
          display: 'grid',
          gridTemplateColumns: '1fr 7fr'
        }
      }
    },
    // 判断页面是否存在
    is_page_exists(direction) {
      if (direction === 'next') {
        return this.info.next !== null
      }
      return this.info.previous !== null
    },
    // 获取页码
    get_page_param(direction) {
      try {
        let url_string
        switch (direction) {
          case 'next':
            url_string = this.info.next
            break
          case 'previous':
            url_string = this.info.previous
            break
          default:
            if (!('page' in this.$route.query)) {
              return 1
            }
            if (this.$route.query.page === null) {
              return 1
            }
            return this.$route.query.page
        }
        const url = new URL(url_string)
        return url.searchParams.get('page')
      } catch (err) {
        return
      }
    },
    // 获取文章列表数据
    get_article_data() {
      let url = '/api/article/'
      let params = new URLSearchParams()
      if (this.isExists(this.$route.query.page)) {
        params.append('page', this.$route.query.page)
      }
      if (this.isExists(this.$route.query.search)) {
        params.append('search', this.$route.query.search)
      }
      const paramsString = params.toString()
      if (paramsString.charAt(0) !== '') {
        url += '/?' + paramsString
      }
      axios.get(url).then(response => {
        this.info = response.data
      }).catch(error => {
        console.log(error)
      })
    },
    // 获取路径
    get_path(direction) {
      let url = ''
      try {
        switch (direction) {
          case 'next':
            if (this.info.next !== undefined) {
              url += (new URL(this.info.next)).search
            }
            break
          case 'previous':
            if (this.info.previous !== undefined) {
              url += (new URL(this.info.previous)).search
            }
            break
        }
      } catch {
        return url
      }
      return url
    },
    // 检查参数是否存在
    isExists(value) {
      return value !== null && value !== undefined
    }
  },
  watch: {
    // 监听路由变化
    $route() {
      this.get_article_data()
    }
  },
  computed: {
    // 格式化时间
    formatted_time() {
      return timeString => new Date(timeString).toLocaleDateString()
    }
  }
}
</script>

<style scoped>
#articles {
  padding: 10px;
}

.article-title {
  font-size: large;
  font-weight: bolder;
  color: black;
  text-decoration: none;
  padding: 5px 0 5px 0;
}

.tag {
  padding: 2px 5px 2px 5px;
  margin: 5px 5px 5px 0;
  font-family: Georgia, Arial, sans-serif;
  font-size: small;
  background-color: #4e4e4e;
  color: whitesmoke;
  border-radius: 5px;
}

#paginator {
  text-align: center;
  padding-top: 50px;
}

a {
  color: black;
}

.current-page {
  font-size: x-large;
  font-weight: bold;
  padding-left: 10px;
  padding-right: 10px;
}

.category {
  padding: 5px 10px 5px 10px;
  margin: 5px 5px 5px 0;
  font-family: Georgia, Arial, sans-serif;
  font-size: small;
  background-color: darkred;
  color: whitesmoke;
  border-radius: 15px;
}

.image {
  width: 180px;
  border-radius: 10px;
  box-shadow: darkslategrey 0 0 12px;
}

.image-container {
  width: 200px;
}

.grid {
  padding-bottom: 10px;
}
</style>
