<template>
  <mdb-container>
    <MDBRow>
      <MDBCol>
        Test 
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
