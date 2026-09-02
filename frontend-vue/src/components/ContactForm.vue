<script setup lang="ts">
import { reactive, ref, computed } from 'vue';
import type { AxiosError } from 'axios';
import { RouterLink, useRouter } from 'vue-router';
import { contactoService } from '@/services/contacto';
import { registrarEvento } from '@/composables/useAnalitica';
import type { CotizacionFormData } from '@/types';

const router = useRouter();
const hoy = new Date().toISOString().split('T')[0];
const loading = ref(false);
const isSubmitting = ref(false);

const form = reactive<CotizacionFormData>({
  nombre: '',
  email: '',
  telefono: '',
  empresa: '',
  tipo_evento: 'corporativo',
  descripcion: '',
  fecha_estimada: '',
  presupuesto_estimado: '',
});

/** Errores por campo que devuelve DRF o validación local */
const errores = ref<Record<string, string>>({});
/** Error transversal */
const errorGeneral = ref('');

const CAMPOS = Object.keys(form);

// Límite de caracteres en descripción
const MAX_DESCRIPCION = 1000;
const caracteresRestantes = computed(() => {
  return MAX_DESCRIPCION - (form.descripcion?.length || 0);
});

// Formateador dinámico de teléfono chileno (+569 XXXX XXXX)
const onTelefonoInput = (e: Event) => {
  const target = e.target as HTMLInputElement;
  let val = target.value.replace(/[^\d+]/g, ''); // Solo dígitos y '+'
  
  // Limpiar dígitos
  let digits = val.replace(/\D/g, '');

  if (digits.startsWith('569')) {
    digits = digits.slice(3);
  } else if (digits.startsWith('56')) {
    digits = digits.slice(2);
  } else if (digits.startsWith('9')) {
    digits = digits.slice(1);
  }

  // Limitar a 8 dígitos locales
  digits = digits.slice(0, 8);

  if (digits.length > 0) {
    if (digits.length <= 4) {
      form.telefono = `+569 ${digits}`;
    } else {
      form.telefono = `+569 ${digits.slice(0, 4)} ${digits.slice(4)}`;
    }
  } else if (val.includes('+')) {
    form.telefono = '+569 ';
  } else {
    form.telefono = '';
  }

  if (errores.value.telefono) {
    validarTelefono();
  }
};

// Formateador dinámico de presupuesto ($ 1.000.000)
const onPresupuestoInput = (e: Event) => {
  const target = e.target as HTMLInputElement;
  const digits = target.value.replace(/\D/g, '');
  if (!digits) {
    form.presupuesto_estimado = '';
    return;
  }
  const num = parseInt(digits, 10);
  if (num <= 0) {
    form.presupuesto_estimado = '$ 0';
  } else {
    form.presupuesto_estimado = `$ ${num.toLocaleString('es-CL')}`;
  }

  if (errores.value.presupuesto_estimado) {
    validarPresupuesto();
  }
};

// Validaciones individuales
const validarNombre = (): boolean => {
  const v = form.nombre.trim();
  if (!v || !/[a-zA-ZáéíóúÁÉÍÓÚñÑ]/.test(v)) {
    errores.value.nombre = 'El nombre debe contener al menos 1 letra.';
    return false;
  }
  delete errores.value.nombre;
  return true;
};

const validarEmail = (): boolean => {
  const v = form.email.trim();
  const emailRegex = /^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$/;
  if (!v || !emailRegex.test(v)) {
    errores.value.email = 'Introduce un correo válido con su dominio (ej: nombre@empresa.cl).';
    return false;
  }
  delete errores.value.email;
  return true;
};

const validarTelefono = (): boolean => {
  const tel = form.telefono?.trim() || '';
  if (!tel) {
    delete errores.value.telefono;
    return true;
  }
  const digits = tel.replace(/\D/g, '');
  if (digits.length < 11) { // 569 + 8 digitos = 11 digitos
    errores.value.telefono = 'El teléfono debe tener formato válido (+569 1234 5678).';
    return false;
  }
  delete errores.value.telefono;
  return true;
};

const validarEmpresa = (): boolean => {
  if (form.empresa && form.empresa.trim().length < 1) {
    errores.value.empresa = 'El nombre de empresa debe tener al menos 1 carácter.';
    return false;
  }
  delete errores.value.empresa;
  return true;
};

const validarDescripcion = (): boolean => {
  const v = form.descripcion?.trim() || '';
  if (!v || v.length < 5) {
    errores.value.descripcion = 'Por favor describe brevemente tu evento (mínimo 5 caracteres).';
    return false;
  }
  if (v.length > MAX_DESCRIPCION) {
    errores.value.descripcion = `La descripción no puede superar los ${MAX_DESCRIPCION} caracteres.`;
    return false;
  }
  delete errores.value.descripcion;
  return true;
};

