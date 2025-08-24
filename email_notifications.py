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

def send_association_registration_notification(association_data):
    """
    Enviar notificación por email cuando se registra una nueva asociación
    """
    sendgrid_key = os.environ.get('SENDGRID_API_KEY')
    if not sendgrid_key:
        print("⚠️ SENDGRID_API_KEY no configurada")
        return False
    
    try:
        sg = SendGridAPIClient(sendgrid_key)
        
        # Email a DiversIA - Notificación interna
        diversia_email_content = f"""
        <div style="font-family: Arial, sans-serif; max-width: 600px; margin: 0 auto;">
            <h2 style="color: #dc3545;">🚨 Nueva Asociación Solicita Registro - REQUIERE VERIFICACIÓN</h2>
            
            <div style="background: #fff3cd; border: 1px solid #ffeaa7; padding: 20px; border-radius: 8px; margin: 20px 0;">
                <h3 style="color: #856404;">⚠️ ATENCIÓN: Verificación de Legitimidad Requerida</h3>
                <p>Esta asociación necesita ser verificada antes de ser aprobada. No todas las organizaciones tienen buenas intenciones.</p>
            </div>
            
            <div style="background: #f8f9fa; padding: 20px; border-radius: 8px; margin: 20px 0;">
                <h3>📋 Información de la Asociación</h3>
                <p><strong>Nombre:</strong> {association_data.get('nombre_asociacion', 'No especificado')}</p>
                <p><strong>Acrónimo:</strong> {association_data.get('acronimo', 'No especificado')}</p>
                <p><strong>País:</strong> {association_data.get('pais', 'No especificado')}</p>
                <p><strong>Ciudad:</strong> {association_data.get('ciudad', 'No especificado')}</p>
                <p><strong>Email:</strong> {association_data.get('email', 'No especificado')}</p>
                <p><strong>Teléfono:</strong> {association_data.get('telefono', 'No especificado')}</p>
                <p><strong>Documento:</strong> {association_data.get('tipo_documento', 'No especificado')} - {association_data.get('numero_documento', 'No especificado')}</p>
                <p><strong>Neurodivergencias:</strong> {association_data.get('neurodivergencias_atendidas', 'No especificado')}</p>
                <p><strong>Servicios:</strong> {association_data.get('servicios', 'No especificado')}</p>
                <p><strong>Contacto:</strong> {association_data.get('contacto_nombre', 'No especificado')} ({association_data.get('contacto_cargo', 'No especificado')})</p>
                <p><strong>Fecha de registro:</strong> {datetime.now().strftime('%d/%m/%Y %H:%M')}</p>
                <p><strong>Estado actual:</strong> PENDIENTE DE VERIFICACIÓN</p>
            </div>
            
            <div style="background: #d1ecf1; border: 1px solid #bee5eb; padding: 20px; border-radius: 8px; margin: 20px 0;">
                <h3 style="color: #0c5460;">🔍 Acciones Requeridas</h3>
                <p>1. Verificar la legitimidad de la asociación</p>
                <p>2. Comprobar documentación legal</p>
                <p>3. Aprobar o rechazar la solicitud</p>
                <p>4. La asociación será notificada automáticamente</p>
            </div>
            
            <p style="text-align: center;">
                <a href="https://{os.environ.get('REPL_SLUG', 'diversia')}.{os.environ.get('REPL_OWNER', 'user')}.repl.co/admin/verificar-asociaciones" 
                   style="background: #dc3545; color: white; padding: 15px 25px; text-decoration: none; border-radius: 5px; display: inline-block; font-weight: bold;">
                   🔐 VERIFICAR ASOCIACIÓN AHORA
                </a>
            </p>
            
            <hr style="margin: 30px 0;">
            <p style="color: #666; font-size: 12px;">
                Este email fue generado automáticamente por el sistema de verificación DiversIA.<br>
                <strong>IMPORTANTE:</strong> No aprobar asociaciones sin verificar su legitimidad.
            </p>
        </div>
        """
        
        diversia_message = Mail(
            from_email=Email("security@diversia.com", "DiversIA - Sistema de Verificación"),
            to_emails=To("diversiaeternals@gmail.com"),
            subject=f"🚨 VERIFICAR: Nueva Asociación - {association_data.get('nombre_asociacion', 'Sin nombre')}",
            html_content=Content("text/html", diversia_email_content)
        )
        
        response = sg.send(diversia_message)
        print(f"✅ Notificación de verificación enviada a DiversIA: {response.status_code}")
        
        return True
        
    except Exception as e:
        print(f"❌ Error enviando notificación de asociación: {str(e)}")
        return False

