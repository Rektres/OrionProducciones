<script setup lang="ts">
import { ref, reactive } from 'vue';
import { useRouter } from 'vue-router';
import { contactoService } from '@/services/contacto';
import { registrarEvento } from '@/composables/useAnalitica';

export interface CampanaData {
  id: string;
  mundo: string;
  titulo: string;
  subtitulo: string;
  descripcion: string;
  poster: string;
  badge: string;
  tagColor: string;
}

const router = useRouter();
const abierto = ref(false);
const campana = ref<CampanaData | null>(null);
const modoCotizar = ref(false);
const loading = ref(false);
const exito = ref(false);
const errorGeneral = ref('');
const escalaZoom = ref(1);

const form = reactive({
  nombre: '',
  email: '',
  telefono: '',
  mensaje: '',
});

const errores = ref<Record<string, string>>({});

const abrir = (c: CampanaData, cotizarDirecto = false) => {
  campana.value = c;
  modoCotizar.value = cotizarDirecto;
  exito.value = false;
  errorGeneral.value = '';
  errores.value = {};
  escalaZoom.value = 1;
  form.nombre = '';
  form.email = '';
  form.telefono = '';
  form.mensaje = `Hola, me gustaría solicitar información detallada y cotización para la campaña: ${c.mundo} - ${c.titulo}.`;
  abierto.value = true;
};

const cerrar = () => {
  abierto.value = false;
  modoCotizar.value = false;
  campana.value = null;
  escalaZoom.value = 1;
};

const toggleZoom = () => {
  escalaZoom.value = escalaZoom.value > 1 ? 1 : 2;
};

const zoomIn = () => {
  if (escalaZoom.value < 3) escalaZoom.value += 0.5;
};

const zoomOut = () => {
  if (escalaZoom.value > 1) escalaZoom.value -= 0.5;
};

const resetZoom = () => {
  escalaZoom.value = 1;
};


// Formateador dinámico de teléfono
const onTelefonoInput = (e: Event) => {
  const target = e.target as HTMLInputElement;
  let val = target.value.replace(/[^\d+]/g, '');
  let digits = val.replace(/\D/g, '');

  if (digits.startsWith('569')) digits = digits.slice(3);
  else if (digits.startsWith('56')) digits = digits.slice(2);
  else if (digits.startsWith('9')) digits = digits.slice(1);

  digits = digits.slice(0, 8);

  if (digits.length > 0) {
    if (digits.length <= 4) form.telefono = `+569 ${digits}`;
    else form.telefono = `+569 ${digits.slice(0, 4)} ${digits.slice(4)}`;
  } else if (val.includes('+')) {
    form.telefono = '+569 ';
  } else {
    form.telefono = '';
  }

  if (errores.value.telefono) validarTelefono();
};

const validarNombre = (): boolean => {
  const v = form.nombre.trim();
  if (!v || !/[a-zA-ZáéíóúÁÉÍÓÚñÑ]/.test(v)) {
    errores.value.nombre = 'Ingresa tu nombre (al menos 1 letra).';
    return false;
  }
  delete errores.value.nombre;
  return true;
};

const validarEmail = (): boolean => {
  const v = form.email.trim();
  const regex = /^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$/;
  if (!v || !regex.test(v)) {
    errores.value.email = 'Introduce un correo válido con dominio (ej: nombre@empresa.cl).';
    return false;
  }
  delete errores.value.email;
  return true;
};

const validarTelefono = (): boolean => {
  if (!form.telefono.trim()) {
    delete errores.value.telefono;
    return true;
  }
  const digits = form.telefono.replace(/\D/g, '');
  if (digits.length < 11) {
    errores.value.telefono = 'Formato inválido (+569 1234 5678).';
    return false;
  }
  delete errores.value.telefono;
  return true;
};

const enviarCotizacionCampana = async () => {
  if (loading.value) return;

  const ok1 = validarNombre();
  const ok2 = validarEmail();
  const ok3 = validarTelefono();
  if (!ok1 || !ok2 || !ok3) {
    errorGeneral.value = 'Por favor completa los campos correctamente.';
    return;
  }

  loading.value = true;
  errorGeneral.value = '';

  try {
    const descFinal = `[SOLICITUD DE CAMPAÑA: ${campana.value?.mundo} - ${campana.value?.titulo}]\n\n${form.mensaje}`;
    await contactoService.crearCotizacion({
      nombre: form.nombre.trim(),
      email: form.email.trim(),
      telefono: form.telefono.trim() || undefined,
      empresa: undefined,
      tipo_evento: 'corporativo',
      descripcion: descFinal,
      fecha_estimada: undefined,
      presupuesto_estimado: undefined,
    });

    registrarEvento('cotizacion_enviada', { tipo_evento: 'campana', campana: campana.value?.titulo });
    exito.value = true;
    setTimeout(() => {
      cerrar();
      router.push('/gracias');
    }, 1800);
  } catch (e) {
    errorGeneral.value = 'Ocurrió un error al enviar tu solicitud. Intenta nuevamente.';
  } finally {
    loading.value = false;
  }
};

