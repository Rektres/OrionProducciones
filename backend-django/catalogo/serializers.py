from rest_framework import serializers
from .models import (
    CategoriaServicio, Servicio, EventoTipo, Evento, FotoEvento,
    Tag, Post, Cotizacion, ImagenArchivo,
)


class ImagenArchivoSerializer(serializers.ModelSerializer):
    class Meta:
        model = ImagenArchivo
        fields = ('id', 'content_type', 'nombre_original', 'tamano', 'created_at')


class CategoriaServicioSerializer(serializers.ModelSerializer):
    class Meta:
        model = CategoriaServicio
        fields = '__all__'


class ServicioSerializer(serializers.ModelSerializer):
    imagen_url = serializers.SerializerMethodField()

    class Meta:
        model = Servicio
        fields = '__all__'

    def get_imagen_url(self, obj):
        if obj.imagen_archivo_id:
            return f'/api/imagenes/{obj.imagen_archivo_id}/'
        return obj.imagen


class EventoTipoSerializer(serializers.ModelSerializer):
    class Meta:
        model = EventoTipo
        fields = '__all__'


class FotoEventoSerializer(serializers.ModelSerializer):
    imagen_url = serializers.SerializerMethodField()

    class Meta:
        model = FotoEvento
        fields = '__all__'

    def get_imagen_url(self, obj):
        if obj.imagen_archivo_id:
            return f'/api/imagenes/{obj.imagen_archivo_id}/'
        return obj.imagen


class EventoSerializer(serializers.ModelSerializer):
    fotos = FotoEventoSerializer(many=True, read_only=True)
    imagen_url = serializers.SerializerMethodField()

    class Meta:
        model = Evento
        fields = '__all__'

    def get_imagen_url(self, obj):
        if obj.imagen_archivo_id:
            return f'/api/imagenes/{obj.imagen_archivo_id}/'
        return obj.imagen_destacada


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = '__all__'


class PostSerializer(serializers.ModelSerializer):
    tags = TagSerializer(many=True, read_only=True)
    imagen_url = serializers.SerializerMethodField()

    class Meta:
        model = Post
        fields = '__all__'

    def get_imagen_url(self, obj):
        if obj.imagen_archivo_id:
            return f'/api/imagenes/{obj.imagen_archivo_id}/'
        return obj.imagen_destacada


class CotizacionSerializer(serializers.ModelSerializer):
    email = serializers.EmailField()
    fecha_estimada = serializers.DateField(required=False, allow_null=True)
    telefono = serializers.CharField(required=False, allow_blank=True, allow_null=True)
    empresa = serializers.CharField(required=False, allow_blank=True, allow_null=True)
    presupuesto_estimado = serializers.CharField(required=False, allow_blank=True, allow_null=True)

    class Meta:
        model = Cotizacion
        fields = '__all__'
        read_only_fields = ('id', 'estado', 'created_at')

    def to_internal_value(self, data):
        if isinstance(data, dict):
            data = data.copy()
            if data.get('fecha_estimada') == '':
                data['fecha_estimada'] = None
            if data.get('empresa') == '':
                data['empresa'] = None
            if data.get('telefono') == '':
                data['telefono'] = None
            if data.get('presupuesto_estimado') == '':
                data['presupuesto_estimado'] = None
        return super().to_internal_value(data)
