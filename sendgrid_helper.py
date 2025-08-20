import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

def send_email(to_email: str, subject: str, html_content: str, text_content: str = None):
    """
    Envía un email usando Gmail SMTP
    """
    gmail_user = os.environ.get('GMAIL_USER', 'diversiaeternals@gmail.com')
    gmail_password = os.environ.get('GMAIL_PASSWORD')
    
    if not gmail_password:
        print('Error: GMAIL_PASSWORD no está configurada')
        return False
    
    try:
        # Crear el mensaje
        msg = MIMEMultipart('alternative')
        msg['From'] = f'DiversIA Platform <{gmail_user}>'
        msg['To'] = to_email
        msg['Subject'] = subject
        
        # Añadir contenido
        if text_content:
            part1 = MIMEText(text_content, 'plain', 'utf-8')
            msg.attach(part1)
        
        if html_content:
            part2 = MIMEText(html_content, 'html', 'utf-8')
            msg.attach(part2)
        
        # Conectar con Gmail SMTP
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(gmail_user, gmail_password)
        
        # Enviar email
        text = msg.as_string()
        server.sendmail(gmail_user, to_email, text)
        server.quit()
        
        print(f"Email enviado exitosamente a {to_email}")
        return True
        
    except Exception as e:
        print(f"Error enviando email: {e}")
        return False

def send_contact_notification(nombre, email, asunto, mensaje):
    """
    Envía notificación de contacto desde el formulario
    """
    subject = f"Nuevo Mensaje de Contacto DiversIA - {asunto}"
    
    html_content = f"""
    <html>
    <head>
        <style>
            body {{ font-family: Arial, sans-serif; line-height: 1.6; color: #333; }}
            .header {{ background: linear-gradient(135deg, #6366F1, #8B5CF6); color: white; padding: 20px; text-align: center; }}
            .content {{ padding: 20px; }}
            .info-section {{ margin: 15px 0; padding: 15px; background: #f8f9fa; border-radius: 8px; }}
            .label {{ font-weight: bold; color: #495057; }}
            .value {{ margin-left: 10px; }}
        </style>
    </head>
    <body>
        <div class="header">
            <h1>💬 Nuevo Mensaje de Contacto</h1>
            <p>Desde el formulario web de DiversIA</p>
        </div>
        <div class="content">
            <div class="info-section">
                <h3>Información del Contacto</h3>
                <p><span class="label">Nombre:</span><span class="value">{nombre}</span></p>
                <p><span class="label">Email:</span><span class="value">{email}</span></p>
                <p><span class="label">Asunto:</span><span class="value">{asunto}</span></p>
            </div>
            
            <div class="info-section">
                <h3>Mensaje</h3>
                <p>{mensaje}</p>
            </div>
            
            <div class="info-section">
                <p><strong>Responder a:</strong> {email}</p>
                <p><em>Este mensaje fue enviado desde el formulario de contacto de DiversIA.</em></p>
            </div>
        </div>
    </body>
    </html>
    """
    
    return send_email('diversiaeternals@gmail.com', subject, html_content)

