# Servicio de integración de formularios web con CRM
import os
import json
from datetime import datetime

# Integración automática de formularios web al CRM
def process_form_submission(form_type, form_data, source='web_form'):
    """
    Procesa automáticamente las submisiones de formularios web e integra los datos al CRM
    """
    try:
        # Importar datos del CRM
        from crm_api_simple import SAMPLE_CRM_DATA
        
        if form_type == 'registro_persona':
            return process_person_registration(form_data, source)
        elif form_type == 'registro_empresa':
            return process_company_registration(form_data, source)
        elif form_type == 'registro_asociacion':
            return process_association_registration(form_data, source)
        elif form_type == 'contacto':
            return process_contact_form(form_data, source)
        else:
            print(f"⚠️ Tipo de formulario no reconocido: {form_type}")
            return False
            
    except Exception as e:
        print(f"⚠️ Error procesando formulario {form_type}: {e}")
        return False

def process_person_registration(form_data, source):
    """
    Convierte registro de persona neurodivergente en contacto CRM
    """
    try:
        from crm_api_simple import SAMPLE_CRM_DATA
        
        # Generar nuevo ID
        new_id = max([c['id'] for c in SAMPLE_CRM_DATA['contacts']], default=0) + 1
        
        # Mapear datos del formulario al formato CRM
        new_contact = {
            'id': new_id,
            'name': f"{form_data.get('nombre', '')} {form_data.get('apellidos', '')}".strip(),
            'email': form_data.get('email', ''),
            'phone': form_data.get('telefono', ''),
            'city': form_data.get('ciudad', ''),
            'neurodivergence': form_data.get('tipo_neurodivergencia', 'TDAH'),
            'formal_diagnosis': form_data.get('diagnostico_formal') == 'si',
            'created_at': datetime.now().isoformat(),
            'source': source,
            # Campos adicionales del formulario
            'age': form_data.get('edad'),
            'education_level': form_data.get('nivel_educativo'),
            'work_experience': form_data.get('experiencia_laboral'),
            'employment_status': form_data.get('situacion_laboral'),
            'accommodations_needed': form_data.get('ajustes_necesarios'),
            'job_interests': form_data.get('areas_interes_laboral'),
            'support_services': form_data.get('servicios_apoyo'),
            'privacy_consent': form_data.get('consentimiento_privacidad', False),
            'newsletter_consent': form_data.get('consentimiento_newsletter', False)
        }
        
        # Agregar al CRM
        SAMPLE_CRM_DATA['contacts'].append(new_contact)
        
        # Enviar notificación al equipo
        send_form_notification('Nuevo registro persona ND', new_contact, form_data)
        
        print(f"✅ Contacto CRM creado desde formulario web: {new_contact['name']}")
        return new_id
        
    except Exception as e:
        print(f"⚠️ Error procesando registro persona: {e}")
        return False

def process_company_registration(form_data, source):
    """
    Convierte registro de empresa en entrada CRM
    """
    try:
        from crm_api_simple import SAMPLE_CRM_DATA
        
        # Generar nuevo ID
        new_id = max([c['id'] for c in SAMPLE_CRM_DATA['companies']], default=0) + 1
        
        # Mapear datos del formulario al formato CRM
        new_company = {
            'id': new_id,
            'name': form_data.get('nombre_empresa', ''),
            'sector': form_data.get('sector', 'Otros'),
            'email': form_data.get('email_contacto', ''),
            'phone': form_data.get('telefono', ''),
            'city': form_data.get('ciudad', ''),
            'size': form_data.get('tamaño_empresa', '1-10'),
            'website': form_data.get('sitio_web', ''),
            'created_at': datetime.now().isoformat(),
            'source': source,
            # Campos adicionales específicos de inclusión
            'inclusion_commitment': form_data.get('compromiso_inclusion'),
            'current_nd_employees': form_data.get('empleados_nd_actuales', 0),
            'inclusion_budget': form_data.get('presupuesto_inclusion'),
            'accommodation_willingness': form_data.get('disposicion_ajustes'),
            'preferred_neurodivergences': form_data.get('neurodivergencias_preferidas', []),
            'remote_work_options': form_data.get('opciones_trabajo_remoto'),
            'contact_person': form_data.get('persona_contacto'),
            'job_offers_count': 0  # Inicializar contador
        }
        
        # Agregar al CRM
        SAMPLE_CRM_DATA['companies'].append(new_company)
        
        # Enviar notificación al equipo
        send_form_notification('Nueva empresa registrada', new_company, form_data)
        
        print(f"✅ Empresa CRM creada desde formulario web: {new_company['name']}")
        return new_id
        
    except Exception as e:
        print(f"⚠️ Error procesando registro empresa: {e}")
        return False

