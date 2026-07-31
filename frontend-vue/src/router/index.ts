import { createRouter, createWebHistory } from 'vue-router';
import { adminAuth } from '@/services/adminAuth';

export const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    { path: '/', component: () => import('@/views/Landing.vue') },
    { path: '/servicios', component: () => import('@/views/Servicios.vue') },
    { path: '/portafolio', component: () => import('@/views/Portafolio.vue') },
    { path: '/portafolio/:slug', component: () => import('@/views/PortafolioDetalle.vue') },
    { path: '/faq', component: () => import('@/views/FAQ.vue') },
    { path: '/quienes-somos', component: () => import('@/views/QuienesSomos.vue') },
    { path: '/terminos-y-condiciones', component: () => import('@/views/Terminos.vue') },
    { path: '/admin/login', component: () => import('@/views/admin/AdminLogin.vue') },
    {
      path: '/admin',
      component: () => import('@/views/admin/AdminLayout.vue'),
      meta: { requiresAuth: true },
      children: [
        { path: '', redirect: '/admin/servicios' },
        { path: 'servicios', component: () => import('@/views/admin/AdminServicios.vue') },
        { path: 'portafolio', component: () => import('@/views/admin/AdminPortafolio.vue') },
        { path: 'faq', component: () => import('@/views/admin/AdminBlog.vue') },
      ],
    },
  ],
  scrollBehavior(to) {
    if (to.hash) return { el: to.hash, top: 80, behavior: 'smooth' };
    return { top: 0 };
  },
});

router.beforeEach((to) => {
  if (to.matched.some((r) => r.meta.requiresAuth) && !adminAuth.isAuthenticated()) {
    return { path: '/admin/login', query: { redirect: to.fullPath } };
  }
  return true;
});
