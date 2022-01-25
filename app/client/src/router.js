import { createRouter, createWebHashHistory } from 'vue-router'

// import Home from '@/views/Home'
// import WallMessages from '@/views/WallMessages'
// import EditWallMessage from '@/views/EditWallMessage'
// import NotFound from '@/views/NotFound'

const Home = { template: '<div>Home</div>' }
const About = { template: '<div>About</div>' }

const router = createRouter({
  history: createWebHashHistory(),
  routes: [
    // testing
    { path: '/', component: Home },
    { path: '/about', component: About },
    // {
    //   path: '/',
    //   name: 'Home',
    //   component: Home
    // },
    // {
    //   path: '/wall-messages',
    //   name: 'WallMessages',
    //   component: WallMessages
    // },
    // {
    //   path: '/edit-message/:uuid',
    //   name: 'EditWallMessage',
    //   component: EditWallMessage
    // },
    // {
    //   path: '*',
    //   name: 'NotFound',
    //   component: NotFound
    // }
  ]
})

export default router