def process_association_registration(form_data, source):
    """
    Convierte registro de asociación en entrada CRM
    """
    try:
        from crm_api_simple import SAMPLE_CRM_DATA
        
        # Generar nuevo ID
        new_id = max([a['id'] for a in SAMPLE_CRM_DATA['associations']], default=0) + 1
        
        # Mapear datos del formulario al formato CRM
        new_association = {
            'id': new_id,
            'name': form_data.get('nombre_asociacion', ''),
            'acronym': form_data.get('acronimo', ''),
            'country': form_data.get('pais', 'España'),
            'city': form_data.get('ciudad', ''),
            'document_type': form_data.get('tipo_documento', 'CIF'),
            'document_number': form_data.get('numero_documento', ''),
            'focus_area': form_data.get('area_enfoque', 'General'),
            'type': form_data.get('tipo_organizacion', 'Asociación'),
            'email': form_data.get('email', ''),
            'phone': form_data.get('telefono', ''),
            'website': form_data.get('sitio_web', ''),
            'description': form_data.get('descripcion', ''),
            'services': form_data.get('servicios_ofrecidos', ''),
            'created_at': datetime.now().isoformat(),
            'source': source,
            # Campos adicionales
            'members_count': form_data.get('numero_miembros', 0),
            'foundation_year': form_data.get('año_fundacion'),
            'geographic_scope': form_data.get('ambito_geografico'),
            'collaboration_interest': form_data.get('interes_colaboracion'),
            'programs_offered': form_data.get('programas_ofrecidos', [])
        }
        
        # Agregar al CRM
        SAMPLE_CRM_DATA['associations'].append(new_association)
        
        # Enviar notificación al equipo
        send_form_notification('Nueva asociación registrada', new_association, form_data)
        
        print(f"✅ Asociación CRM creada desde formulario web: {new_association['name']}")
        return new_id
        
    except Exception as e:
        print(f"⚠️ Error procesando registro asociación: {e}")
        return False

def process_contact_form(form_data, source):
    """
    Procesa formulario de contacto general
    """
    try:
        # Crear entrada de seguimiento para el equipo de ventas
        contact_data = {
            'name': form_data.get('nombre', ''),
            'email': form_data.get('email', ''),
            'phone': form_data.get('telefono', ''),
            'message': form_data.get('mensaje', ''),
            'interest_type': form_data.get('tipo_interes', 'General'),
            'timestamp': datetime.now().isoformat(),
            'source': source,
            'status': 'pending_follow_up'
        }
        
        # Enviar notificación inmediata al equipo
        send_form_notification('Nuevo mensaje de contacto', contact_data, form_data)
        
        print(f"✅ Formulario de contacto procesado: {contact_data['name']}")
        return True
        
    except Exception as e:
        print(f"⚠️ Error procesando formulario contacto: {e}")
        return False

