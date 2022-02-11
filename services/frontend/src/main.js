import '@fortawesome/fontawesome-free/css/all.min.css'
//import 'bootstrap-css-only/css/bootstrap.min.css'
import 'bootstrap/dist/css/bootstrap.css';
import 'mdbvue/lib/css/mdb.min.css'
import axios from 'axios';
import Vue from 'vue'
import App from './App'
//import App from './App.vue';
import router from './router'
import store from './store'
import vuetify from './plugins/vuetify'

axios.defaults.withCredentials = true;
axios.defaults.baseURL = `http://${process.env.VUE_APP_HOST_HOSTNAME}.local:5000/`;  // the FastAPI backend <todo: dynamicly replace with host ip>

Vue.config.productionTip = false

new Vue({
  router,
  store,
  vuetify,
  render: h => h(App)
}).$mount('#app')
