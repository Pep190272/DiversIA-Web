# Endpoint de prueba para CRM y emails
from flask import jsonify, request
from datetime import datetime

def create_test_routes(app):
    """
    Crear rutas de prueba para el sistema
    """
    
    @app.route('/test/email-system')
    def test_email_system_endpoint():
        """
        Endpoint para probar el sistema de emails desde el navegador
        """
        try:
            from test_email_system import run_email_test_only
            result = run_email_test_only()
            
            return jsonify({
                'success': result,
                'message': 'Prueba de emails completada' if result else 'Error en prueba de emails',
                'timestamp': datetime.now().isoformat(),
                'details': 'Revisa los logs del servidor para más información'
            })
            
        except Exception as e:
            return jsonify({
                'success': False,
                'message': f'Error ejecutando prueba: {str(e)}',
                'timestamp': datetime.now().isoformat()
            }), 500
    
    @app.route('/test/crm-integration')
    def test_crm_integration_endpoint():
        """
        Endpoint para probar la integración del CRM
        """
        try:
            from test_email_system import test_crm_integration
            result = test_crm_integration()
            
            return jsonify({
                'success': result,
                'message': 'Prueba de CRM completada' if result else 'Error en prueba de CRM',
                'timestamp': datetime.now().isoformat()
            })
            
        except Exception as e:
            return jsonify({
                'success': False,
                'message': f'Error ejecutando prueba CRM: {str(e)}',
                'timestamp': datetime.now().isoformat()
            }), 500
    
    @app.route('/test/complete-system')
    def test_complete_system_endpoint():
        """
        Endpoint para probar todo el sistema completo
        """
        try:
            from test_email_system import test_complete_system
            result = test_complete_system()
            
            return jsonify({
                'success': result,
                'message': 'Prueba completa del sistema finalizada',
                'timestamp': datetime.now().isoformat(),
                'details': 'Revisa los logs del servidor para información detallada'
            })
            
        except Exception as e:
            return jsonify({
                'success': False,
                'message': f'Error en prueba completa: {str(e)}',
                'timestamp': datetime.now().isoformat()
            }), 500

print("✅ Endpoints de prueba CRM cargados")