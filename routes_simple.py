from flask import Flask, render_template, request, redirect, url_for, flash, session
from app import app, db
from datetime import datetime
import json

# ===== RUTAS BÁSICAS DEL SITIO WEB QUE FALTAN =====
# Nota: '/' ya está en main.py, solo añadimos las que faltan

@app.route('/personas-nd')
def personas_nd():
    return render_template('personas-nd.html')

@app.route('/empresas', methods=['GET', 'POST'])
def empresas():
    from forms import EmpresaForm
    form = EmpresaForm()
    
    if form.validate_on_submit():
        try:
            from models import Company
            nueva_empresa = Company(
                nombre=form.nombre.data,
                email=form.email.data,
                telefono=form.telefono.data,
                sector=form.sector.data,
                tamaño=form.tamaño.data,
                ciudad=form.ciudad.data,
                descripcion=form.descripcion.data,
                contacto_nombre=form.contacto_nombre.data,
                contacto_cargo=form.contacto_cargo.data
            )
            
            db.session.add(nueva_empresa)
            db.session.commit()
            
            flash('¡Empresa registrada exitosamente! Te contactaremos pronto.', 'success')
            return redirect(url_for('empresas'))
            
        except Exception as e:
            print(f"❌ Error registrando empresa: {e}")
            flash('Error al registrar la empresa. Por favor intenta de nuevo.', 'error')
    
    return render_template('empresas.html', form=form)

@app.route('/asociaciones')
def asociaciones():
    return render_template('asociaciones.html')

@app.route('/comunidad')
def comunidad():
    return render_template('comunidad.html')

@app.route('/contacto', methods=['GET', 'POST'])
def contacto():
    """Página de contacto - formulario simple por ahora"""
    return render_template('contacto.html')

@app.route('/sobre-nosotros')
def sobre_nosotros():
    return render_template('sobre-nosotros.html')

@app.route('/privacidad')
def privacidad():
    return render_template('privacidad.html')

@app.route('/aviso-legal')
def aviso_legal():
    return render_template('aviso-legal.html')

@app.route('/terminos')
def terminos():
    return render_template('terminos.html')

# ===== REGISTROS =====
@app.route('/registro')
def registro():
    """Página de registro general"""
    return render_template('registro.html')

# Rutas de registro específicas por neurodivergencia
@app.route('/registro-tdah', methods=['GET', 'POST'])
def registro_tdah():
    from forms import RegistroTDAHForm
    form = RegistroTDAHForm()
    if form.validate_on_submit():
        # Lógica de registro TDAH aquí
        flash('¡Registro TDAH completado exitosamente!', 'success')
        return redirect(url_for('personas_nd'))
    return render_template('registro-tdah.html', form=form)

@app.route('/registro-tea', methods=['GET', 'POST'])  
def registro_tea():
    from forms import RegistroTEAForm
    form = RegistroTEAForm()
    if form.validate_on_submit():
        flash('¡Registro TEA completado exitosamente!', 'success')
        return redirect(url_for('personas_nd'))
    return render_template('registro-tea.html', form=form)

@app.route('/registro-dislexia', methods=['GET', 'POST'])
def registro_dislexia():
    from forms import RegistroDislexiaForm 
    form = RegistroDislexiaForm()
    if form.validate_on_submit():
        flash('¡Registro Dislexia completado exitosamente!', 'success')
        return redirect(url_for('personas_nd'))
    return render_template('registro-dislexia.html', form=form)

# Rutas adicionales que requieren los templates
@app.route('/descargar-guia-laboral')
def descargar_guia_laboral():
    """Descargar guía laboral PDF"""
    return "Descarga de guía laboral (función temporal)", 200

@app.route('/videos-informativos')
def videos_informativos():
    """Videos informativos"""
    return "Videos informativos (función temporal)", 200

@app.route('/recursos-formacion')
def recursos_formacion():
    """Recursos de formación"""
    return "Recursos de formación (función temporal)", 200

@app.route('/comunidad-neurodivergentes')
def comunidad_neurodivergentes():
    """Comunidad neurodivergentes"""
    return "Comunidad neurodivergentes (función temporal)", 200

@app.route('/bolsa-trabajo')
def bolsa_trabajo():
    """Bolsa de trabajo"""
    return "Bolsa de trabajo (función temporal)", 200

@app.route('/test')
def test():
    """Test/evaluaciones"""
    return "Test y evaluaciones (función temporal)", 200

@app.route('/comenzar')
def comenzar():
    """Comenzar proceso"""
    return "Comenzar proceso (función temporal)", 200

@app.route('/podcast-diversia')
def podcast_diversia():
    """Podcast DiversIA"""
    return "Podcast DiversIA (función temporal)", 200

