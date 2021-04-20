import Vue from 'vue';
import App from './App.vue';
import './assets/styles/index.css';
import router from './router';
import Vuelidate from 'vuelidate'

Vue.config.devtools = true;
Vue.use(Vuelidate);

const app = new Vue({
    el: '#app',
    components: {
        App,
    },
    router,
});
