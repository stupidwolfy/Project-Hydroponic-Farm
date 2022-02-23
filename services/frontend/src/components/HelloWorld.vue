<template>
  <v-container>
    <v-sparkline
    class="stackSheet"
      :value="value1"
      :gradient="gradient"
      :smooth="radius || false"
      :padding="padding"
      :line-width="width"
      :stroke-linecap="lineCap"
      :gradient-direction="gradientDirection"
      :fill="fill"
      :type="type"
      :auto-line-width="autoLineWidth"
      auto-draw
    ></v-sparkline>

    <v-sparkline
    class="stackSpark"
      :value="value2"
      :gradient="gradient"
      :smooth="radius || false"
      :padding="padding"
      :line-width="width"
      :stroke-linecap="lineCap"
      :gradient-direction="gradientDirection"
      :fill="fill"
      :type="type"
      :auto-line-width="autoLineWidth"
      auto-draw
    ></v-sparkline>
  </v-container>
</template>

<script>
const gradients = [
  ["#222"],
  ["#42b3f4"],
  ["red", "orange", "yellow"],
  ["purple", "violet"],
  ["#00c6ff", "#F0F", "#FF0"],
  ["#f72047", "#ffd200", "#1feaea"],
];
export default {
  name: "HelloWorld",

  data: () => ({
    width: 2,
    radius: 10,
    padding: 8,
    lineCap: "round",
    gradient: gradients[5],
    value1: [0, 2, 5, 9, 5, 10, 3, 5, 0, 0, 1, 8, 2, 9, 10],
    value2: [0, 3, 6, 7, 8, 10, 9, 0, 1, 0, 2, 4, 3, 8, 11],
    gradientDirection: "top",
    gradients,
    fill: false,
    type: "trend",
    autoLineWidth: false,
  }),
};
</script>
<style lang="css" scoped>
.stackSheet {
  position: relative;
}
.stackSpark {
  top: 0;
  left: 0;
}
</style>
