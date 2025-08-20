# Integración automática de formularios web con CRM
from flask import request, jsonify, flash, redirect
from datetime import datetime
import os

def integrate_web_forms_to_crm():
    """
    Middleware para capturar automáticamente todos los formularios web e integrarlos al CRM
    """
    
    # Rutas de integración automática
    @app.route('/api/form-submit', methods=['POST'])
    def auto_form_submit():
        """
        Endpoint unificado para procesar cualquier formulario y añadirlo automáticamente al CRM
        """
        try:
            form_data = request.get_json() or request.form.to_dict()
            form_type = form_data.get('form_type', 'unknown')
            
            # Procesar según tipo de formulario
            from form_integration_service import process_form_submission
            
            result = process_form_submission(form_type, form_data, 'web_auto_capture')
            
            if result:
                return jsonify({
                    'success': True,
                    'message': 'Formulario procesado y añadido al CRM automáticamente',
                    'crm_id': result
                })
            else:
                return jsonify({
                    'success': False,
                    'message': 'Error procesando formulario'
                }), 400
                
        except Exception as e:
            print(f"⚠️ Error en auto-captura formularios: {e}")
            return jsonify({
                'success': False,
                'message': 'Error interno del servidor'
            }), 500
    
    # Hook para capturar formularios existentes
    @app.before_request
    def capture_form_submissions():
        """
        Captura automáticamente todos los formularios POST y los procesa para el CRM
        """
        if request.method == 'POST' and request.endpoint:
            # Solo procesar formularios específicos de registro
            form_endpoints = [
                'registro_personas_nd',
                'registro_empresas', 
                'registro_asociaciones',
                'contacto_form'
            ]
            
            if any(endpoint in str(request.endpoint) for endpoint in form_endpoints):
                try:
                    form_data = request.form.to_dict()
                    
                    # Determinar tipo de formulario basado en la ruta
                    if 'personas' in str(request.endpoint):
                        form_type = 'registro_persona'
                    elif 'empresas' in str(request.endpoint):
                        form_type = 'registro_empresa'
                    elif 'asociaciones' in str(request.endpoint):
                        form_type = 'registro_asociacion'
                    elif 'contacto' in str(request.endpoint):
                        form_type = 'contacto'
                    else:
                        form_type = 'unknown'
                    
                    # Procesar en segundo plano
                    from form_integration_service import process_form_submission
                    process_form_submission(form_type, form_data, f'web_form_{request.endpoint}')
                    
                except Exception as e:
                    print(f"⚠️ Error en captura automática: {e}")

def create_ai_data_endpoint():
    """
    Endpoint para que la IA acceda a datos del CRM
    """
    @app.route('/api/ai/training-data')
    def get_ai_training_data():
        """
        Proporciona datos estructurados del CRM para entrenamiento/análisis de IA
        """
        try:
            from crm_api_simple import require_admin
            
            # Verificar acceso admin para datos sensibles
            if not require_admin():
                return jsonify({'error': 'No autorizado'}), 401
            
            from form_integration_service import get_ai_training_data
            from crm_api_simple import SAMPLE_CRM_DATA
            
            # Datos estructurados para IA
            ai_data = {
                'dataset_info': {
                    'total_contacts': len(SAMPLE_CRM_DATA.get('contacts', [])),
                    'total_companies': len(SAMPLE_CRM_DATA.get('companies', [])),
                    'total_associations': len(SAMPLE_CRM_DATA.get('associations', [])),
                    'total_offers': len(SAMPLE_CRM_DATA.get('job_offers', [])),
                    'last_updated': datetime.now().isoformat()
                },
                'neurodivergence_distribution': get_neurodivergence_stats(),
                'company_sectors': get_company_sectors(),
                'geographic_distribution': get_geographic_data(),
                'matching_patterns': get_matching_insights(),
                'training_data': get_ai_training_data()
            }
            
            return jsonify(ai_data)
            
        except Exception as e:
            print(f"⚠️ Error generando datos para IA: {e}")
            return jsonify({'error': 'Error interno'}), 500

def get_neurodivergence_stats():
    """Estadísticas de neurodivergencia para IA"""
    try:
        from crm_api_simple import SAMPLE_CRM_DATA
        
        neurodivergence_count = {}
        for contact in SAMPLE_CRM_DATA.get('contacts', []):
            nd_type = contact.get('neurodivergence', 'Unknown')
            neurodivergence_count[nd_type] = neurodivergence_count.get(nd_type, 0) + 1
        
        return neurodivergence_count
    except:
        return {}

def get_company_sectors():
    """Distribución de sectores empresariales"""
    try:
        from crm_api_simple import SAMPLE_CRM_DATA
        
        sectors = {}
        for company in SAMPLE_CRM_DATA.get('companies', []):
            sector = company.get('sector', 'Unknown')
            sectors[sector] = sectors.get(sector, 0) + 1
        
        return sectors
    except:
        return {}

def get_geographic_data():
    """Distribución geográfica"""
    try:
        from crm_api_simple import SAMPLE_CRM_DATA
        
        cities = {}
        # Contar contactos por ciudad
        for contact in SAMPLE_CRM_DATA.get('contacts', []):
            city = contact.get('city', 'Unknown')
            if city and city != 'Unknown':
                cities[city] = cities.get(city, 0) + 1
        
        return cities
    except:
        return {}

def get_matching_insights():
    """Insights de matching para IA"""
    try:
        from crm_api_simple import SAMPLE_CRM_DATA
        
        insights = {
            'successful_matches': 0,  # Pendiente implementar tracking
            'conversion_rate': 0.0,
            'avg_time_to_match': 0,
            'preferred_accommodations': [],
            'high_demand_skills': [],
            'inclusive_companies': []
        }
        
        # Analizar empresas más inclusivas
        for company in SAMPLE_CRM_DATA.get('companies', []):
            if company.get('inclusion_commitment') == 'high':
                insights['inclusive_companies'].append({
                    'name': company.get('name'),
                    'sector': company.get('sector'),
                    'size': company.get('size')
                })
        
        return insights
    except:
        return {}

# Función para testing del sistema de emails
def test_email_system():
    """
    Función de prueba para verificar el sistema de emails
    """
    try:
        from employee_email_service import send_employee_welcome_email, send_admin_notification
        
        # Datos de prueba
        test_employee = {
            'id': 999,
            'first_name': 'Test',
            'last_name': 'Developer',
            'email': 'developer@test.com',  # Cambiar por email real para pruebas
            'position': 'Desarrollador de Prueba',
            'department': 'Testing',
            'role': 'Desarrollador',
            'hire_date': datetime.now().strftime('%Y-%m-%d')
        }
        
        print("🧪 Iniciando prueba del sistema de emails...")
        
        # Enviar email de bienvenida
        welcome_sent = send_employee_welcome_email(test_employee)
        print(f"📧 Email bienvenida enviado: {welcome_sent}")
        
        # Enviar notificación admin
        admin_sent = send_admin_notification(test_employee)
        print(f"📧 Notificación admin enviada: {admin_sent}")
        
        return welcome_sent and admin_sent
        
    except Exception as e:
        print(f"⚠️ Error en prueba de emails: {e}")
        return False

print("✅ Integración CRM-Web cargada con captura automática de formularios")