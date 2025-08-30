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

# configure the database with fallback
try:
    database_url = os.environ.get("DATABASE_URL")
    if database_url and "neon.tech" not in database_url:
        app.config["SQLALCHEMY_DATABASE_URI"] = database_url
        print("✅ Using PostgreSQL database")
    else:
        # Use SQLite as reliable fallback
        app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///diversia.db"
        print("✅ Using SQLite database (reliable mode)")
    
    app.config["SQLALCHEMY_ENGINE_OPTIONS"] = {
        "pool_recycle": 300,
        "pool_pre_ping": True,
    }
except Exception as e:
    print(f"⚠️ Database config error: {e}")
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///diversia.db"

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
    # Import models only (routes imported in main.py)
    try:
        import models
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

@app.route('/test/create-persistent-employee', methods=['POST'])
def create_persistent_employee_test():
    """Crear empleado con persistencia garantizada"""
    try:
        from flask import request, jsonify
        from crm_persistence import add_employee_persistent, fix_sendgrid_email_system
        
        # Datos del empleado (usar datos del request o valores por defecto)
        employee_data = {
            'first_name': request.json.get('first_name', 'Test'),
            'last_name': request.json.get('last_name', 'Employee'),
            'email': request.json.get('email', 'diversiaeternals@gmail.com'),
            'position': request.json.get('position', 'Desarrollador de Prueba'),
            'department': request.json.get('department', 'Testing'),
            'role': 'empleado',
            'salary': 35000
        }
        
        # Crear empleado persistente
        persistent_employee = add_employee_persistent(employee_data)
        
        # Verificar SendGrid
        sendgrid_ok = fix_sendgrid_email_system()
        
        if persistent_employee:
            return jsonify({
                'success': True,
                'message': f'Empleado {persistent_employee["first_name"]} {persistent_employee["last_name"]} creado y guardado persistentemente',
                'employee_id': persistent_employee['id'],
                'sendgrid_status': 'configurado' if sendgrid_ok else 'requiere configuración'
            })
        else:
            return jsonify({
                'success': False,
                'message': 'Error creando empleado persistente'
            }), 500
            
    except Exception as e:
        from flask import jsonify
        return jsonify({
            'success': False, 
            'message': f'Error: {str(e)}'
        }), 500

@app.route('/admin/system-status')
def admin_system_status():
    """Página de estado del sistema para administradores"""
    from flask import session, redirect, flash, render_template
    if 'admin_id' not in session:
        flash('Debes iniciar sesión como administrador.', 'error')
        return redirect('/admin/login')
    return render_template('admin/system_status.html')
