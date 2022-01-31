<template>
  <mdb-container>
    <mdbRow>
      <mdbCol>
        <img :src=hostname width="25%"> 
      </mdbCol>
    </mdbRow>
  </mdb-container>
</template>
<script>

import { mdbContainer, mdbRow, mdbCol } from "mdbvue";

export default {
  name: 'msg',
  components: {
      mdbContainer, 
      mdbRow, 
      mdbCol
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
