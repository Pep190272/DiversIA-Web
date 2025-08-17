"""
Enhanced API Endpoints for DiversIA AI System
Endpoints especializados para el agente inteligente y matching
"""

from flask import Blueprint, request, jsonify, current_app
from datetime import datetime
import logging
import json
import asyncio

# Importar nuestros módulos de IA (con manejo de errores)
try:
    from ai_agent_core import process_chat_message, diversia_agent
    AI_AGENT_AVAILABLE = True
except ImportError as e:
    logging.warning(f"AI Agent not available: {e}")
    AI_AGENT_AVAILABLE = False

try:
    from ai_matching_engine import matching_engine, get_candidate_recommendations
    MATCHING_ENGINE_AVAILABLE = True
except ImportError as e:
    logging.warning(f"Matching Engine not available: {e}")
    MATCHING_ENGINE_AVAILABLE = False

try:
    from google_drive_integration import drive_manager, upload_candidate_document
    DRIVE_INTEGRATION_AVAILABLE = True
except ImportError as e:
    logging.warning(f"Google Drive integration not available: {e}")
    DRIVE_INTEGRATION_AVAILABLE = False

try:
    from security_manager import security_manager, encrypt_user_data, decrypt_user_data
    SECURITY_MANAGER_AVAILABLE = True
except ImportError as e:
    logging.warning(f"Security Manager not available: {e}")
    SECURITY_MANAGER_AVAILABLE = False

from models import db, Usuario, Empresa
from sendgrid_helper import send_notification_email

# Crear blueprint para APIs de IA
ai_api = Blueprint('ai_api', __name__, url_prefix='/api/v2')

logger = logging.getLogger(__name__)

@ai_api.route('/chat/intelligent', methods=['POST'])
def intelligent_chat():
    """
    Endpoint para chat inteligente con el agente de IA
    """
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({'error': 'No data provided'}), 400
        
        message = data.get('message', '')
        user_id = data.get('user_id', 'anonymous')
        session_id = data.get('session_id', 'default')
        page = data.get('page', '/')
        
        if not message:
            return jsonify({'error': 'Message is required'}), 400
        
        # Log de la interacción
        logger.info(f"Intelligent chat request: user={user_id}, message={message[:50]}...")
        
        if AI_AGENT_AVAILABLE:
            # Usar el agente inteligente
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            try:
                result = loop.run_until_complete(
                    process_chat_message(message, user_id, session_id, page)
                )
                
                # Enriquecer con datos del sistema
                if 'system_data' not in result:
                    result['system_data'] = get_system_statistics()
                
                # Formatear respuesta final
                final_response = result.get('final_response', '')
                if result.get('system_data'):
                    stats = result['system_data']
                    if stats.get('total_users', 0) > 0:
                        final_response += f"\n\n📊 Actualmente tenemos {stats['total_users']} profesionales registrados"
                        if stats.get('total_companies', 0) > 0:
                            final_response += f" y {stats['total_companies']} empresas inclusivas"
                
                result['final_response'] = final_response
                result['powered_by'] = 'DiversIA AI Agent'
                
                return jsonify(result)
            finally:
                loop.close()
        else:
            # Fallback a respuestas inteligentes locales
            return intelligent_fallback_response(message, user_id)
        
    except Exception as e:
        logger.error(f"Error in intelligent chat: {e}")
        return jsonify({
            'error': 'Internal server error',
            'fallback_response': get_fallback_message(message),
            'powered_by': 'DiversIA Fallback System'
        }), 500

