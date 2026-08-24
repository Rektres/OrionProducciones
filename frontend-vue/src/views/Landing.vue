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
  { n: '+600', l: 'EVENTOS EXITOSOS' },
  { n: '100%', l: 'COBERTURA EN CHILE' },
  { n: 'LINE-ARRAY', l: 'AUDIO CERTIFICADO' },
];

const pilares = [
  {
    num: '01 / ACÚSTICA',
    title: 'Audio Line Array & Precisión',
    desc: 'Sistemas de sonido de estándar internacional calibrados por ingenieros FOH certificados para una acústica cristalina.'
  },
  {
    num: '02 / ILUMINACIÓN',
    title: 'Magia Lumínica & Shows Láser',
    desc: 'Cabezas móviles Beam/Spot/Wash y atmósferas arquitectónicas cálidas para crear momentos visuales inolvidables.'
  },
  {
    num: '03 / INFRAESTRUCTURA',
    title: 'Escenarios & Pantallas LED',
    desc: 'Estructuras Layher certificadas, tarimas antideslizantes y pantallas LED 4K de alto brillo para interior y exterior.'
  },
  {
    num: '04 / PRODUCCIÓN 360°',
    title: 'Donde Cada Detalle Importa',
    desc: 'Dirección técnica integral, coordinación de proveedores y regiduría en vivo para que tú solo disfrutes de tu gran día.'
  }
];

const paths = [
  {
    index: '01 / CORPORATIVO & MARCAS',
    kicker: 'PRODUCCIÓN EJECUTIVA',
    title: 'Lanzamientos,<br>Galas & Congresos.',
    desc: 'Escenografía a medida, pantallas LED de ultra alta definición, microfonía digital inalámbrica y streaming internacional broadcast.',
    cta: 'Cotizar Corporativo',
    theme: 'path-card--1'
  },
  {
    index: '02 / FESTIVALES & CONCIERTOS',
    kicker: 'GRAN ESCALA',
    title: 'Potencia Sonora<br>& Efectos Láser.',
    desc: 'Sistemas Line Array de alto rendimiento, estructuras Layher y Truss certificadas, show de luces robóticas sincronizadas por timecode.',
    cta: 'Cotizar Festival',
    theme: 'path-card--2'
  },
  {
    index: '03 / BODAS & FIESTAS BOUTIQUE',
    kicker: 'EXPERIENCIA BOUTIQUE',
    title: 'Momentos Únicos,<br>Atmósferas Mágicas.',
    desc: 'Cielo estrellado con micro-luces cálidas, pista de baile iluminada, audio envolvente para banda en vivo y atención personalizada.',
    cta: 'Cotizar Matrimonio',
    theme: 'path-card--3'
  }
];

