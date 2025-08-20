import os
import logging
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase
from werkzeug.middleware.proxy_fix import ProxyFix

# Set up logging
logging.basicConfig(level=logging.DEBUG)

class Base(DeclarativeBase):
    pass

db = SQLAlchemy(model_class=Base)

# create the app
app = Flask(__name__)
app.secret_key = os.environ.get("SESSION_SECRET", "dev-secret-key-change-in-production")
app.wsgi_app = ProxyFix(app.wsgi_app, x_proto=1, x_host=1)

# configure the database
app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get("DATABASE_URL", "sqlite:///diversia.db")
app.config["SQLALCHEMY_ENGINE_OPTIONS"] = {
    "pool_recycle": 300,
    "pool_pre_ping": True,
}

# Security headers
@app.after_request
def after_request(response):
    response.headers['X-Content-Type-Options'] = 'nosniff'
    response.headers['X-Frame-Options'] = 'DENY'
    response.headers['X-XSS-Protection'] = '1; mode=block'
    response.headers['Content-Security-Policy'] = "default-src 'self' 'unsafe-inline' 'unsafe-eval' https://cdn.jsdelivr.net https://cdnjs.cloudflare.com; img-src 'self' data: https:;"
    return response

# initialize the app with the extension
db.init_app(app)

with app.app_context():
    # Import models and routes
    try:
        import models
        import routes
        db.create_all()
        print("✅ Database initialized successfully")
    except Exception as e:
        print(f"⚠️ Database error: {e}")
        print("Application will run with limited functionality")

# Cargar endpoints de prueba del sistema
@app.route('/test/email-system')
def test_email_system_endpoint():
    """Endpoint para probar el sistema de emails desde el navegador"""
    try:
        from test_email_system import run_email_test_only
        result = run_email_test_only()
        from flask import jsonify
        return jsonify({
            'success': result,
            'message': 'Prueba de emails completada' if result else 'Error en prueba de emails - revisa SENDGRID_API_KEY',
            'details': 'Revisa los logs del servidor para más información'
        })
    except Exception as e:
        from flask import jsonify
        return jsonify({'success': False, 'message': f'Error: {str(e)}'}), 500

@app.route('/test/crm-integration')
def test_crm_integration_endpoint():
    """Endpoint para probar la integración del CRM"""
    try:
        from test_email_system import test_crm_integration
        result = test_crm_integration()
        from flask import jsonify
        return jsonify({
            'success': result,
            'message': 'Prueba de CRM completada' if result else 'Error en prueba de CRM'
        })
    except Exception as e:
        from flask import jsonify
        return jsonify({'success': False, 'message': f'Error: {str(e)}'}), 500
