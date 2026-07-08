<script setup lang="ts">
import { onMounted, ref, computed } from 'vue';
import { RouterLink } from 'vue-router';
import { portafolioService } from '@/services/portafolio';
import type { Evento, EventoTipo } from '@/types';

const tipos = ref<EventoTipo[]>([]);
const eventos = ref<Evento[]>([]);
const sel = ref<string | null>(null);

const filtrados = computed(() =>
  sel.value ? eventos.value.filter((e) => e.tipo_slug === sel.value) : eventos.value,
);

onMounted(async () => {
  [tipos.value, eventos.value] = await Promise.all([
    portafolioService.getTipos(),
    portafolioService.getEventos(),
  ]);
});
</script>

<template>
  <section class="py-5 text-center">
    <div class="container">
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
      <div class="row g-4">
        <div v-for="ev in filtrados" :key="ev.id" class="col-md-6 col-lg-4">
          <RouterLink :to="`/portafolio/${ev.slug}`" class="text-decoration-none">
            <div class="card border-0 card-cover d-flex justify-content-end"
              :style="{ backgroundImage: `url('${ev.imagen_destacada}')` }">
              <div class="p-3" style="background: linear-gradient(0deg, rgba(0,0,0,0.85), transparent)">
                <span class="badge text-bg-warning mb-1">{{ ev.tipo_slug }}</span>
                <h6 class="text-white mb-0">{{ ev.nombre }}</h6>
                <small class="text-secondary">{{ ev.lugar }}</small>
              </div>
            </div>
          </RouterLink>
        </div>
      </div>
    </div>
  </section>
</template>
