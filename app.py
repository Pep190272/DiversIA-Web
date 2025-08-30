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


@app.route('/admin/system-status')
def admin_system_status():
    """Página de estado del sistema para administradores"""
    from flask import session, redirect, flash, render_template
    if 'admin_id' not in session:
        flash('Debes iniciar sesión como administrador.', 'error')
        return redirect('/admin/login')
    return render_template('admin/system_status.html')
