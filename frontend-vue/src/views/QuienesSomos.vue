<script setup lang="ts">
import ParticleBackground from '@/components/animations/ParticleBackground.vue';

const equipo = [
  { rol: 'Dirección Creativa', descripcion: 'Da forma al concepto y la estética de cada evento, de principio a fin.' },
  { rol: 'Producción y Logística', descripcion: 'Coordina proveedores, montaje y cronograma para que todo funcione a tiempo.' },
  { rol: 'Atención a Clientes', descripcion: 'Acompaña a cada cliente desde la primera cotización hasta el cierre del evento.' },
  { rol: 'Diseño y Experiencia', descripcion: 'Diseña la ambientación, escenografía y experiencia sensorial del evento.' },
];
</script>

<template>
  <section class="py-5 text-center position-relative overflow-hidden">
    <ParticleBackground />
    <div class="container position-relative" style="z-index: 1">
      <h1 class="display-4 fw-bold">QUIÉNES SOMOS</h1>
      <p class="text-secondary">El equipo detrás de cada evento que creamos</p>
    </div>
  </section>

  <section class="py-4">
    <div class="container" style="max-width: 820px">
      <p class="text-secondary">
        Orion es una productora de eventos chilena dedicada a transformar ideas en experiencias
        memorables, desde celebraciones corporativas hasta encuentros sociales y festivales.
        Combinamos planificación, diseño y logística para que cada detalle funcione, del
        concepto inicial al último invitado.
      </p>
    </div>
  </section>

  <section class="py-4">
    <div class="container">
      <h2 class="text-center fw-bold mb-5">NUESTRO EQUIPO</h2>
      <div class="row g-4">
        <div v-for="m in equipo" :key="m.rol" class="col-sm-6 col-lg-3">
          <div class="card h-100 bg-dark border-secondary text-center p-3">
            <div class="rounded-circle mx-auto mb-3 d-flex align-items-center justify-content-center"
              style="width: 4rem; height: 4rem; background: linear-gradient(135deg, var(--orion-primary), var(--orion-secondary))">
            </div>
            <h6 class="card-title">{{ m.rol }}</h6>
            <p class="card-text text-secondary small">{{ m.descripcion }}</p>
          </div>
        </div>
      </div>
    </div>
  </section>
</template>
