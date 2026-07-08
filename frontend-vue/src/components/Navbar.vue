<script setup lang="ts">
import { RouterLink, useRouter } from 'vue-router';

const router = useRouter();
const links = [
  { label: 'Inicio', to: '/' },
  { label: 'Servicios', to: '/servicios' },
  { label: 'Portafolio', to: '/portafolio' },
  { label: 'Blog', to: '/blog' },
];

const irCotizar = () => router.push({ path: '/', hash: '#cotizacion' });
</script>

<template>
  <nav class="navbar navbar-expand-md fixed-top" style="background: rgba(10, 10, 15, 0.95)">
    <div class="container">
      <RouterLink class="navbar-brand fw-bold text-orion-primary" to="/">⚡ ORION</RouterLink>
      <button
        class="navbar-toggler"
        type="button"
        data-bs-toggle="collapse"
        data-bs-target="#nav"
        aria-label="Menu"
      >
        <span class="navbar-toggler-icon"></span>
      </button>
      <div id="nav" class="collapse navbar-collapse">
        <ul class="navbar-nav ms-auto align-items-md-center gap-2">
          <li v-for="l in links" :key="l.to" class="nav-item">
            <RouterLink class="nav-link" :to="l.to">{{ l.label }}</RouterLink>
          </li>
          <li class="nav-item">
            <button class="btn btn-orion btn-sm" @click="irCotizar">Cotiza</button>
          </li>
        </ul>
      </div>
    </div>
  </nav>
  <div style="height: 64px"></div>
</template>
