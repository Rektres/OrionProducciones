<script setup lang="ts">
import { ref } from 'vue';

const props = defineProps<{
  title: string;
  text?: string;
  url?: string;
}>();

const copiado = ref(false);
const menuAbierto = ref(false);

const obtenerUrl = () => props.url || window.location.href;

const compartirNativo = async () => {
  const shareData = {
    title: props.title,
    text: props.text || 'Mira esta producción de Orión Stage:',
    url: obtenerUrl(),
  };

  if (navigator.share) {
    try {
      await navigator.share(shareData);
    } catch {
      // Usuario canceló o no soportado
    }
  } else {
    menuAbierto.value = !menuAbierto.value;
  }
};

const compartirWsp = () => {
  const msg = encodeURIComponent(`${props.title}: ${obtenerUrl()}`);
  window.open(`https://wa.me/?text=${msg}`, '_blank', 'noopener,noreferrer');
  menuAbierto.value = false;
};

const compartirLinkedin = () => {
  const u = encodeURIComponent(obtenerUrl());
  window.open(`https://www.linkedin.com/sharing/share-offsite/?url=${u}`, '_blank', 'noopener,noreferrer');
  menuAbierto.value = false;
};

const compartirTwitter = () => {
  const u = encodeURIComponent(obtenerUrl());
  const t = encodeURIComponent(props.title);
  window.open(`https://twitter.com/intent/tweet?text=${t}&url=${u}`, '_blank', 'noopener,noreferrer');
  menuAbierto.value = false;
};

const copiarEnlace = async () => {
  try {
    await navigator.clipboard.writeText(obtenerUrl());
    copiado.value = true;
    setTimeout(() => {
      copiado.value = false;
      menuAbierto.value = false;
    }, 2000);
  } catch {
    copiado.value = true;
  }
};
</script>

<template>
  <div class="position-relative d-inline-block">
    <button
      type="button"
      class="btn btn-sm btn-outline-secondary rounded-pill px-3 d-inline-flex align-items-center gap-2"
      @click="compartirNativo"
    >
      <svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
        <circle cx="18" cy="5" r="3"></circle>
        <circle cx="6" cy="12" r="3"></circle>
        <circle cx="18" cy="19" r="3"></circle>
        <line x1="8.59" y1="13.51" x2="15.42" y2="17.49"></line>
        <line x1="15.41" y1="6.51" x2="8.59" y2="10.49"></line>
      </svg>
      <span>{{ copiado ? '¡Enlace copiado!' : 'Compartir Evento' }}</span>
    </button>

    <!-- Menú Desplegable Fallback (Desktop / Navegadores sin Web Share) -->
    <div
      v-if="menuAbierto"
      class="share-dropdown-menu position-absolute mt-2 p-2 rounded-3 shadow-lg"
      style="z-index: 1050; min-width: 190px;"
    >
      <button type="button" class="dropdown-item py-2 px-3 rounded d-flex align-items-center gap-2 small" @click="compartirWsp">
        <span style="color: #25d366;">★</span> WhatsApp
      </button>
      <button type="button" class="dropdown-item py-2 px-3 rounded d-flex align-items-center gap-2 small" @click="compartirLinkedin">
        <span style="color: #0077b5;">★</span> LinkedIn
      </button>
      <button type="button" class="dropdown-item py-2 px-3 rounded d-flex align-items-center gap-2 small" @click="compartirTwitter">
        <span style="color: #1da1f2;">★</span> X / Twitter
      </button>
      <hr class="my-1 border-secondary-subtle" />
      <button type="button" class="dropdown-item py-2 px-3 rounded d-flex align-items-center gap-2 small" @click="copiarEnlace">
        <span>🔗</span> {{ copiado ? '¡Copiado!' : 'Copiar enlace' }}
      </button>
    </div>
  </div>
</template>

<style scoped>
.share-dropdown-menu {
  background: var(--card-surface);
  border: 1px solid var(--card-border);
  backdrop-filter: blur(16px);
  -webkit-backdrop-filter: blur(16px);
}
.dropdown-item {
  color: var(--bs-body-color);
  background: transparent;
  border: none;
  width: 100%;
  text-align: left;
  transition: background 0.15s ease;
}
.dropdown-item:hover {
  background: rgba(127, 127, 127, 0.12);
}
</style>