import Vue from 'vue'
import Router from 'vue-router'

import dashboard from '../views/dashboard'
import jobs from '../views/jobs'

Vue.use(Router)

export default new Router({
  linkActiveClass: 'active',
  mode: 'history',
  routes: [{
    path: '/',
    name: 'dashboard',
    component: dashboard
  },
  {
    path: '/jobs',
    name: 'jobs',
    component: jobs
  }]
})
