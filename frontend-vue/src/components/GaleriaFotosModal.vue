<script setup lang="ts">
import { computed, ref } from 'vue';
import { Modal } from 'bootstrap';
import type { FotoEvento } from '@/types';

const modalEl = ref<HTMLElement | null>(null);
const fotos = ref<FotoEvento[]>([]);
const indice = ref(0);
let instancia: Modal | null = null;

const fotoActual = computed(() => fotos.value[indice.value] ?? null);
const totalFotos = computed(() => fotos.value.length);

const abrir = (nuevasFotos: FotoEvento[], indiceInicial = 0) => {
  fotos.value = nuevasFotos.filter((foto) => Boolean(foto.imagen_url));
  indice.value = Math.min(Math.max(indiceInicial, 0), Math.max(fotos.value.length - 1, 0));
  if (!instancia && modalEl.value) instancia = new Modal(modalEl.value);
  instancia?.show();
};

const anterior = () => {
  if (!totalFotos.value) return;
  indice.value = (indice.value - 1 + totalFotos.value) % totalFotos.value;
};

const siguiente = () => {
  if (!totalFotos.value) return;
  indice.value = (indice.value + 1) % totalFotos.value;
};

defineExpose({ abrir });
</script>

<template>
  <!-- Teleport a body: el modal vive dentro de .site-content, que crea un
       stacking context (position:relative + z-index:1). Bootstrap inserta el
       backdrop (z-index 1050) en <body>, asi que sin esto el backdrop tapa el
       modal: la pantalla queda bloqueada y no se puede cerrar. -->
  <Teleport to="body">
  <div ref="modalEl" class="modal fade galeria-modal" tabindex="-1" aria-hidden="true">
    <div class="modal-dialog modal-dialog-centered modal-xl">
      <div class="modal-content bg-transparent border-0">
        <div class="modal-body position-relative p-0 text-center">
          <button type="button" class="btn-close galeria-modal-cerrar position-absolute top-0 end-0 m-3" style="z-index: 2"
            data-bs-dismiss="modal" aria-label="Cerrar"></button>
          <img v-if="fotoActual?.imagen_url" :src="fotoActual.imagen_url" alt="" class="galeria-modal-imagen" />
          <button v-if="totalFotos > 1" type="button" class="galeria-modal-flecha position-absolute top-50 start-0 translate-middle-y ms-2"
            aria-label="Foto anterior" @click="anterior">‹</button>
          <button v-if="totalFotos > 1" type="button" class="galeria-modal-flecha position-absolute top-50 end-0 translate-middle-y me-2"
            aria-label="Foto siguiente" @click="siguiente">›</button>
          <div v-if="totalFotos > 1" class="galeria-modal-contador">{{ indice + 1 }} / {{ totalFotos }}</div>
        </div>
      </div>
    </div>
  </div>
  </Teleport>
</template>