defineExpose({ abrir, cerrar });
</script>

<template>
  <div
    v-if="abierto && campana"
    class="modal fade show d-block campana-modal-backdrop"
    tabindex="-1"
    @click.self="cerrar"
  >
    <div class="modal-dialog modal-dialog-centered campana-modal-dialog">
      <div class="modal-content campana-modal-content">
        <!-- HEADER -->
        <div class="modal-header border-0 pb-2 px-4 pt-4 d-flex justify-content-between align-items-center">
          <div>
            <span
              class="campana-badge-header"
              :style="{ color: campana.tagColor, borderColor: campana.tagColor }"
            >
              {{ campana.mundo }}
            </span>
            <h3 class="h4 fw-bold mb-0 text-body mt-1">{{ campana.titulo }}</h3>
          </div>
          <button type="button" class="btn-close" aria-label="Cerrar" @click="cerrar"></button>
        </div>

        <!-- MODAL BODY: VISTA POSTER ORGANICO -->
        <div v-if="!modoCotizar" class="modal-body px-4 py-3">
          <div class="campana-poster-full-wrap position-relative mb-3">
            <!-- Barra flotante de controles de zoom -->
            <div class="campana-zoom-toolbar d-flex align-items-center gap-1">
              <button
                type="button"
                class="btn btn-dark btn-sm py-0 px-2"
                title="Alejar imagen"
                :disabled="escalaZoom <= 1"
                @click.stop="zoomOut"
              >
                🔍 -
              </button>
              <span class="badge bg-dark bg-opacity-75 py-1 px-2 font-monospace" style="font-size: 11px;">
                {{ Math.round(escalaZoom * 100) }}%
              </span>
              <button
                type="button"
                class="btn btn-dark btn-sm py-0 px-2"
                title="Acercar imagen"
                :disabled="escalaZoom >= 3"
                @click.stop="zoomIn"
              >
                🔍 +
              </button>
              <button
                v-if="escalaZoom > 1"
                type="button"
                class="btn btn-outline-warning btn-sm py-0 px-2 ms-1"
                title="Restablecer tamaño original"
                @click.stop="resetZoom"
              >
                ↺ Original
              </button>
            </div>

            <div class="campana-zoom-viewport" :class="{ 'is-zoomed': escalaZoom > 1 }">
              <img
                :src="campana.poster"
                :alt="campana.titulo"
                class="campana-poster-highres"
                :style="{
                  transform: `scale(${escalaZoom})`,
                  cursor: escalaZoom > 1 ? 'zoom-out' : 'zoom-in',
                  transformOrigin: 'top center'
                }"
                loading="eager"
                @click="toggleZoom"
              />
            </div>
          </div>
          <p class="text-secondary mb-3 campana-modal-desc">
            {{ campana.descripcion }}
          </p>
        </div>


        <!-- MODAL BODY: VISTA FORMULARIO RAPIDO DE COTIZACION -->
        <div v-else class="modal-body px-4 py-3">
          <div v-if="exito" class="alert alert-success text-center py-4 my-2">
            <div class="fs-4 mb-2">✓ ¡Solicitud Enviada con Éxito!</div>
            <p class="mb-0 text-secondary">
              Hemos recibido tu solicitud y te enviamos un correo de confirmación. Te contactaremos a la brevedad.
            </p>
          </div>

          <div v-else>
            <div class="d-flex align-items-center gap-3 p-3 rounded-4 mb-4 campana-quote-card-header">
              <img :src="campana.poster" :alt="campana.titulo" class="campana-mini-thumb" />
              <div>
                <span class="small fw-bold text-uppercase" :style="{ color: campana.tagColor }">
                  {{ campana.mundo }}
                </span>
                <h4 class="h5 fw-bold mb-1 text-body">{{ campana.titulo }}</h4>
                <small class="text-secondary">{{ campana.subtitulo }}</small>
              </div>
            </div>

            <div v-if="errorGeneral" class="alert alert-danger py-2 mb-3">
              {{ errorGeneral }}
            </div>

            <form @submit.prevent="enviarCotizacionCampana">
              <div class="row g-3">
                <div class="col-md-6">
                  <label class="form-label fw-semibold small">Nombre y Apellido *</label>
                  <input
                    v-model="form.nombre"
                    type="text"
                    required
                    class="form-control"
                    :class="{ 'is-invalid': errores.nombre }"
                    placeholder="Ej: Carolina Rojas"
                    @blur="validarNombre"
                  />
                  <div v-if="errores.nombre" class="invalid-feedback d-block">{{ errores.nombre }}</div>
                </div>

                <div class="col-md-6">
                  <label class="form-label fw-semibold small">Correo Electrónico *</label>
                  <input
                    v-model="form.email"
                    type="email"
                    required
                    class="form-control"
                    :class="{ 'is-invalid': errores.email }"
                    placeholder="contacto@empresa.cl"
                    @blur="validarEmail"
                  />
                  <div v-if="errores.email" class="invalid-feedback d-block">{{ errores.email }}</div>
                </div>

                <div class="col-12">
                  <label class="form-label fw-semibold small">Teléfono / WhatsApp</label>
                  <input
                    :value="form.telefono"
                    type="tel"
                    class="form-control"
                    :class="{ 'is-invalid': errores.telefono }"
                    placeholder="+569 1234 5678"
                    @input="onTelefonoInput"
                    @blur="validarTelefono"
                  />
                  <div v-if="errores.telefono" class="invalid-feedback d-block">{{ errores.telefono }}</div>
                </div>

                <div class="col-12">
                  <label class="form-label fw-semibold small">Mensaje o Requerimientos</label>
                  <textarea
                    v-model="form.mensaje"
                    rows="3"
                    class="form-control"
                    placeholder="Escribe aquí cualquier detalle adicional de tu empresa o fecha estimada..."
                  ></textarea>
                </div>
              </div>

              <div class="d-flex justify-content-between align-items-center mt-4 pt-2 border-top">
                <button type="button" class="btn btn-outline-secondary btn-sm" @click="modoCotizar = false">
                  ← Volver a ver afiche
                </button>
                <button
                  type="submit"
                  class="btn btn-orion px-4 py-2 d-flex align-items-center gap-2"
                  :disabled="loading"
                >
                  <span v-if="loading" class="spinner-border spinner-border-sm"></span>
                  <span>{{ loading ? 'Enviando Solicitud...' : 'Enviar Solicitud de Información' }}</span>
                </button>
              </div>
            </form>
          </div>
        </div>

        <!-- FOOTER: BOTONES DE ACCIÓN CUANDO SE MUESTRA EL POSTER -->
        <div v-if="!modoCotizar" class="modal-footer border-0 px-4 pb-4 pt-0 d-flex justify-content-between">
          <button type="button" class="btn btn-outline-secondary" @click="cerrar">
            Cerrar
          </button>
          <button type="button" class="btn btn-orion d-flex align-items-center gap-2" @click="modoCotizar = true">
            <span>Cotizar / Solicitar Información</span>
            <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><path d="M5 12h14M12 5l7 7-7 7"/></svg>
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
.campana-modal-backdrop {
  background: rgba(0, 0, 0, 0.88);
  z-index: 1060;
  backdrop-filter: blur(8px);
}

