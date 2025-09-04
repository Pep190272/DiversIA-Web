"""
Servicio de emails con SendGrid para DiversIA
Maneja el envío automático de emails de bienvenida
"""
import os
import sys
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail, Email, To, Content
from datetime import datetime

# Configuración de SendGrid
sendgrid_key = os.environ.get('SENDGRID_API_KEY')
if not sendgrid_key:
    print("❌ SENDGRID_API_KEY no encontrado en variables de entorno")
else:
    print("✅ SendGrid API Key configurado")

def send_welcome_email(user_name, user_email, unsubscribe_token=None):
    """
    Envía email de bienvenida personalizado a un nuevo usuario
    
    Args:
        user_name (str): Nombre completo del usuario
        user_email (str): Email del destinatario
        unsubscribe_token (str): Token único para darse de baja
    
    Returns:
        bool: True si se envió correctamente, False si falló
    """
    if not sendgrid_key:
        print("❌ No se puede enviar email: SendGrid API Key no configurado")
        return False
    
    try:
        sg = SendGridAPIClient(sendgrid_key)
        
        # URL de baja (opcional)
        unsubscribe_url = f"https://diversia.replit.app/unsubscribe?token={unsubscribe_token}" if unsubscribe_token else "#"
        
        # Contenido del email personalizado
        html_content = f"""
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>¡Bienvenido/a a DiversIA!</title>
    <style>
        body {{ font-family: Arial, sans-serif; line-height: 1.6; color: #333; }}
        .container {{ max-width: 600px; margin: 0 auto; padding: 20px; }}
        .header {{ background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; padding: 30px; text-align: center; border-radius: 10px 10px 0 0; }}
        .content {{ background: #f8f9fa; padding: 30px; border-radius: 0 0 10px 10px; }}
        .highlight {{ background: #e3f2fd; padding: 15px; border-left: 4px solid #2196f3; margin: 20px 0; }}
        .unsubscribe {{ font-size: 12px; color: #666; text-align: center; margin-top: 30px; }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>¡Hola {user_name}! 👋</h1>
            <p>Bienvenido/a a la comunidad DiversIA</p>
        </div>
        
        <div class="content">
            <h2>¡Gracias por unirte a nosotros!</h2>
            
            <p>Nos alegra enormemente que hayas decidido formar parte de <strong>DiversIA</strong>, la plataforma que conecta el talento neurodivergente con oportunidades laborales inclusivas.</p>
            
            <div class="highlight">
                <h3>📧 ¿Qué puedes esperar de nosotros?</h3>
                <ul>
                    <li><strong>Ofertas de empleo personalizadas</strong> que se adapten a tu perfil</li>
                    <li><strong>Información sobre empresas inclusivas</strong> comprometidas con la diversidad</li>
                    <li><strong>Recursos y consejos</strong> para el desarrollo profesional</li>
                    <li><strong>Noticias de la comunidad</strong> neurodivergente y eventos especiales</li>
                </ul>
            </div>
            
            <p>En DiversIA creemos firmemente que la <em>neurodiversidad es una fortaleza</em> que enriquece los equipos de trabajo y aporta perspectivas únicas e innovadoras.</p>
            
            <h3>🚀 Próximos pasos:</h3>
            <ol>
                <li>Completa tu perfil para recibir oportunidades más personalizadas</li>
                <li>Explora las empresas de nuestra red comprometidas con la inclusión</li>
                <li>Mantente atento/a a nuestros emails con ofertas exclusivas</li>
            </ol>
            
            <p>Si tienes alguna pregunta o necesitas ayuda, no dudes en contactarnos. Estamos aquí para apoyarte en tu camino profesional.</p>
            
            <p><strong>¡Bienvenido/a a DiversIA, donde tu diversidad es tu fortaleza!</strong> 🌟</p>
            
            <p>Atentamente,<br>
            <strong>El equipo de DiversIA</strong></p>
        </div>
        
        <div class="unsubscribe">
            <p>Si no deseas recibir más emails de DiversIA, puedes <a href="{unsubscribe_url}">darte de baja aquí</a>.</p>
            <p>Este email fue enviado automáticamente el {datetime.now().strftime('%d/%m/%Y a las %H:%M')}.</p>
        </div>
    </div>
</body>
</html>
        """
        
        # Versión texto plano
        text_content = f"""
¡Hola {user_name}!

Bienvenido/a a DiversIA, la plataforma que conecta el talento neurodivergente con oportunidades laborales inclusivas.

Te enviaremos información sobre:
- Ofertas de empleo personalizadas
- Empresas inclusivas comprometidas con la diversidad  
- Recursos para desarrollo profesional
- Noticias de nuestra comunidad

En DiversIA creemos que la neurodiversidad es una fortaleza que enriquece los equipos de trabajo.

¡Bienvenido/a a DiversIA, donde tu diversidad es tu fortaleza!

El equipo de DiversIA
        """
        
        message = Mail(
            from_email=Email("no-reply@diversia.es", "DiversIA"),
            to_emails=To(user_email),
            subject=f"¡Bienvenido/a a DiversIA, {user_name.split()[0]}! 🌟"
        )
        
        message.content = [
            Content("text/plain", text_content),
            Content("text/html", html_content)
        ]
        
        response = sg.send(message)
        
        print(f"✅ Email de bienvenida enviado a {user_name} ({user_email})")
        print(f"   Status Code: {response.status_code}")
        
        return True
        
    except Exception as e:
        print(f"❌ Error enviando email de bienvenida a {user_email}: {e}")
        return False

def send_notification_email(to_email, subject, content, user_name="Usuario"):
    """
    Envía un email de notificación genérico
    """
    if not sendgrid_key:
        print("❌ No se puede enviar email: SendGrid API Key no configurado")
        return False
    
    try:
        sg = SendGridAPIClient(sendgrid_key)
        
        message = Mail(
            from_email=Email("no-reply@diversia.es", "DiversIA"),
            to_emails=To(to_email),
            subject=subject,
            html_content=content
        )
        
        response = sg.send(message)
        print(f"✅ Email enviado a {to_email}: {subject}")
        return True
        
    except Exception as e:
        print(f"❌ Error enviando email: {e}")
        return False