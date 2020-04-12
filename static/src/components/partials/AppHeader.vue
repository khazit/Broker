<template lang="html">
  <b-navbar class="fixed-top" toggleable="md" type="dark" variant="info">
    <div class="navbar-menu-wrapper d-flex align-items-center ml-auto ml-lg-0">
      <b-navbar-nav class="header-links d-none d-md-flex">
        <b-nav-item><router-link class="nav-link" to="/"><i class=" mdi mdi-view-dashboard"></i>Dashboards</router-link></b-nav-item>
        <b-nav-item><router-link class="nav-link" to="/jobs/"><i class="mdi mdi-buffer"></i>Jobs</router-link></b-nav-item>
        <b-nav-item><router-link class="nav-link" to="/users/"><i class="mdi mdi-account-multiple"></i>Users</router-link></b-nav-item>
        <b-nav-item><router-link class="nav-link" to="/runners/"><i class="mdi mdi-dns"></i>Runners</router-link></b-nav-item>
      </b-navbar-nav>
      <button class="navbar-toggler navbar-toggler-right align-self-center" type="button" @click="collapedMobileSidebar()">
        <span class="mdi mdi-menu"></span>
      </button>
    </div>
  </b-navbar>
</template>

<script lang="js">
export default {
  name: 'app-header',
  methods: {
    collapedMobileSidebar: () => {
      document.querySelector('.sidebar').classList.toggle('active')
    }
  }
}
</script>

<style scoped lang="scss">
.app-header {
}
</style>
