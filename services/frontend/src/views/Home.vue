<template>
  <div class="home">
    <HelloWorld/>
    <VueBootstrapCharts/>
    <ToggleSwitch/>
  </div>
</template>

<script>
// @ is an alias to /src
import HelloWorld from '@/components/HelloWorld.vue'
import VueBootstrapCharts from '@/components/VueBootstrapCharts.vue'
//import ToggleSwitch from '@/components/ToggleSwitch.vue'

export default {
  name: 'Home',
  components: {
    HelloWorld,
    VueBootstrapCharts,
    //ToggleSwitch
  }
}
</script>
