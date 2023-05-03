import { apiService } from "@/api";

const namespaced = true;

const state = {
  socio: {},
  isLoggedIn: false,
};

const getters = {
  isLoggedIn: (state) => state.isLoggedIn,
  socio: (state) => state.socio,
};

const actions = {
  async loginSocio({ dispatch }, socio) {
    await apiService.post("api/auth", socio);
    await dispatch("fetchSocio");
  },
  async fetchSocio({ commit }) {
    await apiService
      .get("api/socio_jwt")
      .then(({ data }) => commit("setSocio", data));
  },
  async logoutSocio({ commit }) {
    await apiService.get("api/logout_publico");
    commit("logoutSocioState");
  },
};

const mutations = {
  setSocio(state, socio) {
    state.isLoggedIn = true;
    state.socio = socio.profile;
  },
  logoutSocioState(state) {
    state.isLoggedIn = false;
    state.socio = {};
  },
};

export default {
  namespaced,
  state,
  getters,
  actions,
  mutations,
};
