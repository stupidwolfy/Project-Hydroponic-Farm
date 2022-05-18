<template>
  <section id="tables">
    <mdb-row>
      <mdb-col md="12">
        <mdb-card cascade narrow class="mt-5">
          <mdb-view class="gradient-card-header blue darken-2">
            <h4 class="h4-responsive text-white">Basic tables</h4>
          </mdb-view>
          <mdb-card-body>
            <h3 class="mt-5 text-left"><strong>AB Table</strong></h3>
            <p>Using for fertilizer setup.</p>
            <mdb-tbl>
              <thead>
                <tr>
                  <th>Day</th>
                  <th>A</th>
                  <th>B</th>
                  <th>A Interval</th>
                  <th>B Interval</th>
                  <th>Mode</th>
                </tr>
              </thead>
              <tbody>
                <tr>
                  <th scope="row">1</th>
                  <td>10 g</td>
                  <td>20 g</td>
                  <td>10 min</td>
                  <td>10 min</td>
                  <td>Force Auto</td>
                </tr>
                <tr>
                  <th scope="row">2</th>
                  <td>10 g</td>
                  <td>20 g</td>
                  <td>10 min</td>
                  <td>10 min</td>
                  <td>Force Auto</td>
                </tr>
                <tr>
                  <th scope="row">3</th>
                  <td>10 g</td>
                  <td>20 g</td>
                  <td>10 min</td>
                  <td>10 min</td>
                  <td>Force Auto</td>
                </tr>
                <tr>
                  <th scope="row">
                    <div class="form-group">
                      <label for="example3">Small input</label>
                      <input
                        type="text"
                        id="example3"
                        class="form-control form-control-sm"
                      />
                    </div>
                  </th>
                  <td>
                    <div class="form-group">
                      <label for="example3">Small input</label>
                      <input
                        type="text"
                        id="example3"
                        class="form-control form-control-sm"
                      />
                    </div>
                  </td>
                  <td>
                    <div class="form-group">
                      <label for="example3">Small input</label>
                      <input
                        type="text"
                        id="example3"
                        class="form-control form-control-sm"
                      />
                    </div>
                  </td>
                  <td>
                    <div class="form-group">
                      <label for="example3">Small input</label>
                      <input
                        type="text"
                        id="example3"
                        class="form-control form-control-sm"
                      />
                    </div>
                  </td>
                  <td>
                    <div class="form-group">
                      <label for="example3">Small input</label>
                      <input
                        type="text"
                        id="example3"
                        class="form-control form-control-sm"
                      />
                    </div>
                  </td>
                  <td>
                    <div class="form-group">
                      <label for="example3">Small input</label>
                      <input
                        type="text"
                        id="example3"
                        class="form-control form-control-sm"
                      />
                    </div>
                  </td>
                </tr>
              </tbody>
            </mdb-tbl>
            <!-- <h3 class="mt-5 text-left"><strong>Table head options</strong></h3>
            <p>To change a background-color of thead (or any other element) use our color classes. If you are going to use a dark background you should also consider white text (to provide a proper contrast) by adding .text-white class. </p>
            <mdb-tbl>
              <thead class="blue-grey lighten-4">
                <tr><th>#</th><th>First Name</th><th>Last Name</th><th>Username</th></tr>
              </thead>
              <tbody>
                <tr><th scope="row">1</th><td>Mark</td><td>Otto</td><td>@mdo</td></tr><tr><th scope="row">2</th><td>Jacob</td><td>Thornton</td><td>@fat</td></tr><tr><th scope="row">3</th><td>Larry</td><td>the Bird</td><td>@twitter</td></tr>
              </tbody>
            </mdb-tbl>
            <mdb-tbl>
              <thead class="mdb-color darken-3">
                <tr class="text-white"><th>#</th><th>First Name</th><th>Last Name</th><th>Username</th></tr>
              </thead>
              <tbody>
                <tr><th scope="row">1</th><td>Mark</td><td>Otto</td><td>@mdo</td></tr><tr><th scope="row">2</th><td>Jacob</td><td>Thornton</td><td>@fat</td></tr><tr><th scope="row">3</th><td>Larry</td><td>the Bird</td><td>@twitter</td></tr>
              </tbody>
            </mdb-tbl>
            <h3 class="mt-5 text-left"><strong>Striped rows:</strong></h3>
            <table class="table table-striped">
              <thead>
                <tr><th>#</th><th>First Name</th><th>Last Name</th><th>Username</th></tr>
              </thead>
              <tbody>
                <tr><th scope="row">1</th><td>Mark</td><td>Otto</td><td>@mdo</td></tr><tr><th scope="row">2</th><td>Jacob</td><td>Thornton</td><td>@fat</td></tr><tr><th scope="row">3</th><td>Larry</td><td>the Bird</td><td>@twitter</td></tr>
              </tbody>
            </table> -->
          </mdb-card-body>
        </mdb-card>
      </mdb-col>
    </mdb-row>
    
    <mdb-row>
      <mdb-col md="12">
          <mdb-view class="gradient-card-header blue darken-2">
          </mdb-view>
          <mdb-card-body>
            <mdb-tbl>
              <thead>
                <tr>
                  <th>Day</th>
                  <th>A</th>
                  <th>B</th>
                  <th>A Interval</th>
                  <th>B Interval</th>
                  <th>Mode</th>
                </tr>
              </thead>
              <tbody>
                <tr>
                  <th scope="row">
                    <div class="form-group">
                      <label for="example3">Small input</label>
                      <input
                        type="text"
                        id="example3"
                        class="form-control form-control-sm"
                      />
                    </div>
                  </th>
                  <td>
                    <div class="form-group">
                      <label for="example3">Small input</label>
                      <input
                        type="text"
                        id="example3"
                        class="form-control form-control-sm"
                      />
                    </div>
                  </td>
                  <td>
                    <div class="form-group">
                      <label for="example3">Small input</label>
                      <input
                        type="text"
                        id="example3"
                        class="form-control form-control-sm"
                      />
                    </div>
                  </td>
                  <td>
                    <div class="form-group">
                      <label for="example3">Small input</label>
                      <input
                        type="text"
                        id="example3"
                        class="form-control form-control-sm"
                      />
                    </div>
                  </td>
                  <td>
                    <div class="form-group">
                      <label for="example3">Small input</label>
                      <input
                        type="text"
                        id="example3"
                        class="form-control form-control-sm"
                      />
                    </div>
                  </td>
                  <td>
                    <div class="form-group">
                      <label for="example3">Small input</label>
                      <input
                        type="text"
                        id="example3"
                        class="form-control form-control-sm"
                      />
                    </div>
                  </td>
                </tr>
              </tbody>
            </mdb-tbl>
          </mdb-card-body>
      </mdb-col>
    </mdb-row>
  </section>
</template>

<script>
import { mdbRow, mdbCol, mdbCard, mdbView, mdbCardBody, mdbTbl } from "mdbvue";
import axios from "axios";
export default {
  name: "Tables",
  components: {
    mdbRow,
    mdbCol,
    mdbCard,
    mdbView,
    mdbCardBody,
    mdbTbl,
  },
  data() {
    return {
      nutrientTable: {},

    };
  },
  methods: {
    getTable(){
      axios.get("/nutrient/data/0").then((res) => {
        this.nutrientTable = res.data;
      })
    }
  },
  created() {
    this.getTable();
  }
};
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
.card.card-cascade .view.gradient-card-header {
  padding: 1rem 1rem;
  text-align: center;
}
.card.card-cascade h3,
.card.card-cascade h4 {
  margin-bottom: 0;
}
</style>