@ai_api.route('/matching/recommendations/<candidate_id>', methods=['GET'])
def get_matching_recommendations(candidate_id):
    """
    Obtener recomendaciones de matching para un candidato
    """
    try:
        # Obtener parámetros
        max_results = request.args.get('max_results', 5, type=int)
        include_reasons = request.args.get('include_reasons', 'true').lower() == 'true'
        
        if MATCHING_ENGINE_AVAILABLE:
            # Usar motor de matching inteligente
            recommendations = get_candidate_recommendations(candidate_id, max_results)
            
            return jsonify({
                'candidate_id': candidate_id,
                'recommendations': recommendations,
                'total_found': len(recommendations),
                'algorithm_version': '2.0',
                'generated_at': datetime.utcnow().isoformat()
            })
        else:
            # Fallback con datos simulados
            return jsonify({
                'candidate_id': candidate_id,
                'recommendations': get_fallback_recommendations(),
                'total_found': 1,
                'algorithm_version': 'fallback',
                'note': 'Using fallback recommendations - AI engine not available'
            })
    
    except Exception as e:
        logger.error(f"Error getting recommendations: {e}")
        return jsonify({'error': 'Error generating recommendations'}), 500

@ai_api.route('/matching/compatibility', methods=['POST'])
def calculate_compatibility():
    """
    Calcular compatibilidad entre candidato y empresa/oferta
    """
    try:
        data = request.get_json()
        
        candidate_data = data.get('candidate')
        company_data = data.get('company')
        job_offer_data = data.get('job_offer')
        
        if not all([candidate_data, company_data, job_offer_data]):
            return jsonify({'error': 'candidate, company, and job_offer data required'}), 400
        
        if MATCHING_ENGINE_AVAILABLE:
            # Calcular compatibilidad real
            score = matching_engine.calculate_compatibility_score(
                candidate_data, company_data, job_offer_data
            )
            
            # Generar razones del matching
            reasons = matching_engine.generate_match_reasons(
                candidate_data, company_data, job_offer_data, score
            )
            
            return jsonify({
                'compatibility_score': round(score, 2),
                'match_quality': get_match_quality_label(score),
                'reasons': reasons,
                'algorithm_version': '2.0',
                'calculated_at': datetime.utcnow().isoformat()
            })
        else:
            # Fallback simple
            return jsonify({
                'compatibility_score': 75.0,
                'match_quality': 'Good Match',
                'reasons': ['Fallback calculation - AI engine not available'],
                'algorithm_version': 'fallback'
            })
    
    except Exception as e:
        logger.error(f"Error calculating compatibility: {e}")
        return jsonify({'error': 'Error calculating compatibility'}), 500

@ai_api.route('/documents/upload', methods=['POST'])
def upload_document():
    """
    Subir documento de candidato a Google Drive
    """
    try:
        if 'file' not in request.files:
            return jsonify({'error': 'No file provided'}), 400
        
        file = request.files['file']
        candidate_id = request.form.get('candidate_id')
        doc_type = request.form.get('doc_type', 'cv')
        
        if not candidate_id:
            return jsonify({'error': 'candidate_id is required'}), 400
        
        if file.filename == '':
            return jsonify({'error': 'No file selected'}), 400
        
        # Verificar tipo de archivo
        allowed_extensions = {'.pdf', '.doc', '.docx', '.txt'}
        file_ext = os.path.splitext(file.filename)[1].lower()
        
        if file_ext not in allowed_extensions:
            return jsonify({'error': f'File type {file_ext} not allowed'}), 400
        
        if DRIVE_INTEGRATION_AVAILABLE:
            # Guardar archivo temporalmente
            import tempfile
            with tempfile.NamedTemporaryFile(delete=False, suffix=file_ext) as tmp_file:
                file.save(tmp_file.name)
                
                # Metadatos del documento
                metadata = {
                    'original_filename': file.filename,
                    'uploaded_by': request.remote_addr,
                    'upload_date': datetime.utcnow().isoformat()
                }
                
                # Subir a Google Drive
                result = upload_candidate_document(
                    tmp_file.name, candidate_id, doc_type, metadata
                )
                
                # Limpiar archivo temporal
                os.unlink(tmp_file.name)
                
                if result.get('upload_success'):
                    return jsonify({
                        'success': True,
                        'file_id': result.get('file_id'),
                        'message': 'Document uploaded successfully',
                        'extracted_text_length': len(result.get('extracted_text', ''))
                    })
                else:
                    return jsonify({
                        'success': False,
                        'error': result.get('error', 'Upload failed')
                    }), 500
        else:
            return jsonify({
                'success': False,
                'error': 'Google Drive integration not available'
            }), 503
    
    except Exception as e:
        logger.error(f"Error uploading document: {e}")
        return jsonify({'error': 'Error uploading document'}), 500

