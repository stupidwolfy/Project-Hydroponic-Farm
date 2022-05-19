<template>
  <section id="dashboard">
    <section class="mt-lg-5">
      <mdb-row>
        <mdb-col xl="3" md="6" class="mb-r">
          <mdb-card cascade class="cascading-admin-card">
            <div class="admin-up">
              <div class="data">
                <p>Temp</p>
                <h4>
                  <strong>{{ temp }}</strong>
                </h4>
              </div>
            </div>
            <mdb-card-body>
              <div class="progress">
                <div
                  aria-valuemax="100"
                  aria-valuemin="0"
                  aria-valuenow="25"
                  :class="[
                    'progress-bar',
                    temp > 30 ? 'bg-warning ' : 'bg-primary',
                  ]"
                  role="progressbar"
                  v-bind:style="'width:' + temp + '%'"
                ></div>
              </div>
              <mdb-card-text>Max temp 100</mdb-card-text>
            </mdb-card-body>
          </mdb-card>
        </mdb-col>

        <mdb-col xl="3" md="6" class="mb-r">
          <mdb-card cascade class="cascading-admin-card">
            <div class="admin-up">
              <!--<mdb-icon icon="money-bill-alt" far class="primary-color"/>-->
              <div class="data">
                <p>humidity</p>
                <h4>
                  <strong>{{ humidity }}</strong>
                </h4>
              </div>
            </div>
            <mdb-card-body>
              <div class="progress">
                <div
                  aria-valuemax="100"
                  aria-valuemin="0"
                  aria-valuenow="25"
                  :class="[
                    'progress-bar',
                    humidity > 70 ? 'bg-warning ' : 'bg-primary',
                  ]"
                  role="progressbar"
                  v-bind:style="'width:' + humidity + '%'"
                ></div>
              </div>
              <mdb-card-text>Max Humidity 100</mdb-card-text>
            </mdb-card-body>
          </mdb-card>
        </mdb-col>

        <mdb-col xl="3" md="6" class="mb-r">
          <mdb-card cascade class="cascading-admin-card">
            <div class="admin-up">
              <div class="data">
                <p>EC</p>
                <h4>
                  <strong>{{ ec }}</strong>
                </h4>
              </div>
            </div>
            <mdb-card-body>
              <div class="progress">
                <div
                  aria-valuemax="100"
                  aria-valuemin="0"
                  aria-valuenow="25"
                  class="progress-bar bg-primary"
                  role="progressbar"
                  v-bind:style="'width:' + ec%100 + '%'"
                ></div>
              </div>
              <mdb-card-text>EC form Nutrient</mdb-card-text>
            </mdb-card-body>
          </mdb-card>
        </mdb-col>

        <mdb-col xl="3" md="6" class="mb-r">
          <mdb-card cascade class="cascading-admin-card">
            <div class="admin-up">
              <div class="data">
                <p>pH</p>
                <h4>
                  <strong>{{ pHRealtime }}</strong>
                </h4>
              </div>
            </div>
            <mdb-card-body>
              <div class="progress">
                <div
                  aria-valuemax="100"
                  aria-valuemin="0"
                  aria-valuenow="25"
                  :class="[
                    'progress-bar',
                    pHRealtime > 6 ? 'bg-warning ' : 'bg-primary',
                  ]"
                  role="progressbar"
                  v-bind:style="'width:' + pHRealtime*7.143 + '%'"
                ></div>
              </div>
              <mdb-card-text>Max pH 14</mdb-card-text>
            </mdb-card-body>
          </mdb-card>
        </mdb-col>
      </mdb-row>
    </section>
    <section>
      <mdb-row class="mt-5">
        <mdb-col md="9" class="mb-4">
          <mdb-card>
            <mdb-card-body>
              <div style="display: block">
                <mdb-line-chart
                  :data="lineChartData"
                  :options="lineChartOptions"
                  :height="500"
                />
              </div>
            </mdb-card-body>
          </mdb-card>
        </mdb-col>
        <mdb-col md="3" class="mb-4">
          <mdb-card class="mb-4">
            <mdb-card-header class="text-center">
              Pump Control
            </mdb-card-header>
            
            <mdb-input
              type="number"
              :min="0"
              :max="10"
              placeholder="กรอกปริมาณปุ๋ย / ml"
              v-model="amoutML"
              outline
              style="margin-bottom: -5px; margin-top: 10px"
            />
            <mdb-btn
              color="primary"
              size="sm"
              @click="getRelayByAmout(0, amoutML)"
              >Bottom 0</mdb-btn
            >
            <mdb-btn
              color="primary"
              size="sm"
              @click="getRelayByAmout(1, amoutML)"
              >Bottom 1</mdb-btn
            >
            <mdb-btn
              color="primary"
              size="sm"
              @click="getRelayByAmout(2, amoutML)"
              >Bottom 2</mdb-btn
            >
            <mdb-btn
              color="primary"
              size="sm"
              @click="getRelayByAmout(3, amoutML)"
              >Bottom 3</mdb-btn
            >
          </mdb-card>
        </mdb-col>
      </mdb-row>
    </section>
    <section>
      <img
        src="http://raspberrypi.local:5000/cam"
        alt="thumbnail 1"
        class="img-thumbnail img-fluid z-depth-1"
        style="width: 965px"
      />
    </section>
  </section>
</template>

