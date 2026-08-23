<script setup lang="ts">
import { computed, onBeforeUnmount, onMounted, ref } from 'vue';
import { RouterLink } from 'vue-router';
import ContactForm from '@/components/ContactForm.vue';
import ServicioModal from '@/components/ServicioModal.vue';
import FadeInUp from '@/components/animations/FadeInUp.vue';
import ParticleBackground from '@/components/animations/ParticleBackground.vue';
import { useReducedMotion } from '@/composables/useReducedMotion';
import { serviciosService } from '@/services/servicios';
import { portafolioService } from '@/services/portafolio';
import type { Servicio, Evento, FotoEvento } from '@/types';

const servicios = ref<Servicio[]>([]);
const eventosDestacados = ref<Evento[]>([]);
const cargando = ref(true);

const servicioModalRef = ref<InstanceType<typeof ServicioModal> | null>(null);
const abrirServicio = (svc: Servicio) => servicioModalRef.value?.abrir(svc);

const prefersReducedMotion = useReducedMotion();

// Carrusel de servicios: ventana de N items visibles calculada por indice
// (modulo), sin duplicar el arreglo — evita que un mismo servicio aparezca
// repetido en pantalla. Avanzar mueve el indice +1; al pasar el ultimo
// vuelve a 0 (el "final a la izquierda reaparece a la derecha").
const SERVICIOS_VISIBLES = 3;
const servicioInicio = ref(0);
let servicioAutoTimer: ReturnType<typeof setInterval> | undefined;

const serviciosVisibles = computed(() => {
  const total = servicios.value.length;
  if (!total) return [];
  const n = Math.min(SERVICIOS_VISIBLES, total);
  return Array.from({ length: n }, (_, i) => servicios.value[(servicioInicio.value + i) % total]);
});

const servicioSiguiente = () => {
  if (!servicios.value.length) return;
  servicioInicio.value = (servicioInicio.value + 1) % servicios.value.length;
};
const servicioAnterior = () => {
  if (!servicios.value.length) return;
  servicioInicio.value = (servicioInicio.value - 1 + servicios.value.length) % servicios.value.length;
};

const detenerAutoServicios = () => {
  if (servicioAutoTimer) {
    clearInterval(servicioAutoTimer);
    servicioAutoTimer = undefined;
  }
};
const iniciarAutoServicios = () => {
  detenerAutoServicios();
  if (prefersReducedMotion.value || servicios.value.length <= 1) return;
  servicioAutoTimer = setInterval(servicioSiguiente, 5000);
};
const avanzarManual = (fn: () => void) => {
  fn();
  iniciarAutoServicios();
};

// Empresas "que confian en nosotros" — placeholder por ahora, reemplazar
// por logos reales (misma clase .empresa-logo funciona igual con <img>).
const empresasConfianza = [
  { nombre: 'Aurora Corp', color: '#e63946' },
  { nombre: 'Nimbus Group', color: '#2a9d8f' },
  { nombre: 'Vértice SA', color: '#e9c46a' },
  { nombre: 'Solaris Ltda', color: '#f4a261' },
  { nombre: 'Prisma Eventos', color: '#457b9d' },
  { nombre: 'Zenith Co', color: '#8338ec' },
];

// Galeria de fotos de eventos: mosaico aleatorio con tamaños variados.
// Al armar el pool solo entran fotos con imagen, asi que aqui imagen_url nunca es null.
interface FotoGaleria extends Omit<FotoEvento, 'imagen_url'> {
  imagen_url: string;
  eventoNombre: string;
}
const fotosGaleria = ref<FotoGaleria[]>([]);
const fotoGaleriaActiva = ref<string | null>(null);
const TAMANOS_MOSAICO = ['', 'tam-ancho', 'tam-alto', '', 'tam-grande', '', 'tam-alto', 'tam-ancho', '', '', 'tam-ancho', 'tam-alto'];
const tamanoMosaico = (idx: number) => TAMANOS_MOSAICO[idx % TAMANOS_MOSAICO.length];

const stats = [
  { n: '+150', l: 'Eventos realizados' },
  { n: '+8', l: 'Años de experiencia' },
  { n: '+80', l: 'Clientes satisfechos' },
  { n: '+20', l: 'Ciudades alcanzadas' },
];

onMounted(async () => {
  try {
    const [todosServicios, todosEventos] = await Promise.all([
      serviciosService.getServicios(),
      portafolioService.getEventos(),
    ]);
    servicios.value = todosServicios;
    eventosDestacados.value = todosEventos.filter((e) => e.destacado).slice(0, 4);

    const pool: FotoGaleria[] = [];
    for (const ev of todosEventos) {
      for (const f of ev.fotos ?? []) {
        if (f.imagen_url) pool.push({ ...f, imagen_url: f.imagen_url, eventoNombre: ev.nombre });
      }
    }
    for (let i = pool.length - 1; i > 0; i--) {
      const j = Math.floor(Math.random() * (i + 1));
      [pool[i], pool[j]] = [pool[j], pool[i]];
    }
    fotosGaleria.value = pool.slice(0, 16);

    iniciarAutoServicios();
  } catch (e) {
    console.error('Error cargando landing:', e);
  } finally {
    cargando.value = false;
  }
});

