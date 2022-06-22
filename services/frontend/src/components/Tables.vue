<template>
  <section id="tables">
    <mdb-row>
      <mdb-col md="12">
        <mdb-card cascade narrow class="mt-5">
          <mdb-view class="gradient-card-header blue darken-2">
            Nutrient Table</mdb-view
          >

          <mdb-row>
            <mdb-col col="4" style="margin-top: 10px"
              ><mdb-btn block color="primary"  @click="postTable0()" style="margin-left: 10px"
                ><mdb-icon class="mr-1" icon="plus" />Add Day</mdb-btn
              ></mdb-col
            >
            <mdb-col col="4">
              <mdb-input
                type="number"
                :min="0"
                :max="10"
                v-model="number_EC"
                placeholder="EC"
                outline
              />
            </mdb-col>
            <mdb-col col="4">
              <mdb-input
                type="number"
                :min="0"
                :max="10"
                v-model="number_pH"
                placeholder="PH"
                style="margin-right: 10px"
                outline
              />
            </mdb-col>
          </mdb-row>

          <mdb-row>
            <mdb-col col="3" style="margin-top: 10px"
              ><mdb-btn block color="amber" @click="editTable0(number_Day-1), getTable()" style="margin-left: 10px"
                ><mdb-icon class="mr-1" icon="pen" />Edit Day</mdb-btn
              ></mdb-col
            >
            <mdb-col col="3">
              <mdb-input
                type="number"
                :min="0"
                :max="10"
                v-model="number_Day"
                placeholder="Day"
                outline
              />
            </mdb-col>
            <mdb-col col="3">
              <mdb-input
                type="number"
                :min="0"
                :max="10"
                v-model="number_EC"
                placeholder="EC"
                outline
              />
            </mdb-col>
            <mdb-col col="3">
              <mdb-input
                type="number"
                :min="0"
                :max="10"
                v-model="number_pH"
                placeholder="PH"
                style="margin-right: 10px"
                outline
              />
            </mdb-col>
          </mdb-row>
          <table class="table table-striped table-bordered">
            <thead>
              <tr>
                <th>Day</th>
                <th>EC</th>
                <th>pH</th>
              </tr>
            </thead>
            <tbody>
              <tr
                v-for="(nutrientRows,
                nutrientRowsID) in nutrientTable.nutrientRows"
                :key="nutrientRows.id"
              >
                <td>{{ nutrientRows.day }}</td>
                <td>{{ nutrientRows.minEC }}</td>
                <td>{{ nutrientRows.maxPH }}</td>
                <mdb-btn
                  size="sm"
                  color="danger"
                  @click="deleteTableRow0(nutrientRowsID)"
                  style="margin-right: -100px"
                  ><mdb-icon class="mr-1" icon="backspace" /> Remove</mdb-btn
                >
              </tr>
            </tbody>
          </table>
        </mdb-card>
      </mdb-col>
    </mdb-row>
  </section>
</template>

<script>
import {
  mdbRow,
  mdbCol,
  mdbCard,
  mdbView,
  mdbInput,
  mdbBtn,
  mdbIcon,
} from "mdbvue";
import axios from "axios";
export default {
  name: "Tables",
  components: {
    mdbRow,
    mdbCol,
    mdbCard,
    mdbView,
    mdbInput,
    mdbBtn,
    mdbIcon,
    // mdbCardBody,
    //mdbTbl,
  },
  data() {
    return {
      nutrientTable: {},
      number_pH: "",
      number_EC: "",
      number_Day: "",
    };
  },
  methods: {
    getTable() {
      axios.get("/nutrient/data/0").then((res) => {
        //this.nutrientTable = res.data;
        this.nutrientTable = res.data;
        //this.data.rows = this.nutrientTable
      });
    },
    postTable0() {
      axios
        .post(
          "/nutrient/data/0/row",
          { minEC: this.number_EC, maxPH: this.number_pH },
          {
            headers: {
              Authorization: "",
              "Content-Type": "application/json",
            },
          }
        )
    },
    deleteTableRow0(row) {
      axios.delete(`/nutrient/data/0/row?row=${row}`).then(this.getTable());
    },
    editTable0(row) {
      axios
        .put(
          `/nutrient/data/0/row?row=${row}`,
          { minEC: this.number_EC, maxPH: this.number_pH },
          {
            headers: {
              Authorization: "",
              "Content-Type": "application/json",
            },
          }
        )
        .then(this.getTable());
    },
  },
  created() {
    this.getTable();
  },
  watch: {
    nutrientTable(newData) {
      const updatedData = this.data;
      for (let i = 0; i < newData.nutrientRows.length; i++) {
        newData.nutrientRows[i].day = i + 1;
      }
      updatedData.rows = newData.nutrientRows;
      this.data = { ...updatedData };
    },
  },
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
