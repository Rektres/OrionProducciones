<script setup lang="ts">
import { computed, onMounted, ref } from 'vue';
import { RouterLink } from 'vue-router';
import ContactForm from '@/components/ContactForm.vue';
import ServicioModal from '@/components/ServicioModal.vue';
import GaleriaFotosModal from '@/components/GaleriaFotosModal.vue';
import BrandLogo from '@/components/BrandLogo.vue';
import FadeInUp from '@/components/animations/FadeInUp.vue';
import { serviciosService } from '@/services/servicios';
import { portafolioService } from '@/services/portafolio';
import type { Servicio, Evento, FotoEvento } from '@/types';

interface CampanaLanding {
  id: string;
  mundo: string;
  titulo: string;
  subtitulo: string;
  descripcion: string;
  poster: string;
  badge: string;
  tagColor: string;
}

const servicios = ref<Servicio[]>([]);
const eventosDestacados = ref<Evento[]>([]);
const cargando = ref(true);
const filtroCategoria = ref<string>('todos');

const servicioModalRef = ref<InstanceType<typeof ServicioModal> | null>(null);
const abrirServicio = (svc: Servicio) => servicioModalRef.value?.abrir(svc);
const galeriaModalRef = ref<InstanceType<typeof GaleriaFotosModal> | null>(null);

const campanasLanding: CampanaLanding[] = [
  {
    id: 'women',
    mundo: 'ORIÓN WOMEN',
    titulo: 'Confianza en Ti',
    subtitulo: 'Bienestar, Autocuidado & Liderazgo',
    descripcion:
      'Experiencias de bienestar especialmente pensadas para las mujeres de las organizaciones: automaquillaje, nutrición, autocuidado, liderazgo y desarrollo personal.',
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
      'El deporte como punto de encuentro: torneos de pádel corporativos que promueven la integración, el trabajo en equipo, la vida saludable y la camaradería.',
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
      'Ligas y copas de fútbol 7 con arbitraje oficial, transmisión en vivo, premiaciones y ambientación técnica para fortalecer el espíritu de equipo.',
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
      'Acercando la empresa a las familias mediante actividades recreativas y escuelas de verano inolvidables para los hijos de los colaboradores.',
    poster: '/campanas/escuelas-de-verano.png',
    badge: 'Familia & Niñez',
    tagColor: '#f59e0b',
  },
  {
    id: 'celebrations',
    mundo: 'ORIÓN CELEBRATIONS',
    titulo: 'Fiesta de Fin de Año',
    subtitulo: 'Galas, Aniversarios & Hitos',
    descripcion:
      'Celebraciones corporativas, aniversarios y fiestas de fin de año diseñadas para agradecer, reconocer y celebrar los logros del equipo con estándar de festival.',
    poster: '/campanas/fiesta-fin-de-ano.png',
    badge: 'Celebración & Reconocimiento',
    tagColor: '#d06c26',
  },
];

const modalCampanaLanding = ref<CampanaLanding | null>(null);
const abrirCampana = (c: CampanaLanding) => {
  modalCampanaLanding.value = c;
};
const cerrarCampana = () => {
  modalCampanaLanding.value = null;
};

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

// Evento o Servicio destacado para la tarjeta flotante del Hero
const eventoHero = computed(() => {
  return eventosDestacados.value[0] || null;
});

const servicioFallback = computed(() => {
  return servicios.value[0] || null;
});

// Galería de fotos de eventos: mosaico dinámico
interface FotoGaleria extends Omit<FotoEvento, 'imagen_url'> {
  imagen_url: string;
  eventoNombre: string;
}
const fotosGaleria = ref<FotoGaleria[]>([]);
const TAMANOS_MOSAICO = ['', 'tam-ancho', 'tam-alto', '', 'tam-grande', '', 'tam-alto', 'tam-ancho', '', '', 'tam-ancho', 'tam-alto'];
const tamanoMosaico = (idx: number) => TAMANOS_MOSAICO[idx % TAMANOS_MOSAICO.length];
const abrirGaleria = (idx: number) => galeriaModalRef.value?.abrir(fotosGaleria.value, idx);

