<script setup>
import ListadoCuotasImpagas from "../components/pagos/ListadoCuotasImpagas.vue";
import ListadoCuotasPagas from "../components/pagos/ListadoCuotasPagas.vue";
import Footer from "../components/footer.vue"
</script>

<template>
    <main>
        <ListadoCuotasImpagas />
        <div id="espacio" style="min-height: 2.5vh;"></div>
        <ListadoCuotasPagas />
        <Footer />
    </main>
</template>