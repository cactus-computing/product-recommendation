import Vue from 'vue';
import Router from 'vue-router';
import demos from '../views/demos.vue';

Vue.use(Router);
const routes = [
    { path: '/demos', component: demos, name: 'demos' },
];
const router = new Router({
    base: '/',
    routes,
    mode: 'history',
});
export default router;
