import uuid
from django.db import models


class CategoriaServicio(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    nombre = models.TextField()
    slug = models.TextField(unique=True)
    orden = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'categorias_servicio'


class Servicio(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    categoria = models.ForeignKey(
        CategoriaServicio, on_delete=models.SET_NULL, null=True,
        db_column='categoria_id', related_name='servicios',
    )
    categoria_slug = models.TextField(null=True, blank=True)
    nombre = models.TextField()
    descripcion_corta = models.TextField()
    descripcion_larga = models.TextField()
    imagen = models.TextField(null=True, blank=True)
    icono_svg = models.TextField(null=True, blank=True)
    activo = models.BooleanField(default=True)
    orden = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'servicios'


class EventoTipo(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    nombre = models.TextField()
    slug = models.TextField(unique=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'evento_tipos'


class Evento(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    nombre = models.TextField()
    slug = models.TextField(unique=True)
    tipo = models.ForeignKey(
        EventoTipo, on_delete=models.SET_NULL, null=True,
        db_column='tipo_id', related_name='eventos',
    )
    tipo_slug = models.TextField(null=True, blank=True)
    cliente = models.TextField()
    descripcion_corta = models.TextField()
    descripcion_larga = models.TextField()
    imagen_destacada = models.TextField(null=True, blank=True)
    fecha_realizacion = models.DateField()
    lugar = models.TextField()
    asistentes = models.IntegerField(null=True, blank=True)
    destacado = models.BooleanField(default=False)
    publicado = models.BooleanField(default=True)
    orden = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'eventos'


class FotoEvento(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    evento = models.ForeignKey(
        Evento, on_delete=models.CASCADE,
        db_column='evento_id', related_name='fotos',
    )
    imagen = models.TextField()
    descripcion = models.TextField(null=True, blank=True)
    orden = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'fotos_evento'


class Tag(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    nombre = models.TextField()
    slug = models.TextField(unique=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'tags'


class Post(models.Model):
    ESTADOS = [('borrador', 'borrador'), ('revision', 'revision'), ('publicado', 'publicado')]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    titulo = models.TextField()
    slug = models.TextField(unique=True)
    imagen_destacada = models.TextField(null=True, blank=True)
    extracto = models.TextField()
    contenido = models.TextField()
    estado = models.TextField(choices=ESTADOS, default='borrador')
    fecha_publicacion = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    tags = models.ManyToManyField(Tag, through='PostTag', related_name='posts')

    class Meta:
        db_table = 'posts'


class PostTag(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    post = models.ForeignKey(Post, on_delete=models.CASCADE, db_column='post_id')
    tag = models.ForeignKey(Tag, on_delete=models.CASCADE, db_column='tag_id')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'post_tags'
        unique_together = (('post', 'tag'),)


class Cotizacion(models.Model):
    TIPOS = [('corporativo', 'corporativo'), ('social', 'social'),
             ('festival', 'festival'), ('otro', 'otro')]
    ESTADOS = [('nuevo', 'nuevo'), ('en_contacto', 'en_contacto'),
               ('cotizado', 'cotizado'), ('cerrado', 'cerrado'), ('descartado', 'descartado')]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    nombre = models.TextField()
    email = models.TextField()
    telefono = models.TextField(null=True, blank=True)
    empresa = models.TextField(null=True, blank=True)
    tipo_evento = models.TextField(choices=TIPOS)
    descripcion = models.TextField()
    fecha_estimada = models.DateField(null=True, blank=True)
    presupuesto_estimado = models.TextField(null=True, blank=True)
    estado = models.TextField(choices=ESTADOS, default='nuevo')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'cotizaciones'
