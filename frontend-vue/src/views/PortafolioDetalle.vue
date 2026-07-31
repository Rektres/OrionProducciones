<script setup lang="ts">
import { computed, onMounted, ref } from 'vue';
import { useRoute, useRouter } from 'vue-router';
import { Modal } from 'bootstrap';
import { portafolioService } from '@/services/portafolio';
import type { Evento } from '@/types';

const route = useRoute();
const router = useRouter();
const evento = ref<Evento | null>(null);
const loading = ref(true);

const fotoIndex = ref(0);
const modalGaleriaEl = ref<HTMLElement | null>(null);
let modalGaleriaInstance: Modal | null = null;

const fotoActual = computed(() => evento.value?.fotos?.[fotoIndex.value] ?? null);
const totalFotos = computed(() => evento.value?.fotos?.length ?? 0);

const abrirFoto = (idx: number) => {
  fotoIndex.value = idx;
  if (!modalGaleriaInstance && modalGaleriaEl.value) {
    modalGaleriaInstance = new Modal(modalGaleriaEl.value);
  }
  modalGaleriaInstance?.show();
};

const fotoAnterior = () => {
  const total = evento.value?.fotos?.length ?? 0;
  if (!total) return;
  fotoIndex.value = (fotoIndex.value - 1 + total) % total;
};

const fotoSiguiente = () => {
  const total = evento.value?.fotos?.length ?? 0;
  if (!total) return;
  fotoIndex.value = (fotoIndex.value + 1) % total;
};

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
      :style="evento.imagen_url ? { backgroundImage: `url('${evento.imagen_url}')` } : {}">
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
          <div v-for="(f, idx) in evento.fotos" :key="f.id" class="col-6 col-md-4">
            <div class="card-cover rounded" style="height: 12rem; cursor: pointer"
              :style="f.imagen_url ? { backgroundImage: `url('${f.imagen_url}')` } : {}"
              role="button" @click="abrirFoto(idx)"></div>
          </div>
        </div>
      </div>

      <div class="text-center mt-5">
        <button class="btn btn-orion" @click="router.push({ path: '/', hash: '#cotizacion' })">Solicitar cotización</button>
      </div>
    </div>

    <div ref="modalGaleriaEl" class="modal fade" tabindex="-1" aria-hidden="true">
      <div class="modal-dialog modal-dialog-centered modal-lg">
        <div class="modal-content bg-dark border-secondary text-white">
          <div class="modal-header border-secondary">
            <h5 class="modal-title mb-0">{{ fotoActual?.descripcion || 'Foto del evento' }}</h5>
            <button type="button" class="btn-close btn-close-white" data-bs-dismiss="modal" aria-label="Cerrar"></button>
          </div>
          <div class="modal-body position-relative">
            <div v-if="fotoActual?.imagen_url" class="card-cover rounded" style="height: 26rem"
              :style="{ backgroundImage: `url('${fotoActual.imagen_url}')` }"></div>
            <button v-if="totalFotos > 1" type="button"
              class="btn btn-outline-light position-absolute top-50 start-0 translate-middle-y ms-2"
              @click="fotoAnterior">‹</button>
            <button v-if="totalFotos > 1" type="button"
              class="btn btn-outline-light position-absolute top-50 end-0 translate-middle-y me-2"
              @click="fotoSiguiente">›</button>
          </div>
          <div v-if="totalFotos > 1" class="modal-footer border-secondary justify-content-center">
            <small class="text-secondary">{{ fotoIndex + 1 }} / {{ totalFotos }}</small>
          </div>
        </div>
      </div>
    </div>
  </template>
</template>
