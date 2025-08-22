"""
Sistema admin ultra-simple que SÍ FUNCIONA
"""

from flask import render_template, request, redirect, session, flash
from app import app
import hashlib

# Credenciales hardcodeadas que SIEMPRE funcionan
ADMIN_USER = "DiversiaEternals"
ADMIN_PASS = "diversia3ternal$2025"

@app.route('/admin/login-new', methods=['GET', 'POST'])
def admin_login_simple():
    """Login admin ultra-simple que FUNCIONA"""
    if request.method == 'POST':
        username = request.form.get('username', '').strip()
        password = request.form.get('password', '').strip()
        
        if username == ADMIN_USER and password == ADMIN_PASS:
            session['admin_logged_in'] = True
            session['admin_username'] = username
            flash('¡Login exitoso!', 'success')
            return redirect('/crm-minimal')
        else:
            flash('Credenciales incorrectas', 'error')
    
    return render_template('admin/login_simple.html')

@app.route('/admin/logout')
def admin_logout_simple():
    """Logout simple"""
    session.clear()
    flash('Sesión cerrada', 'info')
    return redirect('/')

print("✅ Admin ultra-simple cargado")