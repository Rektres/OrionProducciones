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
      <h1 class="display-4 fw-bold">PORTAFOLIO</h1>
      <p class="text-secondary">{{ eventos.length }} eventos realizados con pasión</p>
    </div>
  </section>

  <section class="py-4">
    <div class="container">
      <div class="d-flex flex-wrap gap-2 justify-content-center mb-4">
        <button class="btn btn-sm" :class="sel === null ? 'btn-orion' : 'btn-outline-light'" @click="sel = null">Todos</button>
        <button v-for="t in tipos" :key="t.id" class="btn btn-sm"
          :class="sel === t.slug ? 'btn-orion' : 'btn-outline-light'" @click="sel = t.slug">
          {{ t.nombre }}
        </button>
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
            <RouterLink :to="`/portafolio/${ev.slug}`" class="text-decoration-none">
              <div class="card border-0 card-cover d-flex justify-content-end position-relative overflow-hidden">
                <img v-if="ev.imagen_url" :src="ev.imagen_url"
                  :alt="`${ev.nombre} — evento producido por Orion en ${ev.lugar}`"
                  class="img-cover position-absolute top-0 start-0" loading="lazy" decoding="async" />
                <div class="p-3 position-relative" style="background: linear-gradient(0deg, rgba(0,0,0,0.85), transparent)">
                  <span class="badge text-bg-warning mb-1">{{ ev.tipo_slug }}</span>
                  <h6 class="text-white mb-0">{{ ev.nombre }}</h6>
                  <small class="text-secondary">{{ ev.lugar }}</small>
                </div>
              </div>
            </RouterLink>
          </FadeInUp>
        </div>
      </div>
    </div>
  </section>
</template>
