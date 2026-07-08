import { createRouter, createWebHistory } from 'vue-router';

export const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    { path: '/', component: () => import('@/views/Landing.vue') },
    { path: '/servicios', component: () => import('@/views/Servicios.vue') },
    { path: '/portafolio', component: () => import('@/views/Portafolio.vue') },
    { path: '/portafolio/:slug', component: () => import('@/views/PortafolioDetalle.vue') },
    { path: '/blog', component: () => import('@/views/Blog.vue') },
    { path: '/blog/:slug', component: () => import('@/views/BlogDetalle.vue') },
  ],
  scrollBehavior(to) {
    if (to.hash) return { el: to.hash, top: 80, behavior: 'smooth' };
    return { top: 0 };
  },
});
