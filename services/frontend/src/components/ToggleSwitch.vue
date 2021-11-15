<template>
  <MDBSwitch
    label="Default switch checkbox input"
    v-model="switch1"
  />
</template>

<script>
  import { MDBSwitch } from "mdb-vue-ui-kit";
  import { ref } from "vue";

  export default {
    components: {
      MDBSwitch
    },
    setup() {
      const switch1 = ref(false);
      const switch2 = ref(true);
      const switch3 = ref(false);
      const switch4 = ref(true);

      return {
        switch1,
        switch2,
        switch3,
        switch4
      };
    }
  };
</script>