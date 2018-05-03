import Vue from 'vue'
import Router from 'vue-router'
import Home from '@/views/Home'
import WallMessages from '@/views/WallMessages'
import NotFound from '@/views/NotFound'

Vue.use(Router)

export default new Router({
  mode: 'history',
  routes: [
    {
      path: '/',
      name: 'Home',
      component: Home
    },
    {
      path: '/wall-messages',
      name: 'WallMessages',
      component: WallMessages
    },
    {
      path: '*',
      name: 'NotFound',
      component: NotFound
    }
  ]
})
