/**
 * Analítica opcional, sin dependencias y desactivada por defecto.
 *
 * Se configura con variables de entorno:
 *   VITE_ANALYTICS_PROVIDER = plausible | ga4   (vacío = no se carga nada)
 *   VITE_ANALYTICS_ID       = dominio (plausible) o G-XXXXXXX (ga4)
 *   VITE_PLAUSIBLE_HOST     = host de la instancia de Plausible (opcional)
 *
 * Plausible es cookieless: parte apenas se configura. GA4 usa cookies, así que
 * espera el consentimiento del banner (ver ConsentimientoCookies.vue).
 */

type Proveedor = 'plausible' | 'ga4' | '';

const proveedor = (import.meta.env.VITE_ANALYTICS_PROVIDER || '') as Proveedor;
const id = import.meta.env.VITE_ANALYTICS_ID || '';
const hostPlausible = import.meta.env.VITE_PLAUSIBLE_HOST || 'https://plausible.io';

/** true solo si el proveedor configurado necesita consentimiento previo (cookies). */
export const requiereConsentimiento = proveedor === 'ga4' && !!id;
/** true si hay analítica configurada, del tipo que sea. */
export const analiticaConfigurada = !!proveedor && !!id;

let cargada = false;

declare global {
  interface Window {
    dataLayer?: unknown[];
    gtag?: (...args: unknown[]) => void;
    plausible?: (evento: string, opciones?: Record<string, unknown>) => void;
  }
}

function inyectarScript(src: string, atributos: Record<string, string> = {}) {
  const s = document.createElement('script');
  s.defer = true;
  s.src = src;
  for (const [k, v] of Object.entries(atributos)) s.setAttribute(k, v);
  document.head.appendChild(s);
}

/** Carga el script del proveedor. Idempotente. */
export function cargarAnalitica() {
  if (cargada || !analiticaConfigurada) return;
  cargada = true;

  if (proveedor === 'plausible') {
    inyectarScript(`${hostPlausible}/js/script.js`, { 'data-domain': id });
    return;
  }

  window.dataLayer = window.dataLayer || [];
  window.gtag = function gtag() {
    // eslint-disable-next-line prefer-rest-params
    window.dataLayer!.push(arguments);
  };
  window.gtag('js', new Date());
  // El SPA envía los pageviews a mano en cada cambio de ruta.
  window.gtag('config', id, { send_page_view: false, anonymize_ip: true });
  inyectarScript(`https://www.googletagmanager.com/gtag/js?id=${encodeURIComponent(id)}`);
}

/** Pageview manual: en un SPA el script no los detecta solo. */
export function registrarPagina(ruta: string) {
  if (!cargada) return;
  if (proveedor === 'ga4') {
    window.gtag?.('event', 'page_view', { page_path: ruta, page_title: document.title });
  }
  // Plausible registra el pageview con el pushState nativo; no hace falta nada.
}

/** Evento de conversión (por ejemplo, cotización enviada). */
export function registrarEvento(nombre: string, datos: Record<string, unknown> = {}) {
  if (!cargada) return;
  if (proveedor === 'ga4') window.gtag?.('event', nombre, datos);
  else window.plausible?.(nombre, { props: datos });
}
