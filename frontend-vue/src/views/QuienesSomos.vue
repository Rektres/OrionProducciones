<script setup lang="ts">
import { ref } from 'vue';
import { RouterLink } from 'vue-router';
import FadeInUp from '@/components/animations/FadeInUp.vue';

interface CampanaInfo {
  id: string;
  mundo: string;
  titulo: string;
  subtitulo: string;
  descripcion: string;
  poster: string;
  badge: string;
  tagColor: string;
}

const campanas: CampanaInfo[] = [
  {
    id: 'women',
    mundo: 'ORIÓN WOMEN',
    titulo: 'Confianza en Ti',
    subtitulo: 'Experiencias de Bienestar & Autocuidado Femenino',
    descripcion:
      'Crea experiencias de bienestar especialmente pensadas para las mujeres de las organizaciones, integrando iniciativas como maquillaje y automaquillaje, nutrición, movimiento, autocuidado, imagen, liderazgo y desarrollo personal.',
    poster: '/campanas/confianza-en-ti.png',
    badge: 'Bienestar & Liderazgo',
    tagColor: '#ec4899',
  },
  {
    id: 'sports-padel',
    mundo: 'ORIÓN SPORTS',
    titulo: 'Campeonato de Pádel Hombres',
    subtitulo: 'Torneo Inter-Empresas & Clima Laboral',
    descripcion:
      'Utiliza el deporte como punto de encuentro a través de torneos de pádel corporativos que promueven la integración, el trabajo en equipo, la vida saludable y la camaradería entre colaboradores.',
    poster: '/campanas/campeonato-padel.png',
    badge: 'Deporte & Integración',
    tagColor: '#13d6ea',
  },
  {
    id: 'sports-futbol',
    mundo: 'ORIÓN SPORTS',
    titulo: 'Futbolito Empresas',
    subtitulo: 'Torneos & Copas Corporativas',
    descripcion:
      'Ligas y campeonatos de fútbol 7 con arbitraje oficial, transmisión en vivo, premiaciones y ambientación técnica para fortalecer el espíritu de equipo y la pertenencia organizacional.',
    poster: '/campanas/futbolito-empresas.png',
    badge: 'Trabajo en Equipo',
    tagColor: '#34d399',
  },
  {
    id: 'family',
    mundo: 'ORIÓN FAMILY',
    titulo: 'Escuelas de Verano en Fantasilandia',
    subtitulo: 'Experiencias para Hijos & Familias',
    descripcion:
      'Acerca la empresa a las familias de sus colaboradores mediante experiencias especialmente diseñadas para sus hijos, combinando diversión, talleres formativos y actividades recreativas inolvidables.',
    poster: '/campanas/escuelas-de-verano.png',
    badge: 'Familia & Niñez',
    tagColor: '#f59e0b',
  },
  {
    id: 'celebrations',
    mundo: 'ORIÓN CELEBRATIONS',
    titulo: 'Fiesta de Fin de Año',
    subtitulo: 'Galas, Aniversarios & Hitos Corporativos',
    descripcion:
      'Transforma celebraciones corporativas, aniversarios y encuentros de cierre de año en momentos mágicos para reconocer, agradecer los logros alcanzados y reencontrarse como equipo con estándar de festival.',
    poster: '/campanas/fiesta-fin-de-ano.png',
    badge: 'Celebración & Reconocimiento',
    tagColor: '#d06c26',
  },
];

const modalCampana = ref<CampanaInfo | null>(null);
const abrirModal = (c: CampanaInfo) => {
  modalCampana.value = c;
};
const cerrarModal = () => {
  modalCampana.value = null;
};

