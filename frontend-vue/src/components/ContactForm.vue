<script setup lang="ts">
import { reactive, ref, computed } from 'vue';
import { contactoService } from '@/services/contacto';
import type { CotizacionFormData } from '@/types';

const hoy = new Date().toISOString().split('T')[0];
const loading = ref(false);
const submitted = ref(false);

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

const numero = import.meta.env.VITE_WHATSAPP_NUMBER || '56944830378';
const whatsapp = computed(() => `https://wa.me/${numero}`);

const onSubmit = async () => {
  loading.value = true;
  try {
    await contactoService.crearCotizacion({ ...form });
    submitted.value = true;
  } catch (e) {
    alert('Error enviando la cotización. Intenta de nuevo.');
  } finally {
    loading.value = false;
  }
};
</script>

<template>
  <div v-if="submitted" class="card bg-dark border-secondary text-center p-4">
    <h3 class="text-orion-primary">Recibimos tu solicitud</h3>
    <p class="text-secondary">Te contactaremos en menos de 24 horas.</p>
    <a :href="whatsapp" target="_blank" rel="noopener noreferrer" class="text-orion-primary">
      Contactar por WhatsApp
    </a>
  </div>

  <form v-else class="row g-3" @submit.prevent="onSubmit">
    <div class="col-md-6">
      <label class="form-label">Nombre *</label>
      <input v-model="form.nombre" type="text" required class="form-control" placeholder="Tu nombre" />
    </div>
    <div class="col-md-6">
      <label class="form-label">Email *</label>
      <input v-model="form.email" type="email" required class="form-control" placeholder="tu@email.com" />
    </div>
    <div class="col-md-6">
      <label class="form-label">Teléfono</label>
      <input v-model="form.telefono" type="tel" class="form-control" placeholder="+56 9 1234 5678" />
    </div>
    <div class="col-md-6">
      <label class="form-label">Empresa</label>
      <input v-model="form.empresa" type="text" class="form-control" placeholder="Tu empresa" />
    </div>
    <div class="col-md-6">
      <label class="form-label">Tipo de Evento *</label>
      <select v-model="form.tipo_evento" class="form-select">
        <option value="corporativo">Corporativo</option>
        <option value="social">Social</option>
        <option value="festival">Festival / Concierto</option>
        <option value="otro">Otro</option>
      </select>
    </div>
    <div class="col-md-6">
      <label class="form-label">Fecha Estimada</label>
      <input v-model="form.fecha_estimada" type="date" :min="hoy" class="form-control" />
    </div>
    <div class="col-12">
      <label class="form-label">Descripción del evento *</label>
      <textarea v-model="form.descripcion" required rows="4" class="form-control"
        placeholder="Cuéntanos sobre tu evento..."></textarea>
    </div>
    <div class="col-12">
      <label class="form-label">Presupuesto estimado</label>
      <input v-model="form.presupuesto_estimado" type="text" class="form-control"
        placeholder="Ej: $500.000 - $1.000.000" />
    </div>
    <div class="col-12">
      <button type="submit" class="btn btn-orion w-100" :disabled="loading">
        {{ loading ? 'Enviando...' : 'Enviar Cotización' }}
      </button>
    </div>
  </form>
</template>
