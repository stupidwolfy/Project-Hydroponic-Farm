<template>
   <section>
     <mdb-toast-notification :show="show"></mdb-toast-notification>
     <mdb-toast-notification :show="show"></mdb-toast-notification>
     <mdb-toast-notification :show="show"></mdb-toast-notification>
   </section>
</template>

<script>
  import {
    mdbToastNotification
  } from "mdbvue";

  export default {
    name: "NotificationsFreePage",
    components: {
      mdbToastNotification,
    },
    data() {
      return {
        show: true
      }
    }
  };
</script>