@app.route('/registro-discalculia', methods=['GET', 'POST'])
def registro_discalculia():
    from forms import RegistroGeneralForm
    form = RegistroGeneralForm()
    if form.validate_on_submit():
        flash('¡Registro completado exitosamente!', 'success')
        return redirect(url_for('personas_nd'))
    return render_template('registro-general.html', form=form, tipo='Discalculia')

@app.route('/registro-tourette', methods=['GET', 'POST'])
def registro_tourette():
    from forms import RegistroGeneralForm
    form = RegistroGeneralForm()
    if form.validate_on_submit():
        flash('¡Registro completado exitosamente!', 'success')
        return redirect(url_for('personas_nd'))
    return render_template('registro-general.html', form=form, tipo='Tourette')

@app.route('/registro-dispraxia', methods=['GET', 'POST'])
def registro_dispraxia():
    from forms import RegistroGeneralForm
    form = RegistroGeneralForm()
    if form.validate_on_submit():
        flash('¡Registro completado exitosamente!', 'success')
        return redirect(url_for('personas_nd'))
    return render_template('registro-general.html', form=form, tipo='Dispraxia')

@app.route('/registro-ansiedad', methods=['GET', 'POST'])
def registro_ansiedad():
    from forms import RegistroGeneralForm
    form = RegistroGeneralForm()
    if form.validate_on_submit():
        flash('¡Registro completado exitosamente!', 'success')
        return redirect(url_for('personas_nd'))
    return render_template('registro-general.html', form=form, tipo='Ansiedad')

@app.route('/registro-bipolar', methods=['GET', 'POST'])
def registro_bipolar():
    from forms import RegistroGeneralForm
    form = RegistroGeneralForm()
    if form.validate_on_submit():
        flash('¡Registro completado exitosamente!', 'success')
        return redirect(url_for('personas_nd'))
    return render_template('registro-general.html', form=form, tipo='Bipolar')

@app.route('/registro-altas-capacidades', methods=['GET', 'POST'])
def registro_altas_capacidades():
    from forms import RegistroGeneralForm
    form = RegistroGeneralForm()
    if form.validate_on_submit():
        flash('¡Registro completado exitosamente!', 'success')
        return redirect(url_for('personas_nd'))
    return render_template('registro-general.html', form=form, tipo='Altas Capacidades')

@app.route('/registro-asociacion', methods=['GET', 'POST'])
def registro_asociacion():
    """Registro de asociaciones neurodivergentes"""
    from forms import RegistroAsociacionForm
    
    form = RegistroAsociacionForm()
    
    if form.validate_on_submit():
        try:
            from models import Asociacion
            
            # Convertir listas a JSON strings
            neurodivergencias = ','.join(form.neurodivergencias_atendidas.data) if form.neurodivergencias_atendidas.data else ''
            servicios = ','.join(form.servicios.data) if form.servicios.data else ''
            certificaciones = ','.join(form.certificaciones.data) if form.certificaciones.data else ''
            
            nueva_asociacion = Asociacion(
                nombre_asociacion=form.nombre_asociacion.data,
                acronimo=form.acronimo.data,
                pais=form.pais.data,
                otro_pais=form.otro_pais.data if form.pais.data == 'otro' else None,
                tipo_documento=form.tipo_documento.data,
                numero_documento=form.numero_documento.data,
                descripcion_otro_documento=form.descripcion_otro_documento.data if form.tipo_documento.data == 'otro' else None,
                neurodivergencias_atendidas=neurodivergencias,
                servicios=servicios,
                certificaciones=certificaciones,
                ciudad=form.ciudad.data,
                direccion=form.direccion.data,
                telefono=form.telefono.data,
                email=form.email.data,
                sitio_web=form.sitio_web.data,
                descripcion=form.descripcion.data,
                años_funcionamiento=form.años_funcionamiento.data,
                numero_socios=form.numero_socios.data,
                contacto_nombre=form.contacto_nombre.data,
                contacto_cargo=form.contacto_cargo.data,
                estado='pendiente',
                ip_solicitud=request.remote_addr,
                user_agent=request.user_agent.string[:500] if request.user_agent else None
            )
            
            db.session.add(nueva_asociacion)
            db.session.commit()
            
            # Enviar notificación inmediata a DiversIA para verificación
            try:
                from email_notifications import send_association_registration_notification
                
                association_data = {
                    'nombre_asociacion': nueva_asociacion.nombre_asociacion,
                    'acronimo': nueva_asociacion.acronimo,
                    'pais': nueva_asociacion.pais,
                    'ciudad': nueva_asociacion.ciudad,
                    'email': nueva_asociacion.email,
                    'telefono': nueva_asociacion.telefono,
                    'tipo_documento': nueva_asociacion.tipo_documento,
                    'numero_documento': nueva_asociacion.numero_documento,
                    'neurodivergencias_atendidas': nueva_asociacion.neurodivergencias_atendidas,
                    'servicios': nueva_asociacion.servicios,
                    'contacto_nombre': nueva_asociacion.contacto_nombre,
                    'contacto_cargo': nueva_asociacion.contacto_cargo
                }
                
                email_sent = send_association_registration_notification(association_data)
                if email_sent:
                    print(f"✅ Notificación de verificación enviada a DiversIA")
                else:
                    print(f"⚠️ No se pudo enviar la notificación a DiversIA")
                    
            except Exception as e:
                print(f"⚠️ Error enviando notificación: {e}")
            
            print(f"✅ Asociación registrada: {nueva_asociacion.nombre_asociacion}")
            flash('¡Solicitud enviada! Te contactaremos cuando hayamos verificado tu asociación.', 'info')
            return redirect(url_for('asociaciones'))
            
        except Exception as e:
            print(f"❌ Error registrando asociación: {e}")
            flash('Error al registrar la asociación. Por favor intenta de nuevo.', 'error')
    
    return render_template('registro-asociacion.html', form=form)

