<template>
    <div id="carnet" class="container"
        style="font-family:'Comic Sans MS','Comic Sans',cursive;width: 300px; min-height: 80vh; " v-if="socio">
        <br>
        <div class="card border-dark border border-5 text-center" style="width: 300px;">
            <div class="row">
                <div class="column-12">
                    <h1 style="font-family:'Brush Script MT', cursive; font-size:2rem; border-bottom:5px solid;">
                        Club Deportivo
                        Villa
                        Elisa</h1>
                </div>
            </div>
            <div class="row">
                <div class="col-12">
                    <div class="card-body">
                        <span style="font-size: 1.5rem ;">{{ socio.profile.user }}</span><br>
                        {{ socio.profile.document_type }}: {{ socio.profile.document_number }} <br>
                        Socio: #{{ socio.profile.number }} <br>
                        Estado: <span v-if="socio.status == 'OK'"> Al día</span> <span v-else>No esta al día</span> <br>
                        Email: {{ socio.profile.email }}<br>
                        Género: {{ socio.profile.gender }}<br>
                        Se identifica como: {{ socio.profile.gender_other }} <br>
                        Dirección: {{ socio.profile.address }}<br>
                        Teléfono: {{ socio.profile.phone }}
                    </div>
                </div>
            </div>
        </div>
    </div>
    <br>
</template>
  
<script>
import { apiService } from "@/api";

export default {
    inject: ['URL_API_LICENCIA'],
    data() {
        return {
            socio: '',
            errors: [],
        };
    },
    // Fetches posts when the component is created.
    created() {
        apiService
            .get("api/me/license")
            .then((response) => {
                // JSON responses are automatically parsed.
                this.socio = response.data;
            })
            .catch((e) => {
                this.errors.push(e);
            });
    },
};
</script>
  