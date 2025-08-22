from app import app

# Importar rutas simplificadas
import routes_simple  # noqa: F401

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

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)