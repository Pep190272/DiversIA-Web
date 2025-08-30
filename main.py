from app import app

# Configuración CORS para permitir formularios desde el navegador
@app.after_request
def after_request(response):
    response.headers.add('Access-Control-Allow-Origin', '*')
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
    response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE,OPTIONS')
    return response
from flask import render_template

# Routes principales - WEB PÚBLICA DE DIVERSIA
@app.route('/')
def index():
    """Página principal pública de DiversIA"""
    return render_template('index.html')

# Panel de administración movido a ruta específica
@app.route('/admin-dashboard')
def admin_dashboard():
    """Panel de administración del sistema"""
    return """
    <html>
    <head>
        <title>DiversIA - Sistema de Gestión</title>
        <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
    </head>
    <body class="bg-light">
        <div class="container mt-5">
            <div class="row justify-content-center">
                <div class="col-md-8">
                    <div class="card">
                        <div class="card-body text-center">
                            <h1 class="card-title">🌟 DiversIA - Sistema de Gestión</h1>
                            <p class="card-text lead">Plataforma integral de gestión empresarial para inclusión laboral</p>
                            <hr>
                            <div class="row">
                                <div class="col-md-6 mb-3">
                                    <div class="card border-primary">
                                        <div class="card-body">
                                            <h5>🎯 Gestión de Tareas</h5>
                                            <p>Sistema completo de asignación y seguimiento de tareas con colaboradores</p>
                                            <a href="/tasks" class="btn btn-primary">Acceder</a>
                                        </div>
                                    </div>
                                </div>
                                <div class="col-md-6 mb-3">
                                    <div class="card border-success">
                                        <div class="card-body">
                                            <h5>📧 Email Marketing</h5>
                                            <p>CRM para gestión de campañas de email a asociaciones</p>
                                            <a href="/email-marketing?admin=true" class="btn btn-success">Acceder</a>
                                        </div>
                                    </div>
                                </div>
                                <div class="col-md-6 mb-3">
                                    <div class="card border-info">
                                        <div class="card-body">
                                            <h5>🏢 CRM Minimal</h5>
                                            <p>Sistema de gestión de contactos empresariales</p>
                                            <a href="/crm-minimal" class="btn btn-info">Acceder</a>
                                        </div>
                                    </div>
                                </div>
                                <div class="col-md-6 mb-3">
                                    <div class="card border-warning">
                                        <div class="card-body">
                                            <h5>👑 Administración</h5>
                                            <p>Panel de administración del sistema</p>
                                            <a href="/diversia-admin" class="btn btn-warning">Acceder</a>
                                        </div>
                                    </div>
                                </div>
                            </div>
                            <hr>
                            <small class="text-muted">
                                Sistema completamente funcional • Presentación lista • Datos reales integrados
                            </small>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </body>
    </html>
    """

# Importar rutas simplificadas
import routes_simple  # noqa: F401

# Sistema de login que FUNCIONA
import login_system  # noqa: F401

# CRM Minimal - Sistema principal
try:
    from crm_minimal import create_minimal_crm_routes
    create_minimal_crm_routes(app)
    print("✅ CRM Minimal cargado")
except Exception as e:
    print(f"⚠️ Error CRM: {e}")

# Admin básico
try:
    import admin_final  # noqa: F401
    print("✅ Admin disponible: /admin/login-new")
except Exception as e:
    print(f"⚠️ Error admin: {e}")

# Email Marketing System
import email_marketing_manager  # noqa: F401
import email_notifications  # noqa: F401
import task_manager
import colaboradores_manager  # noqa: F401

if __name__ == "__main__":
    # Flask development server optimized for web preview
    print("🌐 Iniciando DiversIA Web Preview Server...")
    app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0
    app.config['TEMPLATES_AUTO_RELOAD'] = True
    app.run(host="0.0.0.0", port=5000, debug=True, use_reloader=False, threaded=True)