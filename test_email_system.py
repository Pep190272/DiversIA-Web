# Script de prueba para sistema de emails y CRM
from datetime import datetime
import traceback

def test_complete_system():
    """
    Prueba completa del sistema: emails, CRM, e integración de formularios
    """
    print("🧪 === INICIANDO PRUEBAS DEL SISTEMA COMPLETO ===")
    
    # Prueba 1: Sistema de emails básico
    print("\n📧 PRUEBA 1: Sistema de emails SendGrid...")
    test_email_result = test_sendgrid_system()
    
    # Prueba 2: Integración CRM con formularios
    print("\n🗃️ PRUEBA 2: Integración automática CRM...")
    test_crm_result = test_crm_integration()
    
    # Prueba 3: Datos para IA
    print("\n🤖 PRUEBA 3: Extracción de datos para IA...")
    test_ai_data_result = test_ai_data_extraction()
    
    # Resumen
    print("\n✅ === RESUMEN DE PRUEBAS ===")
    print(f"📧 Emails SendGrid: {'✅ OK' if test_email_result else '❌ FALLO'}")
    print(f"🗃️ Integración CRM: {'✅ OK' if test_crm_result else '❌ FALLO'}")
    print(f"🤖 Datos para IA: {'✅ OK' if test_ai_data_result else '❌ FALLO'}")
    
    return test_email_result and test_crm_result and test_ai_data_result

def test_sendgrid_system():
    """
    Prueba específica del sistema de emails con SendGrid
    """
    try:
        from employee_email_service import send_employee_welcome_email, send_admin_notification
        
        # Datos de empleado de prueba
        test_employee = {
            'id': 999,
            'first_name': 'TestUser',
            'last_name': 'Developer',
            'email': 'diversiaeternals@gmail.com',  # Email real para pruebas
            'position': 'Desarrollador de Prueba',
            'department': 'Testing',
            'role': 'Desarrollador',
            'hire_date': datetime.now().strftime('%Y-%m-%d'),
            'activation_url': 'https://diversia.replit.app/activate?token=test123'
        }
        
        print(f"📤 Enviando email de prueba a: {test_employee['email']}")
        
        # Enviar email de bienvenida
        welcome_result = send_employee_welcome_email(test_employee)
        print(f"📧 Resultado email bienvenida: {welcome_result}")
        
        # Enviar notificación admin
        admin_result = send_admin_notification(test_employee)
        print(f"📧 Resultado notificación admin: {admin_result}")
        
        if welcome_result and admin_result:
            print("✅ Sistema de emails funcionando correctamente")
            return True
        else:
            print("⚠️ Algunos emails fallaron - revisar configuración SendGrid")
            return False
            
    except Exception as e:
        print(f"❌ Error en sistema de emails: {e}")
        traceback.print_exc()
        return False