const propositos = [
  {
    tag: 'CULTURA ORGANIZACIONAL',
    titulo: 'Construir Cultura',
    desc: 'Los mejores eventos no son aquellos que simplemente ocurren, sino aquellos que las personas recuerdan y refuerzan la identidad de la organización.',
  },
  {
    tag: 'INTEGRACIÓN & EQUIPO',
    titulo: 'Fortalecer Vínculos',
    desc: 'Espacios reales para encontrarse, compartir, competir sanamente y derribar las barreras del día a día laboral.',
  },
  {
    tag: 'SENTIDO DE COMUNIDAD',
    titulo: 'Generar Pertenencia',
    desc: 'Demostrar a los colaboradores y a sus familias que son el corazón y la prioridad de la empresa.',
  },
  {
    tag: 'HUELLA EMOCIONAL',
    titulo: 'Crear Recuerdos',
    desc: 'Momentos únicos y significativos que permanecen grabados mucho después de concluido el evento.',
  },
];

interface MiembroEquipo {
  nombre: string;
  genero: 'mujer' | 'hombre';
  cargo: string;
  descripcion: string;
  badge: string;
  avatarGrad: string;
  iniciales: string;
}

const equipoPrincipal: MiembroEquipo[] = [
  {
    nombre: 'Erika Torres',
    genero: 'mujer',
    cargo: 'Dirección de Experiencias & Gestión de Clientes',
    descripcion: 'Lidera el diseño conceptual de cada experiencia, el bienestar corporativo y el acompañamiento cercano a cada organización de principio a fin.',
    badge: 'Producción Ejecutiva',
    avatarGrad: 'linear-gradient(135deg, #ec4899 0%, #d06c26 100%)',
    iniciales: 'ET',
  },
  {
    nombre: 'Carlos Plaza',
    genero: 'hombre',
    cargo: 'Dirección Técnica & Operaciones Escénicas',
    descripcion: 'Especialista en ingeniería acústica Line Array, diseño lumínico robótico, pantallas LED 4K y montaje estructural de estándar internacional.',
    badge: 'Ingeniería Técnica',
    avatarGrad: 'linear-gradient(135deg, #13d6ea 0%, #0d537d 100%)',
    iniciales: 'CP',
  },
  {
    nombre: 'Francisco',
    genero: 'hombre',
    cargo: 'Dirección General & Producción 360°',
    descripcion: 'Coordina la logística integral, recintos, alianzas estratégicas, proveedores y regiduría en terreno para que cada evento funcione a la perfección.',
    badge: 'Producción 360°',
    avatarGrad: 'linear-gradient(135deg, #c5a880 0%, #d06c26 100%)',
    iniciales: 'F',
  },
];

const pilaresProduccion = [
  'Planificación estratégica y cronograma',
  'Espacios, recintos y locaciones premium',
  'Ingeniería acústica Line Array & microfonía',
  'Iluminación robótica, láser y pantallas LED 4K',
  'Escenarios, tarimas y estructuras certificadas',
  'Ambientación, escenografía y mobiliario lounge',
  'Catering, barras gourmet y coctelería',
  'Artistas, bandas en vivo, DJs y animadores',
  'Fotografía profesional, video & aftermovies',
  'Regiduría, staff técnico y coordinación en vivo',
];
</script>

