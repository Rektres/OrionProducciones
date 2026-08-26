import { createRouter, createWebHistory } from 'vue-router';
import { adminAuth } from '@/services/adminAuth';
import { aplicarSeo } from '@/composables/useSeo';
import { registrarPagina } from '@/composables/useAnalitica';

declare module 'vue-router' {
  interface RouteMeta {
    requiresAuth?: boolean;
    /** Título de la pestaña y del resultado de búsqueda. Se le agrega " | Orion". */
    titulo?: string;
    /** Meta description de la página. */
    descripcion?: string;
    /** Excluir de buscadores (páginas privadas o sin valor de indexación). */
    noindex?: boolean;
  }
}

export const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      component: () => import('@/views/Landing.vue'),
      meta: {
        descripcion:
          'Productora de eventos corporativos, sociales y festivales en Chile. Producción ' +
          'integral: escenario, sonido, iluminación y montaje. Cotiza tu evento con Orion.',
      },
    },
    {
      path: '/servicios',
      component: () => import('@/views/Servicios.vue'),
      meta: {
        titulo: 'Servicios de producción de eventos',
        descripcion:
          'Todo lo que Orion produce: eventos corporativos, sociales y festivales, con ' +
          'escenario, sonido, iluminación, montaje y coordinación en terreno.',
      },
    },
    {
      path: '/portafolio',
      component: () => import('@/views/Portafolio.vue'),
      meta: {
        titulo: 'Portafolio de eventos',
        descripcion:
          'Eventos que hemos producido en Chile: fotos, tipo de evento, lugar y cliente. ' +
          'Mira nuestro trabajo antes de cotizar.',
      },
    },
    {
      path: '/portafolio/:slug',
      component: () => import('@/views/PortafolioDetalle.vue'),
      meta: { titulo: 'Portafolio' },
    },
    {
      path: '/faq',
      component: () => import('@/views/FAQ.vue'),
      meta: {
        titulo: 'Preguntas frecuentes',
        descripcion:
          'Plazos, presupuestos, cobertura y cómo trabajamos: las dudas más comunes antes ' +
          'de contratar una productora de eventos.',
      },
    },
    {
      path: '/nosotros',
      alias: ['/quienes-somos'],
      component: () => import('@/views/QuienesSomos.vue'),
      meta: {
        titulo: 'Nosotros · Experiencias que Conectan Personas',
        descripcion:
          'Conoce Orión Stage: nuestro propósito, filosofía, los 4 mundos de experiencias corporativas y la producción 360° que conecta personas.',
      },
    },
    {
      path: '/terminos-y-condiciones',
      component: () => import('@/views/Terminos.vue'),
      meta: {
        titulo: 'Términos y condiciones',
        descripcion: 'Condiciones de uso del sitio de Orion y tratamiento de datos personales.',
      },
    },
    {
      path: '/politica-de-privacidad',
      component: () => import('@/views/Privacidad.vue'),
      meta: {
        titulo: 'Política de privacidad',
        descripcion:
          'Qué datos personales recopila Orion en el formulario de cotización, para qué los usa, ' +
          'cuánto los conserva y cómo ejercer sus derechos ARCO+.',
      },
    },
    {
      path: '/gracias',
      component: () => import('@/views/Gracias.vue'),
      // URL propia para poder medir la conversión; sin valor de indexación.
      meta: { titulo: 'Gracias por tu solicitud', noindex: true },
    },
    {
      path: '/admin/login',
      component: () => import('@/views/admin/AdminLogin.vue'),
      meta: { noindex: true },
    },
    {
      path: '/admin',
      component: () => import('@/views/admin/AdminLayout.vue'),
      meta: { requiresAuth: true, noindex: true },
      children: [
        { path: '', redirect: '/admin/servicios' },
        { path: 'servicios', component: () => import('@/views/admin/AdminServicios.vue') },
        { path: 'portafolio', component: () => import('@/views/admin/AdminPortafolio.vue') },
        { path: 'faq', component: () => import('@/views/admin/AdminBlog.vue') },
      ],
    },
    {
      path: '/:pathMatch(.*)*',
      component: () => import('@/views/NotFound.vue'),
      meta: { titulo: 'Página no encontrada', noindex: true },
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

// SEO base por ruta. Las vistas de detalle vuelven a llamar aplicarSeo() con los
// datos ya cargados (título del evento, su imagen destacada, etc.).
router.afterEach((to) => {
  const meta = to.matched.reduce<Record<string, unknown>>((acc, r) => ({ ...acc, ...r.meta }), {});
  aplicarSeo({
    titulo: meta.titulo as string | undefined,
    descripcion: meta.descripcion as string | undefined,
    noindex: meta.noindex as boolean | undefined,
  });
  registrarPagina(to.fullPath);
});
