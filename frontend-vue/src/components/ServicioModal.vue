<script setup lang="ts">
import { ref } from 'vue';
import { Modal } from 'bootstrap';
import { useTheme } from '@/composables/useTheme';
import type { Servicio } from '@/types';

const { theme } = useTheme();
const modalEl = ref<HTMLElement | null>(null);
const servicio = ref<Servicio | null>(null);
let instance: Modal | null = null;

const abrir = (svc: Servicio) => {
  servicio.value = svc;
  if (!instance && modalEl.value) instance = new Modal(modalEl.value);
  instance?.show();
};

defineExpose({ abrir });
</script>

<template>
  <!-- Teleport a body: ver nota en GaleriaFotosModal.vue. Sin esto el modal
       queda dentro del stacking context de .site-content y el backdrop de
       Bootstrap (en <body>, z-index 1050) lo tapa por completo. -->
  <Teleport to="body">
  <div ref="modalEl" class="modal fade" tabindex="-1" aria-hidden="true">
    <div class="modal-dialog modal-dialog-centered">
      <div class="modal-content bg-dark border-secondary">
        <div class="modal-header border-secondary">
          <h5 class="modal-title mb-0">{{ servicio?.nombre }}</h5>
          <button type="button" class="btn-close" :class="{ 'btn-close-white': theme === 'dark' }"
            data-bs-dismiss="modal" aria-label="Cerrar"></button>
        </div>
        <div class="modal-body">
          <div v-if="servicio?.imagen_url" class="card-cover rounded mb-3" style="height: 14rem"
            :style="{ backgroundImage: `url('${servicio.imagen_url}')` }"></div>
          <p class="text-secondary mb-0">{{ servicio?.descripcion_corta }}</p>
        </div>
      </div>
    </div>
  </div>
  </Teleport>
</template>
