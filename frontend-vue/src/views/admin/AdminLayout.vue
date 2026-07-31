<script setup lang="ts">
import { useRouter } from 'vue-router';
import { adminAuth } from '@/services/adminAuth';

const router = useRouter();

const salir = () => {
  adminAuth.logout();
  router.push('/admin/login');
};
</script>

<template>
  <div class="admin-shell text-white min-vh-100" data-bs-theme="dark">
    <nav class="navbar navbar-dark border-bottom border-secondary px-3">
      <span class="navbar-brand mb-0">Orion — Administración</span>
      <div class="d-flex gap-3">
        <RouterLink to="/admin/servicios" class="nav-link d-inline" active-class="text-orion-primary">Servicios</RouterLink>
        <RouterLink to="/admin/portafolio" class="nav-link d-inline" active-class="text-orion-primary">Portafolio</RouterLink>
        <RouterLink to="/admin/faq" class="nav-link d-inline" active-class="text-orion-primary">FAQ</RouterLink>
        <button type="button" class="btn btn-outline-light btn-sm" @click="salir">Salir</button>
      </div>
    </nav>
    <div class="container-fluid px-4 px-md-5 py-4">
      <router-view />
    </div>
  </div>
</template>
