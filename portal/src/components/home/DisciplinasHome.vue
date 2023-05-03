<template>
  <div class="row" v-if="disciplines && disciplines.length">
    <div class="col-sm-9 col-md-9 col-lg-6 mx-auto">
      <div class="card border-0 shadow rounded-3 my-5">
        <div class="card-body p-4 p-sm-5">
          <h5 class="card-title text-center mb-5 fw-light fs-5">Disciplinas</h5>
          <div class="row mb-4">
            <div class="col-6">
              <input class="form-control me-2" type="search" placeholder="Buscar disciplina por nombre..."
                aria-label="Buscar por nombre" v-model="search" />
            </div>
          </div>
          <div class="row">
            <div class="col-sm-9 col-md-9 col-lg-6 mb-3" v-for="(discipline, index) in filterList" :key="index">
              <div class="card text-center">
                <div class="card-header"></div>
                <div class="card-body">
                  <h5 class="card-title">{{ discipline.name }}</h5>
                  <p class="card-text">
                  <ul class="list-group">
                    <li class="list-group-item"><strong>Profesores: </strong>{{ discipline.teacher }}</li>
                    <li class="list-group-item"><strong>Horarios: </strong>{{ discipline.time }}</li>
                    <li class="list-group-item"><strong>Categoria: </strong>{{ discipline.category }}</li>
                    <li class="list-group-item"><strong>Dias: </strong>{{ discipline.days }}</li>
                    <li class="list-group-item"><strong>Costo: </strong>{{ discipline.price }}</li>
                  </ul>
                  </p>
                </div>
                <div class="card-footer text-muted"></div>
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

export default {
  data() {
    return {
      disciplines: [],
      errors: [],
      search: '',
    };
  },
  computed: {
    filterList() {
      return this.disciplines.filter(discipline => {
        return discipline.name.toLowerCase().includes(this.search.toLowerCase())
      })
    }
  },
  // Fetches posts when the component is created.
  created() {
    apiService
      .get("/api/club/disciplinas")
      .then((response) => {
        // JSON responses are automatically parsed.
        this.disciplines = response.data;
      })
      .catch((e) => {
        this.errors.push(e);
      });
  },
};
</script>
