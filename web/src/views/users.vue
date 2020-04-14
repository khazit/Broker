<template lang="html">
  <section class="users">
    <div class="row">
      <div class="col-12 grid-margin">
        <div class="card">
          <div class="card-body">
            <h5 class="card-title mb-4">Orders</h5>
            <div class="table-responsive">
              <table class="table center-aligned-table">
                <thead>
                  <tr>
                    <th class="border-bottom-0">Order No</th>
                    <th class="border-bottom-0">Product Name</th>
                    <th class="border-bottom-0">Purchased On</th>
                    <th class="border-bottom-0">Shipping Status</th>
                    <th class="border-bottom-0">Payment Method</th>
                    <th class="border-bottom-0">Payment Status</th>
                    <th class="border-bottom-0"></th>
                    <th class="border-bottom-0"></th>
                    <th class="border-bottom-0"></th>
                  </tr>
                </thead>
                <tbody>
                  <tr>
                    <td>034</td>
                    <td>Iphone 7</td>
                    <td>12 May 2017</td>
                    <td>Dispatched</td>
                    <td>Credit card</td>
                    <td><label class="badge badge-teal">Approved</label></td>
                    <td><a href="#" class="btn btn-outline-success btn-sm">View Order</a></td>
                    <td><a href="#" class="btn btn-outline-danger btn-sm">Cancel</a></td>
                  </tr>
                  <tr>
                    <td>035</td>
                    <td>Galaxy S8</td>
                    <td>15 May 2017</td>
                    <td>Dispatched</td>
                    <td>Internet banking</td>
                    <td><label class="badge badge-warning">Pending</label></td>
                    <td><a href="#" class="btn btn-outline-success btn-sm">View Order</a></td>
                    <td><a href="#" class="btn btn-outline-danger btn-sm">Cancel</a></td>
                  </tr>
                  <tr>
                    <td>036</td>
                    <td>Amazon Echo</td>
                    <td>17 May 2017</td>
                    <td>Dispatched</td>
                    <td>Credit card</td>
                    <td><label class="badge badge-teal">Approved</label></td>
                    <td><a href="#" class="btn btn-outline-success btn-sm">View Order</a></td>
                    <td><a href="#" class="btn btn-outline-danger btn-sm">Cancel</a></td>
                  </tr>
                  <tr>
                    <td>037</td>
                    <td>Google Pixel</td>
                    <td>17 May 2017</td>
                    <td>Dispatched</td>
                    <td>Cash on delivery</td>
                    <td><label class="badge badge-danger">Rejected</label></td>
                    <td><a href="#" class="btn btn-outline-success btn-sm">View Order</a></td>
                    <td><a href="#" class="btn btn-outline-danger btn-sm">Cancel</a></td>
                  </tr>
                  <tr>
                    <td>038</td>
                    <td>Mac Mini</td>
                    <td>19 May 2017</td>
                    <td>Dispatched</td>
                    <td>Debit card</td>
                    <td><label class="badge badge-teal">Approved</label></td>
                    <td><a href="#" class="btn btn-outline-success btn-sm">View Order</a></td>
                    <td><a href="#" class="btn btn-outline-danger btn-sm">Cancel</a></td>
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
  name: 'users'
}
</script>

<style scoped lang="scss">
</style>
