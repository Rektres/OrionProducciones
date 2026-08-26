<script setup lang="ts">
import { onMounted, ref } from 'vue';
import { RouterLink } from 'vue-router';
import { cargarAnalitica } from '@/composables/useAnalitica';

const CLAVE_CONSENTIMIENTO = 'orion_cookie_consent';

interface PreferenciasCookies {
  esenciales: boolean;
  analitica: boolean;
  personalizacion: boolean;
  fecha: string;
}

const visible = ref(false);
const modoDetalle = ref(false);

const prefs = ref<PreferenciasCookies>({
  esenciales: true, // Siempre obligatorias
  analitica: true,
  personalizacion: true,
  fecha: '',
});

onMounted(() => {
  const guardado = localStorage.getItem(CLAVE_CONSENTIMIENTO);
  if (guardado) {
    try {
      const parsed: PreferenciasCookies = JSON.parse(guardado);
      prefs.value = parsed;
      if (parsed.analitica) {
        cargarAnalitica();
      }
    } catch {
      visible.value = true;
    }
  } else {
    visible.value = true;
  }
});

const guardarPreferencias = () => {
  prefs.value.fecha = new Date().toISOString();
  localStorage.setItem(CLAVE_CONSENTIMIENTO, JSON.stringify(prefs.value));
  visible.value = false;
  if (prefs.value.analitica) {
    cargarAnalitica();
  }
};

const aceptarTodas = () => {
  prefs.value.analitica = true;
  prefs.value.personalizacion = true;
  guardarPreferencias();
};

const soloEsenciales = () => {
  prefs.value.analitica = false;
  prefs.value.personalizacion = false;
  guardarPreferencias();
};

const toggleDetalle = () => {
  modoDetalle.value = !modoDetalle.value;
};
</script>