@ai_api.route('/security/encrypt', methods=['POST'])
def encrypt_data():
    """
    Cifrar datos sensibles
    """
    try:
        data = request.get_json()
        sensitive_data = data.get('data')
        
        if not sensitive_data:
            return jsonify({'error': 'No data to encrypt'}), 400
        
        if SECURITY_MANAGER_AVAILABLE:
            encrypted = encrypt_user_data(sensitive_data)
            return jsonify({
                'encrypted': True,
                'data': encrypted
            })
        else:
            return jsonify({
                'encrypted': False,
                'error': 'Security manager not available'
            }), 503
    
    except Exception as e:
        logger.error(f"Error encrypting data: {e}")
        return jsonify({'error': 'Encryption failed'}), 500

@ai_api.route('/analytics/user-insights', methods=['GET'])
def get_user_insights():
    """
    Obtener insights inteligentes de usuarios
    """
    try:
        # Obtener estadísticas de la base de datos
        stats = get_system_statistics()
        
        # Análisis inteligente de tendencias
        insights = generate_intelligent_insights(stats)
        
        return jsonify({
            'statistics': stats,
            'insights': insights,
            'generated_at': datetime.utcnow().isoformat(),
            'analysis_version': '2.0'
        })
    
    except Exception as e:
        logger.error(f"Error getting user insights: {e}")
        return jsonify({'error': 'Error generating insights'}), 500

@ai_api.route('/system/health', methods=['GET'])
def system_health():
    """
    Estado de salud del sistema de IA
    """
    try:
        health_status = {
            'ai_agent': AI_AGENT_AVAILABLE,
            'matching_engine': MATCHING_ENGINE_AVAILABLE,
            'google_drive': DRIVE_INTEGRATION_AVAILABLE,
            'security_manager': SECURITY_MANAGER_AVAILABLE,
            'database': check_database_health(),
            'timestamp': datetime.utcnow().isoformat()
        }
        
        # Calcular estado general
        available_services = sum(1 for service in health_status.values() if service is True)
        total_services = len([k for k in health_status.keys() if k != 'timestamp'])
        
        health_status['overall_health'] = available_services / total_services
        health_status['status'] = 'healthy' if health_status['overall_health'] > 0.7 else 'degraded'
        
        return jsonify(health_status)
    
    except Exception as e:
        logger.error(f"Error checking system health: {e}")
        return jsonify({'error': 'Health check failed'}), 500

# Funciones auxiliares

def intelligent_fallback_response(message, user_id):
    """Respuesta inteligente de fallback"""
    message_lower = message.lower()
    
    if 'registro' in message_lower or 'registrar' in message_lower:
        response = 'Te ayudo con el registro. DiversIA conecta talento neurodivergente con empresas inclusivas. ¿Eres candidato o empresa?'
    elif any(word in message_lower for word in ['tdah', 'adhd']):
        response = 'TDAH es una neurodivergencia que apoyamos activamente. Tenemos formularios especializados y recursos específicos.'
    elif any(word in message_lower for word in ['tea', 'autismo']):
        response = 'Para TEA ofrecemos evaluaciones adaptadas y conexión con empresas que valoran la diversidad cognitiva.'
    elif 'dislexia' in message_lower:
        response = 'Apoyamos a personas con dislexia con tests especializados y conexión con asociaciones como DISFAM.'
    elif any(word in message_lower for word in ['trabajo', 'empleo']):
        response = 'Nuestro sistema de matching conecta candidatos con ofertas compatibles. ¿Cuál es tu área de experiencia?'
    else:
        response = 'Soy el asistente de DiversIA. Puedo ayudarte con registro, información sobre neurodivergencia, búsqueda de empleo y más.'
    
    stats = get_system_statistics()
    if stats.get('total_users', 0) > 0:
        response += f" Actualmente tenemos {stats['total_users']} profesionales registrados."
    
    return jsonify({
        'final_response': response,
        'response': response,
        'intent': 'general',
        'confidence': 0.8,
        'powered_by': 'DiversIA Fallback Intelligence'
    })

