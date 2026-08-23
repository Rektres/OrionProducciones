const NOMBRE_SITIO = 'Orion';
const TITULO_DEFECTO = 'Orion — Productora de Eventos en Chile';
const DESCRIPCION_DEFECTO =
  'Productora de eventos corporativos, sociales y festivales en Chile. Producción integral: ' +
  'escenario, sonido, iluminación y montaje. Cotiza tu evento con Orion.';
const IMAGEN_DEFECTO = '/og-image.jpg';

export interface Seo {
  titulo?: string;
  descripcion?: string;
  imagen?: string;
  noindex?: boolean;
}

function etiqueta(atributo: 'name' | 'property', clave: string, contenido: string) {
  let el = document.head.querySelector<HTMLMetaElement>(`meta[${atributo}="${clave}"]`);
  if (!el) {
    el = document.createElement('meta');
    el.setAttribute(atributo, clave);
    document.head.appendChild(el);
  }
  el.setAttribute('content', contenido);
}

function enlace(rel: string, href: string) {
  let el = document.head.querySelector<HTMLLinkElement>(`link[rel="${rel}"]`);
  if (!el) {
    el = document.createElement('link');
    el.setAttribute('rel', rel);
    document.head.appendChild(el);
  }
  el.setAttribute('href', href);
}

/** Aplica title, description, canonical, Open Graph y Twitter Card a la página actual. */
export function aplicarSeo(seo: Seo = {}) {
  const titulo = seo.titulo ? `${seo.titulo} | ${NOMBRE_SITIO}` : TITULO_DEFECTO;
  const descripcion = seo.descripcion || DESCRIPCION_DEFECTO;
  const url = window.location.origin + window.location.pathname;
  const imagen = new URL(seo.imagen || IMAGEN_DEFECTO, window.location.origin).href;

  document.title = titulo;
  etiqueta('name', 'description', descripcion);
  etiqueta('name', 'robots', seo.noindex ? 'noindex, nofollow' : 'index, follow');
  enlace('canonical', url);

  etiqueta('property', 'og:type', 'website');
  etiqueta('property', 'og:site_name', NOMBRE_SITIO);
  etiqueta('property', 'og:locale', 'es_CL');
  etiqueta('property', 'og:title', titulo);
  etiqueta('property', 'og:description', descripcion);
  etiqueta('property', 'og:url', url);
  etiqueta('property', 'og:image', imagen);

  etiqueta('name', 'twitter:card', 'summary_large_image');
  etiqueta('name', 'twitter:title', titulo);
  etiqueta('name', 'twitter:description', descripcion);
  etiqueta('name', 'twitter:image', imagen);
}
