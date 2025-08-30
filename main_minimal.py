from app import app
from flask import render_template

# Start with just the basic routes - WEB PÚBLICA DE DIVERSIA
@app.route('/')
def index():
    """Página principal pública de DiversIA"""
    return render_template('index.html')

@app.route('/test')
def test():
    """Simple test route"""
    return '''
    <h1>✅ DiversIA Working!</h1>
    <p>Basic server is running correctly.</p>
    <a href="/">Home</a>
    '''

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

# Test basic functionality first
print("✅ Minimal main app loaded successfully")

if __name__ == "__main__":
    # Only run Flask dev server if called directly, not when imported by gunicorn
    app.run(host="0.0.0.0", port=5000, debug=True)