onBeforeUnmount(detenerAutoServicios);
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

  <section class="py-5 section-alt">
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

  <section class="py-4">
    <div class="container">
      <p class="text-center text-secondary small text-uppercase mb-4">Confían en nosotros</p>
      <div class="d-flex flex-wrap justify-content-center align-items-center gap-4 gap-md-5">
        <div v-for="e in empresasConfianza" :key="e.nombre" class="empresa-logo" :style="{ color: e.color }">
          {{ e.nombre }}
        </div>
      </div>
    </div>
  </section>

  <section class="py-5 overflow-hidden">
    <div class="container">
      <h2 class="text-center fw-bold mb-5">LO QUE HACEMOS</h2>
      <div v-if="cargando" class="text-center text-secondary py-4" aria-live="polite">
        <div class="spinner-border text-orion-primary" role="status" aria-hidden="true"></div>
        <p class="mt-3 mb-0">Cargando servicios...</p>
      </div>
      <div v-else-if="servicios.length" class="d-flex align-items-center justify-content-center gap-2"
        @mouseenter="detenerAutoServicios" @mouseleave="iniciarAutoServicios">
        <button v-if="servicios.length > 1" type="button" class="carousel-arrow-ghost flex-shrink-0"
          aria-label="Servicio anterior" @click="avanzarManual(servicioAnterior)">‹</button>
        <div class="servicios-carousel-viewport">
          <TransitionGroup name="servicio-slide" tag="div" class="d-flex gap-3 justify-content-center">
            <div v-for="svc in serviciosVisibles" :key="svc.id" class="servicio-carousel-item">
              <div class="card bg-dark border-secondary hover-scale" style="width: 15rem; cursor: pointer"
                @click="abrirServicio(svc)">
                <div class="card-cover rounded-top overflow-hidden" style="height: 10rem">
                  <img v-if="svc.imagen_url" :src="svc.imagen_url" :alt="`Servicio de ${svc.nombre}`"
                    class="img-cover" loading="lazy" decoding="async" />
                </div>
                <div class="card-body text-center">
                  <span class="badge text-bg-warning mb-2">{{ svc.nombre.split(' ')[0] }}</span>
                  <h6 class="card-title mb-0">{{ svc.nombre }}</h6>
                </div>
              </div>
            </div>
          </TransitionGroup>
        </div>
        <button v-if="servicios.length > 1" type="button" class="carousel-arrow-ghost flex-shrink-0"
          aria-label="Servicio siguiente" @click="avanzarManual(servicioSiguiente)">›</button>
      </div>
    </div>
  </section>

  <section class="py-5 section-alt">
    <div class="container">
      <h2 class="text-center fw-bold mb-5">NUESTRO TRABAJO</h2>
      <div v-if="cargando" class="text-center text-secondary py-4" aria-live="polite">
        <div class="spinner-border text-orion-primary" role="status" aria-hidden="true"></div>
        <p class="mt-3 mb-0">Cargando eventos...</p>
      </div>
      <div v-else class="row g-4">
        <div v-for="ev in eventosDestacados" :key="ev.id" class="col-md-6">
          <RouterLink :to="`/portafolio/${ev.slug}`" class="text-decoration-none">
            <div class="card border-0 card-cover d-flex justify-content-end position-relative overflow-hidden">
              <img v-if="ev.imagen_url" :src="ev.imagen_url"
                :alt="`${ev.nombre} — evento producido por Orion en ${ev.lugar}`"
                class="img-cover position-absolute top-0 start-0" loading="lazy" decoding="async" />
              <div class="p-3 position-relative" style="background: linear-gradient(0deg, rgba(0,0,0,0.85), transparent)">
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

  <section v-if="fotosGaleria.length" class="py-5 section-alt">
    <div class="container">
      <h2 class="text-center fw-bold mb-5">MOMENTOS QUE CREAMOS</h2>
      <div class="galeria-mosaico">
        <div v-for="(f, idx) in fotosGaleria" :key="f.id"
          class="galeria-item" :class="[tamanoMosaico(idx), { 'galeria-item-activa': fotoGaleriaActiva === f.id }]"
          @click="fotoGaleriaActiva = fotoGaleriaActiva === f.id ? null : f.id">
          <div class="galeria-item-img">
            <img :src="f.imagen_url" :alt="`Foto del evento ${f.eventoNombre}`" class="img-cover"
              loading="lazy" decoding="async" />
          </div>
          <div class="galeria-item-leyenda">{{ f.eventoNombre }}</div>
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

  <ServicioModal ref="servicioModalRef" />
</template>
