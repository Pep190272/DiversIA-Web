"""
Sistema de correo electrónico fiable para DiversIA
Alternativa a SendGrid usando SMTP nativo y servicios más confiables
"""

import os
import smtplib
import logging
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime
from typing import Optional, Dict, Any

# Configurar logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class ReliableEmailService:
    """Servicio de email confiable con múltiples opciones"""
    
    def __init__(self):
        self.setup_email_config()
    
    def setup_email_config(self):
        """Configurar proveedores de email disponibles"""
        self.email_configs = {
            'gmail': {
                'smtp_server': 'smtp.gmail.com',
                'smtp_port': 587,
                'requires_app_password': True
            },
            'outlook': {
                'smtp_server': 'smtp-mail.outlook.com',
                'smtp_port': 587,
                'requires_app_password': False
            },
            'mailgun': {
                'smtp_server': 'smtp.mailgun.org',
                'smtp_port': 587,
                'requires_app_password': False
            }
        }
        
        # Configuración por defecto
        self.from_email = 'diversiaeternals@gmail.com'
        self.from_name = 'DiversIA'
        
    def send_email_smtp(self, to_email: str, subject: str, html_content: str, 
                       text_content: Optional[str] = None, provider: str = 'gmail') -> bool:
        """Enviar email usando SMTP directo"""
        try:
            # Obtener credenciales de entorno
            email_user = os.getenv('EMAIL_USER', self.from_email)
            email_password = os.getenv('EMAIL_PASSWORD')
            
            if not email_password:
                logger.warning("EMAIL_PASSWORD no configurada. Email no enviado.")
                return False
            
            # Configuración del proveedor
            config = self.email_configs.get(provider, self.email_configs['gmail'])
            
            # Crear mensaje
            message = MIMEMultipart('alternative')
            message['From'] = f"{self.from_name} <{email_user}>"
            message['To'] = to_email
            message['Subject'] = subject
            
            # Añadir contenido
            if text_content:
                text_part = MIMEText(text_content, 'plain', 'utf-8')
                message.attach(text_part)
            
            html_part = MIMEText(html_content, 'html', 'utf-8')
            message.attach(html_part)
            
            # Enviar email
            with smtplib.SMTP(config['smtp_server'], config['smtp_port']) as server:
                server.starttls()
                server.login(email_user, email_password)
                server.send_message(message)
            
            logger.info(f"✅ Email enviado exitosamente a {to_email}")
            return True
            
        except Exception as e:
            logger.error(f"❌ Error enviando email SMTP: {e}")
            return False
    
    def send_contact_notification(self, nombre: str, email: str, asunto: str, mensaje: str) -> bool:
        """Enviar notificación de contacto al equipo DiversIA"""
        
        html_content = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <meta charset="utf-8">
            <title>Nuevo mensaje de contacto - DiversIA</title>
            <style>
                body {{ font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; line-height: 1.6; color: #333; margin: 0; padding: 0; }}
                .container {{ max-width: 600px; margin: 0 auto; background: #ffffff; }}
                .header {{ background: linear-gradient(135deg, #6366F1, #8B5CF6); color: white; padding: 30px 20px; text-align: center; }}
                .content {{ padding: 30px 20px; }}
                .contact-box {{ background: #f8f9ff; border-left: 4px solid #6366F1; padding: 20px; margin: 20px 0; border-radius: 5px; }}
                .message-box {{ background: #fff7ed; border: 1px solid #fed7aa; padding: 20px; border-radius: 8px; margin: 20px 0; }}
                .footer {{ background: #f3f4f6; padding: 20px; text-align: center; color: #6b7280; }}
                .button {{ display: inline-block; background: #6366F1; color: white; padding: 12px 24px; text-decoration: none; border-radius: 6px; margin: 10px 0; }}
                .timestamp {{ color: #6b7280; font-size: 14px; }}
            </style>
        </head>
        <body>
            <div class="container">
                <div class="header">
                    <h1>🔔 Nuevo Mensaje de Contacto</h1>
                    <p>DiversIA - Sistema de Notificaciones</p>
                </div>
                
                <div class="content">
                    <div class="contact-box">
                        <h3>📋 Información del Contacto</h3>
                        <p><strong>Nombre:</strong> {nombre}</p>
                        <p><strong>Email:</strong> <a href="mailto:{email}">{email}</a></p>
                        <p><strong>Asunto:</strong> {asunto}</p>
                        <p class="timestamp"><strong>Fecha:</strong> {datetime.now().strftime('%d/%m/%Y %H:%M')}</p>
                    </div>
                    
                    <div class="message-box">
                        <h3>💬 Mensaje:</h3>
                        <p>{mensaje}</p>
                    </div>
                    
                    <div style="text-align: center; margin: 30px 0;">
                        <a href="mailto:{email}?subject=Re: {asunto}" class="button">
                            Responder Directamente
                        </a>
                        <a href="#" class="button" style="background: #10b981;">
                            Ver en CRM
                        </a>
                    </div>
                    
                    <div style="background: #ecfdf5; padding: 15px; border-radius: 6px; margin: 20px 0;">
                        <p><strong>✅ Acción automática:</strong> Este contacto se ha añadido automáticamente al CRM para seguimiento.</p>
                    </div>
                </div>
                
                <div class="footer">
                    <p>Este es un mensaje automático del sistema DiversIA</p>
                    <p>📧 diversiaeternals@gmail.com | 🌐 diversia.app</p>
                </div>
            </div>
        </body>
        </html>
        """
        
        text_content = f"""
        Nuevo mensaje de contacto - DiversIA
        
        Información del contacto:
        - Nombre: {nombre}
        - Email: {email}
        - Asunto: {asunto}
        - Fecha: {datetime.now().strftime('%d/%m/%Y %H:%M')}
        
        Mensaje:
        {mensaje}
        
        Este contacto se ha añadido automáticamente al CRM.
        """
        
        subject = f"🔔 Nuevo mensaje de contacto: {asunto}"
        
        return self.send_email_smtp(
            to_email='diversiaeternals@gmail.com',
            subject=subject,
            html_content=html_content,
            text_content=text_content
        )
    
    def send_form_submission_notification(self, form_type: str, data: Dict[str, Any]) -> bool:
        """Enviar notificación de nuevo registro de formulario"""
        
        nombre = data.get('nombre', 'Usuario')
        email = data.get('email', 'Sin email')
        tipo_neurodivergencia = data.get('tipo_neurodivergencia', 'No especificado')
        
        html_content = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <meta charset="utf-8">
            <title>Nuevo registro {form_type} - DiversIA</title>
            <style>
                body {{ font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; line-height: 1.6; color: #333; }}
                .container {{ max-width: 600px; margin: 0 auto; background: #ffffff; }}
                .header {{ background: linear-gradient(135deg, #10b981, #059669); color: white; padding: 30px 20px; text-align: center; }}
                .content {{ padding: 30px 20px; }}
                .data-box {{ background: #f0fdf4; border-left: 4px solid #10b981; padding: 20px; margin: 20px 0; border-radius: 5px; }}
                .highlight {{ background: #ddd6fe; padding: 15px; border-radius: 6px; margin: 15px 0; }}
            </style>
        </head>
        <body>
            <div class="container">
                <div class="header">
                    <h1>🎉 Nuevo Registro: {form_type.upper()}</h1>
                    <p>DiversIA - Sistema de Captación</p>
                </div>
                
                <div class="content">
                    <div class="highlight">
                        <strong>📝 Nuevo perfil registrado en la plataforma</strong><br>
                        Usuario interesado en oportunidades laborales inclusivas.
                    </div>
                    
                    <div class="data-box">
                        <h3>Información básica:</h3>
                        <p><strong>Nombre:</strong> {nombre}</p>
                        <p><strong>Email:</strong> <a href="mailto:{email}">{email}</a></p>
                        <p><strong>Tipo:</strong> {tipo_neurodivergencia}</p>
                        <p><strong>Formulario:</strong> {form_type}</p>
                        <p><strong>Fecha:</strong> {datetime.now().strftime('%d/%m/%Y %H:%M')}</p>
                    </div>
                    
                    <div style="text-align: center; margin: 30px 0;">
                        <p><strong>Próximos pasos recomendados:</strong></p>
                        <ul style="text-align: left; display: inline-block;">
                            <li>Revisar perfil completo en el CRM</li>
                            <li>Evaluar compatibilidad con ofertas activas</li>
                            <li>Contactar para bienvenida personalizada</li>
                        </ul>
                    </div>
                </div>
            </div>
        </body>
        </html>
        """
        
        subject = f"🎉 Nuevo registro {form_type}: {nombre}"
        
        return self.send_email_smtp(
            to_email='diversiaeternals@gmail.com',
            subject=subject,
            html_content=html_content
        )
    
    def test_email_connection(self) -> Dict[str, Any]:
        """Probar la conexión de email"""
        test_results = {
            'gmail': False,
            'outlook': False,
            'message': 'Configuración de EMAIL_PASSWORD requerida'
        }
        
        email_password = os.getenv('EMAIL_PASSWORD')
        if not email_password:
            return test_results
        
        # Probar Gmail
        try:
            config = self.email_configs['gmail']
            with smtplib.SMTP(config['smtp_server'], config['smtp_port']) as server:
                server.starttls()
                server.login(os.getenv('EMAIL_USER', self.from_email), email_password)
                test_results['gmail'] = True
        except Exception as e:
            logger.info(f"Gmail no disponible: {e}")
        
        # Probar Outlook
        try:
            config = self.email_configs['outlook']
            with smtplib.SMTP(config['smtp_server'], config['smtp_port']) as server:
                server.starttls()
                test_results['outlook'] = True
        except Exception as e:
            logger.info(f"Outlook no disponible: {e}")
        
        if test_results['gmail'] or test_results['outlook']:
            test_results['message'] = 'Servicios de email disponibles'
        
        return test_results

# Instancia global del servicio
email_service = ReliableEmailService()

def send_contact_notification(nombre: str, email: str, asunto: str, mensaje: str) -> bool:
    """Función principal para enviar notificaciones de contacto"""
    return email_service.send_contact_notification(nombre, email, asunto, mensaje)

def send_form_notification(form_type: str, data: Dict[str, Any]) -> bool:
    """Función principal para enviar notificaciones de formulario"""
    return email_service.send_form_submission_notification(form_type, data)

def test_email_service() -> Dict[str, Any]:
    """Función para probar el servicio de email"""
    return email_service.test_email_connection()

print("✅ Sistema de email fiable inicializado")
print("🔧 Configuración requerida: EMAIL_USER y EMAIL_PASSWORD como variables de entorno")
print("📧 Email por defecto: diversiaeternals@gmail.com")