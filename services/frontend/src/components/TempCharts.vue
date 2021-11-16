<template>
  <mdb-container>
    <mdb-line-chart
      :data="lineChartData"
      :options="lineChartOptions"
      :width="600"
      :height="300"
      reactive
      :time="1000"
    ></mdb-line-chart>
  </mdb-container>
</template>

<script>
  import { mdbLineChart, mdbContainer } from "mdbvue";
  import axios from 'axios';
  
  export default {
    name: "ChartPage",
    components: {
      mdbLineChart,
      mdbContainer
    },
    data() {
      return {
        lineChartData: {
          labels: [
            "January",
            "February",
            "March",
            "April",
            "May",
            "June",
            "July"
          ],
          datasets: [
            {
              label: "Temp",
              backgroundColor: "rgba(255, 99, 132, 0.1)",
              borderColor: "rgba(255, 99, 132, 1)",
              borderWidth: 0.7,
              data: [65, 59, 80, 81, 56, 55, 40]
            },
            {
              label: "Humid",
              backgroundColor: "rgba(151,187,205,0.2)",
              borderColor: "rgba(151,187,205,1)",
              borderWidth: 0.8,
              data: [28, 48, 40, 19, 86, 27, 90]
            }
          ]
        },
        lineChartOptions: {
          responsive: true,
          maintainAspectRatio: false,
          scales: {
            xAxes: [
              {
                gridLines: {
                  display: true,
                  color: "rgba(0, 0, 0, 0.1)"
                }
              }
            ],
            yAxes: [
              {
                gridLines: {
                  display: true,
                  color: "rgba(0, 0, 0, 0.1)"
                }
              }
            ]
          }
        }
      };
    },
    methods: {
      getTemp() {
        axios.get('/sensor/temp')
          .then((res) => {
            return this.temp = res.data.temp;
          })
          .catch((error) => {
            console.error(error);
          });
        },
      },
    async created() {
      this.lineChartData.datasets[0].data.push(this.getTemp());
    }
  };
</script>