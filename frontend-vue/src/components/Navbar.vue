<script setup lang="ts">
import { ref, watch, onMounted, onBeforeUnmount } from 'vue';
import { RouterLink, useRouter, useRoute } from 'vue-router';
import ThemeToggle from '@/components/ThemeToggle.vue';

const router = useRouter();
const route = useRoute();

const links = [
  { label: 'Inicio', to: '/' },
  { label: 'Nosotros', to: '/nosotros' },
  { label: 'Servicios', to: '/servicios' },
  { label: 'Portafolio', to: '/portafolio' },
  { label: 'Preguntas Frecuentes', to: '/faq' },
];

const menuAbierto = ref(false);
const toggleMenu = () => {
  menuAbierto.value = !menuAbierto.value;
};
const cerrarMenu = () => {
  menuAbierto.value = false;
};

// Cerrar automáticamente el menú al cambiar de ruta
watch(() => route.fullPath, () => {
  menuAbierto.value = false;
});

const irCotizar = () => {
  cerrarMenu();
  router.push({ path: '/', hash: '#cotizacion' });
};

const scrolled = ref(false);
const onScroll = () => {
  scrolled.value = window.scrollY > 20;
};
onMounted(() => window.addEventListener('scroll', onScroll));
onBeforeUnmount(() => window.removeEventListener('scroll', onScroll));
</script>

<template>
  <nav class="navbar navbar-expand-lg fixed-top navbar-orion-stage" :class="{ 'navbar-scrolled': scrolled }">
    <div class="container d-flex align-items-center justify-content-between">
      <RouterLink class="navbar-brand d-inline-flex align-items-center gap-2" to="/" @click="cerrarMenu">
        <img src="/logo.png" alt="Orion Stage Logo" height="38" class="brand-logo-glow" />
        <div class="d-flex flex-column lh-1">
          <strong class="brand-title">ORION STAGE</strong>
          <small class="brand-subtitle">PRODUCCIONES</small>
        </div>
      </RouterLink>

      <!-- Botón Burger Personalizado y Reactivo -->
      <button
        class="navbar-toggler-custom d-lg-none"
        type="button"
        :aria-expanded="menuAbierto"
        aria-label="Toggle navigation"
        @click="toggleMenu"
      >
        <svg v-if="!menuAbierto" width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round">
          <line x1="3" y1="6" x2="21" y2="6"></line>
          <line x1="3" y1="12" x2="21" y2="12"></line>
          <line x1="3" y1="18" x2="21" y2="18"></line>
        </svg>
        <svg v-else width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round">
          <line x1="18" y1="6" x2="6" y2="18"></line>
          <line x1="6" y1="6" x2="18" y2="18"></line>
        </svg>
      </button>

      <!-- Menú Colapsable con Soporte Vue y Mobile -->
      <div id="nav" class="collapse navbar-collapse" :class="{ 'show': menuAbierto }">
        <ul class="navbar-nav mx-auto align-items-lg-center gap-lg-3 my-3 my-lg-0">
          <li v-for="l in links" :key="l.to" class="nav-item">
            <RouterLink class="nav-link nav-link-stage" :to="l.to" active-class="is-active" @click="cerrarMenu">
              {{ l.label }}
            </RouterLink>
          </li>
        </ul>
        <div class="d-flex align-items-center justify-content-between justify-content-lg-end gap-3 pt-3 pt-lg-0 border-top border-lg-0 border-secondary-subtle">
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

.navbar-toggler-custom {
  background: rgba(127, 127, 127, 0.1);
  border: 1px solid var(--bs-border-color);
  border-radius: 10px;
  padding: 8px 10px;
  color: var(--bs-body-color);
  cursor: pointer;
  display: inline-flex;
  align-items: center;
  justify-content: center;
  transition: all 0.2s ease;
}
.navbar-toggler-custom:hover {
  background: rgba(127, 127, 127, 0.18);
}

.nav-link-stage {
  position: relative;
  font-size: 13.5px;
  font-weight: 600;
  color: var(--bs-secondary-color) !important;
  padding: 10px 14px !important;
  border-radius: 10px;
  transition: all 0.2s ease;
}
.nav-link-stage:hover {
  color: var(--bs-body-color) !important;
  background: rgba(127, 127, 127, 0.08);
}
.nav-link-stage.is-active {
  color: var(--bs-body-color) !important;
  background: rgba(127, 127, 127, 0.05);
}
.nav-link-stage.is-active::after {
  content: '';
  position: absolute;
  bottom: 0;
  left: 14px;
  right: 14px;
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

@media (max-width: 991.98px) {
  .navbar-collapse {
    background: var(--card-surface);
    border: 1px solid var(--card-border);
    border-radius: 18px;
    padding: 18px 20px;
    margin-top: 14px;
    box-shadow: var(--orion-surface-shadow);
  }
}
</style>
