import Vue from 'vue';
import App from './App.vue';
import './assets/styles/index.css';
import router from './router';

const app = new Vue({
    el: '#app',
    components: {
        App,
    },
    router,
});
