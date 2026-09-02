from django.utils import timezone
from rest_framework import serializers

from .models import CategoriaServicio, Cotizacion, Evento, EventoTipo, FotoEvento, Post, Servicio, Tag


class CategoriaServicioAdminSerializer(serializers.ModelSerializer):
    class Meta:
        model = CategoriaServicio
        fields = '__all__'


class EventoTipoAdminSerializer(serializers.ModelSerializer):
    class Meta:
        model = EventoTipo
        fields = '__all__'


class TagAdminSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = '__all__'


class ServicioAdminSerializer(serializers.ModelSerializer):
    imagen_url = serializers.SerializerMethodField()

    class Meta:
        model = Servicio
        fields = '__all__'
        read_only_fields = ('id', 'created_at', 'categoria_slug', 'imagen_archivo')

    def get_imagen_url(self, obj):
        if obj.imagen_archivo_id:
            return f'/api/imagenes/{obj.imagen_archivo_id}/'
        return obj.imagen

    def save(self, **kwargs):
        categoria = self.validated_data.get('categoria', getattr(self.instance, 'categoria', None))
        kwargs['categoria_slug'] = categoria.slug if categoria else None
        return super().save(**kwargs)


class FotoEventoAdminSerializer(serializers.ModelSerializer):
    imagen_url = serializers.SerializerMethodField()

    class Meta:
        model = FotoEvento
        fields = '__all__'
        read_only_fields = ('id', 'created_at', 'imagen_archivo', 'imagen')

    def get_imagen_url(self, obj):
        if obj.imagen_archivo_id:
            return f'/api/imagenes/{obj.imagen_archivo_id}/'
        return obj.imagen


class EventoAdminSerializer(serializers.ModelSerializer):
    fotos = FotoEventoAdminSerializer(many=True, read_only=True)
    imagen_url = serializers.SerializerMethodField()

    class Meta:
        model = Evento
        fields = '__all__'
        read_only_fields = ('id', 'created_at', 'tipo_slug', 'imagen_archivo')

    def get_imagen_url(self, obj):
        if obj.imagen_archivo_id:
            return f'/api/imagenes/{obj.imagen_archivo_id}/'
        return obj.imagen_destacada

    def save(self, **kwargs):
        tipo = self.validated_data.get('tipo', getattr(self.instance, 'tipo', None))
        kwargs['tipo_slug'] = tipo.slug if tipo else None
        return super().save(**kwargs)


class PostAdminSerializer(serializers.ModelSerializer):
    # M2M con through: DRF lo marca read_only por defecto si no se declara explicito.
    tags = serializers.PrimaryKeyRelatedField(many=True, queryset=Tag.objects.all(), required=False)
    imagen_url = serializers.SerializerMethodField()

    class Meta:
        model = Post
        fields = '__all__'
        read_only_fields = ('id', 'created_at', 'updated_at', 'imagen_archivo')

    def get_imagen_url(self, obj):
        if obj.imagen_archivo_id:
            return f'/api/imagenes/{obj.imagen_archivo_id}/'
        return obj.imagen_destacada

    def validate(self, attrs):
        estado = attrs.get('estado', getattr(self.instance, 'estado', None))
        fecha_publicacion = attrs.get('fecha_publicacion', getattr(self.instance, 'fecha_publicacion', None))
        if estado == 'publicado' and not fecha_publicacion:
            attrs['fecha_publicacion'] = timezone.now()
        return attrs


class CotizacionAdminSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cotizacion
        fields = '__all__'
        read_only_fields = ('id', 'created_at')


class CotizacionResponderSerializer(serializers.Serializer):
    asunto = serializers.CharField(max_length=255, required=True)
    mensaje = serializers.CharField(required=True)
    nuevo_estado = serializers.ChoiceField(
        choices=Cotizacion.ESTADOS,
        required=False,
        default='en_contacto'
    )

