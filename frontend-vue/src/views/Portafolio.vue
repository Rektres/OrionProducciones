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
  <section class="py-5 text-center position-relative overflow-hidden">
    <div class="container position-relative" style="z-index: 1">
      <p class="eyebrow justify-content-center"><span></span> CASOS DE ÉXITO</p>
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
            <RouterLink :to="`/portafolio/${ev.slug}`" class="text-decoration-none d-block h-100">
              <div class="card border-0 card-cover d-flex justify-content-end position-relative overflow-hidden rounded-4 shadow-sm h-100" style="min-height: 280px;">
                <img v-if="ev.imagen_url" :src="ev.imagen_url"
                  :alt="`${ev.nombre} — evento producido por Orion en ${ev.lugar}`"
                  class="img-cover position-absolute top-0 start-0 w-100 h-100" loading="lazy" decoding="async" />
                <div class="p-4 position-relative w-100" style="background: linear-gradient(0deg, rgba(3, 8, 28, 0.92) 0%, rgba(3, 8, 28, 0.6) 65%, transparent 100%); z-index: 2;">
                  <span class="badge mb-2 d-inline-block" style="background: rgba(19, 214, 234, 0.2); color: #13d6ea; border: 1px solid rgba(19, 214, 234, 0.5); font-size: 11px; font-weight: 700; letter-spacing: 0.05em; text-transform: uppercase;">
                    {{ ev.tipo_slug }}
                  </span>
                  <h5 class="text-white mb-1 fw-bold lh-sm">{{ ev.nombre }}</h5>
                  <small class="text-white-50 d-flex align-items-center gap-1 mt-1">
                    <svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M21 10c0 7-9 13-9 13s-9-6-9-13a9 9 0 0 1 18 0z"/><circle cx="12" cy="10" r="3"/></svg>
                    <span>{{ ev.lugar }}</span>
                  </small>
                </div>
              </div>
            </RouterLink>
          </FadeInUp>
        </div>
      </div>
    </div>
  </section>
</template>
