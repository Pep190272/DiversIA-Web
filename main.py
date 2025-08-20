from app import app
try:
    import api_crm  # Importar las rutas de la API CRM
    import admin_auth  # Importar sistema de administración
    print("✅ CRM completo cargado")
except Exception as e:
    print(f"⚠️ Error cargando CRM completo: {e}")
    import crm_simple  # Fallback al CRM simple
    print("✅ CRM simple cargado como fallback")
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