def get_fallback_message(message):
    """Mensaje de fallback básico"""
    return "Gracias por tu mensaje. Estoy aquí para ayudarte con cualquier consulta sobre DiversIA."

def get_fallback_recommendations():
    """Recomendaciones de fallback"""
    return [{
        'company_name': 'Empresa Inclusiva Demo',
        'job_title': 'Posición de Ejemplo',
        'compatibility_score': 75.0,
        'match_reasons': ['Sistema de matching en desarrollo'],
        'next_steps': 'Contactar para más información'
    }]

def get_match_quality_label(score):
    """Etiqueta de calidad del matching"""
    if score >= 90:
        return 'Excellent Match'
    elif score >= 80:
        return 'Very Good Match'
    elif score >= 70:
        return 'Good Match'
    elif score >= 60:
        return 'Fair Match'
    else:
        return 'Poor Match'

def get_system_statistics():
    """Obtener estadísticas del sistema"""
    try:
        stats = {}
        
        # Contar usuarios
        total_users = Usuario.query.count()
        stats['total_users'] = total_users
        
        # Contar por tipo de neurodivergencia
        tdah_users = Usuario.query.filter_by(tipo_neurodivergencia='TDAH').count()
        tea_users = Usuario.query.filter_by(tipo_neurodivergencia='TEA').count()
        dislexia_users = Usuario.query.filter_by(tipo_neurodivergencia='Dislexia').count()
        
        stats['tdah_users'] = tdah_users
        stats['tea_users'] = tea_users
        stats['dislexia_users'] = dislexia_users
        
        # Contar empresas
        total_companies = Empresa.query.count()
        stats['total_companies'] = total_companies
        
        return stats
        
    except Exception as e:
        logger.error(f"Error getting statistics: {e}")
        return {'total_users': 0, 'total_companies': 0}

def generate_intelligent_insights(stats):
    """Generar insights inteligentes"""
    insights = []
    
    total_users = stats.get('total_users', 0)
    total_companies = stats.get('total_companies', 0)
    
    if total_users > 0:
        # Distribución de neurodivergencia
        tdah_pct = (stats.get('tdah_users', 0) / total_users) * 100
        tea_pct = (stats.get('tea_users', 0) / total_users) * 100
        dislexia_pct = (stats.get('dislexia_users', 0) / total_users) * 100
        
        insights.append(f"Distribución: TDAH {tdah_pct:.1f}%, TEA {tea_pct:.1f}%, Dislexia {dislexia_pct:.1f}%")
        
        if total_companies > 0:
            ratio = total_users / total_companies
            insights.append(f"Ratio candidatos/empresas: {ratio:.1f}")
            
            if ratio > 10:
                insights.append("Alta demanda de candidatos - oportunidad para más empresas")
            elif ratio < 3:
                insights.append("Equilibrio favorable - buenas oportunidades de matching")
    
    if not insights:
        insights.append("Sistema en crecimiento - datos insuficientes para análisis detallado")
    
    return insights

def check_database_health():
    """Verificar salud de la base de datos"""
    try:
        # Intentar una consulta simple
        db.session.execute('SELECT 1')
        return True
    except Exception:
        return False

# Registrar el blueprint
def register_ai_endpoints(app):
    """Registrar endpoints de IA en la aplicación"""
    app.register_blueprint(ai_api)
    logger.info("✅ AI API endpoints registered")

if __name__ == "__main__":
    print("AI API Endpoints Module")
    print(f"AI Agent Available: {AI_AGENT_AVAILABLE}")
    print(f"Matching Engine Available: {MATCHING_ENGINE_AVAILABLE}")
    print(f"Google Drive Available: {DRIVE_INTEGRATION_AVAILABLE}")
    print(f"Security Manager Available: {SECURITY_MANAGER_AVAILABLE}")