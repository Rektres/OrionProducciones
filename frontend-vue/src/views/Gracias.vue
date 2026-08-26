<script setup lang="ts">
const numero = import.meta.env.VITE_WHATSAPP_NUMBER || '56944830378';
const whatsapp = `https://wa.me/${numero}`;
</script>

<template>
  <section class="py-5">
    <div class="container py-5 text-center" style="max-width: 640px">
      <h1 class="display-6 fw-bold">Recibimos tu solicitud</h1>
      <p class="lead text-secondary mt-3">
        Gracias por escribirnos. Revisaremos tu evento y te contactaremos en menos de 24 horas
        hábiles al correo que nos dejaste.
      </p>
      <p class="text-secondary">
        ¿Es urgente? Escríbenos directo por WhatsApp y te respondemos al tiro.
      </p>
      <div class="d-flex gap-3 justify-content-center flex-wrap mt-4">
        <a :href="whatsapp" target="_blank" rel="noopener noreferrer" class="btn btn-orion btn-lg">
          Escribir por WhatsApp
        </a>
        <RouterLink to="/portafolio" class="btn btn-outline-secondary btn-lg">Ver portafolio</RouterLink>
      </div>
    </div>
  </section>
</template>
