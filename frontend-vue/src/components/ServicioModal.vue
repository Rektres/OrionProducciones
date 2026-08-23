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
  <div ref="modalEl" class="modal fade" tabindex="-1" aria-hidden="true">
    <div class="modal-dialog modal-dialog-centered">
      <div class="modal-content bg-dark border-secondary">
        <div class="modal-header border-secondary">
          <h5 class="modal-title mb-0">{{ servicio?.nombre }}</h5>
          <button type="button" class="btn-close" :class="{ 'btn-close-white': theme === 'dark' }"
            data-bs-dismiss="modal" aria-label="Cerrar"></button>
        </div>
        <div class="modal-body">
          <div v-if="servicio?.imagen_url" class="card-cover rounded mb-3 overflow-hidden" style="height: 14rem">
            <img :src="servicio.imagen_url" :alt="`Servicio de ${servicio.nombre}`" class="img-cover"
              loading="lazy" decoding="async" />
          </div>
          <p class="text-secondary mb-0">{{ servicio?.descripcion_corta }}</p>
        </div>
      </div>
    </div>
  </div>
</template>
