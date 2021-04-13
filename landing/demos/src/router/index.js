import Vue from 'vue';
import Router from 'vue-router';

Vue.use(Router);
const routes = [
    { path: '/landing', component: () => import('../views/landing.vue'), name: 'landing' },
];
const router = new Router({
    base: '/',
    routes,
});
export default router;
