<template>
  <div class="home">
    <HelloWorld/>
    <VueBootstrapCharts/>
    <VueBootstrapNotifications/>
    <ToggleSwitch/>
  </div>
</template>

<script>
// @ is an alias to /src
import HelloWorld from '@/components/HelloWorld.vue'
import VueBootstrapCharts from '@/components/VueBootstrapCharts.vue'
import VueBootstrapNotifications from '@/components/VueBootstrapNotifications.vue'
//import ToggleSwitch from '@/components/ToggleSwitch.vue'

export default {
  name: 'Home',
  components: {
    HelloWorld,
    VueBootstrapCharts,
    VueBootstrapNotifications,
    //ToggleSwitch
  }
}
</script>
