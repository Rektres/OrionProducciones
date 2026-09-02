from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django.views.decorators.http import require_http_methods
from rest_framework import generics
from rest_framework.throttling import AnonRateThrottle

from .emails import enviar_notificacion_cotizacion
from .imagenes import TIPOS_IMAGEN_PERMITIDOS
from .models import (
    CategoriaServicio, Servicio, EventoTipo, Evento, FotoEvento,
    Tag, Post, Cotizacion, CotizacionHistorial, ImagenArchivo,
)
from .serializers import (
    CategoriaServicioSerializer, ServicioSerializer, EventoTipoSerializer,
    EventoSerializer, FotoEventoSerializer, TagSerializer, PostSerializer,
    CotizacionSerializer,
)


class CategoriaServicioList(generics.ListAPIView):
    serializer_class = CategoriaServicioSerializer
    queryset = CategoriaServicio.objects.order_by('orden')


class ServicioList(generics.ListAPIView):
    serializer_class = ServicioSerializer

    def get_queryset(self):
        qs = Servicio.objects.filter(activo=True).order_by('orden')
        categoria = self.request.query_params.get('categoria')
        if categoria:
            qs = qs.filter(categoria_slug=categoria)
        return qs


class ServicioDetail(generics.RetrieveAPIView):
    serializer_class = ServicioSerializer
    queryset = Servicio.objects.filter(activo=True)


class EventoTipoList(generics.ListAPIView):
    serializer_class = EventoTipoSerializer
    queryset = EventoTipo.objects.order_by('nombre')


class EventoList(generics.ListAPIView):
    serializer_class = EventoSerializer

    def get_queryset(self):
        qs = Evento.objects.filter(publicado=True).order_by('-fecha_realizacion')
        tipo = self.request.query_params.get('tipo')
        if tipo:
            qs = qs.filter(tipo_slug=tipo)
        destacado = self.request.query_params.get('destacado')
        if destacado in ('true', 'false'):
            qs = qs.filter(destacado=(destacado == 'true'))
        return qs


class EventoDetail(generics.RetrieveAPIView):
    serializer_class = EventoSerializer
    lookup_field = 'slug'
    queryset = Evento.objects.filter(publicado=True)


class FotoEventoList(generics.ListAPIView):
    serializer_class = FotoEventoSerializer

    def get_queryset(self):
        return FotoEvento.objects.filter(evento_id=self.kwargs['pk']).order_by('orden')


class TagList(generics.ListAPIView):
    serializer_class = TagSerializer
    queryset = Tag.objects.order_by('nombre')


class PostList(generics.ListAPIView):
    serializer_class = PostSerializer

    def get_queryset(self):
        qs = Post.objects.filter(estado='publicado').order_by('-fecha_publicacion')
        tag = self.request.query_params.get('tag')
        if tag:
            qs = qs.filter(tags__slug=tag)
        try:
            offset = int(self.request.query_params.get('offset', 0))
            limit = int(self.request.query_params.get('limit', 9))
        except ValueError:
            offset, limit = 0, 9
        return qs[offset:offset + limit]


class PostDetail(generics.RetrieveAPIView):
    serializer_class = PostSerializer
    lookup_field = 'slug'
    queryset = Post.objects.filter(estado='publicado')


class CotizacionThrottle(AnonRateThrottle):
    scope = 'cotizacion'


class CotizacionCreate(generics.CreateAPIView):
    serializer_class = CotizacionSerializer
    queryset = Cotizacion.objects.all()
    throttle_classes = [CotizacionThrottle]

    def perform_create(self, serializer):
        cotizacion = serializer.save()
        CotizacionHistorial.objects.create(
            cotizacion=cotizacion,
            usuario_nombre='Web / Cliente',
            tipo_accion='creacion',
            estado_nuevo='nuevo',
            detalle=f'Cotización recibida desde el sitio web ({cotizacion.tipo_evento}).',
        )
        enviar_notificacion_cotizacion(cotizacion)



@require_http_methods(['GET', 'HEAD'])
def imagen_archivo_raw(request, pk):
    imagen = get_object_or_404(
        ImagenArchivo.objects.only('contenido', 'content_type', 'nombre_original'), pk=pk,
    )
    content_type = imagen.content_type if imagen.content_type in TIPOS_IMAGEN_PERMITIDOS else 'application/octet-stream'
    contenido = bytes(imagen.contenido)
    if request.method == 'HEAD':
        # Un HEAD no debe llevar body (RFC 9110). Sin esto gunicorn enviaba
        # igual los bytes de la imagen y el parser estricto de Node (BFF)
        # abortaba con "Parse Error: Data after `Connection: close`" -> 502.
        response = HttpResponse(b'', content_type=content_type)
        response['Content-Length'] = str(len(contenido))
    else:
        response = HttpResponse(contenido, content_type=content_type)
    response['Content-Disposition'] = 'inline'
    response['X-Content-Type-Options'] = 'nosniff'
    response['Cache-Control'] = 'public, max-age=31536000, immutable'
    return response
