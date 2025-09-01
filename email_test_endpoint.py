"""
Endpoint para probar el sistema de emails de DiversIA
"""
from app import app
from flask import jsonify, request
from flask_email_service import email_service

@app.route('/api/test-email', methods=['POST', 'GET'])
def test_email_system():
    """Endpoint para probar que los emails funcionen"""
    try:
        # Probar email de bienvenida para usuario
        user_email_sent = email_service.send_welcome_email_user(
            nombre="Usuario de Prueba",
            email="diversiaeternals@gmail.com",
            tipo_neurodivergencia="Test"
        )
        
        # Probar email de bienvenida para empresa
        company_email_sent = email_service.send_welcome_email_company(
            nombre_empresa="Empresa de Prueba",
            email="diversiaeternals@gmail.com",
            sector="Tecnología",
            tamano="Mediana"
        )
        
        # Probar email de notificación
        notification_sent = email_service.send_notification_email("usuario", {
            'nombre': 'Usuario',
            'apellidos': 'de Prueba',
            'email': 'test@ejemplo.com',
            'ciudad': 'Madrid',
            'tipo_neurodivergencia': 'TDAH'
        })
        
        return jsonify({
            'success': True,
            'message': 'Sistema de emails funcionando correctamente',
            'tests': {
                'user_welcome_email': user_email_sent,
                'company_welcome_email': company_email_sent,
                'notification_email': notification_sent,
                'gmail_configured': email_service.is_configured
            }
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e),
            'gmail_configured': email_service.is_configured
        }), 500

print("✅ Endpoint de test de emails agregado: /api/test-email")