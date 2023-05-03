import { createRouter, createWebHistory } from "vue-router";
import HomeView from "../views/HomeView.vue";
import DisciplinasView from "../views/DisciplinasView.vue";
import LoginView from "../views/LoginView.vue";
import EstadisticasView from "../views/EstadisticasView.vue";
import PagosView from "../views/PagosView.vue";
import carnet from "../views/CarnetView.vue"
import PagarView from "../views/PagarView.vue"

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: "/",
      name: "home",
      component: HomeView,
    },
    {
      path: "/disciplinas",
      name: "disciplinas",
      component: DisciplinasView,
    },
    {
      path: "/auth",
      name: "auth",
      component: LoginView,
    },
    {
      path: "/pagos",
      name: "pagos",
      component: PagosView,
    },
    {
      path: "/pagar",
      name: "pagar",
      component: PagarView
    },
    {
      path: "/estadisticas",
      name: "estadisticas",
      component: EstadisticasView,
    },
    {
      path: "/carnet",
      name: "carnet",
      component: carnet,
    }
  ],
});

export default router;