.campana-modal-dialog {
  max-width: 920px;
  width: 95%;
  margin: 1.5rem auto;
}

.campana-modal-content {
  background: var(--card-surface);
  border: 1px solid var(--card-border);
  border-radius: 24px;
  overflow: hidden;
  box-shadow: 0 24px 60px rgba(0, 0, 0, 0.6);
}

[data-bs-theme='light'] .campana-modal-content {
  background: #ffffff;
  border-color: #dfd8cc;
  box-shadow: 0 24px 60px rgba(0, 0, 0, 0.15);
}

.campana-badge-header {
  font-size: 10px;
  font-weight: 800;
  letter-spacing: 0.1em;
  padding: 3px 8px;
  border-radius: 6px;
  border: 1px solid;
  background: rgba(255, 255, 255, 0.05);
  display: inline-block;
}

.campana-poster-full-wrap {
  width: 100%;
  max-height: 72vh;
  position: relative;
  border-radius: 16px;
  background: rgba(0, 0, 0, 0.4);
  border: 1px solid var(--card-border);
  overflow: hidden;
}

.campana-zoom-toolbar {
  position: absolute;
  top: 12px;
  right: 12px;
  z-index: 10;
  background: rgba(15, 23, 42, 0.85);
  backdrop-filter: blur(6px);
  padding: 4px 8px;
  border-radius: 20px;
  border: 1px solid rgba(255, 255, 255, 0.15);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.4);
}

.campana-zoom-viewport {
  width: 100%;
  max-height: 72vh;
  overflow: auto;
  display: flex;
  justify-content: center;
  align-items: flex-start;
  padding: 8px;
}

.campana-zoom-viewport.is-zoomed {
  display: block;
}

.campana-poster-highres {
  width: 100%;
  height: auto;
  max-height: 70vh;
  object-fit: contain;
  display: block;
  border-radius: 12px;
  transition: transform 0.25s cubic-bezier(0.2, 0.8, 0.2, 1);
}


.campana-modal-desc {
  font-size: 15px;
  line-height: 1.7;
}

.campana-quote-card-header {
  background: rgba(127, 127, 127, 0.07);
  border: 1px solid var(--card-border);
}

.campana-mini-thumb {
  width: 64px;
  height: 64px;
  object-fit: cover;
  border-radius: 12px;
  border: 1px solid var(--card-border);
}
</style>
