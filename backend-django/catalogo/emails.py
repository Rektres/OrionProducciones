import logging

from django.conf import settings
from django.core.mail import send_mail

logger = logging.getLogger(__name__)


def enviar_notificacion_cotizacion(cotizacion):
    """Notifica al admin de una nueva cotizacion y envia confirmacion al cliente con formato HTML.

    Un fallo de envio nunca debe romper la creacion de la cotizacion: se loguea y se descarta.
    """
    if not settings.EMAIL_HOST:
        return

    destino_admin = settings.ADMIN_NOTIFICATION_EMAIL

    # 1. NOTIFICACIÓN AL ADMINISTRADOR
    if destino_admin:
        cuerpo_admin_texto = (
            f"¡HOLA EQUIPO ORION! NUEVA SOLICITUD DE COTIZACIÓN\n\n"
            f"Un cliente acaba de escribirnos a través del sitio web:\n"
            f"----------------------------------------\n"
            f"Nombre: {cotizacion.nombre}\n"
            f"Email: {cotizacion.email}\n"
            f"Teléfono: {cotizacion.telefono or 'No especificado'}\n"
            f"Empresa: {cotizacion.empresa or 'No especificada'}\n"
            f"Tipo de Evento: {str(cotizacion.tipo_evento).capitalize()}\n"
            f"Fecha Estimada: {cotizacion.fecha_estimada or 'A coordinar'}\n"
            f"Presupuesto: {cotizacion.presupuesto_estimado or 'A evaluar'}\n\n"
            f"Mensaje del Cliente:\n"
            f"{cotizacion.descripcion}\n\n"
            f"----------------------------------------\n"
            f"ID de Solicitud: {cotizacion.id}\n"
            f"Orion Stage Producciones - https://orionstage.cl\n"
        )

        cuerpo_admin_html = f"""<!DOCTYPE html>
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
        <table role="presentation" width="100%" style="max-width:600px; background-color:#ffffff; border-radius:14px; overflow:hidden; box-shadow:0 4px 16px rgba(0,0,0,0.06); border:1px solid #e2e8f0;">
          <tr>
            <td style="background-color:#002855; padding:26px 32px; text-align:center;">
              <h1 style="margin:0; font-size:22px; font-weight:700; color:#ffffff; letter-spacing:1px;">
                ORION STAGE
              </h1>
              <p style="margin:4px 0 0 0; font-size:12px; color:#d06c26; font-weight:600; text-transform:uppercase; letter-spacing:1.5px;">
                Experiencias | Tecnología de Escenario | Producción
              </p>
            </td>
          </tr>
          <tr>
            <td style="padding:32px;">
              <div style="display:inline-block; background-color:#e0f2fe; color:#0369a1; font-size:11px; font-weight:700; text-transform:uppercase; letter-spacing:0.8px; padding:4px 10px; border-radius:6px; margin-bottom:16px;">
                Nueva Cotización desde la Web
              </div>
              <h2 style="margin:0 0 14px 0; font-size:18px; color:#0f172a; font-weight:700;">
                ¡Hola equipo! Ha llegado un nuevo requerimiento
              </h2>
              <p style="margin:0 0 20px 0; font-size:14px; color:#475569; line-height:1.6;">
                <strong>{cotizacion.nombre}</strong> nos ha dejado una solicitud de cotización para un evento ({str(cotizacion.tipo_evento).capitalize()}). Aquí tienes el resumen para responderle:
              </p>
              <table width="100%" cellspacing="0" cellpadding="0" style="border-collapse:collapse; margin-bottom:24px;">
                <tr style="background-color:#f8fafc; border-bottom:1px solid #e2e8f0;">
                  <td style="padding:10px 14px; font-size:13px; font-weight:600; color:#475569; width:38%;">Cliente</td>
                  <td style="padding:10px 14px; font-size:13px; font-weight:700; color:#0f172a;">{cotizacion.nombre}</td>
                </tr>
                <tr style="border-bottom:1px solid #e2e8f0;">
                  <td style="padding:10px 14px; font-size:13px; font-weight:600; color:#475569;">Correo</td>
                  <td style="padding:10px 14px; font-size:13px; color:#0284c7;">
                    <a href="mailto:{cotizacion.email}" style="color:#0284c7; text-decoration:none; font-weight:600;">{cotizacion.email}</a>
                  </td>
                </tr>
                <tr style="background-color:#f8fafc; border-bottom:1px solid #e2e8f0;">
                  <td style="padding:10px 14px; font-size:13px; font-weight:600; color:#475569;">Teléfono / WhatsApp</td>
                  <td style="padding:10px 14px; font-size:13px; font-weight:600; color:#0f172a;">{cotizacion.telefono or 'No especificado'}</td>
                </tr>
                <tr style="border-bottom:1px solid #e2e8f0;">
                  <td style="padding:10px 14px; font-size:13px; font-weight:600; color:#475569;">Empresa</td>
                  <td style="padding:10px 14px; font-size:13px; font-weight:600; color:#0f172a;">{cotizacion.empresa or 'No indicada'}</td>
                </tr>
                <tr style="background-color:#f8fafc; border-bottom:1px solid #e2e8f0;">
                  <td style="padding:10px 14px; font-size:13px; font-weight:600; color:#475569;">Tipo de Evento</td>
                  <td style="padding:10px 14px; font-size:13px; font-weight:700; color:#002855; text-transform:capitalize;">{cotizacion.tipo_evento}</td>
                </tr>
                <tr style="border-bottom:1px solid #e2e8f0;">
                  <td style="padding:10px 14px; font-size:13px; font-weight:600; color:#475569;">Fecha Estimada</td>
                  <td style="padding:10px 14px; font-size:13px; font-weight:600; color:#0f172a;">{cotizacion.fecha_estimada or 'A coordinar'}</td>
                </tr>
                <tr style="background-color:#f8fafc;">
                  <td style="padding:10px 14px; font-size:13px; font-weight:600; color:#475569;">Presupuesto</td>
                  <td style="padding:10px 14px; font-size:13px; font-weight:700; color:#16a34a;">{cotizacion.presupuesto_estimado or 'A evaluar'}</td>
                </tr>
              </table>
              <h3 style="margin:0 0 8px 0; font-size:14px; color:#0f172a; font-weight:700;">
                Mensaje o Requerimientos:
              </h3>
              <div style="background-color:#f8fafc; border-left:4px solid #002855; padding:14px 16px; border-radius:0 8px 8px 0; font-size:13.5px; line-height:1.7; color:#334155; margin-bottom:24px; white-space:pre-wrap;">
{cotizacion.descripcion}
              </div>
              <table width="100%" cellspacing="0" cellpadding="0">
                <tr>
                  <td align="center">
                    <a href="mailto:{cotizacion.email}?subject=Respuesta%20a%20tu%20cotizaci%C3%B3n%20en%20Orion%20Stage" style="display:inline-block; background-color:#002855; color:#ffffff; text-decoration:none; font-size:13px; font-weight:600; padding:11px 24px; border-radius:8px; margin-right:8px;">
                      Responder al Cliente
                    </a>
                  </td>
                </tr>
              </table>
            </td>
          </tr>
          <tr>
            <td style="background-color:#f8fafc; border-top:1px solid #e2e8f0; padding:22px 32px; text-align:center;">
              <p style="margin:0 0 4px 0; font-size:13px; font-weight:700; color:#002855;">
                Orion Stage Producciones
              </p>
              <p style="margin:0 0 8px 0; font-size:12px; color:#64748b;">
                Santiago, Chile | <a href="https://orionstage.cl" style="color:#0284c7; text-decoration:none;">orionstage.cl</a>
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
                message=cuerpo_admin_texto,
                html_message=cuerpo_admin_html,
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[destino_admin],
                fail_silently=False,
            )
        except Exception:
            logger.exception("Falló el envío de notificación de la cotización %s al administrador", cotizacion.id)

    # 2. CONFIRMACIÓN AUTOMÁTICA Y HUMANIZADA AL CLIENTE
    if cotizacion.email:
        cuerpo_cliente_texto = (
            f"¡HOLA {cotizacion.nombre.upper()}! QUÉ GUSTO SALUDARTE - ORION STAGE\n\n"
            f"Muchas gracias por escribirnos y pensar en Orion Stage para tu evento ({cotizacion.tipo_evento}).\n\n"
            f"Ya recibimos tu mensaje y estamos revisando todos los detalles con mucho entusiasmo para preparar una propuesta diseñada a tu medida.\n\n"
            f"Resumen de lo que nos enviaste:\n"
            f"----------------------------------------\n"
            f"- Tipo de Evento: {str(cotizacion.tipo_evento).capitalize()}\n"
            f"- Fecha Estimada: {cotizacion.fecha_estimada or 'A coordinar juntos'}\n"
            f"- Teléfono: {cotizacion.telefono or '-'}\n"
            f"- Presupuesto: {cotizacion.presupuesto_estimado or 'A evaluar juntos'}\n"
            f"- Mensaje:\n{cotizacion.descripcion}\n\n"
            f"¿Cómo seguimos? Un productor de nuestro equipo se pondrá en contacto contigo en un plazo máximo de 24 horas hábiles.\n\n"
            f"Si prefieres avanzar más rápido o contarnos más detalles, ¡escríbenos directamente a nuestro WhatsApp! (+56 9 9824 9498)\n\n"
            f"¡Un gran saludo!\n"
            f"Equipo Orion Stage Producciones\n"
            f"https://orionstage.cl\n"
        )

        cuerpo_cliente_html = f"""<!DOCTYPE html>
