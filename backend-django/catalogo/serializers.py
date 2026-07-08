from rest_framework import serializers
from .models import (
    CategoriaServicio, Servicio, EventoTipo, Evento, FotoEvento,
    Tag, Post, Cotizacion,
)


class CategoriaServicioSerializer(serializers.ModelSerializer):
    class Meta:
        model = CategoriaServicio
        fields = '__all__'


class ServicioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Servicio
        fields = '__all__'


class EventoTipoSerializer(serializers.ModelSerializer):
    class Meta:
        model = EventoTipo
        fields = '__all__'


class FotoEventoSerializer(serializers.ModelSerializer):
    class Meta:
        model = FotoEvento
        fields = '__all__'


class EventoSerializer(serializers.ModelSerializer):
    fotos = FotoEventoSerializer(many=True, read_only=True)

    class Meta:
        model = Evento
        fields = '__all__'


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = '__all__'


class PostSerializer(serializers.ModelSerializer):
    tags = TagSerializer(many=True, read_only=True)

    class Meta:
        model = Post
        fields = '__all__'


class CotizacionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cotizacion
        fields = '__all__'
        read_only_fields = ('id', 'estado', 'created_at')
