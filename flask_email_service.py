"""
Servicio de emails automáticos para DiversIA (Flask)
Sistema que envía emails de bienvenida y notificaciones usando Gmail
"""

import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.utils import formataddr
import logging
from datetime import datetime

logger = logging.getLogger(__name__)

class DiversiaEmailService:
    def __init__(self):
        self.gmail_user = os.environ.get("GMAIL_USER")
        self.gmail_password = os.environ.get("GMAIL_APP_PASSWORD")
        self.is_configured = bool(self.gmail_user and self.gmail_password)
        
        if self.is_configured:
            print("✅ Servicio de emails Gmail configurado correctamente")
        else:
            print("❌ Servicio de emails NO configurado - faltan credenciales Gmail")

    def send_email(self, to_email, subject, html_content, text_content=None):
        """Enviar email usando Gmail SMTP"""
        if not self.is_configured:
            logger.error("❌ Gmail no configurado - no se puede enviar email")
            return False

        try:
            # Crear mensaje
            msg = MIMEMultipart('alternative')
            msg['From'] = formataddr(('DiversIA', self.gmail_user))
            msg['To'] = to_email
            msg['Subject'] = subject

            # Agregar contenido de texto plano si se proporciona
            if text_content:
                text_part = MIMEText(text_content, 'plain', 'utf-8')
                msg.attach(text_part)

            # Agregar contenido HTML
            html_part = MIMEText(html_content, 'html', 'utf-8')
            msg.attach(html_part)

            # Conectar y enviar
            with smtplib.SMTP('smtp.gmail.com', 587) as server:
                server.starttls()
                server.login(self.gmail_user, self.gmail_password)
                server.send_message(msg)

            logger.info(f"✅ Email enviado exitosamente a {to_email}")
            return True

        except Exception as e:
            logger.error(f"❌ Error enviando email a {to_email}: {e}")
            return False

    def send_welcome_email_user(self, nombre, email, tipo_neurodivergencia=None):
        """Email de bienvenida para usuarios neurodivergentes"""
        tipo_texto = f" con {tipo_neurodivergencia}" if tipo_neurodivergencia else ""
        
        subject = f"🌟 ¡Bienvenid@ {nombre} a DiversIA!"
        
        html_content = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <meta charset="utf-8">
            <style>
                body {{ font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; line-height: 1.6; color: #333; margin: 0; padding: 0; }}
                .container {{ max-width: 600px; margin: 0 auto; padding: 20px; }}
                .header {{ background: linear-gradient(135deg, #6366f1 0%, #4f46e5 100%); color: white; padding: 30px; text-align: center; border-radius: 10px 10px 0 0; }}
                .content {{ background: #ffffff; padding: 30px; border-radius: 0 0 10px 10px; box-shadow: 0 4px 6px rgba(0,0,0,0.1); }}
                .highlight {{ background: #f0f9ff; padding: 20px; border-radius: 8px; border-left: 4px solid #6366f1; margin: 20px 0; }}
                .button {{ background: #6366f1; color: white; padding: 12px 25px; text-decoration: none; border-radius: 5px; display: inline-block; margin: 20px 0; }}
                .footer {{ text-align: center; color: #666; font-size: 14px; margin-top: 30px; }}
                ul {{ margin: 15px 0; padding-left: 20px; }}
                li {{ margin: 8px 0; }}
            </style>
        </head>
        <body>
            <div class="container">
                <div class="header">
                    <h1>🌟 ¡Bienvenid@ a DiversIA!</h1>
                    <p>Donde tu manera única de pensar es tu mayor fortaleza</p>
                </div>
                <div class="content">
                    <h2>Hola {nombre},</h2>
                    <p>¡Nos emociona que hayas decidido formar parte de DiversIA{tipo_texto}! Tu registro marca el inicio de un camino hacia oportunidades laborales increíbles.</p>
                    
                    <div class="highlight">
                        <h3>✨ ¿Qué viene ahora?</h3>
                        <ul>
                            <li>Nuestro equipo revisará tu perfil personalizado</li>
                            <li>Te conectaremos con empresas que valoran tu potencial único</li>
                            <li>Recibirás oportunidades laborales diseñadas para ti</li>
                            <li>Te acompañaremos en todo el proceso de búsqueda</li>
                        </ul>
                    </div>

                    <h3>🎯 En DiversIA creemos que:</h3>
                    <ul>
                        <li>✅ Tu neurodivergencia es una ventaja competitiva</li>
                        <li>✅ Mereces un ambiente de trabajo que te potencie</li>
                        <li>✅ Las mejores empresas están buscando talento como tú</li>
                        <li>✅ Tienes habilidades únicas que el mundo necesita</li>
                    </ul>

                    <p>Nos pondremos en contacto pronto para conocerte mejor y entender cómo podemos ayudarte a encontrar la oportunidad perfecta.</p>

                    <a href="mailto:diversiaeternals@gmail.com" class="button">¿Preguntas? Escríbenos</a>

                    <p><strong>¡Bienvenid@ a tu futuro profesional!</strong></p>
                </div>
                <div class="footer">
                    <p>DiversIA - Conectando talento neurodivergente con oportunidades extraordinarias</p>
                </div>
            </div>
        </body>
        </html>
        """

        text_content = f"""
Hola {nombre},

¡Bienvenid@ a DiversIA{tipo_texto}!

Nos emociona que hayas decidido formar parte de nuestra comunidad. Tu registro marca el inicio de un camino hacia oportunidades laborales increíbles.

¿Qué viene ahora?
- Nuestro equipo revisará tu perfil personalizado
- Te conectaremos con empresas que valoran tu potencial único
- Recibirás oportunidades laborales diseñadas para ti
- Te acompañaremos en todo el proceso de búsqueda

En DiversIA creemos que:
✅ Tu neurodivergencia es una ventaja competitiva
✅ Mereces un ambiente de trabajo que te potencie
✅ Las mejores empresas están buscando talento como tú
✅ Tienes habilidades únicas que el mundo necesita

Nos pondremos en contacto pronto para conocerte mejor.

¡Bienvenid@ a tu futuro profesional!

DiversIA - Conectando talento neurodivergente con oportunidades extraordinarias
        """

        return self.send_email(email, subject, html_content, text_content)

    def send_welcome_email_company(self, nombre_empresa, email, sector, tamano=None):
        """Email de bienvenida para empresas"""
        subject = f"🤝 ¡Bienvenida {nombre_empresa} a DiversIA!"
        
        tamano_text = f" ({tamano})" if tamano else ""
        
        html_content = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <meta charset="utf-8">
            <style>
                body {{ font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; line-height: 1.6; color: #333; margin: 0; padding: 0; }}
                .container {{ max-width: 600px; margin: 0 auto; padding: 20px; }}
                .header {{ background: linear-gradient(135deg, #2563eb 0%, #1d4ed8 100%); color: white; padding: 30px; text-align: center; border-radius: 10px 10px 0 0; }}
                .content {{ background: #ffffff; padding: 30px; border-radius: 0 0 10px 10px; box-shadow: 0 4px 6px rgba(0,0,0,0.1); }}
                .highlight {{ background: #eff6ff; padding: 20px; border-radius: 8px; border-left: 4px solid #2563eb; margin: 20px 0; }}
                .button {{ background: #2563eb; color: white; padding: 12px 25px; text-decoration: none; border-radius: 5px; display: inline-block; margin: 20px 0; }}
                .footer {{ text-align: center; color: #666; font-size: 14px; margin-top: 30px; }}
                ul {{ margin: 15px 0; padding-left: 20px; }}
                li {{ margin: 8px 0; }}
            </style>
        </head>
        <body>
            <div class="container">
                <div class="header">
                    <h1>🤝 ¡Bienvenida {nombre_empresa} a DiversIA!</h1>
                    <p>Juntos construiremos un futuro laboral más inclusivo</p>
                </div>
                <div class="content">
                    <h2>Estimado equipo de {nombre_empresa},</h2>
                    <p>¡Nos emociona enormemente que <strong>{nombre_empresa}</strong> haya decidido unirse a DiversIA! Su compromiso con la inclusión laboral marca la diferencia en la vida de personas con neurodivergencia.</p>
                    
                    <div class="highlight">
                        <h3>💼 ¿Qué viene ahora para {nombre_empresa}?</h3>
                        <ul>
                            <li>Nuestro equipo revisará el perfil específico de {nombre_empresa}</li>
                            <li>Identificaremos candidatos que encajen perfectamente con la cultura de {nombre_empresa}</li>
                            <li>Les presentaremos talento neurodivergente excepcional para {nombre_empresa}</li>
                            <li>Les apoyaremos en todo el proceso de inclusión en {nombre_empresa}</li>
                        </ul>
                    </div>

                    <h3>🎯 Beneficios de contratar talento neurodivergente:</h3>
                    <ul>
                        <li>✅ Diversidad de pensamiento e innovación</li>
                        <li>✅ Habilidades únicas y especializadas</li>
                        <li>✅ Alta atención al detalle y precisión</li>
                        <li>✅ Lealtad y compromiso excepcional</li>
                        <li>✅ Perspectivas frescas para resolver problemas</li>
                    </ul>

                    <p><strong>Sector de {nombre_empresa}:</strong> {sector}{tamano_text}</p>

                    <p>Nos pondremos en contacto pronto para discutir cómo DiversIA puede ayudar específicamente a <strong>{nombre_empresa}</strong> a encontrar el talento tecnológico neurodivergente perfecto para sus proyectos e innovaciones.</p>
                    
                    <p>Sabemos que el sector de <strong>{sector}</strong> necesita perfiles únicos con habilidades especializadas, y en DiversIA tenemos candidatos excepcionales que pueden aportar exactamente lo que {nombre_empresa} está buscando.</p>

                    <a href="mailto:diversiaeternals@gmail.com" class="button">Contáctanos para más información</a>

                    <p><strong>¡Gracias por apostar por la inclusión!</strong></p>
                </div>
                <div class="footer">
                    <p>DiversIA - Conectando empresas comprometidas con talento excepcional</p>
                </div>
            </div>
        </body>
        </html>
        """

        return self.send_email(email, subject, html_content)

    def send_welcome_email_association(self, nombre_asociacion, email, contacto_nombre, pais):
        """Email de bienvenida para asociaciones neurodivergentes"""
        subject = f"🤝 Bienvenida a DiversIA - {nombre_asociacion}"
        
        html_content = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <meta charset="utf-8">
            <style>
                body {{ font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; line-height: 1.6; color: #333; margin: 0; padding: 0; }}
                .container {{ max-width: 600px; margin: 0 auto; padding: 20px; }}
                .header {{ background: linear-gradient(135deg, #059669 0%, #047857 100%); color: white; padding: 30px; text-align: center; border-radius: 10px 10px 0 0; }}
                .content {{ background: #ffffff; padding: 30px; border-radius: 0 0 10px 10px; box-shadow: 0 4px 6px rgba(0,0,0,0.1); }}
                .highlight {{ background: #ecfdf5; padding: 20px; border-radius: 8px; border-left: 4px solid #059669; margin: 20px 0; }}
                .button {{ background: #059669; color: white; padding: 12px 25px; text-decoration: none; border-radius: 5px; display: inline-block; margin: 20px 0; }}
                .footer {{ text-align: center; color: #666; font-size: 14px; margin-top: 30px; }}
                ul {{ margin: 15px 0; padding-left: 20px; }}
                li {{ margin: 8px 0; }}
            </style>
        </head>
        <body>
            <div class="container">
                <div class="header">
                    <h1>🤝 ¡Bienvenida a la Red DiversIA!</h1>
                    <p>Juntos fortalecemos la comunidad neurodivergente</p>
                </div>
                <div class="content">
                    <h2>Estimado/a {contacto_nombre},</h2>
                    <p>¡Es un honor recibir a <strong>{nombre_asociacion}</strong> en la red de DiversIA! Su solicitud ha sido recibida y valoramos enormemente su compromiso con la comunidad neurodivergente.</p>
                    
                    <div class="highlight">
                        <h3>📋 ¿Qué sigue ahora?</h3>
                        <ul>
                            <li>Nuestro equipo revisará su documentación en los próximos días</li>
                            <li>Verificaremos que {nombre_asociacion} cumple con nuestros estándares</li>
                            <li>Les contactaremos para coordinar la integración completa</li>
                            <li>Una vez aprobada, aparecerán en nuestro directorio oficial</li>
                        </ul>
                    </div>

                    <h3>🌟 Beneficios de formar parte de DiversIA:</h3>
                    <ul>
                        <li>✅ Visibilidad en nuestra plataforma nacional</li>
                        <li>✅ Conexión con otras asociaciones comprometidas</li>
                        <li>✅ Acceso a recursos especializados</li>
                        <li>✅ Participación en eventos y programas conjuntos</li>
                        <li>✅ Red de apoyo profesional continuo</li>
                    </ul>

                    <p><strong>País:</strong> {pais}</p>

                    <p>Nos pondremos en contacto pronto para avanzar en el proceso de verificación.</p>

                    <a href="mailto:diversiaeternals@gmail.com" class="button">¿Preguntas? Contáctanos</a>

                    <p><strong>¡Gracias por fortalecer nuestra comunidad!</strong></p>
                </div>
                <div class="footer">
                    <p>DiversIA - Conectando y fortaleciendo la comunidad neurodivergente</p>
                </div>
            </div>
        </body>
        </html>
        """

        text_content = f"""
Estimado/a {contacto_nombre},

¡Es un honor recibir a {nombre_asociacion} en la red de DiversIA!

Su solicitud ha sido recibida y valoramos enormemente su compromiso con la comunidad neurodivergente.

¿Qué sigue ahora?
- Nuestro equipo revisará su documentación en los próximos días
- Verificaremos que {nombre_asociacion} cumple con nuestros estándares
- Les contactaremos para coordinar la integración completa
- Una vez aprobada, aparecerán en nuestro directorio oficial

Beneficios de formar parte de DiversIA:
✅ Visibilidad en nuestra plataforma nacional
✅ Conexión con otras asociaciones comprometidas  
✅ Acceso a recursos especializados
✅ Participación en eventos y programas conjuntos
✅ Red de apoyo profesional continuo

País: {pais}

Nos pondremos en contacto pronto para avanzar en el proceso de verificación.

¡Gracias por fortalecer nuestra comunidad!

DiversIA - Conectando y fortaleciendo la comunidad neurodivergente
        """

        return self.send_email(email, subject, html_content, text_content)

    def send_notification_email(self, tipo, datos):
        """Enviar email de notificación a DiversIA"""
        diversia_email = "diversiaeternals@gmail.com"
        
        if tipo == "usuario":
            subject = f"🔔 Nuevo registro: {datos.get('nombre', 'Usuario')} - {datos.get('tipo_neurodivergencia', 'General')}"
            content = f"""
            <h2>🆕 Nuevo Usuario Registrado</h2>
            <p><strong>Nombre:</strong> {datos.get('nombre', '')} {datos.get('apellidos', '')}</p>
            <p><strong>Email:</strong> {datos.get('email', '')}</p>
            <p><strong>Teléfono:</strong> {datos.get('telefono', 'No proporcionado')}</p>
            <p><strong>Ciudad:</strong> {datos.get('ciudad', '')}</p>
            <p><strong>Tipo de Neurodivergencia:</strong> {datos.get('tipo_neurodivergencia', 'No especificado')}</p>
            <p><strong>Fecha de Registro:</strong> {datetime.now().strftime('%d/%m/%Y %H:%M')}</p>
            <hr>
            <p>¡Nueva oportunidad de hacer matching!</p>
            """
        elif tipo == "empresa":
            subject = f"🏢 Nueva empresa: {datos.get('nombre_empresa', 'Empresa')}"
            content = f"""
            <h2>🏢 Nueva Empresa Registrada</h2>
            <p><strong>Empresa:</strong> {datos.get('nombre_empresa', '')}</p>
            <p><strong>Email:</strong> {datos.get('email_contacto', '')}</p>
            <p><strong>Teléfono:</strong> {datos.get('telefono', 'No proporcionado')}</p>
            <p><strong>Sector:</strong> {datos.get('sector', '')}</p>
            <p><strong>Tamaño:</strong> {datos.get('tamano_empresa', '')}</p>
            <p><strong>Ciudad:</strong> {datos.get('ciudad', '')}</p>
            <p><strong>Fecha de Registro:</strong> {datetime.now().strftime('%d/%m/%Y %H:%M')}</p>
            <hr>
            <p>¡Nueva oportunidad de colaboración empresarial!</p>
            """
        elif tipo == "asociacion":
            subject = f"🏛️ Nueva asociación: {datos.get('nombre_asociacion', 'Asociación')}"
            content = f"""
            <h2>🏛️ Nueva Asociación Registrada</h2>
            <p><strong>Asociación:</strong> {datos.get('nombre_asociacion', '')}</p>
            <p><strong>Email:</strong> {datos.get('email', '')}</p>
            <p><strong>País:</strong> {datos.get('pais', '')}</p>
            <p><strong>Contacto:</strong> {datos.get('contacto_nombre', '')}</p>
            <p><strong>Fecha de Registro:</strong> {datetime.now().strftime('%d/%m/%Y %H:%M')}</p>
            <hr>
            <p>¡Nueva oportunidad de alianza estratégica!</p>
            """
        else:
            return False

        return self.send_email(diversia_email, subject, content)

# Instancia global del servicio
email_service = DiversiaEmailService()

def test_email_service():
    """Función para probar el servicio de emails"""
    return email_service.send_email(
        "diversiaeternals@gmail.com",
        "🧪 Test de Sistema de Emails - DiversIA",
        "<h1>✅ Sistema de emails funcionando correctamente</h1><p>Este es un email de prueba.</p>",
        "✅ Sistema de emails funcionando correctamente\n\nEste es un email de prueba."
    )