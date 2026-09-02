import logging

from django.conf import settings
from django.core.mail import send_mail

logger = logging.getLogger(__name__)


def enviar_notificacion_cotizacion(cotizacion):
    """Notifica al admin de una nueva cotizacion con formato HTML enriquecido y footer corporativo.

    Un fallo de envio nunca debe romper la creacion de la cotizacion: se loguea y se descarta.
    """
    destino = settings.ADMIN_NOTIFICATION_EMAIL
    if not destino or not settings.EMAIL_HOST:
        return

    # Mensaje en texto plano como respaldo
    cuerpo_texto = (
        f"NUEVA SOLICITUD DE COTIZACIÓN - ORION STAGE\n\n"
        f"Detalles de la Solicitud:\n"
        f"----------------------------------------\n"
        f"Nombre: {cotizacion.nombre}\n"
        f"Email: {cotizacion.email}\n"
        f"Teléfono: {cotizacion.telefono or '-'}\n"
        f"Empresa: {cotizacion.empresa or '-'}\n"
        f"Tipo de Evento: {str(cotizacion.tipo_evento).capitalize()}\n"
        f"Fecha Estimada: {cotizacion.fecha_estimada or '-'}\n"
        f"Presupuesto Estimado: {cotizacion.presupuesto_estimado or '-'}\n\n"
        f"Descripción del Evento:\n"
        f"{cotizacion.descripcion}\n\n"
        f"----------------------------------------\n"
        f"ID de Solicitud: {cotizacion.id}\n"
        f"Fecha de Registro: {cotizacion.created_at}\n"
        f"Orion Stage Producciones · https://orionstage.cl\n"
    )

    # Mensaje HTML enriquecido estilo Light corporativo
    cuerpo_html = f"""<!DOCTYPE html>
<html lang="es">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Nueva Cotización - Orion Stage</title>
</head>
<body style="margin:0; padding:0; background-color:#f1f5f9; font-family:'Helvetica Neue', Helvetica, Arial, sans-serif; color:#1e293b;">
  <table role="presentation" width="100%" cellspacing="0" cellpadding="0" style="background-color:#f1f5f9; padding:24px 12px;">
    <tr>
      <td align="center">
        <table role="presentation" width="100%" style="max-width:600px; background-color:#ffffff; border-radius:12px; overflow:hidden; box-shadow:0 4px 16px rgba(0,0,0,0.06); border:1px solid #e2e8f0;">
          <!-- HEADER -->
          <tr>
            <td style="background-color:#002855; padding:28px 32px; text-align:center;">
              <h1 style="margin:0; font-size:22px; font-weight:700; color:#ffffff; letter-spacing:1px;">
                ORION STAGE
              </h1>
              <p style="margin:4px 0 0 0; font-size:12px; color:#d06c26; font-weight:600; text-transform:uppercase; letter-spacing:1.5px;">
                Experiencias · Tecnología de Escenario · Producción
              </p>
            </td>
          </tr>

          <!-- CONTENIDO -->
          <tr>
            <td style="padding:32px;">
              <div style="display:inline-block; background-color:#e0f2fe; color:#0369a1; font-size:11px; font-weight:700; text-transform:uppercase; letter-spacing:0.8px; padding:4px 10px; border-radius:6px; margin-bottom:16px;">
                Nueva Cotización Web
              </div>
              
              <h2 style="margin:0 0 16px 0; font-size:18px; color:#0f172a; font-weight:700;">
                Has recibido una nueva solicitud de cotización
              </h2>
              
              <p style="margin:0 0 20px 0; font-size:14px; color:#475569; line-height:1.6;">
                Un cliente ha completado el formulario de cotización a través de la plataforma web. A continuación se detallan los datos enviados:
              </p>

              <!-- TABLA DE DETALLES -->
              <table width="100%" cellspacing="0" cellpadding="0" style="border-collapse:collapse; margin-bottom:24px;">
                <tr style="background-color:#f8fafc; border-bottom:1px solid #e2e8f0;">
                  <td style="padding:10px 14px; font-size:13px; font-weight:600; color:#475569; width:38%;">Nombre del Cliente</td>
                  <td style="padding:10px 14px; font-size:13px; font-weight:700; color:#0f172a;">{cotizacion.nombre}</td>
                </tr>
                <tr style="border-bottom:1px solid #e2e8f0;">
                  <td style="padding:10px 14px; font-size:13px; font-weight:600; color:#475569;">Correo Electrónico</td>
                  <td style="padding:10px 14px; font-size:13px; color:#0284c7;">
                    <a href="mailto:{cotizacion.email}" style="color:#0284c7; text-decoration:none; font-weight:600;">{cotizacion.email}</a>
                  </td>
                </tr>
                <tr style="background-color:#f8fafc; border-bottom:1px solid #e2e8f0;">
                  <td style="padding:10px 14px; font-size:13px; font-weight:600; color:#475569;">Teléfono / WhatsApp</td>
                  <td style="padding:10px 14px; font-size:13px; font-weight:600; color:#0f172a;">{cotizacion.telefono or 'No especificado'}</td>
                </tr>
                <tr style="border-bottom:1px solid #e2e8f0;">
                  <td style="padding:10px 14px; font-size:13px; font-weight:600; color:#475569;">Empresa / Organización</td>
                  <td style="padding:10px 14px; font-size:13px; font-weight:600; color:#0f172a;">{cotizacion.empresa or 'No especificada'}</td>
                </tr>
                <tr style="background-color:#f8fafc; border-bottom:1px solid #e2e8f0;">
                  <td style="padding:10px 14px; font-size:13px; font-weight:600; color:#475569;">Tipo de Evento</td>
                  <td style="padding:10px 14px; font-size:13px; font-weight:700; color:#002855; text-transform:capitalize;">{cotizacion.tipo_evento}</td>
                </tr>
                <tr style="border-bottom:1px solid #e2e8f0;">
                  <td style="padding:10px 14px; font-size:13px; font-weight:600; color:#475569;">Fecha Estimada</td>
                  <td style="padding:10px 14px; font-size:13px; font-weight:600; color:#0f172a;">{cotizacion.fecha_estimada or 'Por coordinar'}</td>
                </tr>
                <tr style="background-color:#f8fafc;">
                  <td style="padding:10px 14px; font-size:13px; font-weight:600; color:#475569;">Presupuesto Estimado</td>
                  <td style="padding:10px 14px; font-size:13px; font-weight:700; color:#16a34a;">{cotizacion.presupuesto_estimado or 'A evaluar'}</td>
                </tr>
              </table>

              <!-- DESCRIPCIÓN DEL EVENTO -->
              <h3 style="margin:0 0 8px 0; font-size:14px; color:#0f172a; font-weight:700;">
                Descripción y Requerimientos del Evento:
              </h3>
              <div style="background-color:#f8fafc; border-left:4px solid #002855; padding:14px 16px; border-radius:0 8px 8px 0; font-size:13.5px; line-height:1.7; color:#334155; margin-bottom:24px; white-space:pre-wrap;">
{cotizacion.descripcion}
              </div>

              <!-- ACCIONES RÁPIDAS -->
              <table width="100%" cellspacing="0" cellpadding="0">
                <tr>
                  <td align="center">
                    <a href="mailto:{cotizacion.email}?subject=Respuesta%20a%20tu%20cotizaci%C3%B3n%20en%20Orion%20Stage" style="display:inline-block; background-color:#002855; color:#ffffff; text-decoration:none; font-size:13px; font-weight:600; padding:10px 22px; border-radius:6px; margin-right:8px;">
                      Responder por Correo
                    </a>
                  </td>
                </tr>
              </table>
            </td>
          </tr>

          <!-- FOOTER CORPORATIVO ORION STAGE -->
          <tr>
            <td style="background-color:#f8fafc; border-top:1px solid #e2e8f0; padding:24px 32px; text-align:center;">
              <p style="margin:0 0 6px 0; font-size:13px; font-weight:700; color:#002855;">
                Orion Stage Producciones SpA
              </p>
              <p style="margin:0 0 8px 0; font-size:12px; color:#64748b;">
                Producción Técnica & Integral de Eventos · Santiago, Chile
              </p>
              <p style="margin:0 0 12px 0; font-size:12px; color:#64748b;">
                <a href="https://orionstage.cl" style="color:#0284c7; text-decoration:none; font-weight:600;">orionstage.cl</a> | 
                <a href="mailto:contacto@orionstage.cl" style="color:#0284c7; text-decoration:none;">contacto@orionstage.cl</a> | 
                <a href="https://wa.me/56998249498" style="color:#16a34a; text-decoration:none; font-weight:600;">+56 9 9824 9498</a>
              </p>
              <p style="margin:0; font-size:11px; color:#94a3b8;">
                Este correo fue generado automáticamente por la plataforma web de Orion Stage (ID: {cotizacion.id}).
              </p>
            </td>
          </tr>
        </table>
      </td>
    </tr>
  </table>
</body>
</html>"""

    try:
        send_mail(
            subject=f"Nueva cotización: {cotizacion.nombre} ({str(cotizacion.tipo_evento).capitalize()})",
            message=cuerpo_texto,
            html_message=cuerpo_html,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[destino],
            fail_silently=False,
        )
    except Exception:
        logger.exception("Falló el envío de notificación de la cotización %s", cotizacion.id)
