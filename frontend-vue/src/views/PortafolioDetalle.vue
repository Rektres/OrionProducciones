<script setup lang="ts">
import { onMounted, ref } from 'vue';
import { useRoute, useRouter, RouterLink } from 'vue-router';
import GaleriaFotosModal from '@/components/GaleriaFotosModal.vue';
import ShareButton from '@/components/ShareButton.vue';
import { portafolioService } from '@/services/portafolio';
import { aplicarSeo } from '@/composables/useSeo';
import type { Evento } from '@/types';

const route = useRoute();
const router = useRouter();
const evento = ref<Evento | null>(null);
const loading = ref(true);
const galeriaModalRef = ref<InstanceType<typeof GaleriaFotosModal> | null>(null);

const abrirFoto = (idx: number) => {
  galeriaModalRef.value?.abrir(evento.value?.fotos ?? [], idx);
};

onMounted(async () => {
  try {
    evento.value = await portafolioService.getEventoBySlug(String(route.params.slug));
    if (evento.value) {
      aplicarSeo({
        titulo: evento.value.nombre,
        descripcion: evento.value.descripcion_corta,
        imagen: evento.value.imagen_url || undefined,
      });
    }
  } catch {
    evento.value = null;
    aplicarSeo({ titulo: 'Evento no encontrado', noindex: true });
  } finally {
    loading.value = false;
  }
});
</script>

<template>
  <div v-if="loading" class="container py-5 text-center text-secondary">Cargando evento...</div>
  <div v-else-if="!evento" class="container py-5 text-center text-secondary">Evento no encontrado</div>
  <template v-else>
    <div class="card-cover d-flex align-items-end position-relative overflow-hidden" style="height: 24rem">
      <!-- Imagen principal: sin lazy, es el LCP de la página. -->
      <img v-if="evento.imagen_url" :src="evento.imagen_url"
        :alt="`${evento.nombre} — evento producido por Orion en ${evento.lugar}`"
        class="img-cover position-absolute top-0 start-0" fetchpriority="high" decoding="async" />
      <div class="container p-4 position-relative w-100" style="background: linear-gradient(0deg, rgba(3, 8, 28, 0.92) 0%, rgba(3, 8, 28, 0.5) 60%, transparent 100%)">
        <span class="badge mb-2 d-inline-block" style="background: rgba(19, 214, 234, 0.25); color: #13d6ea; border: 1px solid rgba(19, 214, 234, 0.6); font-size: 12px; font-weight: 700; letter-spacing: 0.05em; text-transform: uppercase;">
          {{ evento.tipo_slug }}
        </span>
        <h1 class="text-white fw-bold mb-0">{{ evento.nombre }}</h1>
      </div>
    </div>

    <div class="container py-5" style="max-width: 900px">
      <div class="d-flex flex-wrap align-items-center justify-content-between gap-3 mb-4">
        <RouterLink to="/portafolio" class="btn btn-sm btn-outline-secondary d-inline-flex align-items-center gap-1 rounded-pill px-3">
          <span>← Volver al Portafolio</span>
        </RouterLink>
        <ShareButton :title="evento.nombre" :text="evento.descripcion_corta || 'Mira esta producción realizada por Orion Stage'" />
      </div>

      <div class="row g-3 mb-4">
        <div class="col-md-4">
          <div class="card p-3 rounded-4" style="background: var(--card-surface); border: 1px solid var(--card-border); box-shadow: var(--orion-surface-shadow);">
            <small class="fw-bold text-uppercase" style="color: var(--orion-primary); font-size: 11px; letter-spacing: 0.05em;">Cliente</small>
            <div class="fw-bold text-body fs-5 mt-1">{{ evento.cliente }}</div>
          </div>
        </div>
        <div class="col-md-4">
          <div class="card p-3 rounded-4" style="background: var(--card-surface); border: 1px solid var(--card-border); box-shadow: var(--orion-surface-shadow);">
            <small class="fw-bold text-uppercase" style="color: var(--orion-primary); font-size: 11px; letter-spacing: 0.05em;">Ubicación</small>
            <div class="fw-bold text-body fs-5 mt-1">{{ evento.lugar }}</div>
          </div>
        </div>
        <div class="col-md-4">
          <div class="card p-3 rounded-4" style="background: var(--card-surface); border: 1px solid var(--card-border); box-shadow: var(--orion-surface-shadow);">
            <small class="fw-bold text-uppercase" style="color: var(--orion-primary); font-size: 11px; letter-spacing: 0.05em;">Asistentes</small>
            <div class="fw-bold text-body fs-5 mt-1">{{ evento.asistentes ? evento.asistentes + '+' : 'N/A' }}</div>
          </div>
        </div>
      </div>

      <h2 class="text-orion-primary">Sobre el evento</h2>
      <p class="text-secondary">{{ evento.descripcion_larga }}</p>

      <div v-if="evento.fotos && evento.fotos.length" class="mt-4">
        <h2 class="text-orion-primary">Galería</h2>
        <div class="row g-3">
          <div v-for="(f, idx) in evento.fotos" :key="f.id" class="col-6 col-md-4">
            <div class="card-cover rounded overflow-hidden" style="height: 12rem; cursor: pointer"
              role="button" tabindex="0" @click="abrirFoto(idx)" @keydown.enter="abrirFoto(idx)">
              <img v-if="f.imagen_url" :src="f.imagen_url"
                :alt="f.descripcion || `Foto ${idx + 1} del evento ${evento.nombre}`"
                class="img-cover" loading="lazy" decoding="async" />
            </div>
          </div>
        </div>
      </div>

      <div class="text-center mt-5">
        <button class="btn btn-orion" @click="router.push({ path: '/', hash: '#cotizacion' })">Solicitar cotización</button>
      </div>
    </div>

    <GaleriaFotosModal ref="galeriaModalRef" />
  </template>
</template>
