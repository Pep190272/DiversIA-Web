import os
import logging
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase
from werkzeug.middleware.proxy_fix import ProxyFix

# Set up logging for production
logging.basicConfig(level=logging.INFO)

class Base(DeclarativeBase):
    pass

db = SQLAlchemy(model_class=Base)

# create the app
app = Flask(__name__)
app.secret_key = os.environ.get("SESSION_SECRET", "dev-secret-key-change-in-production")

# Configuración de cookies y sesiones
app.config.update(
    SESSION_COOKIE_SECURE=False,  # Para desarrollo
    SESSION_COOKIE_HTTPONLY=True,  # Seguridad
    SESSION_COOKIE_SAMESITE='Lax',  # CSRF protection
    PERMANENT_SESSION_LIFETIME=7200,  # 2 horas
    SESSION_PERMANENT=False
)
app.wsgi_app = ProxyFix(app.wsgi_app, x_proto=1, x_host=1)

# configure the database - SOLO POSTGRESQL (CRÍTICO: Sin fallback SQLite)
database_url = os.environ.get("DATABASE_URL")
if not database_url:
    raise RuntimeError("❌ CRÍTICO: DATABASE_URL no configurada. PostgreSQL es obligatorio.")

app.config["SQLALCHEMY_DATABASE_URI"] = database_url
print("✅ PostgreSQL database connected")
app.config["SQLALCHEMY_ENGINE_OPTIONS"] = {
    "pool_recycle": 300,
    "pool_pre_ping": True,
    "pool_timeout": 20,
    "max_overflow": 0,
    "echo": False,
    "connect_args": {
        "connect_timeout": 10,
        "keepalives_idle": 600,
        "keepalives_interval": 30,
        "keepalives_count": 3,
    }
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
    # Import models only (routes imported in main.py)
    try:
        import models
        db.create_all()
        print("✅ Database initialized successfully")
    except Exception as e:
        print(f"⚠️ Database error: {e}")


@app.route('/admin/system-status')
def admin_system_status():
    """Página de estado del sistema para administradores"""
    from flask import session, redirect, flash, render_template
    if 'admin_id' not in session:
        flash('Debes iniciar sesión como administrador.', 'error')
        return redirect('/admin/login')
    return render_template('admin/system_status.html')