const validarPresupuesto = (): boolean => {
  const pres = form.presupuesto_estimado?.trim() || '';
  if (!pres) {
    delete errores.value.presupuesto_estimado;
    return true;
  }
  const digits = pres.replace(/\D/g, '');
  const num = parseInt(digits, 10);
  if (isNaN(num) || num <= 0) {
    errores.value.presupuesto_estimado = 'El presupuesto debe ser un número mayor a 0.';
    return false;
  }
  delete errores.value.presupuesto_estimado;
  return true;
};

const validarTodo = (): boolean => {
  const ok1 = validarNombre();
  const ok2 = validarEmail();
  const ok3 = validarTelefono();
  const ok4 = validarEmpresa();
  const ok5 = validarDescripcion();
  const ok6 = validarPresupuesto();
  return ok1 && ok2 && ok3 && ok4 && ok5 && ok6;
};

const registrarError = (e: unknown) => {
  errores.value = {};
  const respuesta = (e as AxiosError<Record<string, unknown>>)?.response;

  if (!respuesta) {
    errorGeneral.value = 'No pudimos conectar con el servidor. Revisa tu conexión e intenta de nuevo.';
    return;
  }
  if (respuesta.status === 429) {
    errorGeneral.value = 'Recibimos varias solicitudes desde tu conexión. Espera unos minutos e intenta de nuevo.';
    return;
  }

  const datos = respuesta.data;
  if (respuesta.status === 400 && datos && typeof datos === 'object') {
    const generales: string[] = [];
    for (const [campo, valor] of Object.entries(datos)) {
      const mensaje = Array.isArray(valor) ? valor.join(' ') : String(valor);
      if (CAMPOS.includes(campo)) errores.value[campo] = mensaje;
      else generales.push(mensaje);
    }
    errorGeneral.value = generales.join(' ');
    if (!generales.length && !Object.keys(errores.value).length) {
      errorGeneral.value = 'Revisa los datos del formulario e intenta de nuevo.';
    }
    return;
  }

  errorGeneral.value = 'Error enviando la cotización. Intenta de nuevo en unos minutos.';
};

const onSubmit = async () => {
  // Anti-spam / bloqueo estricto de múltiples envíos
  if (loading.value || isSubmitting.value) return;

  errores.value = {};
  errorGeneral.value = '';

  if (!validarTodo()) {
    errorGeneral.value = 'Por favor corrige los campos señalados antes de continuar.';
    return;
  }

  isSubmitting.value = true;
  loading.value = true;

  try {
    await contactoService.crearCotizacion({ ...form });
    registrarEvento('cotizacion_enviada', { tipo_evento: form.tipo_evento });
    router.push('/gracias');
  } catch (e) {
    registrarError(e);
  } finally {
    loading.value = false;
    isSubmitting.value = false;
  }
};
</script>

