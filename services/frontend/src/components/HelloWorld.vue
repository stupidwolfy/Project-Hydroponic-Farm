<template>
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
</template>

<script>
import axios from 'axios';
import { mdbContainer, mdbRow, mdbCol } from "mdbvue";

export default {
  name: 'msg',
  components: { mdbContainer, mdbRow, mdbCol},
  data() {
    return {
      msg: 'err',
      temp: 'err',
      humid: 'err',
      waterTemp: 'err',
      ph: 'err',
      ec: 'err',
      sw: ["err"],
    };
  },
  methods: {
    getMessage() {
      axios.get('/')
        .then((res) => {
          this.msg = res.data;
        })
        .catch((error) => {
          console.error(error);
        });
    },
    getTemp() {
      axios.get('/sensor/temp')
        .then((res) => {
          this.temp = res.data.temp;
          this.humid = res.data.humid;
        })
        .catch((error) => {
          console.error(error);
        });
    },
    getWaterTemp() {
      axios.get('/sensor/water_temp')
        .then((res) => {
          this.waterTemp = res.data.temp;
        })
        .catch((error) => {
          console.error(error);
        });
    },
    getPH() {
      axios.get('/sensor/ph')
        .then((res) => {
          this.ph = res.data.ph;
        })
        .catch((error) => {
          console.error(error);
        });
    },
    getEC() {
      axios.get('/sensor/ec')
        .then((res) => {
          this.ec = res.data.ec;
          this.ec += res.data.unit;
        })
        .catch((error) => {
          console.error(error);
        });
    },
    getSW(swID) {
      axios.get('/switch/'+swID)
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
