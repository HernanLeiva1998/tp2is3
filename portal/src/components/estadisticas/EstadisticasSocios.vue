<template>
  <Doughnut :chart-options="chartOptionsDisciplines" :chart-data="chartDataDisciplines" :chart-id="chartId"
    :dataset-id-key="datasetIdKey" :plugins="plugins" :css-classes="cssClasses" :styles="styles" :width="width"
    :height="height" />
</template>

<script>
import { Doughnut } from "vue-chartjs";
import {
  Chart as ChartJS,
  Title,
  Tooltip,
  Legend,
  ArcElement,
  CategoryScale,
} from "chart.js";
import { apiService } from "@/api";

ChartJS.register(Title, Tooltip, Legend, ArcElement, CategoryScale);

export default {
  name: "DoughnutChart",
  components: {
    Doughnut,
  },
  props: {
    chartId: {
      type: String,
      default: "doughnut-chart",
    },
    width: {
      type: Number,
      default: 400,
    },
    height: {
      type: Number,
      default: 400,
    },
    cssClasses: {
      default: "",
      type: String,
    },
    styles: {
      type: Object,
      default: () => { },
    },
    plugins: {
      type: Array,
      default: () => [],
    },
  },
  data() {
    return {
      chartDataDisciplines: {
        labels: [],
        datasets: [
          {
            backgroundColor: [],
            data: [],
          },
        ],
      },
      chartOptionsDisciplines: {
        responsive: true,
        maintainAspectRatio: false,
      },
      errors: [],
    };
  },
  created() {
    apiService
      .get("/api/club/socios-genero")
      .then((response) => {
        // JSON responses are automatically parsed.
        let cant_lista = []
        let colores = []
        for (let i = 0; i < response.data.length; i++) {
          this.chartDataDisciplines.labels.push(response.data[i][0]);
          cant_lista.push(response.data[i][1])
          colores.push(response.data[i][2])
        }
        this.chartDataDisciplines.datasets[0].data = cant_lista
        this.chartDataDisciplines.datasets[0].backgroundColor = colores
      })
      .catch((e) => {
        this.errors.push(e);
      });
  },
};
</script>