<script setup lang="ts">
import { onMounted, ref, computed } from 'vue';
import FadeInUp from '@/components/animations/FadeInUp.vue';
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
  <section class="pt-4 pb-2 text-center position-relative overflow-hidden">
    <div class="container position-relative" style="z-index: 1">
      <p class="eyebrow justify-content-center"><span></span> SOLUCIONES INTEGRALES</p>
      <h1 class="display-4 fw-bold">CATÁLOGO DE SERVICIOS</h1>
      <p class="text-secondary" style="max-width: 600px; margin: 0 auto;">Equipamiento de audio, iluminación, visuales y montaje escénico de nivel profesional para todo tipo de eventos.</p>
    </div>
  </section>

  <section class="py-4">
    <div class="container">
      <div class="catalog-toolbar">
        <div class="filter-chips">
          <button
            class="filter-chip"
            :class="{ 'is-active': sel === null }"
            @click="sel = null"
          >
            Todos
          </button>
          <button
            v-for="c in categorias"
            :key="c.id"
            class="filter-chip"
            :class="{ 'is-active': sel === c.slug }"
            @click="sel = c.slug"
          >
            {{ c.nombre }}
          </button>
        </div>
        <span class="catalog-count">
          <strong>{{ filtrados.length }}</strong> DISPONIBLES
        </span>
      </div>

      <div v-if="cargando" class="text-center text-secondary py-5" aria-live="polite">
        <div class="spinner-border text-info" role="status" aria-hidden="true"></div>
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
            <article class="stage-card">
              <div class="stage-card__visual" role="button" tabindex="0" @click="abrirServicio(svc)">
                <span class="stage-badge">{{ svc.categoria_slug || 'PRODUCCIÓN' }}</span>
                <img
                  v-if="svc.imagen_url"
                  :src="svc.imagen_url"
                  :alt="svc.nombre"
                  loading="lazy"
                  decoding="async"
                />
                <button type="button" class="stage-card__action-btn" @click.stop="abrirServicio(svc)">
                  <span>Ver especificaciones</span>
                  <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><path d="M5 12h14M12 5l7 7-7 7"/></svg>
                </button>
              </div>
              <div class="stage-card__meta">
                <div>
                  <span>EQUIPAMIENTO PROFESIONAL</span>
                  <h3>{{ svc.nombre }}</h3>
                </div>
              </div>
            </article>
          </FadeInUp>
        </div>
      </div>
    </div>
  </section>

  <ServicioModal ref="servicioModalRef" />
</template>

