<template>
  <footer class="bg-dark text-center text-white">
    <!-- Grid container -->
    <div class="container p-4 pb-0">
      <!-- Section: Social media -->
      <section class="mb-4">
        <!-- Facebook -->
        <a class="btn btn-outline-light btn-floating m-1" href="https://www.facebook.com/eldepove" role="button"><i
            class="fab fa-facebook-f"></i></a>

        <!-- Twitter -->
        <a class="btn btn-outline-light btn-floating m-1" href="#!" role="button"><i class="fab fa-twitter"></i></a>

        <!-- Instagram -->
        <a class="btn btn-outline-light btn-floating m-1" href="https://www.instagram.com/eldepove/?hl=es"
          role="button"><i class="fab fa-instagram"></i></a>
      </section>
      <!-- Section: Social media -->
    </div>
    <!-- Grid container -->
    <div class="row">
      <p class="text-white"><strong>Email: </strong>{{ info_club["email"] }} | <strong>Telefono: </strong>
        {{ info_club["phone"] }}</p>
    </div>
    <!-- Copyright -->
    <div class="text-center p-3" style="background-color: rgba(0, 0, 0, 0.2);">
      © 2022 Copyright:
      <a class="text-white" href="#">Club Villa Elisa</a>
    </div>
    <!-- Copyright -->
  </footer>
</template>

<script>
import { apiService } from "@/api";

export default {
  data() {
    return {
      info_club: [],
      errors: [],
    };
  },
  // Fetches posts when the component is created.
  created() {
    apiService
      .get("/api/club/info")
      .then((response) => {
        // JSON responses are automatically parsed.
        this.info_club = response.data;
      })
      .catch((e) => {
        this.errors.push(e);
      });
  },
};
</script>