<template>
  <div class="home">
    <HelloWorld/>
    <TempCharts/>
    <CameraSelector/>
    <ThreeJSTest/>
  </div>
</template>

<script>
// @ is an alias to /src
import HelloWorld from '@/components/HelloWorld.vue'
import TempCharts from '@/components/TempCharts.vue'
import CameraSelector from '@/components/CameraSelector.vue'
import ThreeJSTest from '@/components/ThreeJSTest.vue'
//import ToggleSwitch from '@/components/ToggleSwitch.vue'

export default {
  name: 'Home',
  components: {
    HelloWorld,
    TempCharts,
    CameraSelector,
    ThreeJSTest,
    //ToggleSwitch
  }
}
</script>
