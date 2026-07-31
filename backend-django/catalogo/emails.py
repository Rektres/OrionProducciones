import logging

from django.conf import settings
from django.core.mail import send_mail

logger = logging.getLogger(__name__)


def enviar_notificacion_cotizacion(cotizacion):
    """Notifica al admin de una nueva cotizacion. No-op si no hay SMTP configurado.

    Un fallo de envio nunca debe romper la creacion de la cotizacion (ya guardada
    en la BD antes de llamar esta funcion): se loguea y se descarta.
    """
    destino = settings.ADMIN_NOTIFICATION_EMAIL
    if not destino or not settings.EMAIL_HOST:
        return

    cuerpo = (
        f'Nueva cotización recibida\n\n'
        f'Nombre: {cotizacion.nombre}\n'
        f'Email: {cotizacion.email}\n'
        f'Teléfono: {cotizacion.telefono or "-"}\n'
        f'Empresa: {cotizacion.empresa or "-"}\n'
        f'Tipo de evento: {cotizacion.tipo_evento}\n'
        f'Fecha estimada: {cotizacion.fecha_estimada or "-"}\n'
        f'Presupuesto estimado: {cotizacion.presupuesto_estimado or "-"}\n\n'
        f'Descripción:\n{cotizacion.descripcion}\n\n'
        f'ID: {cotizacion.id}\n'
        f'Recibida: {cotizacion.created_at}\n'
    )

    try:
        send_mail(
            subject=f'Nueva cotización: {cotizacion.nombre} ({cotizacion.tipo_evento})',
            message=cuerpo,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[destino],
            fail_silently=False,
        )
    except Exception:
        logger.exception('Fallo el envio de notificacion de la cotizacion %s', cotizacion.id)