def send_association_status_update(association_data, status, documents_link=None):
    """
    Enviar email a la asociación cuando cambia su estado
    """
    sendgrid_key = os.environ.get('SENDGRID_API_KEY')
    if not sendgrid_key:
        print("⚠️ SENDGRID_API_KEY no configurada")
        return False
    
    try:
        sg = SendGridAPIClient(sendgrid_key)
        
        # Contenido según el estado
        if status == 'documentos_requeridos':
            subject = "📄 Documentación requerida - DiversIA"
            content = f"""
            <div style="font-family: Arial, sans-serif; max-width: 600px; margin: 0 auto;">
                <h2 style="color: #f39c12;">📄 Documentación Requerida - {association_data.get('nombre_asociacion')}</h2>
                
                <p>¡Hola <strong>{association_data.get('contacto_nombre')}</strong>!</p>
                
                <p>Tu solicitud de registro en DiversIA está siendo procesada. Para completar el proceso de verificación, necesitamos que subas la documentación legal de tu asociación.</p>
                
                <div style="background: #fff3cd; border: 1px solid #ffeaa7; padding: 20px; border-radius: 8px; margin: 20px 0;">
                    <h3>📋 Documentos Requeridos</h3>
                    <ul>
                        <li>Estatutos de la asociación</li>
                        <li>Certificado de registro oficial</li>
                        <li>Documentos de identidad del representante legal</li>
                        <li>Memoria de actividades (si la tienes)</li>
                    </ul>
                </div>
                
                <p style="text-align: center;">
                    <a href="{documents_link or '#'}" 
                       style="background: #f39c12; color: white; padding: 15px 25px; text-decoration: none; border-radius: 5px; display: inline-block; font-weight: bold;">
                       📤 SUBIR DOCUMENTOS
                    </a>
                </p>
                
                <p>Una vez recibida la documentación, procederemos con la verificación final.</p>
                
                <hr style="margin: 30px 0;">
                <p style="color: #666; font-size: 12px;">
                    Si tienes dudas, responde a este email.<br>
                    Equipo DiversIA - Verificación de Asociaciones
                </p>
            </div>
            """
        elif status == 'aprobada':
            subject = "✅ ¡Bienvenida a DiversIA!"
            content = f"""
            <div style="font-family: Arial, sans-serif; max-width: 600px; margin: 0 auto;">
                <h2 style="color: #28a745;">🎉 ¡Bienvenida a la red DiversIA!</h2>
                
                <p>¡Hola <strong>{association_data.get('contacto_nombre')}</strong>!</p>
                
                <p>Nos alegra informarte que <strong>{association_data.get('nombre_asociacion')}</strong> ha sido aprobada y ahora forma parte de la red DiversIA.</p>
                
                <div style="background: #d4edda; border: 1px solid #c3e6cb; padding: 20px; border-radius: 8px; margin: 20px 0;">
                    <h3>🌟 Próximos pasos</h3>
                    <ul>
                        <li>Tu asociación aparecerá en nuestro directorio público</li>
                        <li>Recibirás información sobre colaboraciones</li>
                        <li>Tendrás acceso a recursos exclusivos</li>
                        <li>Podrás participar en eventos de la red</li>
                    </ul>
                </div>
                
                <p>¡Juntos construimos un mundo más inclusivo!</p>
                
                <hr style="margin: 30px 0;">
                <p style="color: #666; font-size: 12px;">
                    Equipo DiversIA<br>
                    Construyendo puentes hacia la inclusión laboral
                </p>
            </div>
            """
        else:  # rechazada
            subject = "❌ Estado de tu solicitud - DiversIA"
            content = f"""
            <div style="font-family: Arial, sans-serif; max-width: 600px; margin: 0 auto;">
                <h2 style="color: #dc3545;">Actualización sobre tu solicitud</h2>
                
                <p>Hola <strong>{association_data.get('contacto_nombre')}</strong>,</p>
                
                <p>Lamentamos informarte que no hemos podido aprobar la solicitud de registro de <strong>{association_data.get('nombre_asociacion')}</strong> en este momento.</p>
                
                <p>Si consideras que ha habido un error, puedes contactarnos directamente para revisar tu caso.</p>
                
                <hr style="margin: 30px 0;">
                <p style="color: #666; font-size: 12px;">
                    Equipo DiversIA
                </p>
            </div>
            """
        
        message = Mail(
            from_email=Email("asociaciones@diversia.com", "DiversIA - Verificación"),
            to_emails=To(association_data.get('email')),
            subject=subject,
            html_content=Content("text/html", content)
        )
        
        response = sg.send(message)
        print(f"✅ Email de estado enviado a {association_data.get('email')}: {response.status_code}")
        
        return True
        
    except Exception as e:
        print(f"❌ Error enviando email de estado: {str(e)}")
        return False

print("✅ Sistema de notificaciones por email cargado")