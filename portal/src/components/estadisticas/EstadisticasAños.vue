<template>
  <Line :chart-options="chartOptions" :chart-data="chartData" :chart-id="chartId" :dataset-id-key="datasetIdKey"
    :plugins="plugins" :css-classes="cssClasses" :styles="styles" :width="width" :height="height" />
</template>
  
<script>
import { Line } from 'vue-chartjs'
import { Chart as ChartJS, Title, Tooltip, Legend, LineElement, LinearScale, PointElement, CategoryScale } from 'chart.js'
import { apiService } from "@/api";

ChartJS.register(Title, Tooltip, Legend, LineElement, LinearScale, PointElement, CategoryScale)

export default {
  name: 'LineChart',
  components: { Line },
  props: {
    chartId: {
      type: String,
      default: 'line-chart'
    },
    datasetIdKey: {
      type: String,
      default: 'label'
    },
    width: {
      type: Number,
      default: 400
    },
    height: {
      type: Number,
      default: 400
    },
    cssClasses: {
      default: '',
      type: String
    },
    styles: {
      type: Object,
      default: () => { }
    },
    plugins: {
      type: Array,
      default: () => { }
    }
  },
  data() {
    return {
      chartData: {
        labels: [],
        datasets: [{
          label: 'Socios',
          data: [],
          backgroundColor: '#f87979'
        }]
      },
      chartOptions: {
        responsive: true,
        maintainAspectRatio: false
      }
    }
  },
  created() {
    apiService
      .get("/api/club/socios-años")
      .then((response) => {
        // JSON responses are automatically parsed.
        let cant_lista = []
        for (let i = 0; i < response.data.length; i++) {
          this.chartData.labels.push(response.data[i][0]);
          cant_lista.push(response.data[i][1])
        }
        this.chartData.datasets[0].data = cant_lista
      })
      .catch((e) => {
        this.errors.push(e);
      });
  },
}
</script>
  