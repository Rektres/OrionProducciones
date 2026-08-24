<script setup lang="ts">
import { computed, onMounted, ref } from 'vue';
import { RouterLink } from 'vue-router';
import ContactForm from '@/components/ContactForm.vue';
import ServicioModal from '@/components/ServicioModal.vue';
import GaleriaFotosModal from '@/components/GaleriaFotosModal.vue';
import FadeInUp from '@/components/animations/FadeInUp.vue';
import { serviciosService } from '@/services/servicios';
import { portafolioService } from '@/services/portafolio';
import type { Servicio, Evento, FotoEvento } from '@/types';

const servicios = ref<Servicio[]>([]);
const eventosDestacados = ref<Evento[]>([]);
const cargando = ref(true);
const filtroCategoria = ref<string>('todos');

const servicioModalRef = ref<InstanceType<typeof ServicioModal> | null>(null);
const abrirServicio = (svc: Servicio) => servicioModalRef.value?.abrir(svc);
const galeriaModalRef = ref<InstanceType<typeof GaleriaFotosModal> | null>(null);

// Categorías dinámicas para los Filter Chips
const categorias = computed(() => {
  const cats = new Set<string>();
  servicios.value.forEach(s => {
    if (s.categoria_slug) cats.add(s.categoria_slug);
    else if (s.nombre) cats.add(s.nombre.split(' ')[0].toLowerCase());
  });
  return ['todos', ...Array.from(cats)];
});

const serviciosFiltrados = computed(() => {
  if (filtroCategoria.value === 'todos') return servicios.value;
  return servicios.value.filter(s => 
    s.categoria_slug === filtroCategoria.value ||
    s.nombre.toLowerCase().includes(filtroCategoria.value)
  );
});

// Servicio destacado para la tarjeta flotante del Hero
const servicioHero = computed(() => {
  return servicios.value[0] || null;
});

// Galeria de fotos de eventos: mosaico dinámico
interface FotoGaleria extends Omit<FotoEvento, 'imagen_url'> {
  imagen_url: string;
  eventoNombre: string;
}
const fotosGaleria = ref<FotoGaleria[]>([]);
const TAMANOS_MOSAICO = ['', 'tam-ancho', 'tam-alto', '', 'tam-grande', '', 'tam-alto', 'tam-ancho', '', '', 'tam-ancho', 'tam-alto'];
const tamanoMosaico = (idx: number) => TAMANOS_MOSAICO[idx % TAMANOS_MOSAICO.length];
const abrirGaleria = (idx: number) => galeriaModalRef.value?.abrir(fotosGaleria.value, idx);

const stats = [
  { n: '100%', l: 'COBERTURA NACIONAL' },
  { n: 'LINE-ARRAY', l: 'AUDIO DE ALTA POTENCIA' },
  { n: 'ROBÓTICA', l: 'ILUMINACIÓN DMX & LÁSER' },
  { n: '360°', l: 'DIRECCIÓN TÉCNICA' },
];

const paths = [
  {
    index: '01 / CORPORATIVO & MARCAS',
    kicker: 'PRODUCCIÓN EJECUTIVA',
    title: 'Lanzamientos,<br>Galas & Congresos.',
    desc: 'Escenografía a medida, pantallas LED de alta definición, microfonía inalámbrica y streaming en directo con estándar broadcast.',
    cta: 'Cotizar Corporativo',
    theme: 'path-card--1'
  },
  {
    index: '02 / FESTIVALES & CONCIERTOS',
    kicker: 'GRAN ESCALA',
    title: 'Potencia sonora<br>& Efectos Visuales.',
    desc: 'Sistemas Line Array de alto rendimiento, estructuras Layher y Truss certificadas, show de luces robóticas y mapping visual.',
    cta: 'Cotizar Festival',
    theme: 'path-card--2'
  },
  {
    index: '03 / PRIVADOS & BODAS',
    kicker: 'EXPERIENCIA BOUTIQUE',
    title: 'Momentos únicos,<br>atmósferas mágicas.',
    desc: 'Iluminación ambiental arquitectónica, pista de baile interactiva, audio envolvente y personalización escénica total.',
    cta: 'Cotizar Privado',
    theme: 'path-card--3'
  }
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
  } catch (e) {
    console.error('Error cargando landing:', e);
  } finally {
    cargando.value = false;
  }
});
</script>

