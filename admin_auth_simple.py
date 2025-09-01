"""
Sistema de autenticación admin simplificado que funciona sin base de datos
Para presentaciones y demos - credenciales hardcodeadas
"""

from functools import wraps
from flask import session, request, redirect, url_for, flash, render_template
from app import app
from datetime import datetime
import hashlib

# Credenciales hardcodeadas para presentación
ADMIN_CREDENTIALS = {
    'DiversiaEternals': {
        'password_hash': hashlib.sha256('diversia3ternal$2025'.encode()).hexdigest(),
        'email': 'diversiaeternals@gmail.com',
        'is_super_admin': True,
        'permissions': ['all']
    }
}

def check_admin_credentials(username, password):
    """Verificar credenciales del admin sin base de datos"""
    if username not in ADMIN_CREDENTIALS:
        return False
    
    password_hash = hashlib.sha256(password.encode()).hexdigest()
    return ADMIN_CREDENTIALS[username]['password_hash'] == password_hash

def admin_required(f):
    """Decorador que requiere autenticación de admin"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'admin_logged_in' not in session or not session['admin_logged_in']:
            flash('Debes iniciar sesión como administrador.', 'error')
            return redirect(url_for('admin_login_simple'))
        return f(*args, **kwargs)
    return decorated_function

# Ruta de login simplificada
@app.route('/admin/login', methods=['GET', 'POST'])
def admin_login_simple():
    """Login admin que funciona sin base de datos"""
    if request.method == 'POST':
        username = request.form.get('username', '').strip()
        password = request.form.get('password', '').strip()
        
        if not username or not password:
            flash('Por favor completa todos los campos.', 'error')
            return render_template('admin/login.html')
        
        if check_admin_credentials(username, password):
            # Establecer sesión
            session['admin_logged_in'] = True
            session['admin_username'] = username
            session['admin_email'] = ADMIN_CREDENTIALS[username]['email']
            session['admin_is_super'] = ADMIN_CREDENTIALS[username]['is_super_admin']
            session['admin_login_time'] = datetime.now().isoformat()
            
            flash(f'¡Bienvenido, {username}!', 'success')
            return redirect(url_for('admin_dashboard_simple'))
        else:
            flash('Credenciales incorrectas. Verifica usuario y contraseña.', 'error')
    
    return render_template('admin/login.html')

@app.route('/admin/logout')
def admin_logout_simple():
    """Logout admin"""
    session.pop('admin_logged_in', None)
    session.pop('admin_username', None)
    session.pop('admin_email', None)
    session.pop('admin_is_super', None)
    session.pop('admin_login_time', None)
    
    flash('Has cerrado sesión correctamente.', 'success')
    return redirect(url_for('index'))

@app.route('/admin/dashboard')
@admin_required
def admin_dashboard_simple():
    """Dashboard admin que funciona sin base de datos"""
    try:
        # Importar CRM que funciona sin base de datos
        from crm_api_simple import get_all_data_summary
        crm_data = get_all_data_summary()
        
        dashboard_data = {
            'admin_username': session.get('admin_username', 'Admin'),
            'admin_email': session.get('admin_email', ''),
            'login_time': session.get('admin_login_time', ''),
            'total_contacts': crm_data.get('total_contacts', 0),
            'total_companies': crm_data.get('total_companies', 0),
            'total_job_offers': crm_data.get('total_job_offers', 0),
            'recent_submissions': crm_data.get('recent_submissions', [])[:5],
            'system_status': 'Operativo - Modo presentación'
        }
        
        return render_template('admin/dashboard.html', **dashboard_data)
        
    except Exception as e:
        flash(f'Error cargando dashboard: {str(e)}', 'error')
        return render_template('admin/dashboard.html', 
                             admin_username=session.get('admin_username', 'Admin'),
                             system_status='Error en datos')

print("✅ Sistema de autenticación admin simplificado cargado")
print("Credenciales: DiversiaEternals / diversia3ternal$2025")