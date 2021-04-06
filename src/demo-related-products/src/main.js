import { createApp } from 'vue'
import App from './App.vue'
import './assets/styles/index.css'

createApp(App).mount('#app')

const link = document.createElement('script');
const head = document.head;

const queryString = window.location.search;
const urlParams = new URLSearchParams(queryString);
const client = urlParams.get('client');

link.type = 'text/javascript';
link.id = 'CactusScript';
link.src = `/Users/rodrigooyarzun/Documents/Proyectos/Cactus/CactusCo/src/demo-related-products/src/cactusFrontDemo.js?client=${client}&environment=dev`;
head.appendChild(link);