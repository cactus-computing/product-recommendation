import Vue from 'vue';
import App from './App.vue';
import './assets/styles/index.css';
import router from './router';

Vue.config.devtools = true;

const app = new Vue({
    el: '#app',
    components: {
        App,
    },
    router,
});
