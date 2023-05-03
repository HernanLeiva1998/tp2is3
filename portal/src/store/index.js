import { createStore } from "vuex";
import authModule from "../store/modules/auth";
import VuexPersistence from 'vuex-persist'

const store = createStore({
  modules: {
    auth: authModule,
  },
  plugins: [
    new VuexPersistence({
      store: window.localStorage
    }).plugin
  ]
});

export default store;
