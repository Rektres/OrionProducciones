import logging

from django.conf import settings
from django.core.mail import send_mail
from django.db.models import Q
from rest_framework import mixins, status, viewsets
from rest_framework.authentication import TokenAuthentication
from rest_framework.decorators import action
from rest_framework.parsers import JSONParser, MultiPartParser
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .admin_serializers import (
    CategoriaServicioAdminSerializer, CotizacionAdminSerializer, CotizacionResponderSerializer,
    EventoAdminSerializer, EventoTipoAdminSerializer, FotoEventoAdminSerializer,
    PostAdminSerializer, ServicioAdminSerializer, TagAdminSerializer,
)
from .imagenes import crear_imagen_archivo
from .models import CategoriaServicio, Cotizacion, CotizacionHistorial, Evento, EventoTipo, FotoEvento, ImagenArchivo, Post, Servicio, Tag

logger = logging.getLogger(__name__)



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


class CotizacionAdminViewSet(AdminViewSetBase):
    serializer_class = CotizacionAdminSerializer
    queryset = Cotizacion.objects.prefetch_related('historial').order_by('-created_at')

    def get_queryset(self):
        qs = Cotizacion.objects.prefetch_related('historial').order_by('-created_at')
        estado = self.request.query_params.get('estado')
        if estado:
            qs = qs.filter(estado=estado)
        search = self.request.query_params.get('search') or self.request.query_params.get('q')
        if search:
            search = search.strip()
            qs = qs.filter(
                Q(nombre__icontains=search) |
                Q(email__icontains=search) |
                Q(empresa__icontains=search) |
                Q(descripcion__icontains=search) |
                Q(tipo_evento__icontains=search)
            )
        return qs

    def perform_update(self, serializer):
        instance = self.get_object()
        prev_estado = instance.estado
        updated = serializer.save()
        nuevo_estado = updated.estado

        if prev_estado != nuevo_estado:
            user = self.request.user if self.request.user and self.request.user.is_authenticated else None
            username = user.username if user else 'Admin'
            CotizacionHistorial.objects.create(
                cotizacion=updated,
                usuario=user,
                usuario_nombre=username,
                tipo_accion='cambio_estado',
                estado_anterior=prev_estado,
                estado_nuevo=nuevo_estado,
                detalle=f'Estado modificado de "{prev_estado}" a "{nuevo_estado}" por {username}.',
            )

    @action(detail=True, methods=['post'], url_path='responder')
    def responder(self, request, pk=None):
        cotizacion = self.get_object()
        serializer = CotizacionResponderSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        asunto = serializer.validated_data['asunto'].strip()
        mensaje = serializer.validated_data['mensaje'].strip()
        nuevo_estado = serializer.validated_data.get('nuevo_estado') or 'en_contacto'

        if not cotizacion.email:
            return Response(
                {'error': 'La cotización no tiene una dirección de correo asociada.'},
                status=status.HTTP_400_BAD_REQUEST,
            )

        # Convert paragraphs and newlines to proper HTML paragraphs and <br>
        parrafos = [p.strip() for p in mensaje.split('\n\n') if p.strip()]
        parrafos_html = []
        for p in parrafos:
            lineas = [l for l in p.split('\n')]
            p_html = '<br>\n'.join(lineas)
            parrafos_html.append(f'<p style="margin:0 0 16px 0; font-size:15px; color:#334155; line-height:1.75;">{p_html}</p>')
        cuerpo_mensaje_html = '\n'.join(parrafos_html) if parrafos_html else f'<p style="margin:0 0 16px 0; font-size:15px; color:#334155; line-height:1.75;">{mensaje}</p>'

        cuerpo_html = f"""<!DOCTYPE html>
<html lang="es">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{asunto}</title>
</head>
<body style="margin:0; padding:0; background-color:#f1f5f9; font-family:'Helvetica Neue', Helvetica, Arial, sans-serif; color:#1e293b;">
  <table role="presentation" width="100%" cellspacing="0" cellpadding="0" style="background-color:#f1f5f9; padding:24px 12px;">
    <tr>
      <td align="center">
        <table role="presentation" width="100%" style="max-width:600px; background-color:#ffffff; border-radius:14px; overflow:hidden; box-shadow:0 4px 16px rgba(0,0,0,0.06); border:1px solid #e2e8f0;">
          <!-- HEADER -->
          <tr>
            <td style="background-color:#002855; padding:28px 32px; text-align:center;">
              <h1 style="margin:0; font-size:22px; font-weight:700; color:#ffffff; letter-spacing:1px;">
                ORION STAGE
              </h1>
              <p style="margin:4px 0 0 0; font-size:12px; color:#d06c26; font-weight:600; text-transform:uppercase; letter-spacing:1.5px;">
                Experiencias | Tecnología de Escenario | Producción
              </p>
            </td>
          </tr>

          <!-- CONTENIDO -->
          <tr>
            <td style="padding:32px;">
              <h2 style="margin:0 0 18px 0; font-size:19px; color:#0f172a; font-weight:700;">
                Hola {cotizacion.nombre},
              </h2>
              
              <div style="margin-bottom:24px;">
{cuerpo_mensaje_html}
              </div>

              <!-- CAJA RESUMEN REFERENCIAL -->
              <div style="background-color:#f8fafc; border:1px solid #e2e8f0; border-radius:10px; padding:16px; margin-bottom:24px;">
                <p style="margin:0 0 8px 0; font-size:12px; font-weight:700; color:#002855; text-transform:uppercase; letter-spacing:0.5px;">
                  En referencia a tu requerimiento ({cotizacion.tipo_evento}):
                </p>
                <p style="margin:0; font-size:13px; color:#64748b; font-style:italic;">
                  "{cotizacion.descripcion}"
                </p>
              </div>

              <!-- BOTÓN WHATSAPP -->
              <div style="background-color:#f0fdf4; border:1px solid #bbf7d0; border-radius:10px; padding:16px; text-align:center; margin-bottom:16px;">
                <p style="margin:0 0 10px 0; font-size:13px; color:#166534; font-weight:600;">
                  ¿Prefieres coordinar o responder por WhatsApp?
                </p>
                <a href="https://wa.me/56998249498?text=Hola,%20recib%C3%AD%20su%20correo%20respecto%20a%20mi%20cotizaci%C3%B3n%20a%20nombre%20de%20{cotizacion.nombre}" style="display:inline-block; background-color:#16a34a; color:#ffffff; text-decoration:none; font-size:13px; font-weight:600; padding:10px 22px; border-radius:8px; box-shadow:0 2px 8px rgba(22,163,74,0.25);">
                  Continuar en WhatsApp (+56 9 9824 9498)
                </a>
              </div>

              <p style="margin:0; font-size:13px; color:#64748b; line-height:1.6;">
                Atentamente,<br>
                <strong style="color:#002855;">Equipo de Producción Orion Stage</strong>
              </p>
            </td>
          </tr>

          <!-- FOOTER -->
          <tr>
            <td style="background-color:#f8fafc; border-top:1px solid #e2e8f0; padding:20px 32px; text-align:center;">
              <p style="margin:0 0 4px 0; font-size:12px; font-weight:700; color:#002855;">
                Orion Stage Producciones SpA
              </p>
              <p style="margin:0; font-size:11px; color:#64748b;">
                <a href="https://orionstage.cl" style="color:#0284c7; text-decoration:none;">orionstage.cl</a> | 
                <a href="mailto:contacto@orionstage.cl" style="color:#0284c7; text-decoration:none;">contacto@orionstage.cl</a>
              </p>
            </td>
          </tr>
        </table>
      </td>
    </tr>
  </table>
</body>
</html>"""

        from_email = 'Orion Stage <contacto@orionstage.cl>'

        try:
            send_mail(
                subject=asunto,
                message=f"Hola {cotizacion.nombre},\n\n{mensaje}\n\n--\nEquipo Orion Stage Producciones\nhttps://orionstage.cl",
                html_message=cuerpo_html,
                from_email=from_email,
                recipient_list=[cotizacion.email],
                fail_silently=False,
            )
        except Exception as e:
            logger.exception("Error enviando respuesta a cotizacion %s: %s", cotizacion.id, e)
            return Response(
                {'error': f'No se pudo enviar el correo: {str(e)}'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

        prev_estado = cotizacion.estado
        cotizacion.estado = nuevo_estado
        cotizacion.save(update_fields=['estado'])

        user = request.user if request.user and request.user.is_authenticated else None
        username = user.username if user else 'Admin'
        CotizacionHistorial.objects.create(
            cotizacion=cotizacion,
            usuario=user,
            usuario_nombre=username,
            tipo_accion='respuesta_correo',
            estado_anterior=prev_estado,
            estado_nuevo=nuevo_estado,
            detalle=f'Respuesta oficial enviada a {cotizacion.email} por {username}. Asunto: "{asunto}"',
        )

        # Recargar instancia fresca con historial completo
        cotizacion_fresca = Cotizacion.objects.prefetch_related('historial').get(pk=cotizacion.pk)

        return Response({
            'status': 'ok',
            'mensaje': f'Respuesta enviada exitosamente a {cotizacion.email}.',
            'cotizacion': CotizacionAdminSerializer(cotizacion_fresca).data,
        })



