<script setup lang="ts">
import { onMounted, ref } from 'vue';
import { RouterLink } from 'vue-router';
import ContactForm from '@/components/ContactForm.vue';
import FadeInUp from '@/components/animations/FadeInUp.vue';
import ParticleBackground from '@/components/animations/ParticleBackground.vue';
import { serviciosService } from '@/services/servicios';
import { portafolioService } from '@/services/portafolio';
import { blogService } from '@/services/blog';
import type { Servicio, Evento, Post } from '@/types';

const servicios = ref<Servicio[]>([]);
const eventos = ref<Evento[]>([]);
const posts = ref<Post[]>([]);

const stats = [
  { n: '+150', l: 'Eventos realizados' },
  { n: '+8', l: 'Años de experiencia' },
  { n: '+80', l: 'Clientes satisfechos' },
  { n: '+20', l: 'Ciudades alcanzadas' },
];

onMounted(async () => {
  try {
    [servicios.value, eventos.value, posts.value] = await Promise.all([
      serviciosService.getServicios(),
      portafolioService.getEventos(undefined, true),
      blogService.getPosts(3),
    ]);
  } catch (e) {
    console.error('Error cargando landing:', e);
  }
});
</script>

<template>
  <section class="py-5 text-center position-relative overflow-hidden">
    <ParticleBackground />
    <div class="container py-5 position-relative" style="z-index: 1">
      <FadeInUp>
        <h1 class="display-3 fw-bold">CREAMOS EXPERIENCIAS<br /><span class="text-orion-primary">INOLVIDABLES</span></h1>
      </FadeInUp>
      <FadeInUp :delay="0.2">
        <p class="lead text-secondary mx-auto mt-3" style="max-width: 640px">
          Desde lo corporativo hasta lo más social. Orion transforma tus ideas en realidad.
        </p>
      </FadeInUp>
      <FadeInUp :delay="0.4">
        <div class="d-flex gap-3 justify-content-center mt-4">
          <RouterLink to="/portafolio" class="btn btn-orion btn-lg">Ver Portafolio</RouterLink>
          <RouterLink :to="{ path: '/', hash: '#cotizacion' }" class="btn btn-outline-light btn-lg">Cotiza tu evento</RouterLink>
        </div>
      </FadeInUp>
    </div>
  </section>

  <section class="py-5 bg-black bg-opacity-25">
    <div class="container">
      <div class="row text-center">
        <div v-for="(s, idx) in stats" :key="s.l" class="col-6 col-md-3 mb-3">
          <FadeInUp :delay="idx * 0.1">
            <div class="display-5 fw-bold text-orion-primary">{{ s.n }}</div>
            <div class="text-secondary small">{{ s.l }}</div>
          </FadeInUp>
        </div>
      </div>
    </div>
  </section>

  <section class="py-5">
    <div class="container">
      <h2 class="text-center fw-bold mb-5">LO QUE HACEMOS</h2>
      <div class="row g-4">
        <div v-for="svc in servicios.slice(0, 6)" :key="svc.id" class="col-md-6 col-lg-4">
          <div class="card h-100 bg-dark border-secondary">
            <div class="card-body">
              <span class="badge text-bg-warning mb-2">{{ svc.nombre.split(' ')[0] }}</span>
              <h5 class="card-title">{{ svc.nombre }}</h5>
              <p class="card-text text-secondary small">{{ svc.descripcion_corta }}</p>
            </div>
          </div>
        </div>
      </div>
    </div>
  </section>

  <section class="py-5 bg-black bg-opacity-25">
    <div class="container">
      <h2 class="text-center fw-bold mb-5">NUESTRO TRABAJO</h2>
      <div class="row g-4">
        <div v-for="ev in eventos.slice(0, 4)" :key="ev.id" class="col-md-6">
          <RouterLink :to="`/portafolio/${ev.slug}`" class="text-decoration-none">
            <div class="card border-0 card-cover d-flex justify-content-end"
              :style="{ backgroundImage: `url('${ev.imagen_destacada}')` }">
              <div class="p-3" style="background: linear-gradient(0deg, rgba(0,0,0,0.85), transparent)">
                <h5 class="text-white mb-0">{{ ev.nombre }}</h5>
                <small class="text-secondary">{{ ev.lugar }}</small>
              </div>
            </div>
          </RouterLink>
        </div>
      </div>
      <div class="text-center mt-4">
        <RouterLink to="/portafolio" class="btn btn-outline-light">Ver todo el portafolio</RouterLink>
      </div>
    </div>
  </section>

  <section class="py-5">
    <div class="container">
      <h2 class="text-center fw-bold mb-5">DESDE EL EQUIPO</h2>
      <div class="row g-4">
        <div v-for="p in posts" :key="p.id" class="col-md-4">
          <RouterLink :to="`/blog/${p.slug}`" class="text-decoration-none">
            <div class="card h-100 bg-dark border-secondary">
              <div class="card-cover" style="height: 12rem" :style="{ backgroundImage: `url('${p.imagen_destacada}')` }"></div>
              <div class="card-body">
                <span class="badge text-bg-danger mb-2">Blog</span>
                <h6 class="card-title">{{ p.titulo }}</h6>
                <p class="card-text text-secondary small">{{ p.extracto }}</p>
              </div>
            </div>
          </RouterLink>
        </div>
      </div>
    </div>
  </section>

  <section id="cotizacion" class="py-5 cotiza-section">
    <div class="container" style="max-width: 720px">
      <h2 class="text-center fw-bold mb-2">¿TIENES UN EVENTO EN MENTE?</h2>
      <p class="text-center text-secondary mb-4">Cuéntanos tu idea y te contactamos en menos de 24 horas</p>
      <ContactForm />
    </div>
  </section>
</template>
