<template lang="html">
  <section class="dashboard">
    <div class="row">

      <div class="col-xl-3 col-sm-6 grid-margin stretch-card">
        <div class="card card-statistics">
          <router-link class="nav-link" to="/jobs/">
            <div class="card-body">
              <div class="d-flex justify-content-between flex-wrap">
                <div>
                  <i class="mdi mdi-buffer text-danger icon-lg"></i>
                </div>
                <div>
                  <p class="card-text text-right">Jobs</p>
                  <div class="fluid-container">
                    <h3 class="card-title font-weight-bold text-right mb-0">{{ jobs.length }}</h3>
                  </div>
                </div>
              </div>
            </div>
          </router-link>
        </div>
      </div>

      <div class="col-xl-3 col-sm-6 grid-margin stretch-card">
        <div class="card card-statistics">
          <div class="card-body">
            <div class="d-flex justify-content-between flex-wrap">
              <div>
                <i class="mdi mdi-account-multiple text-warning icon-lg"></i>
              </div>
              <div>
                <p class="card-text text-right">Users</p>
                <div class="fluid-container">
                  <h3 class="card-title font-weight-bold text-right mb-0"></h3>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>

      <div class="col-xl-3 col-sm-6 grid-margin stretch-card">
        <div class="card card-statistics">
          <div class="card-body">
            <div class="d-flex justify-content-between flex-wrap">
              <div>
                <i class="mdi mdi-dns text-teal icon-lg"></i>
              </div>
              <div>
                <p class="card-text text-right">Runners</p>
                <div class="fluid-container">
                  <h3 class="card-title font-weight-bold text-right mb-0"></h3>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>

    </div>
  </section>
</template>

<script lang="js">
import axios from 'axios'
export default {
  data () {
    return {
      jobs: []
    }
  },
  methods: {
    getJobs () {
      const path = 'http://localhost:5000/jobs'
      axios.get(path)
        .then((res) => {
          this.jobs = res.data
        })
        .catch((error) => {
          // eslint-disable-next-line
          console.error(error);
        })
    }
  },
  created () {
    this.getJobs()
  }
}

</script>

<style scoped lang="scss">
</style>
