<template>
  <div class="home">
    <HelloWorld/>
    <TempCharts/>
  </div>
</template>

<script>
// @ is an alias to /src
import HelloWorld from '@/components/HelloWorld.vue'
import TempCharts from '@/components/TempCharts.vue'
//import ToggleSwitch from '@/components/ToggleSwitch.vue'

export default {
  name: 'Home',
  components: {
    HelloWorld,
    TempCharts,
    //ToggleSwitch
  }
}
</script>
