from rest_framework import mixins, status, viewsets
from rest_framework.authentication import TokenAuthentication
from rest_framework.decorators import action
from rest_framework.parsers import JSONParser, MultiPartParser
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .admin_serializers import (
    CategoriaServicioAdminSerializer, EventoAdminSerializer, EventoTipoAdminSerializer,
    FotoEventoAdminSerializer, PostAdminSerializer, ServicioAdminSerializer, TagAdminSerializer,
)
from .imagenes import crear_imagen_archivo
from .models import CategoriaServicio, Evento, EventoTipo, FotoEvento, ImagenArchivo, Post, Servicio, Tag


class AdminViewSetBase(viewsets.ModelViewSet):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]


class ImagenArchivoMixin:
    """Agrega subir/quitar imagen a un ViewSet cuyo modelo tiene imagen_archivo FK."""

    @action(detail=True, methods=['post'], url_path='imagen', parser_classes=[MultiPartParser])
    def imagen(self, request, pk=None):
        obj = self.get_object()
        archivo = request.FILES.get('archivo')
        if archivo is None:
            return Response({'archivo': 'Falta el archivo.'}, status=status.HTTP_400_BAD_REQUEST)
        anterior_id = obj.imagen_archivo_id
        obj.imagen_archivo = crear_imagen_archivo(archivo)
        obj.save(update_fields=['imagen_archivo'])
        if anterior_id:
            ImagenArchivo.objects.filter(pk=anterior_id).delete()
        return Response(self.get_serializer(obj).data)

    @imagen.mapping.delete
    def quitar_imagen(self, request, pk=None):
        obj = self.get_object()
        anterior_id = obj.imagen_archivo_id
        obj.imagen_archivo = None
        obj.save(update_fields=['imagen_archivo'])
        if anterior_id:
            ImagenArchivo.objects.filter(pk=anterior_id).delete()
        return Response(self.get_serializer(obj).data)


class CategoriaServicioAdminViewSet(AdminViewSetBase):
    serializer_class = CategoriaServicioAdminSerializer
    queryset = CategoriaServicio.objects.order_by('orden')


class ServicioAdminViewSet(ImagenArchivoMixin, AdminViewSetBase):
    serializer_class = ServicioAdminSerializer
    queryset = Servicio.objects.order_by('orden')

    def perform_destroy(self, instance):
        imagen_id = instance.imagen_archivo_id
        instance.delete()
        if imagen_id:
            ImagenArchivo.objects.filter(pk=imagen_id).delete()


class EventoTipoAdminViewSet(AdminViewSetBase):
    serializer_class = EventoTipoAdminSerializer
    queryset = EventoTipo.objects.order_by('nombre')


class EventoAdminViewSet(ImagenArchivoMixin, AdminViewSetBase):
    serializer_class = EventoAdminSerializer
    queryset = Evento.objects.order_by('-fecha_realizacion')

    def perform_destroy(self, instance):
        imagen_ids = [instance.imagen_archivo_id]
        imagen_ids += list(instance.fotos.values_list('imagen_archivo_id', flat=True))
        instance.delete()
        ImagenArchivo.objects.filter(pk__in=[i for i in imagen_ids if i]).delete()

    @action(detail=True, methods=['get', 'post'], url_path='fotos',
            parser_classes=[MultiPartParser, JSONParser])
    def fotos(self, request, pk=None):
        evento = self.get_object()
        if request.method == 'GET':
            fotos = evento.fotos.order_by('orden')
            return Response(FotoEventoAdminSerializer(fotos, many=True).data)

        archivo = request.FILES.get('archivo')
        if archivo is None:
            return Response({'archivo': 'Falta el archivo.'}, status=status.HTTP_400_BAD_REQUEST)
        imagen = crear_imagen_archivo(archivo)
        try:
            orden = int(request.data.get('orden', 0))
        except (TypeError, ValueError):
            orden = 0
        foto = FotoEvento.objects.create(
            evento=evento,
            imagen_archivo=imagen,
            descripcion=request.data.get('descripcion') or None,
            orden=orden,
        )
        return Response(FotoEventoAdminSerializer(foto).data, status=status.HTTP_201_CREATED)


class FotoEventoAdminViewSet(mixins.ListModelMixin, mixins.UpdateModelMixin,
                              mixins.DestroyModelMixin, viewsets.GenericViewSet):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    serializer_class = FotoEventoAdminSerializer
    queryset = FotoEvento.objects.order_by('orden')

    def perform_destroy(self, instance):
        imagen_id = instance.imagen_archivo_id
        instance.delete()
        if imagen_id:
            ImagenArchivo.objects.filter(pk=imagen_id).delete()


class TagAdminViewSet(AdminViewSetBase):
    serializer_class = TagAdminSerializer
    queryset = Tag.objects.order_by('nombre')


class PostAdminViewSet(ImagenArchivoMixin, AdminViewSetBase):
    serializer_class = PostAdminSerializer
    queryset = Post.objects.order_by('-created_at')

    def perform_destroy(self, instance):
        imagen_id = instance.imagen_archivo_id
        instance.delete()
        if imagen_id:
            ImagenArchivo.objects.filter(pk=imagen_id).delete()