const stats = [
  { n: '+12 AÑOS', l: 'DE TRAYECTORIA' },
  { n: '+600', l: 'EXPERIENCIAS & EVENTOS' },
  { n: '100%', l: 'COBERTURA EN CHILE' },
  { n: '360°', l: 'PRODUCCIÓN INTEGRAL' },
];

const marcas = [
  { nombre: 'Banco Santander', tag: 'Galas & Convenciones', logoKey: 'santander' },
  { nombre: 'Entel', tag: 'Festivales Masivos', logoKey: 'entel' },
  { nombre: 'Viña Santa Rita', tag: 'Bodas de Alta Gama', logoKey: 'santa-rita' },
  { nombre: 'Mallplaza', tag: 'Activaciones 360', logoKey: 'mallplaza' },
  { nombre: 'BHP Escondida', tag: 'Corporativo Minero', logoKey: 'bhp' },
  { nombre: 'Codelco', tag: 'Eventos Masivos', logoKey: 'codelco' },
  { nombre: 'Copec', tag: 'Lanzamientos', logoKey: 'copec' },
  { nombre: 'Lotus Producciones', tag: 'Conciertos', logoKey: 'lotus' },
  { nombre: 'Universidad de Chile', tag: 'Ceremonias Oficiales', logoKey: 'uchile' },
  { nombre: 'Red Bull Chile', tag: 'Escenarios & Shows', logoKey: 'redbull' },
  { nombre: 'Gran Arena Monticello', tag: 'Música en Vivo', logoKey: 'monticello' },
  { nombre: 'Espacio Riesco', tag: 'Convenciones & Ferias', logoKey: 'espacio-riesco' },
];

const pilares = [
  {
    num: '01 / BIENESTAR & PERSONAS',
    title: 'Experiencias que Conectan',
    desc: 'Escuchamos a cada organización para diseñar actividades con sentido: bienestar, integración deportiva, familia y celebraciones corporativas.'
  },
  {
    num: '02 / INGENIERÍA ACÚSTICA',
    title: 'Audio Line Array & Precisión',
    desc: 'Sistemas de sonido de estándar internacional calibrados por ingenieros FOH certificados para una acústica cristalina.'
  },
  {
    num: '03 / ILUMINACIÓN & ESCENOGRAFÍA',
    title: 'Magia Visual & Shows Láser',
    desc: 'Cabezas robóticas, efectos sincronizados, pantallas LED 4K y ambientación arquitectónica para crear momentos inolvidables.'
  },
  {
    num: '04 / PRODUCCIÓN 360°',
    title: 'Desde la Idea al Último Detalle',
    desc: 'Nos encargamos de toda la complejidad técnica y logística para que tu empresa solo se concentre en vivir la experiencia.'
  }
];

const paths = [
  {
    index: '01 / CORPORATIVO & EXPERIENCIAS',
    kicker: 'MUNDOS ORIÓN STAGE',
    title: 'Bienestar, Deporte<br>& Cultura Organizacional.',
    desc: 'Experiencias a medida para empresas: Orión Women, Orión Sports, Orión Family y celebraciones de fin de año con producción integral.',
    cta: 'Explorar Campañas',
    theme: 'path-card--1'
  },
  {
    index: '02 / FESTIVALES & CONCIERTOS',
    kicker: 'GRAN ESCALA',
    title: 'Potencia Sonora<br>& Efectos Láser.',
    desc: 'Sistemas Line Array de alto rendimiento, estructuras Layher certificadas, pantallas LED 4K y show de luces robóticas por timecode.',
    cta: 'Cotizar Festival',
    theme: 'path-card--2'
  },
  {
    index: '03 / BODAS & FIESTAS BOUTIQUE',
    kicker: 'EXPERIENCIA BOUTIQUE',
    title: 'Momentos Únicos,<br>Atmósferas Mágicas.',
    desc: 'Cielo estrellado con micro-luces cálidas, pista de baile iluminada, audio envolvente para banda en vivo y regiduría en terreno.',
    cta: 'Cotizar Matrimonio',
    theme: 'path-card--3'
  }
];

