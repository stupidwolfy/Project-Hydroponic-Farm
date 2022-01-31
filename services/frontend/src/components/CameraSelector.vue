<template>
  <mdb-container>
    <MDBRow>
      <MDBCol>
        <img :src=hostname width="25%"> 
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
    return {
      hostname: 'http://'+process.env.VUE_APP_HOST_HOSTNAME+'.local:5000/cam',
    };
  },
  methods: {
  },
  created() {
  },
};
</script>
