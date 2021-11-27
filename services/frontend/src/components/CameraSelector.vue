<template>
  <mdb-container>
    <MDBRow>
      <MDBCol>
        <img :src="'http://192.168.1.11:5000/cam'"> 
      </MDBCol>
    </MDBRow>
  </mdb-container>
</template>
<script>

import { mdbContainer, MDBRow, MDBCol } from "mdbvue";

export default {
  name: 'msg',
  components: {
      mdbContainer, 
      MDBRow, 
      MDBCol
    },
  data() {
  },
  methods: {
  },
  created() {
  },
};
</script>
