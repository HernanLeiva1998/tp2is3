<script setup>
import EstadisticasDisciplinas from "../components/estadisticas/EstadisticasDisciplinas.vue";
import EstadisticasSocios from "../components/estadisticas/EstadisticasSocios.vue";
import EstadisticasAños from "../components/estadisticas/EstadisticasAños.vue";
import Footer from "../components/footer.vue"
</script>

<template>
  <main>
    <div class="row" style="min-height: 80vh">
    <div class="col-sm-9 col-md-9 col-lg-10 mx-auto">
      <div class="card border-0 shadow rounded-3 my-5">
        <div class="card-body p-4 p-sm-5">
          <h5 class="card-title text-center mb-5 fw-light fs-5">
            Estadisticas
          </h5>
          <div class="row mb-4">
            <div class="col-6">
              <h4 class="text-center">Socios por Disciplina</h4>
              <EstadisticasDisciplinas />
            </div>
            <div class="col-6">
              <h4 class="text-center">Socios por Genero</h4>
              <EstadisticasSocios />
            </div>
          </div>
          <div class="row">
            <div class="col-12">
              <h4 class="text-center">Socios inscriptos por año</h4>
              <EstadisticasAños />
            </div>
          </div>
        </div>
      </div>
    </div>
    </div>
    <Footer />
  </main>
</template>