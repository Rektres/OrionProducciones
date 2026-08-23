<script setup lang="ts">
import { onMounted, ref, computed } from 'vue';
import FadeInUp from '@/components/animations/FadeInUp.vue';
import ParticleBackground from '@/components/animations/ParticleBackground.vue';
import ServicioModal from '@/components/ServicioModal.vue';
import { serviciosService } from '@/services/servicios';
import type { Servicio, CategoriaServicio } from '@/types';

const categorias = ref<CategoriaServicio[]>([]);
const servicios = ref<Servicio[]>([]);
const sel = ref<string | null>(null);
const cargando = ref(true);
const error = ref(false);

const servicioModalRef = ref<InstanceType<typeof ServicioModal> | null>(null);
const abrirServicio = (svc: Servicio) => servicioModalRef.value?.abrir(svc);

const filtrados = computed(() =>
  sel.value ? servicios.value.filter((s) => s.categoria_slug === sel.value) : servicios.value,
);

onMounted(async () => {
  try {
    [categorias.value, servicios.value] = await Promise.all([
      serviciosService.getCategorias(),
      serviciosService.getServicios(),
    ]);
  } catch (e) {
    error.value = true;
    console.error('Error cargando servicios:', e);
  } finally {
    cargando.value = false;
  }
});
</script>

<template>
  <section class="py-5 text-center position-relative overflow-hidden">
    <ParticleBackground />
    <div class="container position-relative" style="z-index: 1">
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
      <div v-if="cargando" class="text-center text-secondary py-5" aria-live="polite">
        <div class="spinner-border text-orion-primary" role="status" aria-hidden="true"></div>
        <p class="mt-3 mb-0">Cargando servicios...</p>
      </div>
      <div v-else-if="error" class="text-center text-secondary py-5">
        No pudimos cargar los servicios. Recarga la página en unos momentos.
      </div>
      <div v-else-if="!filtrados.length" class="text-center text-secondary py-5">
        Todavía no hay servicios publicados en esta categoría.
      </div>
      <div v-else class="row g-4">
        <div v-for="(svc, idx) in filtrados" :key="svc.id" class="col-md-6 col-lg-4">
          <FadeInUp :delay="idx * 0.05">
            <div class="card h-100 bg-dark border-secondary hover-scale" style="cursor: pointer" @click="abrirServicio(svc)">
              <div v-if="svc.imagen_url" class="card-cover overflow-hidden rounded-top" style="height: 10rem">
                <img :src="svc.imagen_url" :alt="`Servicio de ${svc.nombre}`" class="img-cover"
                  loading="lazy" decoding="async" />
              </div>
              <div class="card-body">
                <h5 class="card-title mb-0">{{ svc.nombre }}</h5>
              </div>
            </div>
          </FadeInUp>
        </div>
      </div>
    </div>
  </section>

  <ServicioModal ref="servicioModalRef" />
</template>
