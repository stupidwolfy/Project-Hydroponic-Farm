<template>
  <div>
    <v-row v-for="n in 1" :key="n">
      <v-col
        v-for="value in [['Temp',temp], ['pH',ph], ['EC',ec], ['Humid',humid]]"
        :key="value"
      >
        <v-card class="mx-auto" max-width="300">
          <v-card-text>
            <div>{{ value[0] }}</div>
            <p class="text-h4 text--primary">
              {{ value[1] }}
            </p>
          </v-card-text>
        </v-card>
      </v-col>
    </v-row>
  </div>
</template>

<script>
import axios from "axios";

export default {
  name: "TempBox",

  data() {
    return {
      msg: "err",
      temp: "err",
      humid: "err",
      waterTemp: "err",
      ph: "err",
      ec: "err",
      sw: ["err"],
    };
  },
  methods: {
    getMessage() {
      axios
        .get("/")
        .then((res) => {
          this.msg = res.data;
        })
        .catch((error) => {
          console.error(error);
        });
    },
    getTemp() {
      axios
        .get("/sensor/temp")
        .then((res) => {
          this.temp = res.data.temp;
          this.humid = res.data.humid;
        })
        .catch((error) => {
          console.error(error);
        });
    },
    getWaterTemp() {
      axios
        .get("/sensor/water_temp")
        .then((res) => {
          this.waterTemp = res.data.temp;
        })
        .catch((error) => {
          console.error(error);
        });
    },
    getPH() {
      axios
        .get("/sensor/ph")
        .then((res) => {
          this.ph = res.data.ph;
        })
        .catch((error) => {
          console.error(error);
        });
    },
    getEC() {
      axios
        .get("/sensor/ec")
        .then((res) => {
          this.ec = res.data.ec;
          this.ec += res.data.unit;
        })
        .catch((error) => {
          console.error(error);
        });
    },
    getSW(swID) {
      axios
        .get("/switch/" + swID)
        .then((res) => {
          this.sw[swID] = res.data;
        })
        .catch((error) => {
          console.error(error);
        });
    },
  },
  created() {
    //this.getMessage();
    this.getTemp();
    this.getWaterTemp();
    this.getPH();
    this.getEC();
    this.getSW(0);
  },
};
</script>

<!-- <template>
  <mdbContainer>
    <mdbRow>
      <mdbCol>Temp = {{ temp }}C  </mdbCol>
      <mdbCol>Humid = {{ humid }} %  </mdbCol>
      <mdbCol>Water temp = {{ waterTemp }}C  </mdbCol>
      <mdbCol>PH = {{ ph }}  </mdbCol>
      <mdbCol>EC = {{ ec }}  </mdbCol>
      <mdbCol>{{ sw[0].name }}  = {{ sw[0].value }} </mdbCol>
    </mdbRow>
  </mdbContainer>
</template> -->
