<template>
  <div class="search">
    <form>
      <input type="text" v-model="searchText" placeholder="输入搜索内容...">
      <button @click.prevent="searchArticle"></button>
    </form>
  </div>
</template>

<script>
export default {
  name: 'SearchButton',
  data() {
    return {
      searchText: '',
    }
  },
  methods: {
    searchArticle() {
      const text = this.searchText.trim()
      if (text.charAt(0) !== '') {
        this.$router.push({ name: 'Home', query: { search: text } })
      } else {
        this.$router.push({ name: 'Home' })
      }
    }
  }
}
</script>

<style scoped>
.search {
  padding-top: 22px;
}

* {
  box-sizing: border-box;
}

form {
  position: relative;
  width: 200px;
  margin: 0 auto;
}

input,
button {
  border: none;
  outline: none;
}

input {
  width: 100%;
  height: 35px;
  padding-left: 13px;
  padding-right: 46px;
}

button {
  height: 35px;
  width: 35px;
  cursor: pointer;
  position: absolute;
}

.search input {
  border: 2px solid gray;
  border-radius: 5px;
  background: transparent;
  top: 0;
  right: 0;
}

.search button {
  background: gray;
  border-radius: 0 5px 5px 0;
  width: 45px;
  top: 0;
  right: 0;
}

.search button:before {
  content: "搜索";
  font-size: 13px;
  color: white;
}
</style>