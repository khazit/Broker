<template lang="html">
  <div id="app">
    <div class="container-scroller">
      <app-header/>
      <div class="container-fluid page-body-wrapper">
        <div class="main-panel">
          <div class="content-wrapper">
            <router-view></router-view>
          </div>
          <!-- content wrapper ends -->
        </div>
        <!-- main panel ends -->
      </div>
      <!-- page-body-wrapper ends -->
    </div>
  </div>
</template>

<script lang="js">
import AppHeader from '../src/components/partials/AppHeader'
export default{
  name: 'app',
  components: {
    AppHeader
  }
}
</script>

<style>
  @import "../node_modules/mdi/css/materialdesignicons.min.css";
  @import "../node_modules/flag-icon-css/css/flag-icon.min.css";
  @import "../node_modules/font-awesome/css/font-awesome.min.css";
</style>

<style lang="scss">
@import "./assets/scss/style";
</style>