def test_crm_integration():
    """
    Prueba la integración automática de formularios con CRM
    """
    try:
        from form_integration_service import process_form_submission
        
        # Datos de prueba - Persona neurodivergente
        test_person_data = {
            'nombre': 'María',
            'apellidos': 'González Testuser',
            'email': 'maria.test@example.com',
            'telefono': '+34 600 123 456',
            'ciudad': 'Madrid',
            'tipo_neurodivergencia': 'TDAH',
            'diagnostico_formal': 'si',
            'edad': '28',
            'nivel_educativo': 'Universitario',
            'experiencia_laboral': '2-5 años',
            'situacion_laboral': 'Desempleado',
            'ajustes_necesarios': 'Ambiente silencioso, pausas frecuentes',
            'areas_interes_laboral': 'Tecnología, Diseño',
            'servicios_apoyo': 'Coaching laboral',
            'consentimiento_privacidad': True,
            'consentimiento_newsletter': True
        }
        
        # Datos de prueba - Empresa
        test_company_data = {
            'nombre_empresa': 'TechInclusiva S.L.',
            'email_contacto': 'rrhh@techinclusiva.com',
            'telefono': '+34 900 987 654',
            'sector': 'Tecnología',
            'tamaño_empresa': '50-100',
            'ciudad': 'Barcelona',
            'sitio_web': 'https://techinclusiva.com',
            'compromiso_inclusion': 'high',
            'empleados_nd_actuales': 5,
            'presupuesto_inclusion': '10000-25000',
            'disposicion_ajustes': 'total',
            'neurodivergencias_preferidas': ['TDAH', 'TEA'],
            'opciones_trabajo_remoto': 'hybrid',
            'persona_contacto': 'Ana Martínez - RRHH'
        }
        
        # Datos de prueba - Asociación
        test_association_data = {
            'nombre_asociacion': 'Asociación Test Neurodivergentes',
            'acronimo': 'ATN',
            'pais': 'España',
            'ciudad': 'Valencia',
            'tipo_documento': 'CIF',
            'numero_documento': 'G12345678',
            'area_enfoque': 'TDAH',
            'tipo_organizacion': 'Asociación',
            'email': 'info@atn-test.org',
            'telefono': '+34 600 555 123',
            'sitio_web': 'https://atn-test.org',
            'descripcion': 'Asociación de prueba para personas neurodivergentes',
            'servicios_ofrecidos': 'Apoyo, formación, advocacy',
            'numero_miembros': 150,
            'año_fundacion': 2020,
            'ambito_geografico': 'Nacional',
            'interes_colaboracion': 'alto',
            'programas_ofrecidos': ['Formación laboral', 'Apoyo psicológico']
        }
        
        print("📋 Procesando formulario de persona...")
        person_id = process_form_submission('registro_persona', test_person_data, 'test_system')
        print(f"✅ Persona añadida al CRM con ID: {person_id}")
        
        print("🏢 Procesando formulario de empresa...")
        company_id = process_form_submission('registro_empresa', test_company_data, 'test_system')
        print(f"✅ Empresa añadida al CRM con ID: {company_id}")
        
        print("🤝 Procesando formulario de asociación...")
        association_id = process_form_submission('registro_asociacion', test_association_data, 'test_system')
        print(f"✅ Asociación añadida al CRM con ID: {association_id}")
        
        if person_id and company_id and association_id:
            print("✅ Integración CRM funcionando perfectamente")
            return True
        else:
            print("⚠️ Algunos registros fallaron")
            return False
            
    except Exception as e:
        print(f"❌ Error en integración CRM: {e}")
        traceback.print_exc()
        return False

def test_ai_data_extraction():
    """
    Prueba la extracción de datos para alimentar la IA
    """
    try:
        from form_integration_service import get_ai_training_data
        from crm_api_simple import SAMPLE_CRM_DATA
        
        print("🧠 Extrayendo datos actuales del CRM...")
        
        # Estadísticas básicas
        contacts_count = len(SAMPLE_CRM_DATA.get('contacts', []))
        companies_count = len(SAMPLE_CRM_DATA.get('companies', []))
        associations_count = len(SAMPLE_CRM_DATA.get('associations', []))
        
        print(f"📊 Estadísticas CRM:")
        print(f"  - Contactos: {contacts_count}")
        print(f"  - Empresas: {companies_count}")
        print(f"  - Asociaciones: {associations_count}")
        
        # Extraer datos para IA
        ai_data = get_ai_training_data()
        
        neurodivergent_profiles = len(ai_data.get('neurodivergent_profiles', []))
        inclusion_patterns = len(ai_data.get('company_inclusion_patterns', []))
        
        print(f"🤖 Datos para IA generados:")
        print(f"  - Perfiles neurodivergentes: {neurodivergent_profiles}")
        print(f"  - Patrones de inclusión: {inclusion_patterns}")
        
        # Verificar calidad de datos
        if neurodivergent_profiles > 0 and inclusion_patterns > 0:
            print("✅ Datos para IA extraídos correctamente")
            return True
        else:
            print("⚠️ Datos insuficientes para entrenamiento de IA")
            return False
            
    except Exception as e:
        print(f"❌ Error extrayendo datos para IA: {e}")
        traceback.print_exc()
        return False

def run_email_test_only():
    """
    Ejecuta solo la prueba de emails para debugging
    """
    print("🧪 === PRUEBA INDIVIDUAL: SISTEMA DE EMAILS ===")
    result = test_sendgrid_system()
    
    if result:
        print("\n✅ ¡Sistema de emails funcionando correctamente!")
        print("📧 Deberías haber recibido emails en diversiaeternals@gmail.com")
    else:
        print("\n❌ El sistema de emails tiene problemas")
        print("🔧 Revisa la configuración de SENDGRID_API_KEY")
    
    return result

if __name__ == "__main__":
    # Ejecutar solo prueba de emails si se ejecuta directamente
    run_email_test_only()