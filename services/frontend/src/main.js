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

axios.defaults.withCredentials = true;
axios.defaults.baseURL = 'http://192.168.1.11:5000/';  // the FastAPI backend <tood: dynamicly replace with host ip>

Vue.config.productionTip = false

new Vue({
  router,
  store,
  render: h => h(App)
}).$mount('#app')
