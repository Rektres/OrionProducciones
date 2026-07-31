from rest_framework.exceptions import ValidationError

from .models import ImagenArchivo

TIPOS_IMAGEN_PERMITIDOS = {'image/jpeg', 'image/png', 'image/webp', 'image/gif'}
TAMANO_MAX_IMAGEN = 10 * 1024 * 1024

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

    return ImagenArchivo.objects.create(
        contenido=contenido,
        content_type=content_type,
        nombre_original=archivo.name,
        tamano=len(contenido),
    )
