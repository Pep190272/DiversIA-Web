from app import app

# Routes principales
@app.route('/')
def index():
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
import task_manager  # noqa: F401

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)