<html lang="es">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>¡Hola! Recibimos tu cotización - Orion Stage</title>
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

          <!-- CONTENIDO HUMANIZADO -->
          <tr>
            <td style="padding:32px;">
              <div style="display:inline-block; background-color:#dcfce7; color:#15803d; font-size:11px; font-weight:700; text-transform:uppercase; letter-spacing:0.8px; padding:4px 10px; border-radius:6px; margin-bottom:16px;">
                ✓ Solicitud Recibida
              </div>
              
              <h2 style="margin:0 0 14px 0; font-size:20px; color:#0f172a; font-weight:700;">
                ¡Hola {cotizacion.nombre}! Qué alegría saludarte.
              </h2>
              
              <p style="margin:0 0 16px 0; font-size:14.5px; color:#475569; line-height:1.7;">
                Muchas gracias por escribirnos y pensar en <strong>Orion Stage</strong> para tu próximo evento. Ya recibimos tu solicitud y estamos revisando los detalles para armar una propuesta impecable y a la medida de tu equipo.
              </p>

              <!-- CAJA RESUMEN -->
              <div style="background-color:#f8fafc; border:1px solid #e2e8f0; border-radius:10px; padding:20px; margin-bottom:24px;">
                <h3 style="margin:0 0 12px 0; font-size:13px; font-weight:700; color:#002855; text-transform:uppercase; letter-spacing:0.5px;">
                  Lo que nos compartiste:
                </h3>
                <table width="100%" cellspacing="0" cellpadding="0" style="border-collapse:collapse;">
                  <tr style="border-bottom:1px solid #e2e8f0;">
                    <td style="padding:7px 0; font-size:13px; color:#64748b; width:40%;">Tipo de Evento:</td>
                    <td style="padding:7px 0; font-size:13px; font-weight:700; color:#0f172a; text-transform:capitalize;">{cotizacion.tipo_evento}</td>
                  </tr>
                  <tr style="border-bottom:1px solid #e2e8f0;">
                    <td style="padding:7px 0; font-size:13px; color:#64748b;">Fecha Estimada:</td>
                    <td style="padding:7px 0; font-size:13px; font-weight:600; color:#0f172a;">{cotizacion.fecha_estimada or 'A coordinar juntos'}</td>
                  </tr>
                  <tr style="border-bottom:1px solid #e2e8f0;">
                    <td style="padding:7px 0; font-size:13px; color:#64748b;">Teléfono:</td>
                    <td style="padding:7px 0; font-size:13px; font-weight:600; color:#0f172a;">{cotizacion.telefono or 'No indicado'}</td>
                  </tr>
                  <tr>
                    <td style="padding:7px 0; font-size:13px; color:#64748b;">Presupuesto:</td>
                    <td style="padding:7px 0; font-size:13px; font-weight:700; color:#16a34a;">{cotizacion.presupuesto_estimado or 'A evaluar juntos'}</td>
                  </tr>
                </table>
              </div>

              <!-- PASOS SIGUIENTES -->
              <p style="margin:0 0 18px 0; font-size:14px; color:#475569; line-height:1.7;">
                Un productor de nuestro equipo se pondrá en contacto contigo en un plazo máximo de <strong>24 horas hábiles</strong> para afinar detalles y presentarte una cotización formal.
              </p>

              <!-- BOTÓN WHATSAPP -->
              <div style="background-color:#f0fdf4; border:1px solid #bbf7d0; border-radius:10px; padding:18px; text-align:center; margin-bottom:20px;">
                <p style="margin:0 0 12px 0; font-size:13.5px; color:#166534; font-weight:600;">
                  ¿Quieres avanzar más rápido o tienes dudas puntuales? ¡Conversemos directo!
                </p>
                <a href="https://wa.me/56998249498?text=Hola,%20acabo%20de%20escribirles%20por%20la%20web%20a%20nombre%20de%20{cotizacion.nombre}" style="display:inline-block; background-color:#16a34a; color:#ffffff; text-decoration:none; font-size:13.5px; font-weight:600; padding:11px 24px; border-radius:8px; box-shadow:0 2px 8px rgba(22,163,74,0.25);">
                  Escribirnos al WhatsApp (+56 9 9824 9498)
                </a>
              </div>

              <p style="margin:0; font-size:13.5px; color:#64748b; line-height:1.6;">
                ¡Un gran saludo y quedamos en contacto!<br>
                <strong style="color:#002855;">Equipo Orion Stage Producciones</strong>
              </p>
            </td>
          </tr>

          <!-- FOOTER -->
          <tr>
            <td style="background-color:#f8fafc; border-top:1px solid #e2e8f0; padding:22px 32px; text-align:center;">
              <p style="margin:0 0 6px 0; font-size:13px; font-weight:700; color:#002855;">
                Orion Stage Producciones SpA
              </p>
              <p style="margin:0 0 8px 0; font-size:12px; color:#64748b;">
                Producción Técnica & Integral de Eventos | Santiago, Chile
              </p>
              <p style="margin:0; font-size:12px; color:#64748b;">
                <a href="https://orionstage.cl" style="color:#0284c7; text-decoration:none; font-weight:600;">orionstage.cl</a> | 
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

        try:
            send_mail(
                subject=f"¡Hola {cotizacion.nombre}! Recibimos tu cotización — Orion Stage",
                message=cuerpo_cliente_texto,
                html_message=cuerpo_cliente_html,
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[cotizacion.email],
                fail_silently=False,
            )
        except Exception:
            logger.exception("Falló el envío de confirmación de la cotización %s al cliente %s", cotizacion.id, cotizacion.email)
