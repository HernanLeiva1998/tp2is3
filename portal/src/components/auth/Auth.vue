<template>
  <div v-if="isLoggedIn">
    <h3>Usuario: {{ authSocio.nombre }}</h3>
    <h3>Mail: {{ authSocio.email }}</h3>
    <h3>Id: {{ authSocio.id }}</h3>
    <h3>{{ this.error }}</h3>

    <button type="button" @click="logout">Logout</button>
  </div>

  <div v-else style="min-height: 80vh">
    <div v-if="this.error">
      <div class="alert alert-warning alert-dismissible fade show" role="alert">
        <p>Credenciales Invalidas</p>
        <button
          type="button"
          class="btn-close"
          data-bs-dismiss="alert"
          aria-label="Close"
          v-on:click="swapEsconder"
        ></button>
      </div>
    </div>
    <div class="col-sm-9 col-md-7 col-lg-5 mx-auto">
      <div class="card border-0 shadow rounded-3 my-5">
        <div class="card-body p-4 p-sm-5">
          <h5 class="card-title text-center mb-5 fw-light fs-5">Log In</h5>
          <form action class="form" @submit.prevent="login">
            <div class="mb-3">
              <label class="form-label" for="#socio.email">Email</label>
              <input
                class="form-control"
                type="email"
                name="email"
                placeholder="Correo"
                v-model="socio.email"
                id="email"
                required
              />
            </div>
            <div class="mb-3">
              <label class="form-label" for="#socio.password">Password</label>
              <input
                class="form-control"
                type="password"
                name="password"
                placeholder="Clave"
                v-model="socio.password"
                id="password"
                required
              />
            </div>
            <input
              class="btn btn-primary btn-login text-uppercase fw-bold"
              type="submit"
              value="Login"
            />
          </form>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { mapActions, mapGetters } from "vuex";

export default {
  data: () => ({
    socio: {
      email: null,
      password: null,
    },
  }),

  computed: {
    ...mapGetters({
      authSocio: "auth/socio",
      isLoggedIn: "auth/isLoggedIn",
    }),
  },

  methods: {
    ...mapActions("auth", ["loginSocio", "logoutSocio"]),

    async login() {
      await this.loginSocio(this.socio).catch(() => {
        this.error = true;
      });
      this.socio = {
        email: null,
        password: null,
      };

      if (this.isLoggedIn) {
        this.$router.push("/");
      }
    },

    async logout() {
      await this.logoutSocio().catch((err) => {
        console.log(err);
      });
      this.error = false;
      this.socio = {
        email: null,
        password: null,
      };
      this.$router.push("/");
    },

    swapEsconder() {
      this.error = false;
    }

  },
};
</script>
