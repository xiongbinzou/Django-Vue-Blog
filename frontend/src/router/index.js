import { createRouter, createWebHistory } from 'vue-router'

const Home = () => import('@/views/Home.vue')
const ArticleDetail = () => import('@/views/ArticleDetail.vue')
const Login = () => import('@/views/Login.vue')
const UserCenter = () => import('@/views/UserCenter.vue')
const ArticleCreate = () => import('@/views/ArticleCreate.vue')
const ArticleEdit = () => import('@/views/ArticleEdit.vue')
const routes = [
  {
    path: '/',
    name: 'Home',
    component: Home
  },
  {
    path: '/article/:id',
    name: 'ArticleDetail',
    component: ArticleDetail
  },
  {
    path: '/login',
    name: 'Login',
    component: Login
  },
  {
    path: '/user/:username',
    name: 'UserCenter',
    component: UserCenter,
    meta: { requireAuth: true }
  },
  {
    path: '/article/create',
    name: 'ArticleCreate',
    component: ArticleCreate,
  },
  {
    path: '/article/edit/:id',
    name: 'ArticleEdit',
    component: ArticleEdit,
  },
]

const router = createRouter({
  history: createWebHistory(),
  routes,
})

router.beforeEach((to, from, next) => {
  if (to.meta.requireAuth) {
    if (localStorage.getItem('access.myblog') && to.params.username === localStorage.getItem('username.myblog')) {
      next()
    } else if (to.params.username !== localStorage.getItem('username.myblog')) {
      next({
        path: from.path
      })
    }
    else {
      if (to.path === '/login') {
        next()
      } else {
        alert('请先登录！')
        next({
          path: '/login'
        })
      }
    }
  } else {
    next()
  }
})

export default router