<script>
import {
  mdbRow,
  mdbCol,
  mdbBtn,
  mdbCard,
  mdbCardBody,
  mdbCardHeader,
  mdbCardText,
  mdbLineChart,
  mdbInput,
} from "mdbvue";

import axios from "axios";
export default {
  name: "Dashboard",
  components: {
    mdbRow,
    mdbCol,
    mdbBtn,
    mdbCard,
    mdbCardBody,
    mdbCardHeader,
    mdbCardText,
    mdbLineChart,
    mdbInput,
  },
  data() {
    return {
      showFrameModalTop: false,
      showFrameModalBottom: false,
      showSideModalTopRight: false,
      showSideModalTopLeft: false,
      showSideModalBottomRight: false,
      showSideModalBottomLeft: false,
      showCentralModalSmall: false,
      showCentralModalMedium: false,
      showCentralModalLarge: false,
      showCentralModalFluid: false,
      showFluidModalRight: false,
      showFluidModalLeft: false,
      showFluidModalTop: false,
      showFluidModalBottom: false,

      lineChartData: {
        //labels: ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul"],
        datasets: [
          {
            label: "PH",
            backgroundColor: "rgba(245, 74, 85, 0.5)",
            data: [1, 2, 3],
          },
        ],
      },
      lineChartOptions: {
        responsive: true,
        maintainAspectRatio: false,
        scales: {
          xAxes: [
            {
              gridLines: {
                display: false,
                color: "rgba(0, 0, 0, 0.1)",
              },
            },
          ],
          yAxes: [
            {
              gridLines: {
                display: true,
                color: "rgba(0, 0, 0, 0.1)",
              },
            },
          ],
        },
      },
      temp: "",
      humidity: "",
      phData: [],
      isToggled: [false, false, false, false, false, false, false, false],
      pHRealtime: "",
      ec: "",
      number: "",
      amoutML: "",
    };
  },
  methods: {
    getTemp() {
      axios
        .get("/sensor/temp")
        .then((res) => {
          if (res.data.temp == null) {
            this.temp = "ไม่มีข้อมูล";
          }
          if (res.data.humid == null) {
            this.humidity = "No data";
          } else {
            this.temp = res.data.temp;
            this.humidity = res.data.humid;
          }
          console.log("Test" + res.data.temp);
        })
        .catch((error) => {
          console.log(error);
        });
    },
    getPHData() {
      axios
        .get("/data/ph?limit=8")
        .then((res) => {
          this.phData = res.data.data;
          console.log(res.data.data);
        })
        .catch((error) => {
          console.log(error);
        });
    },
    RelayControl(number) {
      console.log("Relays: " + this.isToggled);
      axios
        .get(`/relay/${number}/${this.isToggled[number]}`)
        .then(() => {
          //console.log(res.data);
        })
        .catch((error) => {
          console.log(error);
        });
    },
    getStatusRelay() {
      axios.get("/relay").then((res) => {
        for (let i = 0; i < 8; i++) {
          //this.isToggled[i] = res.data.Relays[i].isOn
          this.isToggled[i] = true;
        }
        console.log("Status: " + res.data.Relays[0].isOn);
      });
    },
    getPHrealtime() {
      axios.get("/sensor/ph").then((res) => {
        if (res.data.ph == null) {
          this.pHRealtime = "ไม่มีข้อมูล";
        } else {
          this.pHRealtime = res.data.ph.toFixed(2);
        }
      });
    },
    getEC() {
      axios.get("/sensor/tds").then((res) => {
        this.ec = res.data.ec.toFixed(2);
      });
    },
    getRelayByAmout(number, amoutML) {
      axios
        .get(`relay/on_by_rate/${number}/${amoutML}`)
        .then(() => {
          //console.log(res.data);
        })
        .catch((error) => {
          console.log(error);
        });
    },
  },
  created() {
    //this.interval1 = setInterval(() => this.getTemp(), 5000);
    this.getPHData();
    this.getStatusRelay();
    this.getTemp();
    this.interval1 = setInterval(() => this.getPHrealtime(), 5000);
    //this.getPHrealtime();
    this.getEC();
  },
  watch: {
    phData(newData) {
      const data = this.lineChartData;
      data.datasets[0].data = newData.map((x) => x[1]);
      data.labels = newData.map((x) => x[0]);
      this.lineChartData = { ...data };
    },
  },
};
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
.cascading-admin-card {
  margin: 20px 0;
}
.cascading-admin-card .admin-up {
  margin-left: 4%;
  margin-right: 4%;
  margin-top: -20px;
}
.cascading-admin-card .admin-up .fas,
.cascading-admin-card .admin-up .far {
  box-shadow: 0 2px 9px 0 rgba(0, 0, 0, 0.2), 0 2px 13px 0 rgba(0, 0, 0, 0.19);
  padding: 1.7rem;
  font-size: 2rem;
  color: #fff;
  text-align: left;
  margin-right: 1rem;
  border-radius: 3px;
}
.cascading-admin-card .admin-up .data {
  float: right;
  margin-top: 2rem;
  text-align: right;
}
.admin-up .data p {
  color: #999999;
  font-size: 20px;
}
.classic-admin-card .card-body {
  color: #fff;
  margin-bottom: 0;
  padding: 0.9rem;
}
.classic-admin-card .card-body p {
  font-size: 13px;
  opacity: 0.7;
  margin-bottom: 0;
}
.classic-admin-card .card-body h4 {
  margin-top: 10px;
}
</style>
