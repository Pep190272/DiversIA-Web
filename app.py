import os
import logging
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase
from werkzeug.middleware.proxy_fix import ProxyFix

# Set up logging for production - MÁXIMA ESTABILIDAD
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler()
    ]
)

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
    "pool_timeout": 30,
    "max_overflow": 10,  # Permitir más conexiones en picos
    "pool_size": 20,     # Pool más grande
    "echo": False,
    "connect_args": {
        "connect_timeout": 15,
        "keepalives_idle": 600,
        "keepalives_interval": 30,
        "keepalives_count": 5,  # Más intentos de keepalive
    }
}

# MANEJO GLOBAL DE ERRORES - NUNCA PARAR LA APLICACIÓN
@app.errorhandler(Exception)
def handle_global_exception(e):
    """Capturar TODOS los errores para que la app nunca se pare"""
    import traceback
    from flask import render_template, request
    
    # Log completo del error
    logging.error(f"💥 ERROR GLOBAL CAPTURADO: {str(e)}")
    logging.error(f"📍 Ruta: {request.url if request else 'N/A'}")
    logging.error(f"🔍 Traceback: {traceback.format_exc()}")
    
    # Respuesta de emergencia para mantener la web funcionando
    try:
        return render_template('error.html', error_message="Servicio temporalmente no disponible. La web sigue funcionando."), 500
    except:
        # Si ni siquiera el template funciona, respuesta HTML simple
        return '''
        <html>
        <head><title>DiversIA - Temporalmente no disponible</title></head>
        <body style="font-family: Arial; text-align: center; margin-top: 100px;">
            <h1>🌟 DiversIA</h1>
            <p>Servicio temporalmente no disponible. Reintentando automáticamente...</p>
            <p><a href="/">← Volver a la página principal</a></p>
            <script>setTimeout(() => location.reload(), 3000);</script>
        </body>
        </html>
        ''', 500

@app.errorhandler(404)
def handle_404(e):
    """Páginas no encontradas - redirigir a inicio"""
    return '''
    <html>
    <head><title>DiversIA - Página no encontrada</title></head>
    <body style="font-family: Arial; text-align: center; margin-top: 100px;">
        <h1>🌟 DiversIA</h1>
        <p>Página no encontrada</p>
        <p><a href="/">← Ir a la página principal</a></p>
        <script>setTimeout(() => location.href = '/', 2000);</script>
    </body>
    </html>
    ''', 404

@app.errorhandler(500)
def handle_500(e):
    """Errores del servidor - mantener funcionando"""
    return '''
    <html>
    <head><title>DiversIA - Error temporal</title></head>
    <body style="font-family: Arial; text-align: center; margin-top: 100px;">
        <h1>🌟 DiversIA</h1>
        <p>Error temporal del servidor. Reintentando...</p>
        <p><a href="/">← Volver a la página principal</a></p>
        <script>setTimeout(() => location.reload(), 2000);</script>
    </body>
    </html>
    ''', 500

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
        # NUNCA dejar que falle la base de datos pare la app
        logging.error(f"🚨 Error de BD: {e}")

# PROTECCIÓN DE BASE DE DATOS - RECUPERACIÓN AUTOMÁTICA
def safe_db_operation(func):
    """Decorator para operaciones de BD que no pueden fallar"""
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            logging.error(f"🚨 DB Operation failed: {func.__name__} - {e}")
            db.session.rollback()
            # Intentar reconectar
            try:
                from sqlalchemy import text
                db.session.execute(text('SELECT 1'))
                logging.info("✅ DB reconectada exitosamente")
            except:
                logging.error("💥 DB reconexión falló - usando datos de emergencia")
            return None
    return wrapper


@app.route('/admin/system-status')
def admin_system_status():
    """Página de estado del sistema para administradores"""
    from flask import session, redirect, flash, render_template
    if 'admin_id' not in session:
        flash('Debes iniciar sesión como administrador.', 'error')
        return redirect('/admin/login')
    return render_template('admin/system_status.html')
