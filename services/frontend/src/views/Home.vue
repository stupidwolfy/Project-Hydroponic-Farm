<template>
  <div class="home">
    <HelloWorld/>
    <TempCharts/>
    <img :src="'http://192.168.1.11:5000/cam'">
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
