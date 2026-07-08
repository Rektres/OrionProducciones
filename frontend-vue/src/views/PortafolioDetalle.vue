<script setup lang="ts">
import { onMounted, ref } from 'vue';
import { useRoute, useRouter } from 'vue-router';
import { portafolioService } from '@/services/portafolio';
import type { Evento } from '@/types';

const route = useRoute();
const router = useRouter();
const evento = ref<Evento | null>(null);
const loading = ref(true);

onMounted(async () => {
  try {
    evento.value = await portafolioService.getEventoBySlug(String(route.params.slug));
  } catch (e) {
    evento.value = null;
  } finally {
    loading.value = false;
  }
});
</script>

<template>
  <div v-if="loading" class="container py-5 text-center text-secondary">Cargando evento...</div>
  <div v-else-if="!evento" class="container py-5 text-center text-secondary">Evento no encontrado</div>
  <template v-else>
    <div class="card-cover d-flex align-items-end" style="height: 24rem"
      :style="{ backgroundImage: `url('${evento.imagen_destacada}')` }">
      <div class="container p-4" style="background: linear-gradient(0deg, rgba(0,0,0,0.85), transparent)">
        <span class="badge text-bg-warning mb-2">{{ evento.tipo_slug }}</span>
        <h1 class="text-white">{{ evento.nombre }}</h1>
      </div>
    </div>

    <div class="container py-5" style="max-width: 900px">
      <div class="row g-3 mb-4">
        <div class="col-md-4"><div class="card bg-dark border-secondary p-3"><small class="text-orion-primary">Cliente</small><div>{{ evento.cliente }}</div></div></div>
        <div class="col-md-4"><div class="card bg-dark border-secondary p-3"><small class="text-orion-primary">Ubicación</small><div>{{ evento.lugar }}</div></div></div>
        <div class="col-md-4"><div class="card bg-dark border-secondary p-3"><small class="text-orion-primary">Asistentes</small><div>{{ evento.asistentes ? evento.asistentes + '+' : 'N/A' }}</div></div></div>
      </div>

      <h2 class="text-orion-primary">Sobre el evento</h2>
      <p class="text-secondary">{{ evento.descripcion_larga }}</p>

      <div v-if="evento.fotos && evento.fotos.length" class="mt-4">
        <h2 class="text-orion-primary">Galería</h2>
        <div class="row g-3">
          <div v-for="f in evento.fotos" :key="f.id" class="col-6 col-md-4">
            <a :href="f.imagen" target="_blank" rel="noopener noreferrer">
              <div class="card-cover rounded" style="height: 12rem" :style="{ backgroundImage: `url('${f.imagen}')` }"></div>
            </a>
          </div>
        </div>
      </div>

      <div class="text-center mt-5">
        <button class="btn btn-orion" @click="router.push({ path: '/', hash: '#cotizacion' })">Solicitar cotización</button>
      </div>
    </div>
  </template>
</template>
