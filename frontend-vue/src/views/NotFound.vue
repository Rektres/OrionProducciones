<script setup lang="ts">
</script>

<template>
  <section class="py-5">
    <div class="container py-5 text-center" style="max-width: 640px">
      <p class="display-1 fw-bold text-orion-primary mb-0">404</p>
      <h1 class="h3 fw-bold mt-3">Esta página no existe</h1>
      <p class="text-secondary mt-3">
        El enlace que seguiste puede estar roto o la página pudo haber sido movida.
      </p>
      <div class="d-flex gap-3 justify-content-center flex-wrap mt-4">
        <RouterLink to="/" class="btn btn-orion btn-lg">Volver al inicio</RouterLink>
        <RouterLink to="/portafolio" class="btn btn-outline-light btn-lg">Ver portafolio</RouterLink>
      </div>
    </div>
  </section>
</template>
