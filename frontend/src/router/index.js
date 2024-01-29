import { createRouter, createWebHistory } from 'vue-router';
import TheWelcome from '@/components/TheWelcome.vue';
import Categories from '@/components/Categories.vue';
import OSpage from '@/components/OSpage.vue';

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
            path: '/win/category',
            name: 'Categories',
            component: Categories
        },
    ]
});

export default router;