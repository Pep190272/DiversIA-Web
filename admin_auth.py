from functools import wraps
from flask import session, request, redirect, url_for, flash, render_template
from app import app, db
from datetime import datetime
import hashlib

# Modelo para administradores
class Admin(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    is_active = db.Column(db.Boolean, default=True)
    is_super_admin = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    last_login = db.Column(db.DateTime)
    permissions = db.Column(db.Text)  # JSON string with permissions

    def set_password(self, password):
        self.password_hash = hashlib.sha256(password.encode()).hexdigest()

    def check_password(self, password):
        return self.password_hash == hashlib.sha256(password.encode()).hexdigest()

    def has_permission(self, permission):
        if self.is_super_admin:
            return True
        if not self.permissions:
            return False
        import json
        perms = json.loads(self.permissions)
        return permission in perms

# Decorador para requerir autenticación de admin
def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'admin_id' not in session:
            flash('Debes iniciar sesión como administrador.', 'error')
            return redirect(url_for('admin_login'))
        
        admin = Admin.query.get(session['admin_id'])
        if not admin or not admin.is_active:
            session.pop('admin_id', None)
            flash('Tu sesión ha expirado o la cuenta ha sido desactivada.', 'error')
            return redirect(url_for('admin_login'))
        
        return f(*args, **kwargs)
    return decorated_function

# Decorador para requerir permisos específicos
def permission_required(permission):
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if 'admin_id' not in session:
                return redirect(url_for('admin_login'))
            
            admin = Admin.query.get(session['admin_id'])
            if not admin or not admin.has_permission(permission):
                flash('No tienes permisos para acceder a esta sección.', 'error')
                return redirect(url_for('admin_dashboard'))
            
            return f(*args, **kwargs)
        return decorated_function
    return decorator

# Rutas de autenticación
@app.route('/admin/login', methods=['GET', 'POST'])
def admin_login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        admin = Admin.query.filter_by(username=username, is_active=True).first()
        
        if admin and admin.check_password(password):
            session['admin_id'] = admin.id
            session['admin_username'] = admin.username
            session['is_super_admin'] = admin.is_super_admin
            
            admin.last_login = datetime.utcnow()
            db.session.commit()
            
            flash(f'Bienvenido {admin.username}', 'success')
            return redirect(url_for('admin_dashboard'))
        else:
            flash('Credenciales incorrectas.', 'error')
    
    return render_template('admin/login.html')

@app.route('/admin/logout')
def admin_logout():
    session.pop('admin_id', None)
    session.pop('admin_username', None)
    session.pop('is_super_admin', None)
    flash('Sesión cerrada correctamente.', 'success')
    return redirect(url_for('index'))

@app.route('/admin')
@admin_required
def admin_dashboard():
    return redirect(url_for('crm_dashboard'))

# Crear admin inicial si no existe
def create_initial_admin():
    with app.app_context():
        if not Admin.query.first():
            admin = Admin(
                username='admin',
                email='diversiaeternals@gmail.com',
                is_super_admin=True
            )
            admin.set_password('diversia2025')  # Cambiar esta contraseña
            db.session.add(admin)
            db.session.commit()
            print("✅ Admin inicial creado: admin/diversia2025")

# Inicializar admin al arrancar
try:
    create_initial_admin()
except:
    pass