# Panel de administración para verificar asociaciones
@app.route('/admin/verificar-asociaciones')
def verificar_asociaciones():
    """Panel para que DiversIA verifique y gestione asociaciones"""
    from flask import session, redirect
    
    # Verificar que es administrador
    if 'admin_ok' not in session or not session.get('admin_ok'):
        flash('Acceso restringido. Inicia sesión como administrador.', 'error')
        return redirect('/admin/login-new')
    
    from models import Asociacion, NotificationBackup
    
    # Obtener todas las asociaciones pendientes de verificación
    asociaciones_pendientes = Asociacion.query.filter(
        Asociacion.estado.in_(['verificando_documentacion', 'pendiente', 'documentos_requeridos'])
    ).order_by(Asociacion.created_at.desc()).all()
    
    # Marcar notificaciones como leídas cuando se accede al panel
    try:
        notifications = NotificationBackup.query.filter_by(
            tipo='asociacion_registro',
            estado='pendiente'
        ).all()
        
        for notification in notifications:
            notification.mark_as_read()
        
        if notifications:
            db.session.commit()
            print(f"✅ {len(notifications)} notificaciones marcadas como leídas")
            
    except Exception as e:
        print(f"⚠️ Error marcando notificaciones: {e}")
    
    # Contar notificaciones pendientes para el badge
    notificaciones_pendientes = NotificationBackup.query.filter_by(
        tipo='asociacion_registro',
        estado='pendiente'
    ).count()
    
    return render_template('admin/verificar-asociaciones.html', 
                         asociaciones=asociaciones_pendientes,
                         notificaciones_pendientes=notificaciones_pendientes)

# Ruta para mostrar el estado de las notificaciones
@app.route('/admin/notificaciones-pendientes')
def notificaciones_pendientes():
    """Dashboard de notificaciones de respaldo"""
    from flask import session, redirect
    
    if 'admin_ok' not in session or not session.get('admin_ok'):
        flash('Acceso restringido. Inicia sesión como administrador.', 'error')
        return redirect('/admin/login-new')
    
    from models import NotificationBackup
    
    # Obtener todas las notificaciones pendientes
    notifications = NotificationBackup.query.filter_by(
        estado='pendiente'
    ).order_by(NotificationBackup.created_at.desc()).all()
    
    # Contar por tipo
    registro_count = NotificationBackup.query.filter_by(
        tipo='asociacion_registro',
        estado='pendiente'
    ).count()
    
    return render_template('admin/notificaciones-pendientes.html',
                         notifications=notifications,
                         registro_count=registro_count)

@app.route('/admin/marcar-notificacion-leida/<int:notification_id>', methods=['POST'])
def marcar_notificacion_leida(notification_id):
    """Marcar una notificación como leída"""
    from flask import session, redirect
    
    if 'admin_ok' not in session or not session.get('admin_ok'):
        return redirect('/admin/login-new')
    
    try:
        from models import NotificationBackup
        notification = NotificationBackup.query.get_or_404(notification_id)
        notification.mark_as_read()
        db.session.commit()
        
        flash('Notificación marcada como leída.', 'success')
    except Exception as e:
        flash('Error al marcar la notificación.', 'error')
    
    return redirect('/admin/notificaciones-pendientes')

