# Servicio de notificación por email para empleados
import os
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
from flask import url_for

def send_employee_welcome_email(employee_data):
    """
    Envía email de bienvenida a nuevo empleado con instrucciones para crear contraseña
    """
    try:
        # Verificar que SendGrid esté configurado
        sendgrid_key = os.environ.get('SENDGRID_API_KEY')
        if not sendgrid_key:
            print("⚠️ SENDGRID_API_KEY no está configurado")
            return False
        
        sg = SendGridAPIClient(sendgrid_key)
        
        # Crear URL de activación de cuenta (simulado)
        activation_url = f"https://{os.environ.get('REPL_SLUG', 'diversia')}.replit.app/admin/activate-account?token=temp_token_{employee_data['id']}"
        
        # Contenido del email
        html_content = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <meta charset="utf-8">
            <title>Bienvenido a DiversIA</title>
            <style>
                body {{ font-family: Arial, sans-serif; line-height: 1.6; color: #333; }}
                .header {{ background-color: #4a90e2; color: white; padding: 20px; text-align: center; }}
                .content {{ padding: 30px; background-color: #f9f9f9; }}
                .button {{ 
                    display: inline-block; 
                    background-color: #4a90e2; 
                    color: white; 
                    padding: 12px 30px; 
                    text-decoration: none; 
                    border-radius: 5px; 
                    margin: 20px 0;
                }}
                .footer {{ padding: 20px; text-align: center; font-size: 12px; color: #666; }}
            </style>
        </head>
        <body>
            <div class="header">
                <h1>¡Bienvenido a DiversIA!</h1>
            </div>
            
            <div class="content">
                <h2>Hola {employee_data['first_name']} {employee_data['last_name']},</h2>
                
                <p>¡Te damos la bienvenida al equipo de DiversIA! Nos complace informarte que has sido registrado como <strong>{employee_data['role']}</strong> en el departamento de <strong>{employee_data['department']}</strong>.</p>
                
                <h3>Detalles de tu cuenta:</h3>
                <ul>
                    <li><strong>Posición:</strong> {employee_data['position']}</li>
                    <li><strong>Departamento:</strong> {employee_data['department']}</li>
                    <li><strong>Email corporativo:</strong> {employee_data['email']}</li>
                    <li><strong>Fecha de ingreso:</strong> {employee_data['hire_date']}</li>
                </ul>
                
                <h3>Próximos pasos:</h3>
                <ol>
                    <li>Haz clic en el siguiente enlace para activar tu cuenta y crear tu contraseña:</li>
                </ol>
                
                <div style="text-align: center;">
                    <a href="{activation_url}" class="button">Activar mi cuenta</a>
                </div>
                
                <p><strong>Importante:</strong> Este enlace estará disponible por 48 horas. Si tienes problemas para acceder, contacta al administrador del sistema.</p>
                
                <h3>Acceso al sistema CRM:</h3>
                <p>Una vez activada tu cuenta, podrás acceder al sistema CRM de DiversIA donde podrás:</p>
                <ul>
                    <li>Ver y gestionar tus tareas asignadas</li>
                    <li>Actualizar el estado de tus proyectos</li>
                    <li>Colaborar con otros miembros del equipo</li>
                    <li>Acceder a recursos y documentación</li>
                </ul>
                
                <p>Si tienes alguna pregunta, no dudes en contactarnos. ¡Esperamos trabajar contigo!</p>
                
                <p>Saludos cordiales,<br>
                <strong>Equipo DiversIA</strong></p>
            </div>
            
            <div class="footer">
                <p>Este es un email automático del sistema CRM de DiversIA.<br>
                Si no esperabas este mensaje, por favor contacta al administrador.</p>
            </div>
        </body>
        </html>
        """
        
        # Crear el mensaje
        message = Mail(
            from_email='noreply@diversia.com',
            to_emails=employee_data['email'],
            subject=f'¡Bienvenido a DiversIA, {employee_data["first_name"]}! - Activa tu cuenta',
            html_content=html_content
        )
        
        # Enviar el email
        response = sg.send(message)
        
        if response.status_code == 202:
            print(f"✅ Email de bienvenida enviado a {employee_data['email']}")
            return True
        else:
            print(f"⚠️ Error enviando email: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"⚠️ Error en servicio de email: {str(e)}")
        return False

def send_admin_notification(employee_data):
    """
    Notifica a los administradores sobre el nuevo empleado creado
    """
    try:
        sendgrid_key = os.environ.get('SENDGRID_API_KEY')
        if not sendgrid_key:
            return False
        
        sg = SendGridAPIClient(sendgrid_key)
        
        html_content = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <meta charset="utf-8">
            <title>Nuevo empleado registrado - DiversIA CRM</title>
            <style>
                body {{ font-family: Arial, sans-serif; line-height: 1.6; color: #333; }}
                .header {{ background-color: #28a745; color: white; padding: 20px; text-align: center; }}
                .content {{ padding: 30px; }}
                .info-box {{ background-color: #f8f9fa; border-left: 4px solid #28a745; padding: 15px; margin: 20px 0; }}
            </style>
        </head>
        <body>
            <div class="header">
                <h1>Nuevo empleado registrado</h1>
            </div>
            
            <div class="content">
                <p>Se ha registrado un nuevo empleado en el sistema CRM de DiversIA:</p>
                
                <div class="info-box">
                    <strong>Información del empleado:</strong><br>
                    Nombre: {employee_data['first_name']} {employee_data['last_name']}<br>
                    Email: {employee_data['email']}<br>
                    Posición: {employee_data['position']}<br>
                    Departamento: {employee_data['department']}<br>
                    Rol: {employee_data['role']}<br>
                    Fecha de ingreso: {employee_data['hire_date']}
                </div>
                
                <p>El email de activación ha sido enviado automáticamente al nuevo empleado.</p>
                
                <p><strong>Sistema CRM DiversIA</strong></p>
            </div>
        </body>
        </html>
        """
        
        message = Mail(
            from_email='noreply@diversia.com',
            to_emails='diversiaeternals@gmail.com',  # Email del administrador
            subject=f'Nuevo empleado: {employee_data["first_name"]} {employee_data["last_name"]}',
            html_content=html_content
        )
        
        response = sg.send(message)
        
        if response.status_code == 202:
            print(f"✅ Notificación enviada a administradores")
            return True
        else:
            print(f"⚠️ Error enviando notificación: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"⚠️ Error en notificación admin: {str(e)}")
        return False

print("✅ Servicio de email para empleados cargado")