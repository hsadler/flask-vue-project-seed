import { createRouter, createWebHashHistory } from 'vue-router'

import Home from '@/views/Home'
import WallMessages from '@/views/WallMessages'
import EditWallMessage from '@/views/EditWallMessage'
import NotFound from '@/views/NotFound'

const router = createRouter({
  history: createWebHashHistory(),
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
    { path:
      '/:pathMatch(.*)*',
      name: 'NotFound',
      component: NotFound
    },
  ]
})

export default router
