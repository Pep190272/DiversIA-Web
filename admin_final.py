"""
Sistema final de autenticación admin que funciona con PostgreSQL
Elimina conflictos y usa la nueva base de datos activa
"""

from functools import wraps
from flask import session, request, redirect, url_for, flash, render_template
from app import app, db
from datetime import datetime
import hashlib
import os

# Modelo Admin que funciona con PostgreSQL
class AdminUser(db.Model):
    __tablename__ = 'admin_users'
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    last_login = db.Column(db.DateTime)

    def set_password(self, password):
        self.password_hash = hashlib.sha256(password.encode()).hexdigest()

    def check_password(self, password):
        return self.password_hash == hashlib.sha256(password.encode()).hexdigest()

def init_admin_system():
    """Inicializar sistema admin con usuario por defecto"""
    try:
        with app.app_context():
            db.create_all()
            
            # Crear admin por defecto si no existe
            admin = AdminUser.query.filter_by(username='DiversiaEternals').first()
            if not admin:
                admin = AdminUser(
                    username='DiversiaEternals',
                    email='diversiaeternals@gmail.com'
                )
                admin.set_password('diversia3ternal$2025')
                db.session.add(admin)
                db.session.commit()
                print("✅ Usuario admin creado: DiversiaEternals")
            else:
                print("✅ Usuario admin ya existe")
        return True
    except Exception as e:
        print(f"⚠️ Error inicializando admin: {e}")
        return False

def admin_required_new(f):
    """Decorador para rutas que requieren autenticación admin"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'admin_user_id' not in session:
            flash('Debes iniciar sesión como administrador.', 'error')
            return redirect(url_for('admin_login_new'))
        
        try:
            admin = AdminUser.query.get(session['admin_user_id'])
            if not admin or not admin.is_active:
                session.pop('admin_user_id', None)
                flash('Tu sesión ha expirado.', 'error')
                return redirect(url_for('admin_login_new'))
        except Exception:
            # Si hay error de BD, usar credenciales hardcodeadas
            if session.get('admin_username') != 'DiversiaEternals':
                session.clear()
                flash('Sesión inválida.', 'error')
                return redirect(url_for('admin_login_new'))
        
        return f(*args, **kwargs)
    return decorated_function

@app.route('/admin/login-new', methods=['GET', 'POST'])
def admin_login_new():
    """Login admin que funciona con PostgreSQL y fallback"""
    if request.method == 'POST':
        username = request.form.get('username', '').strip()
        password = request.form.get('password', '').strip()
        
        if not username or not password:
            flash('Por favor completa todos los campos.', 'error')
            return render_template('admin/login.html')
        
        try:
            # Intentar autenticación con PostgreSQL
            admin = AdminUser.query.filter_by(username=username).first()
            if admin and admin.check_password(password) and admin.is_active:
                session['admin_user_id'] = admin.id
                session['admin_username'] = admin.username
                session['admin_email'] = admin.email
                
                admin.last_login = datetime.utcnow()
                db.session.commit()
                
                flash(f'¡Bienvenido, {username}!', 'success')
                return redirect(url_for('admin_dashboard_new'))
            else:
                flash('Credenciales incorrectas.', 'error')
                
        except Exception as e:
            print(f"Error BD en login: {e}")
            # Fallback a credenciales hardcodeadas
            if (username == 'DiversiaEternals' and 
                hashlib.sha256(password.encode()).hexdigest() == 
                hashlib.sha256('diversia3ternal$2025'.encode()).hexdigest()):
                
                session['admin_user_id'] = 999  # ID temporal
                session['admin_username'] = username
                session['admin_email'] = 'diversiaeternals@gmail.com'
                
                flash(f'¡Bienvenido, {username}! (Modo respaldo)', 'success')
                return redirect(url_for('admin_dashboard_new'))
            else:
                flash('Credenciales incorrectas.', 'error')
    
    return render_template('admin/login.html')

@app.route('/admin/dashboard-new')
@admin_required_new
def admin_dashboard_new():
    """Dashboard admin funcional"""
    try:
        from crm_api_simple import get_all_data_summary
        crm_data = get_all_data_summary()
        
        dashboard_data = {
            'admin_username': session.get('admin_username', 'Admin'),
            'admin_email': session.get('admin_email', ''),
            'login_time': datetime.now().strftime('%Y-%m-%d %H:%M'),
            'total_contacts': crm_data.get('total_contacts', 0),
            'total_companies': crm_data.get('total_companies', 0),
            'total_job_offers': crm_data.get('total_job_offers', 0),
            'recent_submissions': crm_data.get('recent_submissions', [])[:5],
            'system_status': 'Operativo'
        }
        
        return render_template('admin/dashboard.html', **dashboard_data)
        
    except Exception as e:
        flash(f'Error cargando dashboard: {str(e)}', 'error')
        return render_template('admin/dashboard.html', 
                             admin_username=session.get('admin_username', 'Admin'),
                             system_status='Error')

@app.route('/admin/logout-new')
def admin_logout_new():
    """Logout admin"""
    session.clear()
    flash('Has cerrado sesión correctamente.', 'success')
    return redirect(url_for('index'))

# Inicializar sistema
if init_admin_system():
    print("✅ Sistema admin final inicializado correctamente")
    print("🔑 Acceso: /admin/login-new")
else:
    print("⚠️ Sistema admin funcionará en modo respaldo")