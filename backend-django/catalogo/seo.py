"""robots.txt y sitemap.xml servidos desde Django.

Van aquí y no como archivos estáticos del frontend porque el sitemap necesita los
slugs publicados de la base, y porque ambos requieren la URL pública absoluta del
sitio, que solo se conoce en runtime (hoy una IP, mañana un dominio). Nginx expone
/robots.txt y /sitemap.xml en la raíz y los proxea a estas dos vistas.
"""

from xml.sax.saxutils import escape

from django.http import HttpResponse
from django.views.decorators.http import require_http_methods

from .models import Evento

# Rutas estáticas del SPA: (path, prioridad, frecuencia de cambio).
RUTAS_PUBLICAS = [
    ('/', '1.0', 'weekly'),
    ('/servicios', '0.9', 'monthly'),
    ('/portafolio', '0.9', 'weekly'),
    ('/quienes-somos', '0.6', 'yearly'),
    ('/faq', '0.6', 'monthly'),
    ('/terminos-y-condiciones', '0.3', 'yearly'),
    ('/politica-de-privacidad', '0.3', 'yearly'),
]

RUTAS_PRIVADAS = ['/admin', '/gracias']


def _primer_valor(cabecera):
    """La petición pasa por dos proxies (nginx y el BFF), así que las cabeceras
    X-Forwarded-* pueden llegar como lista: "https,http". El valor original del
    cliente es siempre el primero."""
    return cabecera.split(',')[0].strip() if cabecera else ''


def _base_url(request):
    """Origen público del sitio, respetando el proxy (nginx → express → django)."""
    esquema = _primer_valor(request.headers.get('X-Forwarded-Proto')) or request.scheme
    host = _primer_valor(request.headers.get('X-Forwarded-Host')) or request.get_host()
    return f'{esquema}://{host}'


@require_http_methods(['GET', 'HEAD'])
def robots_txt(request):
    base = _base_url(request)
    lineas = ['User-agent: *', 'Allow: /']
    lineas += [f'Disallow: {ruta}' for ruta in RUTAS_PRIVADAS]
    lineas += ['', f'Sitemap: {base}/sitemap.xml', '']
    return HttpResponse('\n'.join(lineas), content_type='text/plain; charset=utf-8')


@require_http_methods(['GET', 'HEAD'])
def sitemap_xml(request):
    base = _base_url(request)
    urls = [
        (f'{base}{ruta}', None, prioridad, frecuencia)
        for ruta, prioridad, frecuencia in RUTAS_PUBLICAS
    ]

    eventos = Evento.objects.filter(publicado=True).order_by('-fecha_realizacion')
    urls += [
        (f'{base}/portafolio/{evento.slug}', evento.created_at, '0.7', 'monthly')
        for evento in eventos
    ]

    cuerpo = []
    for loc, lastmod, prioridad, frecuencia in urls:
        cuerpo.append('  <url>')
        cuerpo.append(f'    <loc>{escape(loc)}</loc>')
        if lastmod:
            cuerpo.append(f'    <lastmod>{lastmod.date().isoformat()}</lastmod>')
        cuerpo.append(f'    <changefreq>{frecuencia}</changefreq>')
        cuerpo.append(f'    <priority>{prioridad}</priority>')
        cuerpo.append('  </url>')

    xml = (
        '<?xml version="1.0" encoding="UTF-8"?>\n'
        '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
        + '\n'.join(cuerpo)
        + '\n</urlset>\n'
    )
    return HttpResponse(xml, content_type='application/xml; charset=utf-8')
