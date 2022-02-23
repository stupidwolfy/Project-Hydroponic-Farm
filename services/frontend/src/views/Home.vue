<template>
  <div>
    <Navbarhome>
      <template v-slot:tempbox>
        <TempBox />
      </template>
      <template v-slot:helloworld>
        <HelloWorld />
      </template>
      <template v-slot:chartpage>
        <ChartPage />
      </template>
    </Navbarhome>
  </div>
</template>

<script>
import HelloWorld from "../components/HelloWorld";
import ChartPage from "../components/TempCharts";
import TempBox from "../components/TempBox";
import Navbarhome from "../components/Navigater";

export default {
  name: "Home",

  components: {
    HelloWorld,
    ChartPage,
    TempBox,
    Navbarhome,
  },
};
</script>
