<template>
  <mdbContainer>
    <MDBRow>
      <MDBCol>Temp = {{ temp }}C | </MDBCol>
      <MDBCol>Humid = {{ humid }} % | </MDBCol>
      <MDBCol>Water temp = {{ waterTemp }}C | </MDBCol>
      <MDBCol>PH = {{ ph }} | </MDBCol>
      <MDBCol>EC = {{ ec }} | </MDBCol>
      <MDBCol>{{ sw[0].name }}  = {{ sw[0].value }} </MDBCol>
    </MDBRow>
  </mdbContainer>
</template>

<script>
import axios from 'axios';
import { mdbContainer, MDBRow, MDBCol } from "mdbvue";

export default {
  name: 'msg',
  components: { mdbContainer, MDBRow, MDBCol},
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