const testimonios = [
  {
    quote: 'La potencia y fidelidad del sonido Line Array en nuestro festival superó todas las expectativas. El montaje fue puntual y de máxima categoría.',
    author: 'Rodrigo Morales',
    role: 'Director de Producción, Sunset Chile'
  },
  {
    quote: 'Hicieron de nuestro matrimonio en Viña Santa Rita una noche de ensueño. La iluminación cálida y la música sonaron con una claridad impecable.',
    author: 'Valentina & Ignacio',
    role: 'Novios · Matrimonio Boutique 2026'
  },
  {
    quote: 'Nuestra gala anual corporativa tuvo un estándar audiovisual internacional. La tranquilidad de trabajar con ingenieros expertos no tiene precio.',
    author: 'Camila Santander',
    role: 'Gerente de Comunicaciones, Minería del Cobre'
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
  <!-- HERO SECTION FUSIÓN: ARCADIA + ORION + TU DÍA PERFECTO -->
  <section class="hero-fusion">
    <div class="hero__veil"></div>
    <div class="hero__glow hero__glow--gold"></div>
    <div class="hero__glow hero__glow--cyan"></div>

    <div class="container position-relative" style="z-index: 2;">
      <div class="row align-items-center g-5">
        <div class="col-lg-7">
          <FadeInUp>
            <div class="eyebrow-luxury">
              <span>★</span> PRODUCCIÓN INTEGRAL DE EVENTOS & EXPERIENCIAS ESCÉNICAS
            </div>
            <h1 class="hero-title-giant">
              <span>DONDE CADA DETALLE IMPORTA,</span><br />
              <span class="highlight-gold">CREAMOS MOMENTOS</span><br />
              <em>INOLVIDABLES.</em>
            </h1>
            <p class="lead text-secondary mt-3 mb-4" style="max-width: 580px; font-size: 16px; line-height: 1.75;">
              Ingeniería acústica Line Array, iluminación robótica de vanguardia y dirección técnica 360° para matrimonios de lujo, festivales masivos y eventos corporativos en todo Chile.
            </p>
            <div class="d-flex flex-wrap gap-3">
              <RouterLink :to="{ path: '/', hash: '#cotizacion' }" class="btn btn-orion d-inline-flex align-items-center gap-2">
                <span>Cotizar mi Evento</span>
                <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><path d="M5 12h14M12 5l7 7-7 7"/></svg>
              </RouterLink>
              <a href="#catalogo" class="btn-glass">
                <span>Explorar Catálogo</span>
                <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M19 9l-7 7-7-7"/></svg>
              </a>
            </div>
          </FadeInUp>
        </div>

        <div class="col-lg-5 d-none d-lg-flex justify-content-end">
          <FadeInUp :delay="0.3">
            <aside v-if="servicioHero" class="hero-card-preview">
              <div class="d-flex align-items-center gap-2 mb-2 px-1">
                <span class="live-dot"></span>
                <span class="small fw-bold text-uppercase" style="letter-spacing: 0.1em; font-size: 10px;">PRODUCCIÓN EN VIVO</span>
                <span class="ms-auto small text-secondary" style="font-size: 10px;">TEMPORADA 2026</span>
              </div>
              <img
                :src="servicioHero.imagen_url || '/logo.png'"
                :alt="servicioHero.nombre"
                class="hero-card-preview__img"
              />
              <div class="d-flex align-items-end justify-content-between pt-3 px-1">
                <div>
                  <span class="small fw-bold text-uppercase text-orion-gold" style="font-size: 10px; letter-spacing: 0.1em;">
                    {{ servicioHero.categoria_slug || 'PRODUCCIÓN TÉCNICA' }}
                  </span>
                  <h3 class="h5 mb-0 fw-bold mt-1">{{ servicioHero.nombre }}</h3>
                </div>
                <button
                  type="button"
                  class="btn btn-sm btn-outline-secondary rounded-circle p-2"
                  aria-label="Ver detalles"
                  @click="abrirServicio(servicioHero)"
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

  <!-- 4 PILARES: "DONDE CADA DETALLE IMPORTA" (TU DÍA PERFECTO + ORION) -->
  <section class="py-5">
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
          <article class="pillar-card">
            <span class="pillar-card__num">{{ pil.num }}</span>
            <h3>{{ pil.title }}</h3>
            <p>{{ pil.desc }}</p>
          </article>
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

  <!-- SECCIÓN MANIFIESTO ORION CON ORBE HOLOGRÁFICO -->
  <section class="py-4">
    <div class="container">
      <div class="manifesto">
        <div class="manifesto__index">ORION / 01</div>
        <div class="manifesto__content">
          <div class="eyebrow-luxury">
            <span>★</span> NUESTRA VISIÓN
          </div>
          <h2>Potencia Sonora.<br>Impacto Visual Inolvidable.</h2>
          <p>
            En Orion Stage fusionamos la precisión acústica de clase mundial con el arte de la iluminación y la escenografía. Nos encargamos de toda la complejidad técnica para que tú y tus invitados vivan una experiencia mágica.
          </p>
          <RouterLink :to="{ path: '/', hash: '#cotizacion' }" class="btn-glass">
            <span>Conversar con un Ingeniero Técnico</span>
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

  <!-- TESTIMONIOS Y CONFIANZA (TOQUE TU DÍA PERFECTO) -->
  <section class="py-5" style="background: var(--section-alt-bg);">
    <div class="container">
      <div class="text-center max-w-700 mx-auto mb-5">
        <div class="eyebrow-luxury justify-content-center">
          <span>★</span> TESTIMONIOS REALES
        </div>
        <h2 class="display-5 fw-bold mt-2">La Confianza de Nuestros Clientes.</h2>
        <p class="text-secondary mt-2" style="font-size: 15px;">
          Productores ejecutivos, empresas y parejas que confiaron en nosotros para su gran momento.
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
        <p class="text-secondary small mt-2">Fotografías reales capturadas en conciertos, bodas y galas producidas por Orion Stage</p>
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
          <h2 class="display-5 fw-bold mb-2">Hagamos Realidad tu Gran Evento.</h2>
          <p class="text-secondary">Cuéntanos sobre tu fecha, recinto y requerimientos técnicos. Diseñaremos una propuesta a tu medida en menos de 24 horas.</p>
        </div>
        <ContactForm />
      </div>
    </div>
  </section>

  <ServicioModal ref="servicioModalRef" />
  <GaleriaFotosModal ref="galeriaModalRef" />
</template>

