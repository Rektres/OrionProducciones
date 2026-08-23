<script setup lang="ts">
import { reactive, ref } from 'vue';
import type { AxiosError } from 'axios';
import { RouterLink, useRouter } from 'vue-router';
import { contactoService } from '@/services/contacto';
import { registrarEvento } from '@/composables/useAnalitica';
import type { CotizacionFormData } from '@/types';

const router = useRouter();
const hoy = new Date().toISOString().split('T')[0];
const loading = ref(false);

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

/** Errores por campo que devuelve DRF: { email: ["Introduzca una dirección..."] }. */
const errores = ref<Record<string, string>>({});
/** Error transversal: red caída, 500, throttle (429) o non_field_errors. */
const errorGeneral = ref('');

const CAMPOS = Object.keys(form);

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
  loading.value = true;
  errores.value = {};
  errorGeneral.value = '';
  try {
    await contactoService.crearCotizacion({ ...form });
    registrarEvento('cotizacion_enviada', { tipo_evento: form.tipo_evento });
    router.push('/gracias');
  } catch (e) {
    registrarError(e);
  } finally {
    loading.value = false;
  }
};
</script>

<template>
  <form class="row g-3" @submit.prevent="onSubmit">
    <div v-if="errorGeneral" class="col-12">
      <div class="alert alert-danger py-2 mb-0" role="alert" aria-live="assertive">
        {{ errorGeneral }}
      </div>
    </div>
    <div class="col-md-6">
      <label class="form-label">Nombre *</label>
      <input v-model="form.nombre" type="text" required class="form-control"
        :class="{ 'is-invalid': errores.nombre }" placeholder="Tu nombre" />
      <div v-if="errores.nombre" class="invalid-feedback d-block">{{ errores.nombre }}</div>
    </div>
    <div class="col-md-6">
      <label class="form-label">Email *</label>
      <input v-model="form.email" type="email" required class="form-control"
        :class="{ 'is-invalid': errores.email }" placeholder="tu@email.com" />
      <div v-if="errores.email" class="invalid-feedback d-block">{{ errores.email }}</div>
    </div>
    <div class="col-md-6">
      <label class="form-label">Teléfono</label>
      <input v-model="form.telefono" type="tel" class="form-control"
        :class="{ 'is-invalid': errores.telefono }" placeholder="+56 9 1234 5678" />
      <div v-if="errores.telefono" class="invalid-feedback d-block">{{ errores.telefono }}</div>
    </div>
    <div class="col-md-6">
      <label class="form-label">Empresa</label>
      <input v-model="form.empresa" type="text" class="form-control"
        :class="{ 'is-invalid': errores.empresa }" placeholder="Tu empresa" />
      <div v-if="errores.empresa" class="invalid-feedback d-block">{{ errores.empresa }}</div>
    </div>
    <div class="col-md-6">
      <label class="form-label">Tipo de Evento *</label>
      <select v-model="form.tipo_evento" class="form-select"
        :class="{ 'is-invalid': errores.tipo_evento }">
        <option value="corporativo">Corporativo</option>
        <option value="social">Social</option>
        <option value="festival">Festival / Concierto</option>
        <option value="otro">Otro</option>
      </select>
      <div v-if="errores.tipo_evento" class="invalid-feedback d-block">{{ errores.tipo_evento }}</div>
    </div>
    <div class="col-md-6">
      <label class="form-label">Fecha Estimada</label>
      <input v-model="form.fecha_estimada" type="date" :min="hoy" class="form-control"
        :class="{ 'is-invalid': errores.fecha_estimada }" />
      <div v-if="errores.fecha_estimada" class="invalid-feedback d-block">{{ errores.fecha_estimada }}</div>
    </div>
    <div class="col-12">
      <label class="form-label">Descripción del evento *</label>
      <textarea v-model="form.descripcion" required rows="4" class="form-control"
        :class="{ 'is-invalid': errores.descripcion }"
        placeholder="Cuéntanos sobre tu evento..."></textarea>
      <div v-if="errores.descripcion" class="invalid-feedback d-block">{{ errores.descripcion }}</div>
    </div>
    <div class="col-12">
      <label class="form-label">Presupuesto estimado</label>
      <input v-model="form.presupuesto_estimado" type="text" class="form-control"
        :class="{ 'is-invalid': errores.presupuesto_estimado }"
        placeholder="Ej: $500.000 - $1.000.000" />
      <div v-if="errores.presupuesto_estimado" class="invalid-feedback d-block">{{ errores.presupuesto_estimado }}</div>
    </div>
    <div class="col-12">
      <button type="submit" class="btn btn-orion w-100" :disabled="loading">
        {{ loading ? 'Enviando...' : 'Enviar Cotización' }}
      </button>
      <p class="text-secondary small mt-2 mb-0">
        Al enviar aceptas nuestra
        <RouterLink to="/politica-de-privacidad" class="link-secondary">política de privacidad</RouterLink>.
        Usamos tus datos solo para responder esta cotización.
      </p>
    </div>
  </form>
</template>
