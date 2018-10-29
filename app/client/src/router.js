import Vue from 'vue'
import Router from 'vue-router'
import Home from '@/views/Home'
import WallMessages from '@/views/WallMessages'
import EditWallMessage from '@/views/EditWallMessage'
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
      path: '/edit-message/:uuid',
      name: 'EditWallMessage',
      component: EditWallMessage
    },
    {
      path: '*',
      name: 'NotFound',
      component: NotFound
    }
  ]
})
