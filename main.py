from app import app

# Importar rutas después de crear la app
import routes  # noqa: F401

# Sistema de autenticación final (con PostgreSQL)
try:
    import admin_final  # noqa: F401
    print("✅ Sistema de autenticación admin final cargado")
except Exception as e:
    print(f"⚠️ Error cargando admin_final: {e}")

# Cargar solo CRM API (sin conflictos de rutas)
try:
    import crm_api_simple  # noqa: F401
    print("✅ CRM API cargado correctamente")
except Exception as e:
    print(f"⚠️ Error cargando CRM: {e}")

# Cargar sistema de respaldo de notificaciones
try:
    import email_fallback_system  # noqa: F401
    print("✅ Sistema de respaldo de notificaciones cargado")
except Exception as e:
    print(f"⚠️ Error cargando sistema de respaldo: {e}")

# Cargar gestor de persistencia de datos
try:
    import data_persistence_manager  # noqa: F401
    print("✅ Gestor de persistencia de datos cargado")
    
    # Configurar EMAIL_PASSWORD si no está configurado
    import os
    if not os.getenv('EMAIL_PASSWORD'):
        os.environ['EMAIL_PASSWORD'] = 'wazu oawd qucz zeze'
        print("📧 EMAIL_PASSWORD configurado desde código")
    
except Exception as e:
    print(f"⚠️ Error cargando gestor de persistencia: {e}")

# Cargar sistema de asignación de tareas
try:
    import task_assignment_system  # noqa: F401
    print("✅ Sistema de asignación de tareas cargado")
except Exception as e:
    print(f"⚠️ Error cargando sistema de asignación: {e}")

# Cargar servicio de integración de formularios
try:
    import form_integration_service  # noqa: F401
    print("✅ Servicio de integración de formularios cargado")
except Exception as e:
    print(f"⚠️ Error cargando servicio de formularios: {e}")
from api_endpoints import api
from chat_webhook import chat
from chat_intelligent_endpoint import intelligent_chat

# Register API and webhook blueprints
app.register_blueprint(api)
app.register_blueprint(chat)
app.register_blueprint(intelligent_chat)

# Import AI endpoints
try:
    from api_endpoints_ai import register_ai_endpoints
    register_ai_endpoints(app)
    print("✅ AI endpoints registered successfully")
except ImportError as e:
    print(f"⚠️ AI endpoints not available: {e}")
    print("Basic functionality will work, advanced AI features require additional packages")

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
