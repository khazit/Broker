<template lang="html">
  <b-navbar class="fixed-top" toggleable="md" type="dark" variant="info">
    <div class="navbar-menu-wrapper d-flex align-items-center ml-auto ml-lg-0">
      <b-navbar-nav class="header-links d-none d-md-flex">
        <b-nav-item><router-link class="nav-link" to="/dashboard/"><i class=" mdi mdi-view-dashboard"></i>Dashboards</router-link></b-nav-item>
        <b-nav-item><router-link class="nav-link" to="/jobs/"><i class="mdi mdi-buffer"></i>Jobs</router-link></b-nav-item>
        <b-nav-item><i class="mdi mdi-account-multiple"></i>Users</b-nav-item>
        <b-nav-item><i class="mdi mdi-dns"></i>Runners</b-nav-item>
      </b-navbar-nav>
    </div>
  </b-navbar>
</template>

<script lang="js">
</script>

<style scoped lang="scss">
.app-header {
}
</style>