def send_form_notification(notification_type, crm_data, original_form_data):
    """
    Envía notificación por email cuando se recibe un nuevo formulario
    """
    try:
        from employee_email_service import SendGridAPIClient, Mail
        
        sendgrid_key = os.environ.get('SENDGRID_API_KEY')
        if not sendgrid_key:
            print("⚠️ SENDGRID_API_KEY no configurado para notificaciones")
            return False
        
        sg = SendGridAPIClient(sendgrid_key)
        
        # Crear contenido del email
        html_content = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <meta charset="utf-8">
            <title>{notification_type} - DiversIA</title>
            <style>
                body {{ font-family: Arial, sans-serif; line-height: 1.6; color: #333; }}
                .header {{ background-color: #4a90e2; color: white; padding: 20px; text-align: center; }}
                .content {{ padding: 30px; }}
                .data-box {{ background-color: #f8f9fa; border-left: 4px solid #4a90e2; padding: 15px; margin: 20px 0; }}
                .highlight {{ background-color: #fff3cd; padding: 10px; border-radius: 5px; margin: 10px 0; }}
            </style>
        </head>
        <body>
            <div class="header">
                <h1>{notification_type}</h1>
                <p>Sistema de Integración Automática - DiversIA</p>
            </div>
            
            <div class="content">
                <div class="highlight">
                    <strong>📋 Nuevo lead capturado automáticamente del sitio web</strong><br>
                    Los datos se han integrado automáticamente al CRM y están listos para seguimiento.
                </div>
                
                <div class="data-box">
                    <h3>Información registrada:</h3>
                    <pre>{json.dumps(crm_data, indent=2, ensure_ascii=False)}</pre>
                </div>
                
                <div class="data-box">
                    <h3>Datos originales del formulario:</h3>
                    <pre>{json.dumps(original_form_data, indent=2, ensure_ascii=False)}</pre>
                </div>
                
                <p><strong>Próximos pasos:</strong></p>
                <ul>
                    <li>Revisar la información en el CRM dashboard</li>
                    <li>Realizar seguimiento personalizado según el perfil</li>
                    <li>Actualizar el estado del lead</li>
                </ul>
                
                <p><a href="{os.environ.get('REPL_SLUG', 'diversia')}.replit.app/crm" target="_blank">
                    Ver en CRM Dashboard →
                </a></p>
            </div>
        </body>
        </html>
        """
        
        message = Mail(
            from_email='diversiaeternals@gmail.com',
            to_emails='diversiaeternals@gmail.com',
            subject=f'🔔 {notification_type} - DiversIA CRM',
            html_content=html_content
        )
        
        response = sg.send(message)
        
        if response.status_code == 202:
            print(f"✅ Notificación enviada: {notification_type}")
            return True
        else:
            print(f"⚠️ Error enviando notificación: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"⚠️ Error en notificación: {e}")
        return False

def get_ai_training_data():
    """
    Extrae datos formateados para entrenamiento de IA
    """
    try:
        from crm_api_simple import SAMPLE_CRM_DATA
        
        training_data = {
            'neurodivergent_profiles': [],
            'company_inclusion_patterns': [],
            'successful_matches': [],
            'market_insights': []
        }
        
        # Procesar perfiles neurodivergentes
        for contact in SAMPLE_CRM_DATA['contacts']:
            profile = {
                'neurodivergence_type': contact.get('neurodivergence'),
                'age_range': categorize_age(contact.get('age')),
                'education_level': contact.get('education_level'),
                'experience_level': contact.get('work_experience'),
                'accommodation_needs': contact.get('accommodations_needed'),
                'job_preferences': contact.get('job_interests'),
                'location': contact.get('city'),
                'formal_diagnosis': contact.get('formal_diagnosis', False)
            }
            training_data['neurodivergent_profiles'].append(profile)
        
        # Procesar patrones de empresas inclusivas
        for company in SAMPLE_CRM_DATA['companies']:
            pattern = {
                'sector': company.get('sector'),
                'size': company.get('size'),
                'inclusion_commitment': company.get('inclusion_commitment'),
                'remote_work_options': company.get('remote_work_options'),
                'preferred_neurodivergences': company.get('preferred_neurodivergences', []),
                'location': company.get('city'),
                'offers_count': company.get('job_offers_count', 0)
            }
            training_data['company_inclusion_patterns'].append(pattern)
        
        return training_data
        
    except Exception as e:
        print(f"⚠️ Error extrayendo datos para IA: {e}")
        return {}

def categorize_age(age):
    """Categoriza edades para análisis IA"""
    if not age:
        return 'unknown'
    age = int(age)
    if age < 25:
        return 'young_adult'
    elif age < 35:
        return 'early_career'
    elif age < 45:
        return 'mid_career'
    elif age < 55:
        return 'experienced'
    else:
        return 'senior'

print("✅ Servicio de integración de formularios web cargado")