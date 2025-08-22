"""
Sistema de Notificaciones por Email para DiversIA
Envío automático de emails cuando se añaden colaboradores
"""

import os
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail, Email, To, Content
from datetime import datetime

def send_employee_notification(employee_data):
    """
    Enviar notificación por email cuando se añade un nuevo colaborador
    """
    sendgrid_key = os.environ.get('SENDGRID_API_KEY')
    if not sendgrid_key:
        print("⚠️ SENDGRID_API_KEY no configurada")
        return False
    
    try:
        sg = SendGridAPIClient(sendgrid_key)
        
        # Email a DiversIA
        diversia_email_content = f"""
        <h2>🎉 Nuevo Colaborador Añadido - DiversIA</h2>
        
        <p>Se ha añadido un nuevo colaborador al sistema de gestión de tareas:</p>
        
        <div style="background: #f8f9fa; padding: 20px; border-radius: 8px; margin: 20px 0;">
            <h3>📋 Información del Colaborador</h3>
            <p><strong>Nombre:</strong> {employee_data['name']}</p>
            <p><strong>Email:</strong> {employee_data['email']}</p>
            <p><strong>Rol:</strong> {employee_data['rol']}</p>
            <p><strong>Departamento:</strong> {employee_data.get('department', 'No especificado')}</p>
            <p><strong>Fecha de registro:</strong> {datetime.now().strftime('%d/%m/%Y %H:%M')}</p>
        </div>
        
        <p>El colaborador ya puede ser asignado a tareas en el sistema de gestión.</p>
        
        <p><a href="https://{os.environ.get('REPL_SLUG', 'diversia')}.{os.environ.get('REPL_OWNER', 'user')}.repl.co/tasks" 
           style="background: #007bff; color: white; padding: 10px 20px; text-decoration: none; border-radius: 5px;">
           Ver Sistema de Tareas
        </a></p>
        
        <hr style="margin: 30px 0;">
        <p style="color: #666; font-size: 12px;">
            Este email fue generado automáticamente por el sistema DiversIA.<br>
            Para gestionar colaboradores, accede al panel de administración.
        </p>
        """
        
        diversia_message = Mail(
            from_email=Email("noreply@diversia.com", "DiversIA - Sistema de Gestión"),
            to_emails=To("diversiaeternals@gmail.com"),
            subject=f"🆕 Nuevo Colaborador: {employee_data['name']} ({employee_data['rol']})",
            html_content=Content("text/html", diversia_email_content)
        )
        
        # Enviar email a DiversIA
        response_diversia = sg.send(diversia_message)
        print(f"✅ Email enviado a DiversIA: {response_diversia.status_code}")
        
        # Email de bienvenida al colaborador
        welcome_email_content = f"""
        <h2>🎉 ¡Bienvenido al equipo DiversIA!</h2>
        
        <p>Hola <strong>{employee_data['name']}</strong>,</p>
        
        <p>Te damos la bienvenida al equipo de DiversIA como <strong>{employee_data['rol']}</strong>. 
        Has sido añadido a nuestro sistema de gestión de tareas y proyectos.</p>
        
        <div style="background: #e7f3ff; padding: 20px; border-radius: 8px; margin: 20px 0; border-left: 4px solid #007bff;">
            <h3>📋 Tu Información en el Sistema</h3>
            <p><strong>Rol asignado:</strong> {employee_data['rol']}</p>
            <p><strong>Departamento:</strong> {employee_data.get('department', 'No especificado')}</p>
            <p><strong>Email de contacto:</strong> {employee_data['email']}</p>
        </div>
        
        <h3>🚀 ¿Qué sigue?</h3>
        <ul>
            <li>Pronto recibirás tareas asignadas específicamente para tu rol</li>
            <li>Podrás colaborar en proyectos de inclusión laboral para personas neurodivergentes</li>
            <li>Tendrás acceso a herramientas de seguimiento y analytics de productividad</li>
        </ul>
        
        <div style="background: #f8f9fa; padding: 15px; border-radius: 8px; margin: 20px 0;">
            <h4>📞 Información de Contacto</h4>
            <p><strong>Email:</strong> diversiaeternals@gmail.com</p>
            <p><strong>Telegram:</strong> <a href="https://t.me/DiversiaSupport">@DiversiaSupport</a></p>
        </div>
        
        <p>¡Estamos emocionados de tenerte en el equipo!</p>
        
        <p style="margin-top: 30px;">
            <strong>El equipo de DiversIA</strong><br>
            <em>Construyendo puentes hacia la inclusión laboral</em>
        </p>
        
        <hr style="margin: 30px 0;">
        <p style="color: #666; font-size: 12px;">
            Este email fue generado automáticamente por el sistema DiversIA.<br>
            Si tienes preguntas, contacta con el equipo de administración.
        </p>
        """
        
        collaborator_message = Mail(
            from_email=Email("team@diversia.com", "Equipo DiversIA"),
            to_emails=To(employee_data['email']),
            subject=f"🎉 ¡Bienvenido al equipo DiversIA, {employee_data['name']}!",
            html_content=Content("text/html", welcome_email_content)
        )
        
        # Enviar email de bienvenida al colaborador
        response_collaborator = sg.send(collaborator_message)
        print(f"✅ Email de bienvenida enviado a {employee_data['email']}: {response_collaborator.status_code}")
        
        return True
        
    except Exception as e:
        print(f"❌ Error enviando emails: {str(e)}")
        return False

def send_task_assignment_notification(task_data, employee_email):
    """
    Enviar notificación cuando se asigna una tarea a un colaborador
    """
    sendgrid_key = os.environ.get('SENDGRID_API_KEY')
    if not sendgrid_key:
        return False
    
    try:
        sg = SendGridAPIClient(sendgrid_key)
        
        email_content = f"""
        <h2>📋 Nueva Tarea Asignada - DiversIA</h2>
        
        <p>Se te ha asignado una nueva tarea en el sistema DiversIA:</p>
        
        <div style="background: #fff3cd; padding: 20px; border-radius: 8px; margin: 20px 0; border-left: 4px solid #ffc107;">
            <h3>📌 Detalles de la Tarea</h3>
            <p><strong>Tarea:</strong> {task_data.get('tarea', 'No especificada')}</p>
            <p><strong>Estado:</strong> {task_data.get('estado', 'Pendiente')}</p>
            <p><strong>Fecha de inicio:</strong> {task_data.get('fecha_inicio', 'No especificada')}</p>
            <p><strong>Fecha límite:</strong> {task_data.get('fecha_final', 'No especificada')}</p>
        </div>
        
        <p>Puedes ver el estado de todas tus tareas en el sistema de gestión.</p>
        
        <p><a href="https://{os.environ.get('REPL_SLUG', 'diversia')}.{os.environ.get('REPL_OWNER', 'user')}.repl.co/tasks" 
           style="background: #28a745; color: white; padding: 10px 20px; text-decoration: none; border-radius: 5px;">
           Ver Mis Tareas
        </a></p>
        """
        
        message = Mail(
            from_email=Email("tasks@diversia.com", "DiversIA - Gestión de Tareas"),
            to_emails=To(employee_email),
            subject=f"📋 Nueva tarea asignada: {task_data.get('tarea', 'Tarea')[:50]}...",
            html_content=Content("text/html", email_content)
        )
        
        response = sg.send(message)
        print(f"✅ Notificación de tarea enviada a {employee_email}: {response.status_code}")
        return True
        
    except Exception as e:
        print(f"❌ Error enviando notificación de tarea: {str(e)}")
        return False

print("✅ Sistema de notificaciones por email cargado")