def send_registration_notification(user_data, registration_type="General"):
    """
    Envía notificación de nuevo registro a diversiaeternals@gmail.com
    """
    subject = f"Nuevo Registro DiversIA - {registration_type}"
    
    html_content = f"""
    <html>
    <head>
        <style>
            body {{ font-family: Arial, sans-serif; line-height: 1.6; color: #333; }}
            .header {{ background: linear-gradient(135deg, #6366F1, #8B5CF6); color: white; padding: 20px; text-align: center; }}
            .content {{ padding: 20px; }}
            .info-section {{ margin: 15px 0; padding: 15px; background: #f8f9fa; border-radius: 8px; }}
            .label {{ font-weight: bold; color: #495057; }}
            .value {{ margin-left: 10px; }}
        </style>
    </head>
    <body>
        <div class="header">
            <h1>🌟 Nuevo Registro en DiversIA</h1>
            <p>Tipo: {registration_type}</p>
        </div>
        <div class="content">
            <div class="info-section">
                <h3>Información Personal</h3>
                <p><span class="label">Nombre:</span><span class="value">{user_data.get('nombre', 'N/A')} {user_data.get('apellidos', '')}</span></p>
                <p><span class="label">Email:</span><span class="value">{user_data.get('email', 'N/A')}</span></p>
                <p><span class="label">Teléfono:</span><span class="value">{user_data.get('telefono', 'N/A')}</span></p>
                <p><span class="label">Ciudad:</span><span class="value">{user_data.get('ciudad', 'N/A')}</span></p>
                <p><span class="label">Fecha de Nacimiento:</span><span class="value">{user_data.get('fecha_nacimiento', 'N/A')}</span></p>
            </div>
            
            <div class="info-section">
                <h3>Información de Neurodivergencia</h3>
                <p><span class="label">Tipo:</span><span class="value">{user_data.get('tipo_neurodivergencia', 'N/A')}</span></p>
                <p><span class="label">Diagnóstico Formal:</span><span class="value">{'Sí' if user_data.get('diagnostico_formal') else 'No'}</span></p>
            </div>
            
            <div class="info-section">
                <h3>Información Laboral</h3>
                <p><span class="label">Experiencia:</span><span class="value">{user_data.get('experiencia_laboral', 'N/A')}</span></p>
                <p><span class="label">Formación:</span><span class="value">{user_data.get('formacion_academica', 'N/A')}</span></p>
                <p><span class="label">Habilidades:</span><span class="value">{user_data.get('habilidades', 'N/A')}</span></p>
                <p><span class="label">Intereses Laborales:</span><span class="value">{user_data.get('intereses_laborales', 'N/A')}</span></p>
            </div>
            
            <div class="info-section">
                <h3>Adaptaciones Necesarias</h3>
                <p>{user_data.get('adaptaciones_necesarias', 'Ninguna especificada')}</p>
            </div>
        </div>
    </body>
    </html>
    """
    
    return send_email('diversiaeternals@gmail.com', subject, html_content)

def send_company_registration_notification(company_data):
    """
    Envía notificación de nuevo registro de empresa
    """
    subject = "Nueva Empresa Registrada en DiversIA"
    
    html_content = f"""
    <html>
    <head>
        <style>
            body {{ font-family: Arial, sans-serif; line-height: 1.6; color: #333; }}
            .header {{ background: linear-gradient(135deg, #10B981, #059669); color: white; padding: 20px; text-align: center; }}
            .content {{ padding: 20px; }}
            .info-section {{ margin: 15px 0; padding: 15px; background: #f0fdf4; border-radius: 8px; }}
            .label {{ font-weight: bold; color: #065f46; }}
            .value {{ margin-left: 10px; }}
        </style>
    </head>
    <body>
        <div class="header">
            <h1>🏢 Nueva Empresa en DiversIA</h1>
        </div>
        <div class="content">
            <div class="info-section">
                <h3>Información de la Empresa</h3>
                <p><span class="label">Nombre:</span><span class="value">{company_data.get('nombre', 'N/A')}</span></p>
                <p><span class="label">Sector:</span><span class="value">{company_data.get('sector', 'N/A')}</span></p>
                <p><span class="label">Tamaño:</span><span class="value">{company_data.get('tamaño', 'N/A')}</span></p>
                <p><span class="label">Ubicación:</span><span class="value">{company_data.get('ubicacion', 'N/A')}</span></p>
                <p><span class="label">Sitio Web:</span><span class="value">{company_data.get('sitio_web', 'N/A')}</span></p>
            </div>
            
            <div class="info-section">
                <h3>Contacto</h3>
                <p><span class="label">Persona de Contacto:</span><span class="value">{company_data.get('contacto_nombre', 'N/A')}</span></p>
                <p><span class="label">Email:</span><span class="value">{company_data.get('contacto_email', 'N/A')}</span></p>
                <p><span class="label">Teléfono:</span><span class="value">{company_data.get('contacto_telefono', 'N/A')}</span></p>
            </div>
            
            <div class="info-section">
                <h3>Información de Inclusión</h3>
                <p><span class="label">Experiencia con Neurodivergentes:</span><span class="value">{'Sí' if company_data.get('experiencia_neurodivergentes') else 'No'}</span></p>
                <p><span class="label">Políticas de Inclusión:</span><span class="value">{company_data.get('politicas_inclusion', 'N/A')}</span></p>
                <p><span class="label">Adaptaciones Disponibles:</span><span class="value">{company_data.get('adaptaciones_disponibles', 'N/A')}</span></p>
            </div>
        </div>
    </body>
    </html>
    """
    
    return send_email('diversiaeternals@gmail.com', subject, html_content)