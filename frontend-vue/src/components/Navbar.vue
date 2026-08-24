<script setup lang="ts">
import { ref, onMounted, onBeforeUnmount } from 'vue';
import { RouterLink, useRouter } from 'vue-router';
import ThemeToggle from '@/components/ThemeToggle.vue';

const router = useRouter();
const links = [
  { label: 'Inicio', to: '/' },
  { label: 'Servicios', to: '/servicios' },
  { label: 'Portafolio', to: '/portafolio' },
  { label: 'Preguntas Frecuentes', to: '/faq' },
];

const irCotizar = () => router.push({ path: '/', hash: '#cotizacion' });

const scrolled = ref(false);
const onScroll = () => { scrolled.value = window.scrollY > 20; };
onMounted(() => window.addEventListener('scroll', onScroll));
onBeforeUnmount(() => window.removeEventListener('scroll', onScroll));
</script>

<template>
  <nav class="navbar navbar-expand-lg fixed-top navbar-orion-stage" :class="{ 'navbar-scrolled': scrolled }">
    <div class="container d-flex align-items-center justify-content-between">
      <RouterLink class="navbar-brand d-inline-flex align-items-center gap-2" to="/">
        <img src="/logo.png" alt="Orion Stage Logo" height="38" class="brand-logo-glow" />
        <div class="d-flex flex-column lh-1">
          <strong class="brand-title">ORION STAGE</strong>
          <small class="brand-subtitle">PRODUCCIONES</small>
        </div>
      </RouterLink>

      <button
        class="navbar-toggler border-0 shadow-none text-white"
        type="button"
        data-bs-toggle="collapse"
        data-bs-target="#nav"
        aria-label="Toggle navigation"
      >
        <span class="navbar-toggler-icon" style="filter: invert(1);"></span>
      </button>

      <div id="nav" class="collapse navbar-collapse">
        <ul class="navbar-nav mx-auto align-items-lg-center gap-lg-3 my-3 my-lg-0">
          <li v-for="l in links" :key="l.to" class="nav-item">
            <RouterLink class="nav-link nav-link-stage" :to="l.to" active-class="is-active">
              {{ l.label }}
            </RouterLink>
          </li>
        </ul>
        <div class="d-flex align-items-center gap-3">
          <ThemeToggle />
          <button class="btn btn-cotizar-neon" @click="irCotizar">
            <span>Cotizar Evento</span>
            <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><path d="M5 12h14M12 5l7 7-7 7"/></svg>
          </button>
        </div>
      </div>
    </div>
  </nav>
  <div style="height: 76px"></div>
</template>

<style scoped>
.navbar-orion-stage {
  padding: 14px 0;
  background: var(--navbar-bg);
  border-bottom: 1px solid var(--bs-border-color);
  backdrop-filter: blur(20px) saturate(140%);
  -webkit-backdrop-filter: blur(20px) saturate(140%);
  transition: all 0.3s ease;
  z-index: 1030;
}
.navbar-scrolled {
  background: var(--navbar-bg-scrolled);
  border-bottom-color: var(--bs-border-color);
  box-shadow: var(--orion-surface-shadow);
  padding: 10px 0;
}

.brand-logo-glow {
  filter: drop-shadow(0 0 8px rgba(34, 211, 238, 0.4));
  border-radius: 8px;
}
.brand-title {
  font-family: var(--shell-display);
  font-size: 16px;
  letter-spacing: -0.02em;
  color: var(--bs-body-color);
}
.brand-subtitle {
  font-size: 9px;
  font-weight: 800;
  letter-spacing: 0.18em;
  color: var(--orion-primary);
}

.nav-link-stage {
  position: relative;
  font-size: 13px;
  font-weight: 600;
  color: var(--bs-secondary-color) !important;
  padding: 8px 12px !important;
  border-radius: 8px;
  transition: all 0.2s ease;
}
.nav-link-stage:hover {
  color: var(--bs-body-color) !important;
  background: rgba(127, 127, 127, 0.08);
}
.nav-link-stage.is-active {
  color: var(--bs-body-color) !important;
}
.nav-link-stage.is-active::after {
  content: '';
  position: absolute;
  bottom: 0;
  left: 12px;
  right: 12px;
  height: 2px;
  border-radius: 2px;
  background: linear-gradient(90deg, var(--orion-primary), var(--orion-secondary));
  box-shadow: 0 0 8px var(--orion-primary);
}

.btn-cotizar-neon {
  display: inline-flex;
  align-items: center;
  gap: 8px;
  padding: 8px 18px;
  border-radius: 10px;
  font-size: 12px;
  font-weight: 800;
  border: 1px solid var(--bs-border-color);
  color: var(--bs-body-bg);
  background: var(--bs-body-color);
  cursor: pointer;
  transition: all 0.2s ease;
}
.btn-cotizar-neon:hover {
  transform: translateY(-1px);
  box-shadow: 0 4px 18px rgba(0, 0, 0, 0.2);
}
</style>
