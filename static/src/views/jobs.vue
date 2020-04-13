<template lang="html">
  <section class="jobs">
    <div class="row">
      <div class="col-12 grid-margin">
        <div class="card">
          <div class="card-body">
            <b-row>
              <b-col align-self="start"><h5 class="card-title mb-4">Jobs</h5></b-col>
              <b-button v-b-modal.job-modal align-self="end" variant="dark" size="xs"><i class="mdi mdi-database-plus"></i>New Job</b-button>
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
                      <b-button type="submit" variant="secondary" class="mr-2" size="sm">Submit</b-button>
                    </b-form>
                  </div>
              </b-modal>
            </b-row>
            <div class="table-responsive">
              <table class="table center-aligned-table">
                <thead>
                  <tr>
                    <th class="border-bottom-0">ID</th>
                    <th class="border-bottom-0">User</th>
                    <th class="border-bottom-0">Received on</th>
                    <th class="border-bottom-0">Status</th>
                    <th class="border-bottom-0"></th>
                    <th class="border-bottom-0"></th>
                  </tr>
                </thead>
                <tbody>
                  <tr v-for="(job, index) in jobs" :key="index">
                    <td>{{ job.identifier }}</td>
                    <td>{{ job.user }}</td>
                    <td>{{ job.epoch_received }}</td>
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
                        <b-btn v-b-modal="'modalsm' + job.identifier" variant="secondary" size="xs" class="btn-fw">Show command</b-btn>
                      </div>
                      <b-modal :id="'modalsm' + job.identifier" ok-only size="sm">
                        <p>{{ job.description }}</p>
                      </b-modal>
                    </td>
                    <td><a href="#" class="btn btn-outline-danger btn-xs">Cancel</a></td>
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
  methods: {
    getJobs () {
      const path = 'http://localhost:5000/jobs/all'
      axios.get(path)
        .then((res) => {
          this.jobs = res.data
        })
        .catch((error) => {
          // eslint-disable-next-line
          console.error(error);
        })
    },
    addJob (payload) {
      const path = 'http://localhost:5000/jobs/add'
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
    },
    onSubmit (evt) {
      evt.preventDefault()
      this.$refs.addJobModal.hide()
      const payload = {
        user: this.addJobForm.username,
        command: this.addJobForm.command
      }
      this.addJob(payload)
      this.initForm()
    }
  },
  created () {
    this.getJobs()
  }
}
</script>

<style scoped lang="scss">
</style>
