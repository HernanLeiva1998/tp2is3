<template>
  <div>
    <div v-if="estaLogueado">
      <div class="row justify-content-center mt-3">
        <div class="col-sm-4 col-md-4 col-lg-6">
          <button v-on:click="swapMostrar" class="btn btn-outline-success" type="submit">Verificar Estado Cuota</button>
        </div>
      </div>
      <div class="row mt-2 justify-content-center" v-if="mostrar_estado">
        <div class="col-6">
          <div class="alert alert-warning alert-dismissible fade show" role="alert">
            <p v-if="errors && errors.length">El numero de socio ingresado no existe</p>
            <p v-else-if="mostrar_vacio">Debe ingresar algun numero de socio</p>
            <p v-else>{{ info_socio["description"] }}</p>
            <button v-on:click="swapEsconder" type="button" class="btn-close" data-bs-dismiss="alert"
              aria-label="Close"></button>
          </div>
        </div>
      </div>
    </div>
    <div class="row">
      <div class="col-sm-9 col-md-7 col-lg-6 mx-auto mt-4">
        <div class="card mb-3">
          <div class="row g-0">
            <div class="col-md-4">
              <img src="../../../public/imagen_club.jpg" class="img-fluid rounded-start" alt="imagen del club" />
            </div>
            <div class="col-md-8">
              <div class="card-body">
                <h5 class="card-title">Informacion General</h5>
                <p class="card-text">
                  En este portal podrán obtener información de interés sobre el
                  club, como disciplinas habilitadas, actividades, estado de la
                  cuota societaria (carnet digital), acreditacion/visualizacion
                  de pagos, etc.
                </p>
                <p class="card-text">
                  <small class="text-muted"></small>
                </p>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
    <div class="row card-group justify-content-center">
      <div class="col-sm-9 col-md-7 col-lg-3">
        <div class="card mb-3">
          <div class="row g-0">
            <div class="col-md-4">
              <img src="../../../public/basquet.jpg" class="img-fluid rounded-start" alt="imagen de socios"
                style="height: 100%" />
            </div>
            <div class="col-md-8">
              <div class="card-body">
                <h5 class="card-title">Informacion sobre disciplinas</h5>
                <p class="card-text">
                  En este portal podran acceder a la informacion sobre las
                  disciplinas como por ejemplo los horarios, sus costos, los
                  intructores, etc.
                </p>
                <p class="card-text">
                  <small class="text-muted"></small>
                </p>
              </div>
            </div>
          </div>
        </div>
      </div>
      <div class="col-sm-9 col-md-7 col-lg-3">
        <div class="card mb-3">
          <div class="row g-0">
            <div class="col-md-4">
              <img src="../../../public/socios.jpg" class="img-fluid rounded-start" alt="imagen de socios"
                style="height: 100%" />
            </div>
            <div class="col-md-8">
              <div class="card-body">
                <h5 class="card-title">Informacion para socios</h5>
                <p class="card-text">
                  En este portal podran realizar algunas tareas, como por
                  ejemplo realizar pagos, verificar el estado de las cuotas,
                  visualizar estadisticas, etc.
                </p>
                <p class="card-text">
                  <small class="text-muted"></small>
                </p>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { apiService } from "@/api";
import { mapGetters } from 'vuex';

export default {
  data() {
    return {
      info_socio: [],
      mostrar_estado: false,
      mostrar_vacio: false,
      errors: [],
    };
  },
  computed: {
    ...mapGetters({
      estaLogueado: "auth/isLoggedIn",
    }),
  },
  methods: {
    swapMostrar() {
      this.errors.pop()
      apiService
        .get("/api/me/license")
        .then((response) => {
          // JSON responses are automatically parsed.
          this.info_socio = response.data;
        })
        .catch((e) => {
          console.log(e)
          this.errors.push(e);
        });
      this.mostrar_estado = true;
    },
    swapEsconder() {
      this.mostrar_estado = false;
      this.mostrar_vacio = false;
    }
  },
  // Fetches posts when the component is created.
};
</script>
