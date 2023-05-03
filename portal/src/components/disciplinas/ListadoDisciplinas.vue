<template>
    <div id="espacio" style="min-height: 80vh;">
    <h1 style="text-align:center">
        <strong>Disciplinas</strong>
    </h1>
    <table id="tableComponent" class="table table-bordered table-hover">
        <thead>
            <tr>
                <th style="text-align: center" v-for="(campo, i) in campos" :key="i">
                    <!-- Listar los campos para la tabla -->
                    {{ campo }}
                </th>
            </tr>
        </thead>
        <tbody>
            <tr style="text-align: center;" v-for="(disciplina, i) in dataPagina" :key="i">
                <td>{{ disciplina.name }}</td>
                <td>{{ disciplina.category }}</td>
                <td>{{ disciplina.days }}</td>
                <td>{{ disciplina.time }}</td>
                <td>{{ disciplina.teacher }}</td>
                <td> $ {{ disciplina.price }}</td>
            </tr>
        </tbody>
    </table>
    <nav aria-label="Page navigation example">
        <ul class="pagination justify-content-center">
            <li class="page-item" v-on:click="getPaginaAnterior()"><a class="page-link" href="#">Anterior</a></li>
            <li v-for="(pagina, i) in getTotalPaginas()" :key="i" v-on:click="getDataPagina(pagina)" class="page-item"
                v-bind:class="estaActiva(pagina)">
                <a class="page-link" href="#"> {{ pagina }} </a>
            </li>
            <li class="page-item" v-on:click="getPaginaSiguiente()"> <a class="page-link" href="#">Siguiente</a></li>
        </ul>
    </nav>
    </div>
</template>
  
<script>
import { apiService } from "@/api";

export default {
    data() {
        return {
            disciplines: [],
            errors: [],
            campos: ["Nombre", "Categoria", "Dias", "Horario", "Profesor", "Precio"],
            porPagina: 5,
            dataPagina: [],
            paginaActual: 1
        };
    },
    mounted() {

    },
    methods: {
        getTotalPaginas() {    // Redondeo por si da con decimales
            return Math.ceil(this.disciplines.length / this.porPagina);
        },
        getDataPagina(numPagina) {
            this.paginaActual = numPagina;
            this.dataPagina = [];
            let inicio = (numPagina * this.porPagina) - this.porPagina;
            let fin = (numPagina * this.porPagina);
            this.dataPagina = this.disciplines.slice(inicio, fin);
        },
        getPaginaSiguiente() {
            if (this.paginaActual < this.getTotalPaginas()) {
                this.paginaActual++;
            }
            this.getDataPagina(this.paginaActual);
        },
        getPaginaAnterior() {
            if (this.paginaActual > 1) {
                this.paginaActual--;
            }
            this.getDataPagina(this.paginaActual);
        },
        estaActiva(numPagina) {
            return numPagina == this.paginaActual ? "active" : "";
        }
    },
    computed: {
    },
    // Fetches posts when the component is created.
    created() {
        apiService
            .get("/api/club/disciplinas")
            .then((response) => {
                // JSON responses are automatically parsed.
                this.disciplines = response.data;
                this.getDataPagina(1);
            })
            .catch((e) => {
                this.errors.push(e);
            });
    },
};
</script>
  