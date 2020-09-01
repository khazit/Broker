<template lang="html">
  <section class="jobs">
    <div class="row">
      <div class="col-12 grid-margin">
        <div class="card">
          <div class="card-body">
            <!-- Title bar -->
            <b-row>
              <b-col align-self="start"><h5 class="card-title mb-4">Jobs</h5></b-col>
              <b-button v-b-modal.job-modal align-self="end" variant="dark" size="sm"><i class="mdi mdi-database-plus"></i>New Job</b-button>
              <b-modal ref="addJobModal"
                       id="job-modal"
                       title="Create a new job"
                       hide-footer
                       size="md">
                  <div class="card-body">
                    <b-form @submit="onSubmit" class="forms-sample">
                      <b-form-group id="form-username-group">
                        <b-input-group>
                          <b-input-group-text slot="prepend" class="bg-info text-white">
                            <span>@</span>
                          </b-input-group-text>
                          <b-form-input id="username"
                                        type="text"
                                        v-model="addJobForm.username"
                                        required
                                        placeholder="Username" >
                          </b-form-input>
                        </b-input-group>
                      </b-form-group>
                      <b-form-group id="form-command-group" label="" label-for="command">
                        <b-form-input id="command"
                                      type="text"
                                      v-model="addJobForm.command"
                                      required
                                      placeholder="Command">
                        </b-form-input>
                      </b-form-group>
                      <b-form-group id="form-description-group" label="" label-for="description">
                        <b-form-input id="description"
                                      type="text"
                                      v-model="addJobForm.description"
                                      required
                                      placeholder="Description">
                        </b-form-input>
                      </b-form-group>
                      <b-button type="submit" variant="secondary" class="mr-2" size="sm">Submit</b-button>
                    </b-form>
                  </div>
              </b-modal>
            </b-row>

            <!-- Jobs table -->
            <div class="table-responsive">
              <table class="table center-aligned-table">
                <thead>
                  <tr>
                    <th class="border-bottom-0">ID</th>
                    <th class="border-bottom-0">User</th>
                    <th class="border-bottom-0">Description</th>
                    <th class="border-bottom-0">Status</th>
                    <th class="border-bottom-0"></th>
                    <th class="border-bottom-0"></th>
                  </tr>
                </thead>
                <tbody>
                  <tr v-for="(job, index) in jobs" :key="index">
                    <td>{{ job.identifier }}</td>
                    <td>{{ job.user }}</td>
                    <td style="white-space: nowrap; text-overflow:ellipsis; overflow: hidden; max-width:0px;">{{ job.description}}</td>
                    <td>
                      <span v-if="job.status == 0">
                        <b-badge variant="warning">Unknown</b-badge>
                      </span>
                      <span v-if="job.status == 1">
                        <b-badge variant="info">Sleeping</b-badge>
                      </span>
                      <span v-if="job.status == 2">
                        <b-badge variant="info">Waiting</b-badge>
                      </span>
                      <span v-if="job.status == 3">
                        <b-badge variant="success">Running</b-badge>
                      </span>
                      <span v-if="job.status == 4">
                        <b-badge variant="danger">Terminated</b-badge>
                      </span>
                      <span v-if="job.status == 5">
                        <b-badge variant="success">Done</b-badge>
                      </span>
                    </td>
                    <td>
                      <div class="text-center">
                        <b-btn v-b-modal="'modalmd' + job.identifier" variant="secondary" size="sm" class="btn-fw">View Job</b-btn>
                      </div>
                      <b-modal :id="'modalmd' + job.identifier" ok-only size="md">
                        <h5>Command</h5>
                        <p class="text-white bg-dark pl-1">$ {{ job.command }}</p>
                        <h5>Events</h5>
                        <div class="table-responsive">
                          <thead>
                            <tr>
                              <th class="border-bottom-0">Time</th>
                              <th class="border-bottom-0">Status</th>
                            </tr>
                          </thead>
                          <tbody>
                            <tr v-for="(event, index) in job.events" :key="index">
                              <td>{{ formatEpoch(event.timestamp) }}</td>
                              <td>
                                <span v-if="event.status == 0">
                                  <b-badge variant="warning">Unknown</b-badge>
                                </span>
                                <span v-if="event.status == 1">
                                  <b-badge variant="info">Sleeping</b-badge>
                                </span>
                                <span v-if="event.status == 2">
                                  <b-badge variant="info">Waiting</b-badge>
                                </span>
                                <span v-if="event.status == 3">
                                  <b-badge variant="success">Running</b-badge>
                                </span>
                                <span v-if="event.status == 4">
                                  <b-badge variant="danger">Terminated</b-badge>
                                </span>
                                <span v-if="event.status == 5">
                                  <b-badge variant="success">Done</b-badge>
                                </span>
                              </td>
                            </tr>
                          </tbody>
                        </div>
                        <span v-if="job.status > 3">
                          <b-btn :href="'http://localhost:5000/jobs/'+job.identifier+'/logs'" variant="primary" size="sm" class="btn-fw">Download logs</b-btn>
                        </span>
                      </b-modal>
                    </td>
                    <td><button @click="onRemoveJob(job)" class="btn btn-outline-danger btn-sm">Cancel</button></td>
                  </tr>
                </tbody>
              </table>
            </div>
          </div>
        </div>
      </div>
    </div>
  </section>
</template>

<script lang="js">
import axios from 'axios'
import moment from 'moment'
export default {
  data () {
    return {
      jobs: [],
      addJobForm: {
        username: '',
        command: ''
      }
    }
  },
  created () {
    this.getJobs()
  },
  methods: {
    getJobs () {
      const path = 'http://localhost:5000/jobs'
      axios.get(path)
        .then((res) => {
          this.jobs = res.data
          for (var i = 0; i < this.jobs.length; i++) {
            this.jobs[i].status = this.jobs[i].events[this.jobs[i].events.length - 1].status
          }
        })
        .catch((error) => {
          // eslint-disable-next-line
          console.error(error);
        })
    },
    addJob (payload) {
      const path = 'http://localhost:5000/jobs'
      axios.post(path, payload)
        .then(() => {
          // update page with GET request
          this.getJobs()
        })
        .catch((error) => {
          // eslint-disable-next-line
          console.log(error)
          this.getJobs()
        })
    },
    initForm () {
      this.addJobForm.username = ''
      this.addJobForm.command = ''
      this.addJobForm.description = ''
    },
    onSubmit (evt) {
      evt.preventDefault()
      this.$refs.addJobModal.hide()
      const payload = {
        user: this.addJobForm.username,
        command: this.addJobForm.command,
        description: this.addJobForm.description
      }
      this.addJob(payload)
      this.initForm()
    },
    removeJob (jobID) {
      const path = `http://localhost:5000/jobs/${jobID}`
      axios.delete(path)
        .then(() => {
          this.getJobs()
          this.message = 'Job removed'
          this.showMessage = true
        })
        .catch((error) => {
          // eslint-disable-next-line
          console.error(error)
          this.getJobs()
        })
    },
    onRemoveJob (job) {
      this.removeJob(job.identifier)
    },
    formatEpoch (epoch) {
      var date = new Date(epoch * 1000)
      return moment(date).format('DD/MM/YYYY - HH:mm:ss')
    }
  }
}
</script>

<style scoped lang="scss">
</style>
