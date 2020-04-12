import Vue from 'vue'
import Router from 'vue-router'

import dashboard from '../views/dashboard'
import jobs from '../views/jobs'
import users from '../views/users'
import runners from '../views/runners'

Vue.use(Router)

export default new Router({
  linkActiveClass: 'active',
  routes: [{
    path: '/',
    name: 'dashboard',
    component: dashboard
  },
  {
    path: '/jobs',
    name: 'jobs',
    component: jobs
  },
  {
    path: '/users',
    name: 'users',
    component: users
  },
  {
    path: '/runners',
    name: 'runners',
    component: runners
  }]
})
