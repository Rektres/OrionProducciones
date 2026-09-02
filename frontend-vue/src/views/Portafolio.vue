<script setup lang="ts">
import { onMounted, ref, computed } from 'vue';
import { RouterLink } from 'vue-router';
import FadeInUp from '@/components/animations/FadeInUp.vue';
import { portafolioService } from '@/services/portafolio';
import type { Evento, EventoTipo } from '@/types';

const tipos = ref<EventoTipo[]>([]);
const eventos = ref<Evento[]>([]);
const sel = ref<string | null>(null);
const cargando = ref(true);
const error = ref(false);

const filtrados = computed(() =>
  sel.value ? eventos.value.filter((e) => e.tipo_slug === sel.value) : eventos.value,
);

onMounted(async () => {
  try {
    [tipos.value, eventos.value] = await Promise.all([
      portafolioService.getTipos(),
      portafolioService.getEventos(),
    ]);
  } catch (e) {
    error.value = true;
    console.error('Error cargando portafolio:', e);
  } finally {
    cargando.value = false;
  }
});
</script>

<template>
  <section class="pt-4 pb-2 text-center position-relative overflow-hidden">
    <div class="container position-relative" style="z-index: 1">
      <h1 class="display-4 fw-bold">PORTAFOLIO DE EVENTOS</h1>
      <p class="text-secondary" style="max-width: 600px; margin: 0 auto;">
        Explora nuestros montajes en vivo, festivales, bodas de alta gama y experiencias corporativas producidas en todo Chile.
      </p>
    </div>
  </section>

  <section class="py-4 pb-5">
    <div class="container">
      <div class="catalog-toolbar mb-4">
        <div class="filter-chips">
          <button
            class="filter-chip"
            :class="{ 'is-active': sel === null }"
            @click="sel = null"
          >
            Todos
          </button>
          <button
            v-for="t in tipos"
            :key="t.id"
            class="filter-chip"
            :class="{ 'is-active': sel === t.slug }"
            @click="sel = t.slug"
          >
            {{ t.nombre }}
          </button>
        </div>
        <span class="catalog-count">
          <strong>{{ filtrados.length }}</strong> EVENTOS
        </span>
      </div>

      <div v-if="cargando" class="text-center text-secondary py-5" aria-live="polite">
        <div class="spinner-border text-orion-primary" role="status" aria-hidden="true"></div>
        <p class="mt-3 mb-0">Cargando portafolio...</p>
      </div>
      <div v-else-if="error" class="text-center text-secondary py-5">
        No pudimos cargar el portafolio. Recarga la página en unos momentos.
      </div>
      <div v-else-if="!filtrados.length" class="text-center text-secondary py-5">
        Todavía no hay eventos publicados en esta categoría.
      </div>
      <div v-else class="row g-4">
        <div v-for="ev in filtrados" :key="ev.id" class="col-md-6 col-lg-4">
          <FadeInUp>
            <article class="stage-card h-100">
              <!-- Top Header Bar -->
              <div class="stage-card__top">
                <div class="d-flex align-items-center gap-2">
                  <span class="stage-card__status-dot"></span>
                  <span class="stage-card__status-text">PRODUCCIÓN DESTACADA</span>
                </div>
                <span class="stage-card__badge-edition">Temporada 2026</span>
              </div>

              <!-- Center Image with Overlay -->
              <div class="stage-card__visual">
                <img
                  v-if="ev.imagen_url"
                  :src="ev.imagen_url"
                  :alt="`${ev.nombre} — evento producido por Orion Stage en ${ev.lugar}`"
                  loading="lazy"
                  decoding="async"
                />
                <div class="stage-card__overlay-bottom">
                  <span class="stage-card__tag-pill">{{ ev.tipo_slug || 'PRODUCCIÓN ESCÉNICA' }}</span>
                  <h3 class="stage-card__overlay-title">{{ ev.nombre }}</h3>
                </div>
              </div>

              <!-- Bottom Footer with Meta & Action -->
              <div class="stage-card__footer">
                <div class="stage-card__footer-meta">
                  <span>Locación & Producción</span>
                  <strong>{{ ev.lugar || 'Santiago, Chile' }}</strong>
                </div>
                <RouterLink :to="`/portafolio/${ev.slug}`" class="stage-card__detail-btn text-decoration-none">
                  <span>Ver Detalle</span>
                  <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><path d="M5 12h14M12 5l7 7-7 7"/></svg>
                </RouterLink>
              </div>
            </article>
          </FadeInUp>
        </div>
      </div>
    </div>
  </section>
</template>
