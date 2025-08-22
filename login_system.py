"""
Sistema de login que FUNCIONA - Sin conflictos
"""

from flask import render_template, request, redirect, session, flash
from app import app

@app.route('/diversia-admin')
def diversia_admin_page():
    """Página de login admin que FUNCIONA"""
    return render_template('login_admin.html')

@app.route('/diversia-admin-check', methods=['POST'])
def diversia_admin_check():
    """Verificar credenciales admin"""
    username = request.form.get('username', '').strip()
    password = request.form.get('password', '').strip()
    
    if username == 'DiversiaEternals' and password == 'diversia3ternal$2025':
        session['admin_ok'] = True
        session['admin_user'] = username
        return redirect('/sistema-gestion')
    else:
        flash('Credenciales incorrectas', 'error')
        return redirect('/diversia-admin')

@app.route('/diversia-admin-logout')
def diversia_admin_logout():
    """Logout admin"""
    session.clear()
    return redirect('/')

print("Login system cargado - /diversia-admin")