const testimonios = [
  {
    quote: 'Orión Stage transformó nuestra jornada anual en un recuerdo imborrable para nuestros colaboradores. La producción, la puntualidad y el cariño en cada detalle marcaron la diferencia.',
    author: 'Rodrigo Morales',
    role: 'Director de Personas, Empresa Tecnológica'
  },
  {
    quote: 'La experiencia del torneo de pádel y la ambientación de cierre fueron de primer nivel. Lograron unir a las distintas áreas de la empresa como nunca antes.',
    author: 'Camila Santander',
    role: 'Gerente de Comunicaciones & Clima Laboral'
  },
  {
    quote: 'El estándar técnico y la calidad humana del equipo superaron todas las expectativas. La tranquilidad de trabajar con verdaderos profesionales no tiene precio.',
    author: 'Valentina & Ignacio',
    role: 'Productores de Eventos · Santiago'
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
  <!-- HERO SECTION: ORIÓN STAGE -->
  <section class="hero-fusion">
    <div class="hero__veil"></div>
    <div class="hero__glow hero__glow--gold"></div>
    <div class="hero__glow hero__glow--cyan"></div>

    <div class="container position-relative" style="z-index: 2;">
      <div class="row align-items-center g-5">
        <div class="col-lg-7">
          <FadeInUp>
            <div class="eyebrow-luxury">
              <span>★</span> EXPERIENCIAS CORPORATIVAS · PRODUCCIÓN · ESPECTÁCULOS
            </div>
            <h1 class="hero-title-giant">
              <span>NO ORGANIZAMOS SOLO EVENTOS,</span><br />
              <span class="highlight-gold">CREAMOS EXPERIENCIAS</span><br />
              <em>QUE CONECTAN PERSONAS.</em>
            </h1>
            <p class="lead text-secondary mt-3 mb-4" style="max-width: 580px; font-size: 16px; line-height: 1.75;">
              Desde la primera idea hasta el último detalle: experiencias de bienestar, deporte corporativo, encuentros familiares y celebraciones de fin de año con ingeniería escénica de clase mundial.
            </p>
            <div class="d-flex flex-wrap gap-3">
              <RouterLink :to="{ path: '/', hash: '#cotizacion' }" class="btn btn-orion d-inline-flex align-items-center gap-2">
                <span>Cotizar Experiencia</span>
                <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><path d="M5 12h14M12 5l7 7-7 7"/></svg>
              </RouterLink>
              <a href="#campanas" class="btn-glass">
                <span>Ver Campañas Activas</span>
                <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M19 9l-7 7-7-7"/></svg>
              </a>
            </div>
          </FadeInUp>
        </div>

        <div class="col-lg-5 d-none d-lg-flex justify-content-end">
          <FadeInUp :delay="0.3">
            <!-- Tarjeta Flotante Hero (Navega directamente al Evento) -->
            <aside v-if="eventoHero" class="hero-card-preview">
              <div class="d-flex align-items-center gap-2 mb-2 px-1">
                <span class="live-dot"></span>
                <span class="small fw-bold text-uppercase" style="letter-spacing: 0.1em; font-size: 10px;">PRODUCCIÓN DESTACADA</span>
                <span class="ms-auto small text-secondary" style="font-size: 10px;">TEMPORADA 2026</span>
              </div>
              <RouterLink :to="`/portafolio/${eventoHero.slug}`" class="d-block text-decoration-none">
                <img
                  :src="eventoHero.imagen_destacada || '/logo.png'"
                  :alt="eventoHero.nombre"
                  class="hero-card-preview__img"
                />
              </RouterLink>
              <div class="d-flex align-items-end justify-content-between pt-3 px-1">
                <div>
                  <span class="small fw-bold text-uppercase text-orion-gold" style="font-size: 10px; letter-spacing: 0.1em;">
                    {{ eventoHero.tipo_slug || 'PRODUCCIÓN ESCÉNICA' }}
                  </span>
                  <RouterLink :to="`/portafolio/${eventoHero.slug}`" class="text-decoration-none d-block">
                    <h3 class="h5 mb-0 fw-bold mt-1 text-body">{{ eventoHero.nombre }}</h3>
                  </RouterLink>
                </div>
                <RouterLink
                  :to="`/portafolio/${eventoHero.slug}`"
                  class="btn btn-sm btn-outline-secondary rounded-circle p-2 d-inline-flex align-items-center justify-content-center"
                  aria-label="Ir al evento"
                  title="Ver detalle del evento"
                >
                  <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><path d="M5 12h14M12 5l7 7-7 7"/></svg>
                </RouterLink>
              </div>
            </aside>
            <aside v-else-if="servicioFallback" class="hero-card-preview">
              <div class="d-flex align-items-center gap-2 mb-2 px-1">
                <span class="live-dot"></span>
                <span class="small fw-bold text-uppercase" style="letter-spacing: 0.1em; font-size: 10px;">EQUIPAMIENTO DESTACADO</span>
              </div>
              <img
                :src="servicioFallback.imagen_url || '/logo.png'"
                :alt="servicioFallback.nombre"
                class="hero-card-preview__img"
              />
              <div class="d-flex align-items-end justify-content-between pt-3 px-1">
                <div>
                  <span class="small fw-bold text-uppercase text-orion-gold" style="font-size: 10px;">
                    {{ servicioFallback.categoria_slug || 'PRODUCCIÓN TÉCNICA' }}
                  </span>
                  <h3 class="h5 mb-0 fw-bold mt-1 text-body">{{ servicioFallback.nombre }}</h3>
                </div>
                <button
                  type="button"
                  class="btn btn-sm btn-outline-secondary rounded-circle p-2"
                  @click="abrirServicio(servicioFallback)"
                >
                  <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><path d="M5 12h14M12 5l7 7-7 7"/></svg>
                </button>
              </div>
            </aside>
          </FadeInUp>
        </div>
      </div>
    </div>
  </section>

  <!-- TRUST BAR / STATS BAR -->
  <section class="trust-bar">
    <div class="container">
      <div class="row g-4 text-center text-md-start">
        <div v-for="st in stats" :key="st.l" class="col-6 col-md-3">
          <div class="trust-stat">
            <strong>{{ st.n }}</strong>
            <span>{{ st.l }}</span>
          </div>
        </div>
      </div>
    </div>
  </section>

  <!-- CARRUSEL ORGÁNICO: CONFÍAN EN NOSOTROS -->
  <section class="brand-marquee-section">
    <div class="container mb-3 text-center">
      <div class="eyebrow-luxury justify-content-center mb-0" style="font-size: 10px;">
        <span>★</span> EMPRESAS & PRODUCTORAS QUE CONFÍAN EN ORION
      </div>
    </div>
    <div class="brand-marquee-container">
      <div class="brand-marquee-track">
        <div v-for="(m, i) in marcas" :key="`m1-${i}`" class="brand-pill">
          <BrandLogo :name="m.logoKey" />
          <span>{{ m.nombre }}</span>
          <small class="text-secondary" style="font-size: 11px; opacity: 0.7;">· {{ m.tag }}</small>
        </div>
      </div>
      <div class="brand-marquee-track" aria-hidden="true">
        <div v-for="(m, i) in marcas" :key="`m2-${i}`" class="brand-pill">
          <BrandLogo :name="m.logoKey" />
          <span>{{ m.nombre }}</span>
          <small class="text-secondary" style="font-size: 11px; opacity: 0.7;">· {{ m.tag }}</small>
        </div>
      </div>
    </div>
  </section>

  <!-- SECCIÓN DE CAMPAÑAS ACTIVAS (ORIÓN WOMEN, SPORTS, FAMILY, CELEBRATIONS) -->
  <section id="campanas" class="py-5">
    <div class="container">
      <div class="text-center max-w-700 mx-auto mb-5">
        <div class="eyebrow-luxury justify-content-center">
          <span>★</span> NUESTRAS CAMPAÑAS CORPORATIVAS
        </div>
        <h2 class="display-5 fw-bold mt-2">Mundos de Experiencia para tu Empresa</h2>
        <p class="text-secondary mt-2" style="font-size: 15px;">
          Diseñadas para acompañar a las organizaciones durante todo el año: bienestar femenino, deporte, familia y celebraciones inolvidables.
        </p>
      </div>

      <div class="row g-4">
        <div v-for="c in campanasLanding" :key="c.id" class="col-md-6 col-lg-4">
          <article class="campana-card">
            <div class="campana-card__poster" role="button" tabindex="0" @click="abrirCampana(c)">
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
                <button type="button" class="btn btn-sm btn-outline-secondary rounded-pill px-3" @click="abrirCampana(c)">
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

  <!-- 4 PILARES: "DONDE CADA DETALLE IMPORTA" -->
  <section class="py-5" style="background: var(--section-alt-bg);">
    <div class="container">
      <div class="text-center max-w-700 mx-auto mb-5">
        <div class="eyebrow-luxury justify-content-center">
          <span>★</span> NUESTROS PILARES DE EXCELENCIA
        </div>
        <h2 class="display-5 fw-bold mt-2">La Tranquilidad de un Evento Perfecto.</h2>
        <p class="text-secondary mt-2" style="font-size: 15px;">
          Combinamos la calidez humana y el cuidado de cada detalle con la potencia técnica y la ingeniería de vanguardia.
        </p>
      </div>

      <div class="row g-4">
        <div v-for="pil in pilares" :key="pil.num" class="col-md-6 col-lg-3">
          <article class="pillar-card h-100">
            <span class="pillar-card__num">{{ pil.num }}</span>
            <h3>{{ pil.title }}</h3>
            <p>{{ pil.desc }}</p>
          </article>
        </div>
      </div>
    </div>
  </section>

  <!-- SECCIÓN LEY DE DONACIONES CULTURALES (GOBIERNO DE CHILE) -->
  <section class="py-4">
    <div class="container">
      <div class="cultural-law-card">
        <div class="row align-items-center g-4">
          <div class="col-lg-8">
            <div class="d-flex flex-wrap align-items-center gap-3 mb-3">
              <div class="gob-badge">
                <span class="live-dot" style="background: #0039a6; box-shadow: 0 0 8px #0039a6;"></span>
                <span>LEY N° 18.985 / LEY VALDÉS</span>
              </div>
              <span class="badge bg-orion-gold text-dark fw-bold px-3 py-2" style="font-size: 11px; border-radius: 6px;">
                50% CRÉDITO TRIBUTARIO
              </span>
            </div>
            <h2 class="display-6 fw-bold mb-3 text-body">
              Proyectos & Festivales Acogidos a la Ley de Donaciones Culturales
            </h2>
            <p class="text-secondary mb-4" style="font-size: 15px; line-height: 1.75;">
              En Orion Stage contamos con proyectos de música en vivo, festivales y montajes escénicos adjudicados y respaldados bajo la <strong>Ley de Donaciones Culturales del Ministerio de las Culturas, las Artes y el Patrimonio de Chile</strong>. Empresas y personas jurídicas de primera categoría pueden financiar eventos culturales obteniendo una <strong>rebaja y crédito fiscal directo del 50%</strong> del aporte realizado.
            </p>
            <div class="d-flex flex-wrap gap-3">
              <RouterLink :to="{ path: '/', hash: '#cotizacion' }" class="btn btn-orion d-inline-flex align-items-center gap-2">
                <span>Consultar por Ley de Donaciones</span>
                <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><path d="M5 12h14M12 5l7 7-7 7"/></svg>
              </RouterLink>
              <a href="https://wa.me/56944830378?text=Hola,%20quisiera%20información%20sobre%20la%20Ley%20de%20Donaciones%20Culturales%20para%20eventos" target="_blank" rel="noopener noreferrer" class="btn-glass">
                <span>Asesoría Directa por WhatsApp</span>
              </a>
            </div>
          </div>
          <div class="col-lg-4 text-center text-lg-end">
            <div class="d-inline-flex flex-column align-items-center align-items-lg-end p-4 rounded-4" style="background: rgba(127,127,127,0.06); border: 1px solid var(--card-border);">
              <div class="gob-logo-container mb-2">
                <div class="gob-chile-flag">
                  <div class="gob-chile-flag__top">
                    <div class="gob-chile-flag__blue">★</div>
                    <div class="gob-chile-flag__white"></div>
                  </div>
                  <div class="gob-chile-flag__bottom"></div>
                </div>
                <div class="text-start lh-1">
                  <strong class="d-block" style="font-size: 13px; letter-spacing: -0.02em; color: var(--bs-body-color);">Ministerio de las Culturas,</strong>
                  <span class="small text-secondary" style="font-size: 11px;">las Artes y el Patrimonio</span>
                </div>
              </div>
              <small class="text-secondary text-uppercase fw-bold mt-2" style="font-size: 9px; letter-spacing: 0.1em;">
                Gobierno de Chile
              </small>
              <div class="mt-3 small text-secondary text-center text-lg-end" style="font-size: 11px; max-width: 220px;">
                Certificación y asesoría legal para donantes corporativos disponible.
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </section>

  <!-- CATÁLOGO DE SERVICIOS CON FILTER CHIPS -->
  <section id="catalogo" class="py-5" style="background: var(--section-alt-bg);">
    <div class="container">
      <div class="row align-items-end g-4 mb-2">
        <div class="col-lg-7">
          <div class="eyebrow-luxury">
            <span>★</span> EQUIPAMIENTO PROFESIONAL
          </div>
          <h2 class="display-5 fw-bold mb-0">Tecnología de Escenario & Experiencias.</h2>
        </div>
        <div class="col-lg-5">
          <p class="text-secondary mb-0" style="font-size: 14px; line-height: 1.7;">
            Soluciones integrales de sonido, iluminación, video y estructuras certificadas para garantizar un evento impecable de principio a fin.
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
        <span class="small fw-bold text-uppercase text-secondary" style="letter-spacing: 0.1em; font-size: 11px;">
          <strong class="text-body">{{ serviciosFiltrados.length }}</strong> SERVICIOS DISPONIBLES
        </span>
      </div>

      <!-- Grid de Servicios -->
      <div v-if="cargando" class="text-center py-5">
        <div class="spinner-border text-warning" role="status"></div>
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
                <span>Ver especificaciones técnicas</span>
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

  <!-- SECCIÓN MANIFIESTO ORION CON ORBE HOLOGRÁFICO (EXTRACTO DE ORIONSTAGE.TXT) -->
  <section class="py-4">
    <div class="container">
      <div class="manifesto">
        <div class="manifesto__index">ORION / 01</div>
        <div class="manifesto__content">
          <div class="eyebrow-luxury">
            <span>★</span> NUESTRO PROPÓSITO
          </div>
          <h2>¿Por qué nace Orión Stage?<br>Creamos Experiencias que Conectan.</h2>
          <p>
            Entendemos que detrás de cada empresa existen personas: colaboradores que trabajan juntos, superan desafíos y necesitan espacios para encontrarse, cuidarse y celebrar. Diseñamos y producimos experiencias de principio a fin, combinando creatividad, bienestar y tecnología escénica.
          </p>
          <div class="d-flex flex-wrap gap-3">
            <RouterLink to="/nosotros" class="btn btn-orion d-inline-flex align-items-center gap-2">
              <span>Conoce Nuestra Historia</span>
              <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><path d="M5 12h14M12 5l7 7-7 7"/></svg>
            </RouterLink>
            <RouterLink :to="{ path: '/', hash: '#cotizacion' }" class="btn-glass">
              <span>Conversar con el Equipo</span>
            </RouterLink>
          </div>
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
          <div class="eyebrow-luxury">
            <span>★</span> SOLUCIONES A TU MEDIDA
          </div>
          <h2 class="display-5 fw-bold mb-0">Cada Escenario Tiene su Propia Magia.</h2>
        </div>
        <div class="col-lg-5">
          <p class="text-secondary mb-0" style="font-size: 14px; line-height: 1.7;">
            Diseñamos propuestas llave en mano adaptadas a las dimensiones de tu recinto, tipo de público y requerimientos de producción.
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

  <!-- TESTIMONIOS Y CONFIANZA -->
  <section class="py-5" style="background: var(--section-alt-bg);">
    <div class="container">
      <div class="text-center max-w-700 mx-auto mb-5">
        <div class="eyebrow-luxury justify-content-center">
          <span>★</span> TESTIMONIOS REALES
        </div>
        <h2 class="display-5 fw-bold mt-2">La Confianza de Quienes Crean con Nosotros.</h2>
        <p class="text-secondary mt-2" style="font-size: 15px;">
          Líderes de personas, productoras y empresas que confiaron en Orión Stage para sus momentos más importantes.
        </p>
      </div>

      <div class="row g-4">
        <div v-for="t in testimonios" :key="t.author" class="col-md-4">
          <div class="testimonial-card">
            <p class="testimonial-quote">“{{ t.quote }}”</p>
            <div class="testimonial-author">
              <div>
                <strong>{{ t.author }}</strong>
                <span>{{ t.role }}</span>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </section>

  <!-- GALERÍA MOSAICO DE EVENTOS REALES -->
  <section v-if="fotosGaleria.length" class="py-5">
    <div class="container galeria-home-container">
      <div class="text-center mb-5">
        <div class="eyebrow-luxury justify-content-center">
          <span>★</span> PORTAFOLIO EN ACCIÓN
        </div>
        <h2 class="display-5 fw-bold">Momentos en Vivo</h2>
        <p class="text-secondary small mt-2">Fotografías reales capturadas en conciertos, eventos corporativos y bodas producidas por Orion Stage</p>
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

  <!-- FORMULARIO DE COTIZACIÓN LUXURY BOX -->
  <section id="cotizacion" class="py-5 cotiza-section">
    <div class="container" style="max-width: 820px">
      <div class="cotiza-box">
        <div class="text-center mb-4">
          <div class="eyebrow-luxury justify-content-center">
            <span>★</span> COTIZACIÓN SIN COMPROMISO
          </div>
          <h2 class="display-5 fw-bold mb-2">Hagamos Realidad tu Gran Experiencia.</h2>
          <p class="text-secondary">Cuéntanos sobre tu fecha, cantidad de colaboradores y tipo de experiencia deseada. Diseñaremos una propuesta a tu medida en menos de 24 horas.</p>
        </div>
        <ContactForm />
      </div>
    </div>
  </section>

  <!-- MODAL DE CAMPAÑAS EN LANDING -->
  <div
    v-if="modalCampanaLanding"
    class="modal fade show d-block"
    tabindex="-1"
    style="background: rgba(0, 0, 0, 0.85); z-index: 1060;"
    @click.self="cerrarCampana"
  >
    <div class="modal-dialog campana-modal-dialog modal-dialog-centered">
      <div class="modal-content campana-modal-content">
        <div class="modal-header border-0 pb-0 px-4 pt-4 d-flex justify-content-between align-items-center">
          <div>
            <span class="campana-card__badge mb-1" :style="{ color: modalCampanaLanding.tagColor, borderColor: modalCampanaLanding.tagColor }">
              {{ modalCampanaLanding.mundo }}
            </span>
            <h3 class="h4 fw-bold mb-0 text-body">{{ modalCampanaLanding.titulo }}</h3>
          </div>
          <button type="button" class="btn-close" aria-label="Cerrar" @click="cerrarCampana"></button>
        </div>
        <div class="modal-body px-4 py-3">
          <div class="campana-modal-img-wrap mb-3">
            <img :src="modalCampanaLanding.poster" :alt="modalCampanaLanding.titulo" class="campana-modal-img" />
          </div>
          <p class="text-secondary mb-3" style="font-size: 14.5px; line-height: 1.7;">
            {{ modalCampanaLanding.descripcion }}
          </p>
        </div>
        <div class="modal-footer border-0 px-4 pb-4 pt-0 d-flex justify-content-between">
          <button type="button" class="btn btn-outline-secondary" @click="cerrarCampana">
            Cerrar
          </button>
          <RouterLink :to="{ path: '/', hash: '#cotizacion' }" class="btn btn-orion" @click="cerrarCampana">
            Cotizar esta Campaña
          </RouterLink>
        </div>
      </div>
    </div>
  </div>

  <ServicioModal ref="servicioModalRef" />
  <GaleriaFotosModal ref="galeriaModalRef" />
</template>