<template>
  <form class="contact-quote-form" @submit.prevent="onSubmit">
    <div v-if="errorGeneral" class="col-12 mb-3">
      <div class="alert alert-danger py-2 mb-0" role="alert" aria-live="assertive">
        {{ errorGeneral }}
      </div>
    </div>

    <!-- FILA 1: 3 COLUMNAS (Nombre, Email, Teléfono) -->
    <div class="row g-3 mb-3">
      <div class="col-lg-4 col-md-6">
        <label class="form-label fw-semibold">Nombre y Apellido *</label>
        <div class="input-icon-wrap">
          <input
            v-model="form.nombre"
            type="text"
            required
            class="form-control"
            :class="{ 'is-invalid': errores.nombre }"
            placeholder="Ej: Carolina Rojas"
            @blur="validarNombre"
          />
        </div>
        <div v-if="errores.nombre" class="invalid-feedback d-block">{{ errores.nombre }}</div>
      </div>

      <div class="col-lg-4 col-md-6">
        <label class="form-label fw-semibold">Correo Electrónico *</label>
        <div class="input-icon-wrap">
          <input
            v-model="form.email"
            type="email"
            required
            class="form-control"
            :class="{ 'is-invalid': errores.email }"
            placeholder="contacto@empresa.cl"
            @blur="validarEmail"
          />
        </div>
        <div v-if="errores.email" class="invalid-feedback d-block">{{ errores.email }}</div>
      </div>

      <div class="col-lg-4 col-md-12">
        <label class="form-label fw-semibold">Teléfono / WhatsApp</label>
        <div class="input-icon-wrap">
          <input
            :value="form.telefono"
            type="tel"
            class="form-control"
            :class="{ 'is-invalid': errores.telefono }"
            placeholder="+569 1234 5678"
            @input="onTelefonoInput"
            @blur="validarTelefono"
          />
        </div>
        <div v-if="errores.telefono" class="invalid-feedback d-block">{{ errores.telefono }}</div>
      </div>
    </div>

    <!-- FILA 2: 3 COLUMNAS (Empresa, Tipo de Evento, Fecha Estimada) -->
    <div class="row g-3 mb-3">
      <div class="col-lg-4 col-md-6">
        <label class="form-label fw-semibold">Empresa u Organización</label>
        <input
          v-model="form.empresa"
          type="text"
          class="form-control"
          :class="{ 'is-invalid': errores.empresa }"
          placeholder="Nombre de tu empresa"
          @blur="validarEmpresa"
        />
        <div v-if="errores.empresa" class="invalid-feedback d-block">{{ errores.empresa }}</div>
      </div>

      <div class="col-lg-4 col-md-6">
        <label class="form-label fw-semibold">Tipo de Evento *</label>
        <select
          v-model="form.tipo_evento"
          class="form-select custom-select-modern"
          :class="{ 'is-invalid': errores.tipo_evento }"
        >
          <option value="corporativo">Corporativo / Gala Anual</option>
          <option value="social">Social / Aniversario / Graduación</option>
          <option value="festival">Festival / Concierto en Vivo</option>
          <option value="otro">Lanzamiento / Otro Formato</option>
        </select>
        <div v-if="errores.tipo_evento" class="invalid-feedback d-block">{{ errores.tipo_evento }}</div>
      </div>

      <div class="col-lg-4 col-md-12">
        <label class="form-label fw-semibold">Fecha Estimada</label>
        <div class="modern-datepicker-wrapper">
          <input
            v-model="form.fecha_estimada"
            type="date"
            :min="hoy"
            class="form-control modern-date-input"
            :class="{ 'is-invalid': errores.fecha_estimada }"
          />
        </div>
        <div v-if="errores.fecha_estimada" class="invalid-feedback d-block">{{ errores.fecha_estimada }}</div>
      </div>
    </div>

    <!-- FILA 3: PRESUPUESTO & DESCRIPCIÓN -->
    <div class="row g-3 mb-3">
      <div class="col-lg-4 col-md-12">
        <label class="form-label fw-semibold">Presupuesto Estimado (CLP)</label>
        <input
          :value="form.presupuesto_estimado"
          type="text"
          class="form-control"
          :class="{ 'is-invalid': errores.presupuesto_estimado }"
          placeholder="Ej: $ 2.500.000"
          @input="onPresupuestoInput"
          @blur="validarPresupuesto"
        />
        <div v-if="errores.presupuesto_estimado" class="invalid-feedback d-block">{{ errores.presupuesto_estimado }}</div>
        <div class="form-text text-secondary" style="font-size: 11.5px;">
          Ingresa solo valores mayores a $0 o déjalo vacío si deseas que lo evaluemos juntos.
        </div>
      </div>

      <div class="col-lg-8 col-md-12">
        <div class="d-flex justify-content-between align-items-center mb-1">
          <label class="form-label fw-semibold mb-0">Descripción del Evento *</label>
          <span
            class="badge-char-count"
            :class="{ 'text-danger': caracteresRestantes < 50, 'text-secondary': caracteresRestantes >= 50 }"
          >
            {{ caracteresRestantes }} caracteres restantes
          </span>
        </div>
        <textarea
          v-model="form.descripcion"
          required
          rows="3"
          :maxlength="MAX_DESCRIPCION"
          class="form-control"
          :class="{ 'is-invalid': errores.descripcion }"
          placeholder="Cuéntanos detalles clave: cantidad de personas estimada, lugar del evento, requerimientos de sonido, iluminación o pantallas..."
          @blur="validarDescripcion"
        ></textarea>
        <div v-if="errores.descripcion" class="invalid-feedback d-block">{{ errores.descripcion }}</div>
      </div>
    </div>

    <!-- FILA 4: TÉRMINOS Y BOTÓN DE ACCIÓN -->
    <div class="row g-3 align-items-center pt-2">
      <div class="col-lg-8 col-md-7">
        <p class="small text-secondary mb-0" style="font-size: 12px; line-height: 1.5;">
          Al enviar esta solicitud aceptas nuestra
          <RouterLink to="/privacidad" class="text-decoration-underline text-body">Política de Privacidad</RouterLink>
          y
          <RouterLink to="/terminos" class="text-decoration-underline text-body">Términos de Servicio</RouterLink>.
          Tus datos se manejan con estricta confidencialidad.
        </p>
      </div>

      <div class="col-lg-4 col-md-5 text-md-end">
        <button
          type="submit"
          class="btn btn-orion w-100 py-3 d-flex align-items-center justify-content-center gap-2"
          :disabled="loading || isSubmitting"
        >
          <span v-if="loading" class="spinner-border spinner-border-sm" role="status" aria-hidden="true"></span>
          <span v-if="loading">Enviando Cotización...</span>
          <template v-else>
            <span>Enviar Solicitud</span>
            <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><path d="M5 12h14M12 5l7 7-7 7"/></svg>
          </template>
        </button>
      </div>
    </div>
  </form>
</template>

<style scoped>
.contact-quote-form {
  position: relative;
  width: 100%;
}

.modern-datepicker-wrapper {
  position: relative;
}

.modern-date-input {
  cursor: pointer;
  font-family: inherit;
}

.badge-char-count {
  font-size: 11px;
  font-weight: 500;
  letter-spacing: 0.2px;
}

.custom-select-modern {
  cursor: pointer;
}
</style>
