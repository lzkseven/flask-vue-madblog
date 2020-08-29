import Vue from 'vue'
import Router from 'vue-router'
import ping from '@/components/ping'

Vue.use(Router)

export default new Router({
  routes: [
    {
      path: '/',
      name: 'ping',
      component: ping
    }
  ]
})
