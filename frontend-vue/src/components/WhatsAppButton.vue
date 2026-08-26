<script setup lang="ts">
import { onMounted, ref } from 'vue';

const numero = import.meta.env.VITE_WHATSAPP_NUMBER || '56944830378';
const url = `https://wa.me/${numero}?text=Hola,%20quisiera%20cotizar%20un%20evento%20con%20Orion%20Stage`;

const visible = ref(true);

onMounted(() => {
  if (sessionStorage.getItem('orion_wsp_dismissed') === '1') {
    visible.value = false;
  }
});

const cerrarWsp = () => {
  visible.value = false;
  sessionStorage.setItem('orion_wsp_dismissed', '1');
};
</script>

<template>
  <transition name="wsp-pop">
    <div
      v-if="visible"
      class="floating-wsp-wrapper position-fixed"
      style="bottom: 2rem; right: 2rem; z-index: 1040;"
    >
      <!-- Botón de Cerrar / Quitar -->
      <button
        type="button"
        class="wsp-close-btn"
        aria-label="Cerrar botón de WhatsApp"
        title="Ocultar botón de WhatsApp"
        @click.stop="cerrarWsp"
      >
        <svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5">
          <line x1="18" y1="6" x2="6" y2="18"></line>
          <line x1="6" y1="6" x2="18" y2="18"></line>
        </svg>
      </button>

      <!-- Botón de Enlace WhatsApp -->
      <a
        :href="url"
        target="_blank"
        rel="noopener noreferrer"
        class="floating-wsp-btn d-flex align-items-center justify-content-center shadow-lg"
        title="Cotiza por WhatsApp con Orión Stage"
        aria-label="Contactar por WhatsApp"
      >
        <svg width="28" height="28" viewBox="0 0 24 24" fill="currentColor" aria-hidden="true">
          <path d="M17.472 14.382c-.297-.149-1.758-.867-2.03-.967-.273-.099-.471-.148-.67.15-.197.297-.767.966-.94 1.164-.173.199-.347.223-.644.075-.297-.15-1.255-.463-2.39-1.475-.883-.788-1.48-1.761-1.653-2.059-.173-.297-.018-.458.13-.606.134-.133.298-.347.446-.52.149-.174.198-.298.298-.497.099-.198.05-.371-.025-.52-.075-.149-.669-1.612-.916-2.207-.242-.579-.487-.5-.669-.51-.173-.008-.371-.01-.57-.01-.198 0-.52.074-.792.372-.272.297-1.04 1.016-1.04 2.479 0 1.462 1.065 2.875 1.213 3.074.149.198 2.096 3.2 5.077 4.487.709.306 1.263.489 1.694.625.712.227 1.36.195 1.872.118.571-.085 1.758-.719 2.006-1.413.248-.694.248-1.289.173-1.413-.074-.124-.272-.198-.57-.347m-5.421 7.403h-.004a9.87 9.87 0 01-5.031-1.378l-.361-.214-3.741.982.998-3.648-.235-.374a9.86 9.86 0 01-1.51-5.26c.001-5.45 4.436-9.884 9.888-9.884 2.64 0 5.122 1.03 6.988 2.898a9.825 9.825 0 012.893 6.994c-.003 5.45-4.437 9.884-9.885 9.884m8.413-18.297A11.815 11.815 0 0012.05 0C5.495 0 .16 5.335.157 11.892c0 2.096.547 4.142 1.588 5.945L.057 24l6.305-1.654a11.882 11.882 0 005.683 1.448h.005c6.554 0 11.89-5.335 11.893-11.893a11.821 11.821 0 00-3.48-8.413z" />
        </svg>
      </a>
    </div>
  </transition>
</template>

<style scoped>
.floating-wsp-wrapper {
  position: relative;
}
.floating-wsp-btn {
  width: 56px;
  height: 56px;
  border-radius: 50%;
  background: #25d366;
  color: #ffffff;
  transition: transform 0.25s cubic-bezier(0.16, 1, 0.3, 1), box-shadow 0.25s ease;
  box-shadow: 0 8px 25px rgba(37, 211, 102, 0.4);
}
.floating-wsp-btn:hover {
  transform: scale(1.1);
  box-shadow: 0 12px 30px rgba(37, 211, 102, 0.6);
  color: #ffffff;
}
.wsp-close-btn {
  position: absolute;
  top: -6px;
  right: -6px;
  width: 22px;
  height: 22px;
  border-radius: 50%;
  background: #111827;
  color: #f3f4f6;
  border: 1px solid rgba(255, 255, 255, 0.3);
  display: grid;
  place-items: center;
  cursor: pointer;
  z-index: 10;
  transition: transform 0.2s ease, background-color 0.2s ease;
  padding: 0;
}
.wsp-close-btn:hover {
  transform: scale(1.15);
  background: #ef4444;
  color: #ffffff;
}
.wsp-pop-enter-active,
.wsp-pop-leave-active {
  transition: all 0.3s cubic-bezier(0.16, 1, 0.3, 1);
}
.wsp-pop-enter-from,
.wsp-pop-leave-to {
  opacity: 0;
  transform: scale(0.6) translateY(20px);
}
</style>
