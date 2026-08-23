import io
import os

from PIL import Image, UnidentifiedImageError
from rest_framework.exceptions import ValidationError

from .models import ImagenArchivo

TIPOS_IMAGEN_PERMITIDOS = {'image/jpeg', 'image/png', 'image/webp', 'image/gif'}
TAMANO_MAX_IMAGEN = 10 * 1024 * 1024

# Las imagenes viajan desde Postgres en cada carga de pagina, asi que se guardan ya
# optimizadas: reescaladas al lado maximo y recodificadas a WebP.
LADO_MAX = 1920
CALIDAD_WEBP = 82
# Los GIF pueden ser animados y Pillow no siempre conserva bien la animacion al
# recodificar: se guardan tal cual.
TIPOS_SIN_RECODIFICAR = {'image/gif'}

_FIRMAS = {
    'image/jpeg': lambda b: b[:3] == b'\xff\xd8\xff',
    'image/png': lambda b: b[:8] == b'\x89PNG\r\n\x1a\n',
    'image/gif': lambda b: b[:6] in (b'GIF87a', b'GIF89a'),
    'image/webp': lambda b: b[:4] == b'RIFF' and b[8:12] == b'WEBP',
}


def _firma_coincide(contenido, content_type):
    verificar = _FIRMAS.get(content_type)
    return verificar is not None and verificar(contenido)


def crear_imagen_archivo(archivo):
    """Valida un UploadedFile y crea el ImagenArchivo correspondiente."""
    if archivo.size > TAMANO_MAX_IMAGEN:
        raise ValidationError({'archivo': 'La imagen supera el tamaño máximo permitido (10MB).'})

    content_type = (archivo.content_type or '').split(';')[0].strip().lower()
    if not content_type.startswith('image/'):
        raise ValidationError({'archivo': 'El archivo no es una imagen.'})
    if content_type not in TIPOS_IMAGEN_PERMITIDOS:
        raise ValidationError({'archivo': 'Formato de imagen no soportado. Usa JPEG, PNG, WEBP o GIF.'})

    contenido = archivo.read()
    if not _firma_coincide(contenido, content_type):
        raise ValidationError({'archivo': 'El contenido del archivo no coincide con una imagen válida.'})

    contenido, content_type, nombre = _optimizar(contenido, content_type, archivo.name)

    return ImagenArchivo.objects.create(
        contenido=contenido,
        content_type=content_type,
        nombre_original=nombre,
        tamano=len(contenido),
    )


def _optimizar(contenido, content_type, nombre):
    """Reescala y recodifica a WebP. Devuelve (bytes, content_type, nombre)."""
    if content_type in TIPOS_SIN_RECODIFICAR:
        return contenido, content_type, nombre

    try:
        imagen = Image.open(io.BytesIO(contenido))
        imagen.load()
    except (UnidentifiedImageError, OSError):
        raise ValidationError({'archivo': 'No pudimos procesar la imagen. Prueba con otro archivo.'})

    if max(imagen.size) > LADO_MAX:
        imagen.thumbnail((LADO_MAX, LADO_MAX), Image.LANCZOS)

    if imagen.mode not in ('RGB', 'RGBA'):
        imagen = imagen.convert('RGBA' if 'A' in imagen.getbands() else 'RGB')

    buffer = io.BytesIO()
    imagen.save(buffer, format='WEBP', quality=CALIDAD_WEBP, method=6)
    optimizado = buffer.getvalue()

    # Si la recodificacion no mejora (imagenes chicas ya optimizadas), conserva el original.
    if len(optimizado) >= len(contenido) and max(imagen.size) <= LADO_MAX:
        return contenido, content_type, nombre

    return optimizado, 'image/webp', f'{os.path.splitext(nombre)[0]}.webp'