<template>
  <!-- HERO SECTION ESTILO ARCADIA -->
  <section class="hero-stage">
    <div class="hero__veil"></div>
    <div class="hero__glow hero__glow--violet"></div>
    <div class="hero__glow hero__glow--cyan"></div>

    <div class="container position-relative" style="z-index: 2;">
      <div class="row align-items-center g-5">
        <div class="col-lg-7">
          <FadeInUp>
            <p class="eyebrow"><span></span> UNA NUEVA ERA EN EVENTOS & ESCENARIOS</p>
            <h1 class="hero-title-giant">
              <span>EL ESCENARIO DE</span><br />
              <span>TU PRÓXIMO EVENTO</span><br />
              <em>EMPIEZA AQUÍ.</em>
            </h1>
            <p class="lead text-secondary mt-3 mb-4" style="max-width: 580px; font-size: 16px; line-height: 1.7;">
              Ingeniería de sonido, iluminación escénica robótica, estructuras de escenario y dirección técnica integral en Chile. Creamos experiencias que dejan huella.
            </p>
            <div class="d-flex flex-wrap gap-3">
              <a href="#catalogo" class="btn btn-orion px-4 py-2 d-inline-flex align-items-center gap-2">
                <span>Explorar Catálogo</span>
                <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><path d="M5 12h14M12 5l7 7-7 7"/></svg>
              </a>
              <RouterLink :to="{ path: '/', hash: '#cotizacion' }" class="btn btn-outline-light px-4 py-2">
                Cotizar Proyecto
              </RouterLink>
            </div>
            <ul class="hero-facts-list">
              <li v-for="st in stats" :key="st.l">
                <strong>{{ st.n }}</strong>
                <span>{{ st.l }}</span>
              </li>
            </ul>
          </FadeInUp>
        </div>

        <div class="col-lg-5 d-none d-lg-flex justify-content-end">
          <FadeInUp :delay="0.3">
            <aside v-if="servicioHero" class="hero-feature">
              <div class="hero-feature__top">
                <span class="live-dot"></span>
                <span>DESTACADO ORION</span>
                <span class="ms-auto" style="color: rgba(255,255,255,0.4);">01 / 04</span>
              </div>
              <img
                :src="servicioHero.imagen_url || '/logo.png'"
                :alt="servicioHero.nombre"
                class="hero-feature__img"
              />
              <div class="hero-feature__body">
                <div>
                  <span class="feature-kicker">{{ servicioHero.categoria_slug || 'PRODUCCIÓN TÉCNICA' }}</span>
                  <h3>{{ servicioHero.nombre }}</h3>
                </div>
                <button
                  type="button"
                  class="round-action"
                  aria-label="Ver detalles"
                  @click="abrirServicio(servicioHero)"
                >
                  <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><path d="M1 12s4-8 11-8 11 8 11 8-4 8-11 8-11-8-11-8z"/><circle cx="12" cy="12" r="3"/></svg>
                </button>
              </div>
            </aside>
          </FadeInUp>
        </div>
      </div>
    </div>
  </section>

  <!-- CATÁLOGO DE SERVICIOS CON FILTER CHIPS -->
  <section id="catalogo" class="py-5">
    <div class="container">
      <div class="row align-items-end g-4 mb-2">
        <div class="col-lg-7">
          <p class="eyebrow"><span></span> EQUIPAMIENTO Y SOLUCIONES</p>
          <h2 class="display-5 fw-bold mb-0">Tecnología de Escenario de Vanguardia.</h2>
        </div>
        <div class="col-lg-5">
          <p class="text-secondary mb-0" style="font-size: 14px; line-height: 1.7;">
            Una gama completa de servicios modulares listos para desplegar en conciertos, conferencias, eventos corporativos y bodas en todo el territorio nacional.
          </p>
        </div>
      </div>

      <!-- Barra de Filtros Chips -->
      <div class="catalog-toolbar">
        <div class="filter-chips">
          <button
            v-for="cat in categorias"
            :key="cat"
            type="button"
            class="filter-chip"
            :class="{ 'is-active': filtroCategoria === cat }"
            @click="filtroCategoria = cat"
          >
            {{ cat.charAt(0).toUpperCase() + cat.slice(1) }}
          </button>
        </div>
        <span class="catalog-count">
          <strong>{{ serviciosFiltrados.length }}</strong> SERVICIOS
        </span>
      </div>

      <!-- Grid de Servicios -->
      <div v-if="cargando" class="text-center py-5">
        <div class="spinner-border text-info" role="status"></div>
        <p class="text-secondary mt-3">Cargando catálogo técnico...</p>
      </div>
      <div v-else-if="serviciosFiltrados.length" class="row g-4">
        <div
          v-for="svc in serviciosFiltrados"
          :key="svc.id"
          class="col-md-6 col-lg-4"
        >
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
        </div>
      </div>
      <div v-else class="text-center py-5 text-secondary">
        No se encontraron servicios para la categoría seleccionada.
      </div>
    </div>
  </section>

  <!-- SECCIÓN MANIFIESTO ORION CON ORBE HOLOGRÁFICO -->
  <section class="py-4">
    <div class="container">
      <div class="manifesto">
        <div class="manifesto__index">ORION / 01</div>
        <div class="manifesto__content">
          <p class="eyebrow"><span></span> NUESTRA VISIÓN</p>
          <h2>Potencia Sonora.<br>Impacto Visual Inolvidable.</h2>
          <p>
            En Orion Stage fusionamos la precisión técnica del audio profesional con el arte de la iluminación arquitectónica y robótica. Cada evento es diseñado como un espectáculo único.
          </p>
          <RouterLink :to="{ path: '/', hash: '#cotizacion' }" class="btn btn-outline-light px-4 py-2 d-inline-flex align-items-center gap-2">
            <span>Conversar con un Ingeniero</span>
            <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><path d="M5 12h14M12 5l7 7-7 7"/></svg>
          </RouterLink>
        </div>
        <div class="manifesto__orb" aria-hidden="true">
          <span></span>
        </div>
      </div>
    </div>
  </section>

  <!-- PLATFORM PATHS: RECORRIDOS POR TIPO DE EVENTO -->
  <section class="py-5">
    <div class="container">
      <div class="row align-items-end g-4 mb-4">
        <div class="col-lg-7">
          <p class="eyebrow"><span></span> SOLUCIONES A TU MEDIDA</p>
          <h2 class="display-5 fw-bold mb-0">Cada Escenario Tiene su Identidad.</h2>
        </div>
        <div class="col-lg-5">
          <p class="text-secondary mb-0" style="font-size: 14px; line-height: 1.7;">
            Diseñamos paquetes llave en mano adaptados al tamaño de la audiencia, la acústica del recinto y los objetivos de tu producción.
          </p>
        </div>
      </div>

      <div class="platform-path-grid">
        <article
          v-for="p in paths"
          :key="p.index"
          class="path-card"
          :class="p.theme"
        >
          <span class="path-card__index">{{ p.index }}</span>
          <strong>{{ p.kicker }}</strong>
          <h3 v-html="p.title"></h3>
          <p>{{ p.desc }}</p>
          <RouterLink :to="{ path: '/', hash: '#cotizacion' }" class="path-card__cta">
            <span>{{ p.cta }}</span>
            <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><path d="M5 12h14M12 5l7 7-7 7"/></svg>
          </RouterLink>
        </article>
      </div>
    </div>
  </section>

  <!-- GALERÍA MOSAICO DE EVENTOS REALES -->
  <section v-if="fotosGaleria.length" class="py-5">
    <div class="container galeria-home-container">
      <div class="text-center mb-5">
        <p class="eyebrow justify-content-center"><span></span> PORTAFOLIO EN ACCIÓN</p>
        <h2 class="display-5 fw-bold">Momentos en Vivo</h2>
        <p class="text-secondary small mt-2">Fotografías reales capturadas en eventos producidos por Orion Stage</p>
      </div>

      <div class="galeria-mosaico">
        <div
          v-for="(f, idx) in fotosGaleria"
          :key="f.id"
          class="galeria-item"
          :class="tamanoMosaico(idx)"
          role="button"
          tabindex="0"
          @click="abrirGaleria(idx)"
          @keydown.enter="abrirGaleria(idx)"
        >
          <div class="galeria-item-img">
            <img
              :src="f.imagen_url"
              :alt="`Foto de ${f.eventoNombre}`"
              class="img-cover"
              loading="lazy"
              decoding="async"
            />
          </div>
          <div class="galeria-item-leyenda">{{ f.eventoNombre }}</div>
        </div>
      </div>
    </div>
  </section>

  <!-- FORMULARIO DE COTIZACIÓN -->
  <section id="cotizacion" class="py-5 cotiza-section">
    <div class="container" style="max-width: 780px">
      <div class="cotiza-box">
        <div class="text-center mb-4">
          <p class="eyebrow justify-content-center"><span></span> COTIZACIÓN SIN COMPROMISO</p>
          <h2 class="display-5 fw-bold mb-2">¿Tienes un Evento en Mente?</h2>
          <p class="text-secondary">Cuéntanos sobre tu fecha, recinto y requerimientos. Te responderemos en menos de 24 horas.</p>
        </div>
        <ContactForm />
      </div>
    </div>
  </section>

  <ServicioModal ref="servicioModalRef" />
  <GaleriaFotosModal ref="galeriaModalRef" />
</template>