<template>
  <!-- HERO NOSOTROS -->
  <section class="hero-fusion text-center position-relative overflow-hidden">
    <div class="hero__veil"></div>
    <div class="hero__glow hero__glow--gold"></div>
    <div class="hero__glow hero__glow--cyan"></div>

    <div class="container position-relative py-2" style="z-index: 2">
      <FadeInUp>
        <div class="eyebrow-luxury justify-content-center mb-3">
          <span>★</span> NUESTRO PROPÓSITO & FILOSOFÍA
        </div>
        <h1 class="display-4 fw-bold hero-title-giant mb-3">
          <span>NO ORGANIZAMOS SOLO EVENTOS.</span><br />
          <span class="highlight-gold">CREAMOS EXPERIENCIAS</span><br />
          <em>QUE CONECTAN PERSONAS.</em>
        </h1>
        <p class="lead text-secondary mx-auto mb-4" style="max-width: 780px; font-size: 16.5px; line-height: 1.8;">
          Orión Stage nace de una convicción simple: los mejores eventos no son aquellos que simplemente ocurren, sino aquellos que las personas recuerdan. Nacemos para transformar una actividad corporativa en una experiencia capaz de <strong>conectar, emocionar, integrar y dejar huella</strong>.
        </p>
        <div class="d-flex flex-wrap justify-content-center gap-3">
          <RouterLink :to="{ path: '/', hash: '#cotizacion' }" class="btn btn-orion d-inline-flex align-items-center gap-2">
            <span>Cotizar mi Experiencia</span>
            <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><path d="M5 12h14M12 5l7 7-7 7"/></svg>
          </RouterLink>
          <a href="#mundos" class="btn-glass">
            <span>Explorar Mundos de Experiencia</span>
            <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M19 9l-7 7-7-7"/></svg>
          </a>
        </div>
      </FadeInUp>
    </div>
  </section>

  <!-- ¿POR QUÉ NACE ORIÓN STAGE? -->
  <section class="py-5">
    <div class="container" style="max-width: 960px">
      <div class="row align-items-center g-5">
        <div class="col-lg-12">
          <div class="eyebrow-luxury mb-2">
            <span>★</span> ¿POR QUÉ NACE ORIÓN STAGE?
          </div>
          <h2 class="display-5 fw-bold mb-4">Nacemos para hacer las cosas de una manera diferente.</h2>
          
          <div class="text-secondary" style="font-size: 15.5px; line-height: 1.8;">
            <p>
              Entendemos que detrás de cada empresa existen personas. Personas que trabajan juntas, enfrentan desafíos, construyen resultados, celebran logros y necesitan también espacios para encontrarse, compartir, disfrutar y sentirse parte de algo.
            </p>
            <p>
              Por eso, <strong>Orión Stage fue concebida como mucho más que una productora de eventos</strong>. Somos una empresa dedicada a diseñar, producir y ejecutar experiencias corporativas de principio a fin, combinando creatividad, planificación, producción, entretención, bienestar y una cuidadosa gestión de cada detalle.
            </p>
            <p>
              Nuestra propuesta parte escuchando a cada organización: queremos comprender su cultura, sus personas y el objetivo que existe detrás de cada actividad para convertir una idea en una experiencia especialmente diseñada para ellas.
            </p>
          </div>
        </div>
      </div>
    </div>
  </section>

  <!-- LOS 4 MUNDOS DE EXPERIENCIAS CORPORATIVAS & CAMPAÑAS -->
  <section id="mundos" class="py-5" style="background: var(--section-alt-bg);">
    <div class="container">
      <div class="text-center max-w-700 mx-auto mb-5">
        <div class="eyebrow-luxury justify-content-center">
          <span>★</span> LÍNEAS DE EXPERIENCIAS
        </div>
        <h2 class="display-5 fw-bold mt-2">Mundos de Experiencia Orión Stage</h2>
        <p class="text-secondary mt-2" style="font-size: 15px;">
          Propuestas especializadas para acompañar a las organizaciones en los momentos clave de su vida corporativa durante todo el año.
        </p>
      </div>

      <div class="row g-4">
        <div v-for="c in campanas" :key="c.id" class="col-md-6 col-lg-4">
          <article class="campana-card">
            <div class="campana-card__poster" role="button" tabindex="0" @click="abrirModal(c)">
              <img :src="c.poster" :alt="c.titulo" loading="lazy" decoding="async" />
              <div class="campana-card__overlay">
                <span class="campana-card__badge" :style="{ color: c.tagColor, borderColor: c.tagColor }">
                  {{ c.mundo }}
                </span>
                <h3 class="text-white h5 mb-0 fw-bold">{{ c.titulo }}</h3>
              </div>
            </div>
            <div class="campana-card__body">
              <span class="small fw-bold text-uppercase text-secondary mb-1" style="font-size: 11px;">
                {{ c.subtitulo }}
              </span>
              <p class="campana-card__desc">
                {{ c.descripcion }}
              </p>
              <div class="campana-card__action">
                <button type="button" class="btn btn-sm btn-outline-secondary rounded-pill px-3" @click="abrirModal(c)">
                  Ver Campaña
                </button>
                <RouterLink :to="{ path: '/', hash: '#cotizacion' }" class="btn btn-sm btn-orion">
                  Cotizar
                </RouterLink>
              </div>
            </div>
          </article>
        </div>
      </div>
    </div>
  </section>

  <!-- BLOQUE EQUIPO PRINCIPAL (ERIKA TORRES, CARLOS PLAZA, FRANCISCO) -->
  <section class="py-5">
    <div class="container">
      <div class="text-center max-w-700 mx-auto mb-5">
        <div class="eyebrow-luxury justify-content-center">
          <span>★</span> NUESTRO EQUIPO
        </div>
        <h2 class="display-5 fw-bold mt-2">El Equipo Detrás de Cada Escenario</h2>
        <p class="text-secondary mt-2" style="font-size: 15px;">
          Profesionales apasionados por el detalle, la ingeniería escénica y la gestión humana para transformar cada evento en una experiencia inolvidable.
        </p>
      </div>

      <div class="row g-4 justify-content-center">
        <div v-for="m in equipoPrincipal" :key="m.nombre" class="col-md-6 col-lg-4">
          <article class="card h-100 p-4 border-1 rounded-4 text-center position-relative overflow-hidden"
            style="background: var(--card-surface); border-color: var(--card-border); box-shadow: var(--orion-surface-shadow);">
            
            <!-- Avatar Iniciales / Gradiante -->
            <div class="rounded-circle mx-auto mb-3 d-flex align-items-center justify-content-center text-white shadow-lg"
              :style="{ width: '5.2rem', height: '5.2rem', background: m.avatarGrad, fontSize: '1.4rem', fontWeight: '800', letterSpacing: '-0.02em' }">
              {{ m.iniciales }}
            </div>

            <span class="badge rounded-pill mb-2 px-3 py-1 text-uppercase mx-auto"
              style="font-size: 10px; letter-spacing: 0.08em; background: rgba(19, 214, 234, 0.12); color: var(--orion-primary); border: 1px solid rgba(19, 214, 234, 0.3);">
              {{ m.badge }}
            </span>

            <h3 class="h4 fw-bold mb-1 text-body">{{ m.nombre }}</h3>
            <span class="small fw-bold text-secondary text-uppercase mb-3 d-block" style="font-size: 11px; letter-spacing: 0.04em;">
              {{ m.cargo }}
            </span>

            <p class="text-secondary small mb-0" style="line-height: 1.7;">
              {{ m.descripcion }}
            </p>
          </article>
        </div>
      </div>
    </div>
  </section>

  <!-- PRODUCCIÓN INTEGRAL 360°: NOS ENCARGAMOS DE HACERLO REALIDAD -->
  <section class="py-5" style="background: var(--section-alt-bg);">
    <div class="container">
      <div class="cultural-law-card">
        <div class="row align-items-center g-5">
          <div class="col-lg-7">
            <div class="eyebrow-luxury mb-2">
              <span>★</span> PRODUCCIÓN TÉCNICA & EJECUTIVA 360°
            </div>
            <h2 class="display-6 fw-bold mb-3">Nos encargamos de hacerlo realidad.</h2>
            <p class="text-secondary mb-4" style="font-size: 15px; line-height: 1.8;">
              Detrás de cada experiencia existe una producción rigurosa: planificación, recintos, logística, ambientación, entretención, catering, actividades deportivas, artistas, fotografía y coordinación en terreno.
            </p>
            <p class="text-secondary mb-4" style="font-size: 15px; line-height: 1.8;">
              <strong>Nuestro propósito es que tu empresa pueda concentrarse en sus colaboradores y en vivir la experiencia, mientras nosotros nos preocupamos de hacer que todo funcione a la perfección.</strong> Desde la primera idea hasta el último detalle.
            </p>
            <RouterLink :to="{ path: '/', hash: '#cotizacion' }" class="btn btn-orion d-inline-flex align-items-center gap-2">
              <span>Conversar con el Equipo de Producción</span>
              <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><path d="M5 12h14M12 5l7 7-7 7"/></svg>
            </RouterLink>
          </div>

          <div class="col-lg-5">
            <div class="p-4 rounded-4" style="background: rgba(127,127,127,0.06); border: 1px solid var(--card-border);">
              <h3 class="h6 fw-bold text-uppercase mb-3" style="letter-spacing: 0.1em; color: var(--orion-primary);">
                Cobertura Integral de Producción
              </h3>
              <ul class="list-unstyled mb-0 d-flex flex-column gap-2 small text-secondary">
                <li v-for="item in pilaresProduccion" :key="item" class="d-flex align-items-center gap-2">
                  <span style="color: var(--orion-primary);">✓</span>
                  <span>{{ item }}</span>
                </li>
              </ul>
            </div>
          </div>
        </div>
      </div>
    </div>
  </section>

  <!-- NUESTRO PROPÓSITO -->
  <section class="py-5">
    <div class="container">
      <div class="text-center max-w-700 mx-auto mb-5">
        <div class="eyebrow-luxury justify-content-center">
          <span>★</span> NUESTRO PROPÓSITO
        </div>
        <h2 class="display-5 fw-bold mt-2">Construir Cultura y Fortalecer Vínculos.</h2>
        <p class="text-secondary mt-2" style="font-size: 15px;">
          Porque creemos que cuando una empresa crea experiencias significativas para sus colaboradores, no está simplemente realizando una actividad: está creando recuerdos que permanecen.
        </p>
      </div>

      <div class="row g-4">
        <div v-for="p in propositos" :key="p.tag" class="col-md-6 col-lg-3">
          <article class="pillar-card h-100">
            <span class="pillar-card__num">{{ p.tag }}</span>
            <h3>{{ p.titulo }}</h3>
            <p>{{ p.desc }}</p>
          </article>
        </div>
      </div>
    </div>
  </section>

  <!-- MODAL DE VISUALIZACIÓN DE CAMPAÑA -->
  <div
    v-if="modalCampana"
    class="modal fade show d-block"
    tabindex="-1"
    style="background: rgba(0, 0, 0, 0.85); z-index: 1060;"
    @click.self="cerrarModal"
  >
    <div class="modal-dialog campana-modal-dialog modal-dialog-centered">
      <div class="modal-content campana-modal-content">
        <div class="modal-header border-0 pb-0 px-4 pt-4 d-flex justify-content-between align-items-center">
          <div>
            <span class="campana-card__badge mb-1" :style="{ color: modalCampana.tagColor, borderColor: modalCampana.tagColor }">
              {{ modalCampana.mundo }}
            </span>
            <h3 class="h4 fw-bold mb-0 text-body">{{ modalCampana.titulo }}</h3>
          </div>
          <button type="button" class="btn-close" aria-label="Cerrar" @click="cerrarModal"></button>
        </div>
        <div class="modal-body px-4 py-3">
          <div class="campana-modal-img-wrap mb-3">
            <img :src="modalCampana.poster" :alt="modalCampana.titulo" class="campana-modal-img" />
          </div>
          <p class="text-secondary mb-3" style="font-size: 14.5px; line-height: 1.7;">
            {{ modalCampana.descripcion }}
          </p>
        </div>
        <div class="modal-footer border-0 px-4 pb-4 pt-0 d-flex justify-content-between">
          <button type="button" class="btn btn-outline-secondary" @click="cerrarModal">
            Cerrar
          </button>
          <RouterLink :to="{ path: '/', hash: '#cotizacion' }" class="btn btn-orion" @click="cerrarModal">
            Cotizar esta Campaña
          </RouterLink>
        </div>
      </div>
    </div>
  </div>
</template>