<template>
  <transition name="fade-slide">
    <aside
      v-if="visible"
      class="cookie-banner-wrap position-fixed bottom-0 start-0 end-0 p-3 p-md-4"
      role="dialog"
      aria-live="polite"
      aria-label="Panel de Privacidad y Consentimiento de Cookies"
    >
      <div class="container" style="max-width: 920px">
        <div class="card cookie-card shadow-lg">
          <div class="card-body p-4">
            <div class="d-flex align-items-start gap-3">
              <div class="cookie-icon flex-shrink-0">
                <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                  <path d="M12 2a10 10 0 1 0 10 10 4 4 0 0 1-5-5 4 4 0 0 1-5-5z" />
                  <path d="M8.5 8.5v.01M7.5 15.5v.01M16.5 15.5v.01M12 12v.01" stroke-width="3" stroke-linecap="round" />
                </svg>
              </div>
              <div class="flex-grow-1">
                <h3 class="h5 fw-bold mb-1 d-flex align-items-center gap-2">
                  <span>Control de Privacidad & Cookies</span>
                  <span class="badge text-bg-warning-subtle text-warning border border-warning-subtle small" style="font-size: 10px;">
                    Ley N° 19.628 / Transparencia
                  </span>
                </h3>
                <p class="text-secondary small mb-3" style="line-height: 1.6;">
                  En <strong>Orión Stage</strong> respetamos tu privacidad. Te informamos qué datos almacenamos localmente para asegurar el funcionamiento del sitio y te permitimos escoger qué categorías activar. Conoce más en nuestra
                  <RouterLink to="/politica-de-privacidad" class="text-decoration-underline text-body fw-bold">política de privacidad</RouterLink>.
                </p>

                <!-- PANEL DETALLADO DE CATEGORÍAS (QUÉ DATOS SE GUARDAN) -->
                <div v-if="modoDetalle" class="cookie-categories my-3 p-3 rounded-3">
                  <!-- Categoría 1: Esenciales -->
                  <div class="cookie-category-item d-flex align-items-center justify-content-between py-2 border-bottom border-secondary-subtle">
                    <div>
                      <strong class="d-block text-body small">1. Técnicas & Necesarias</strong>
                      <span class="text-secondary" style="font-size: 11.5px;">
                        Guarda tu preferencia de tema (Dark/Light), sesión de administración y seguridad. No rastrea datos personales.
                      </span>
                    </div>
                    <span class="badge bg-secondary-subtle text-secondary small flex-shrink-0 ms-3">Siempre Activas</span>
                  </div>

                  <!-- Categoría 2: Analítica -->
                  <div class="cookie-category-item d-flex align-items-center justify-content-between py-2 border-bottom border-secondary-subtle">
                    <div>
                      <strong class="d-block text-body small">2. Analítica de Navegación</strong>
                      <span class="text-secondary" style="font-size: 11.5px;">
                        Métricas agregadas y anónimas para saber qué servicios y eventos son los más visitados y optimizar la velocidad.
                      </span>
                    </div>
                    <div class="form-check form-switch ms-3 flex-shrink-0">
                      <input
                        v-model="prefs.analitica"
                        class="form-check-input"
                        type="checkbox"
                        role="switch"
                        id="cookie-analitica-switch"
                      />
                    </div>
                  </div>

                  <!-- Categoría 3: Personalización -->
                  <div class="cookie-category-item d-flex align-items-center justify-content-between py-2">
                    <div>
                      <strong class="d-block text-body small">3. Experiencias & Campañas</strong>
                      <span class="text-secondary" style="font-size: 11.5px;">
                        Recuerda temporalmente las campañas de interés consultadas para facilitar cotizaciones personalizadas.
                      </span>
                    </div>
                    <div class="form-check form-switch ms-3 flex-shrink-0">
                      <input
                        v-model="prefs.personalizacion"
                        class="form-check-input"
                        type="checkbox"
                        role="switch"
                        id="cookie-personalizacion-switch"
                      />
                    </div>
                  </div>
                </div>

                <!-- BOTONES DE ACCIÓN -->
                <div class="d-flex flex-wrap align-items-center gap-2 justify-content-between mt-3 pt-2 border-top border-secondary-subtle">
                  <button
                    type="button"
                    class="btn btn-sm btn-link text-decoration-none text-secondary p-0"
                    @click="toggleDetalle"
                  >
                    {{ modoDetalle ? '▲ Ocultar detalles' : '⚙ Personalizar / Ver qué datos guardamos' }}
                  </button>

                  <div class="d-flex flex-wrap gap-2">
                    <button
                      v-if="modoDetalle"
                      type="button"
                      class="btn btn-sm btn-outline-secondary"
                      @click="guardarPreferencias"
                    >
                      Guardar Selección
                    </button>
                    <button
                      type="button"
                      class="btn btn-sm btn-outline-secondary"
                      @click="soloEsenciales"
                    >
                      Solo Necesarias
                    </button>
                    <button
                      type="button"
                      class="btn btn-sm btn-orion"
                      @click="aceptarTodas"
                    >
                      Aceptar Todas
                    </button>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </aside>
  </transition>
</template>

<style scoped>
.cookie-banner-wrap {
  z-index: 1080;
}
.cookie-card {
  background: var(--card-surface);
  border: 1px solid var(--card-border);
  backdrop-filter: blur(20px);
  -webkit-backdrop-filter: blur(20px);
  border-radius: 20px;
  box-shadow: 0 25px 60px rgba(0, 0, 0, 0.4);
}
.cookie-icon {
  width: 44px;
  height: 44px;
  border-radius: 12px;
  background: rgba(19, 214, 234, 0.12);
  color: var(--orion-primary);
  display: grid;
  place-items: center;
}
.cookie-categories {
  background: rgba(127, 127, 127, 0.06);
  border: 1px solid var(--card-border);
}
.fade-slide-enter-active,
.fade-slide-leave-active {
  transition: all 0.35s ease;
}
.fade-slide-enter-from,
.fade-slide-leave-to {
  opacity: 0;
  transform: translateY(30px);
}
</style>