@app.route('/admin/asociacion/<int:asociacion_id>/aprobar', methods=['POST'])
def aprobar_asociacion(asociacion_id):
    """Aprobar una asociación"""
    from flask import session, redirect, jsonify
    
    if 'admin_ok' not in session or not session.get('admin_ok'):
        return jsonify({'error': 'Acceso denegado'}), 403
    
    try:
        from models import Asociacion
        
        asociacion = Asociacion.query.get_or_404(asociacion_id)
        asociacion.estado = 'aprobada'
        db.session.commit()
        
        # Enviar email de bienvenida
        try:
            from email_notifications import send_association_status_update
            
            association_data = {
                'nombre_asociacion': asociacion.nombre_asociacion,
                'email': asociacion.email,
                'contacto_nombre': asociacion.contacto_nombre
            }
            
            send_association_status_update(association_data, 'aprobada')
            print(f"✅ Email de aprobación enviado a {asociacion.email}")
        except Exception as e:
            print(f"⚠️ Error enviando email de aprobación: {e}")
        
        flash(f'Asociación {asociacion.nombre_asociacion} aprobada exitosamente.', 'success')
        return redirect('/admin/verificar-asociaciones')
        
    except Exception as e:
        print(f"❌ Error aprobando asociación: {e}")
        flash('Error al aprobar la asociación.', 'error')
        return redirect('/admin/verificar-asociaciones')

@app.route('/admin/asociacion/<int:asociacion_id>/rechazar', methods=['POST'])
def rechazar_asociacion(asociacion_id):
    """Rechazar una asociación"""
    from flask import session, redirect, request
    
    if 'admin_ok' not in session or not session.get('admin_ok'):
        flash('Acceso denegado', 'error')
        return redirect('/admin/login-new')
    
    try:
        from models import Asociacion
        
        asociacion = Asociacion.query.get_or_404(asociacion_id)
        motivo = request.form.get('motivo', 'No especificado')
        
        asociacion.estado = 'rechazada'
        asociacion.notas = f"Rechazada: {motivo}"
        db.session.commit()
        
        # Enviar email de rechazo
        try:
            from email_notifications import send_association_status_update
            
            association_data = {
                'nombre_asociacion': asociacion.nombre_asociacion,
                'email': asociacion.email,
                'contacto_nombre': asociacion.contacto_nombre
            }
            
            send_association_status_update(association_data, 'rechazada')
            print(f"✅ Email de rechazo enviado a {asociacion.email}")
        except Exception as e:
            print(f"⚠️ Error enviando email de rechazo: {e}")
        
        flash(f'Asociación {asociacion.nombre_asociacion} rechazada.', 'warning')
        return redirect('/admin/verificar-asociaciones')
        
    except Exception as e:
        print(f"❌ Error rechazando asociación: {e}")
        flash('Error al rechazar la asociación.', 'error')
        return redirect('/admin/verificar-asociaciones')

@app.route('/admin/asociacion/<int:asociacion_id>/solicitar-documentos', methods=['POST'])
def solicitar_documentos(asociacion_id):
    """Solicitar documentos a una asociación"""
    from flask import session, redirect
    
    if 'admin_ok' not in session or not session.get('admin_ok'):
        flash('Acceso denegado', 'error')
        return redirect('/admin/login-new')
    
    try:
        from models import Asociacion
        
        asociacion = Asociacion.query.get_or_404(asociacion_id)
        asociacion.estado = 'documentos_requeridos'
        db.session.commit()
        
        # Crear enlace único para subir documentos (simplificado)
        documents_link = f"https://{request.host}/subir-documentos/{asociacion.id}"
        
        # Enviar email solicitando documentos
        try:
            from email_notifications import send_association_status_update
            
            association_data = {
                'nombre_asociacion': asociacion.nombre_asociacion,
                'email': asociacion.email,
                'contacto_nombre': asociacion.contacto_nombre
            }
            
            send_association_status_update(association_data, 'documentos_requeridos', documents_link)
            print(f"✅ Email de documentos enviado a {asociacion.email}")
        except Exception as e:
            print(f"⚠️ Error enviando email de documentos: {e}")
        
        flash(f'Documentos solicitados a {asociacion.nombre_asociacion}.', 'info')
        return redirect('/admin/verificar-asociaciones')
        
    except Exception as e:
        print(f"❌ Error solicitando documentos: {e}")
        flash('Error al solicitar documentos.', 'error')
        return redirect('/admin/verificar-asociaciones')

# Ruta simplificada para subir documentos (las asociaciones pueden enviar por email)
@app.route('/subir-documentos/<int:asociacion_id>')
def subir_documentos(asociacion_id):
    """Página para que las asociaciones suban documentos"""
    from models import Asociacion
    
    try:
        asociacion = Asociacion.query.get_or_404(asociacion_id)
        
        if asociacion.estado != 'documentos_requeridos':
            return "Esta solicitud ya ha sido procesada o no requiere documentos.", 400
        
        return render_template('subir-documentos.html', asociacion=asociacion)
        
    except Exception as e:
        return f"Error: {e}", 500

print("✅ Routes simplificado cargado correctamente")