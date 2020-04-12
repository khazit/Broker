<template lang="html">
  <section class="jobs">
    <div class="row">
      <div class="col-12 grid-margin">
        <div class="card">
          <div class="card-body">
            <b-row>
              <b-col align-self="start"><h5 class="card-title mb-4">Jobs</h5></b-col>
              <b-button v-b-modal.form align-self="end" variant="dark" size="xs"><i class="mdi mdi-database-plus"></i>New Job</b-button>
              <b-modal id="form" title="Create a new job" hide-footer="true" size="md">
                  <div class="card-body">
                    <form class="forms-sample">
                    <b-form-group>
                      <b-input-group>
                        <b-input-group-text slot="prepend" class="bg-info text-white">
                          <span>@</span>
                        </b-input-group-text>
                        <b-form-input placeholder="Username" id="username"></b-form-input>
                      </b-input-group>
                    </b-form-group>
                      <b-form-group label="" label-for="command">
                        <b-form-input id="command" placeholder="Command"></b-form-input>
                      </b-form-group>
                      <b-button type="submit" variant="secondary" class="mr-2">Submit</b-button>
                    </form>
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
                  </tr>
                </thead>
                <tbody>
                  <tr>
                  <td>34</td>
                  <td>ali.benkassou@insa-rouen.fr</td>
                  <td>11 April 2020 - 13:38:31</td>
                  <td><label class="badge badge-teal">Running</label></td>
                  <td>
                    <div class="text-center">
                      <b-btn v-b-modal.modalsm variant="secondary" size="xs" class="btn-fw">Show command</b-btn>
                    </div>
                    <b-modal id="modalsm" ok-only size="sm">
                      <p class="my-4">docker run ...</p>
                    </b-modal>
                  </td>
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
export default {
  name: 'jobs'
}
</script>

<style scoped lang="scss">
</style>
