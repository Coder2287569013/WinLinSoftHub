import { createRouter, createWebHistory } from 'vue-router';
import TheWelcome from '@/components/TheWelcome.vue';
import Categories from '@/components/Categories.vue';
import OSpage from '@/components/OSpage.vue';
import CategoriesLin from '@/components/CategoriesLin.vue';
import LinuxPage from '@/components/LinuxPage.vue';
import LinProgs from '@/components/LinProgs.vue'
import Register from '@/components/Register.vue'
import Login from '@/components/Login.vue';

const router = createRouter({
    history: createWebHistory(),
    routes: [
        {
            path: '/',
            name: 'OSpage',
            component: OSpage
        },
        {
            path: '/win/progs/:category?',
            name: 'WinProgs',
            component: TheWelcome,
            props: true
        },
        {
            path: '/lin/:os?/progs/:category_l?',
            name: 'LinProgs',
            component: LinProgs,
            props: true
        },
        {
            path: '/win/category',
            name: 'Categories',
            component: Categories
        },
        //CONTINUE
        {
            path: '/lin/os-page',
            name: 'LinuxPage',
            component: LinuxPage
        },
        {
            path: '/lin/:os?/category',
            name: 'LinCategory',
            component: CategoriesLin
        },
        {
            path: '/register',
            name: 'RegistrationForm',
            component: Register,
        },
        {
            path: '/login',
            name: 'LoginForm',
            component: Login,
        },
    ]
});

export default router;