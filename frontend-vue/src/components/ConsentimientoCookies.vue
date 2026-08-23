<script setup lang="ts">
import { onMounted, ref } from 'vue';
import { RouterLink } from 'vue-router';
import { cargarAnalitica, requiereConsentimiento } from '@/composables/useAnalitica';

const CLAVE = 'orion_consentimiento_cookies';
const visible = ref(false);

// Solo aparece si hay un proveedor de analítica con cookies configurado. Sin eso
// el sitio no instala cookies de terceros y el banner sería puro ruido.
onMounted(() => {
  if (!requiereConsentimiento) return;
  const guardado = localStorage.getItem(CLAVE);
  if (guardado === 'aceptado') cargarAnalitica();
  else if (guardado !== 'rechazado') visible.value = true;
});

const aceptar = () => {
  localStorage.setItem(CLAVE, 'aceptado');
  visible.value = false;
  cargarAnalitica();
};

const rechazar = () => {
  localStorage.setItem(CLAVE, 'rechazado');
  visible.value = false;
};
</script>

<template>
  <div v-if="visible" class="cookies-banner position-fixed bottom-0 start-0 end-0 p-3"
    role="dialog" aria-live="polite" aria-label="Aviso de cookies">
    <div class="container">
      <div class="card bg-dark border-secondary">
        <div class="card-body d-flex flex-column flex-md-row align-items-md-center gap-3">
          <p class="text-secondary small mb-0 flex-grow-1">
            Usamos cookies de analítica para entender cómo se navega el sitio y mejorarlo. Puedes
            rechazarlas sin perder ninguna funcionalidad. Más detalles en nuestra
            <RouterLink to="/politica-de-privacidad" class="link-light">política de privacidad</RouterLink>.
          </p>
          <div class="d-flex gap-2 flex-shrink-0">
            <button type="button" class="btn btn-sm btn-outline-light" @click="rechazar">Rechazar</button>
            <button type="button" class="btn btn-sm btn-orion" @click="aceptar">Aceptar</button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
.cookies-banner {
  z-index: 1080;
}
</style>
