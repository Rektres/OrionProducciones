<script setup lang="ts">
import { onMounted, ref, computed } from 'vue';
import ContactForm from '@/components/ContactForm.vue';
import { serviciosService } from '@/services/servicios';
import type { Servicio, CategoriaServicio } from '@/types';

const categorias = ref<CategoriaServicio[]>([]);
const servicios = ref<Servicio[]>([]);
const sel = ref<string | null>(null);

const filtrados = computed(() =>
  sel.value ? servicios.value.filter((s) => s.categoria_slug === sel.value) : servicios.value,
);

onMounted(async () => {
  [categorias.value, servicios.value] = await Promise.all([
    serviciosService.getCategorias(),
    serviciosService.getServicios(),
  ]);
});
</script>

<template>
  <section class="py-5 text-center">
    <div class="container">
      <h1 class="display-4 fw-bold">SERVICIOS</h1>
      <p class="text-secondary">Lo que hacemos para tu evento</p>
    </div>
  </section>

  <section class="py-4">
    <div class="container">
      <div class="d-flex flex-wrap gap-2 justify-content-center mb-4">
        <button class="btn btn-sm" :class="sel === null ? 'btn-orion' : 'btn-outline-light'" @click="sel = null">Todos</button>
        <button v-for="c in categorias" :key="c.id" class="btn btn-sm"
          :class="sel === c.slug ? 'btn-orion' : 'btn-outline-light'" @click="sel = c.slug">
          {{ c.nombre }}
        </button>
      </div>
      <div class="row g-4">
        <div v-for="svc in filtrados" :key="svc.id" class="col-md-6 col-lg-4">
          <div class="card h-100 bg-dark border-secondary">
            <div class="card-body">
              <h5 class="card-title">{{ svc.nombre }}</h5>
              <p class="card-text text-secondary small">{{ svc.descripcion_corta }}</p>
            </div>
          </div>
        </div>
      </div>
    </div>
  </section>

  <section id="cotizacion-servicios" class="py-5 cotiza-section">
    <div class="container" style="max-width: 720px">
      <h2 class="text-center fw-bold mb-4">CUÉNTANOS TU IDEA</h2>
      <ContactForm />
    </div>
  </section>
</template>
