<script setup lang="ts">
import { useRouter } from 'vue-router';
import { adminAuth } from '@/services/adminAuth';
import ThemeToggle from '@/components/ThemeToggle.vue';

const router = useRouter();

const salir = () => {
  adminAuth.logout();
  router.push('/admin/login');
};

const secciones = [
  { to: '/admin/servicios', label: 'Servicios' },
  { to: '/admin/portafolio', label: 'Portafolio' },
  { to: '/admin/faq', label: 'FAQ' },
];
</script>

<template>
  <div class="admin-shell min-vh-100">
    <nav class="admin-topbar d-flex flex-wrap align-items-center justify-content-between gap-2 px-3 px-md-4 py-2">
      <span class="navbar-brand mb-0 fs-6">Orion — Administración</span>
      <div class="d-flex align-items-center gap-2 gap-md-3">
        <RouterLink v-for="s in secciones" :key="s.to" :to="s.to"
          class="nav-link d-inline px-1" active-class="text-orion-primary fw-semibold">
          {{ s.label }}
        </RouterLink>
        <RouterLink to="/" class="nav-link d-inline px-1" title="Ver el sitio público">Ver sitio</RouterLink>
        <ThemeToggle />
        <button type="button" class="btn btn-outline-secondary btn-sm" @click="salir">Salir</button>
      </div>
    </nav>
    <div class="container-fluid px-3 px-md-5 py-4">
      <router-view />
    </div>
  </div>
</template>
