from flask import render_template, request, redirect, url_for, flash, jsonify
from app import app, db
from models import User, Company, JobOffer, TestResult
from forms import (RegistroGeneralForm, RegistroTDAHForm, RegistroDislexiaForm, RegistroTEAForm, 
                  RegistroDiscalculiaForm, RegistroTouretteForm, RegistroDispraxiaForm, 
                  RegistroAnsiedadForm, RegistroBipolarForm, RegistroAltasCapacidadesForm,
                  EmpresaForm, OfertaTrabajoForm)
from sendgrid_helper import send_registration_notification, send_company_registration_notification

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/personas-nd')
def personas_nd():
    return render_template('personas-nd.html')

@app.route('/empresas')
def empresas():
    form = EmpresaForm()
    oferta_form = OfertaTrabajoForm()
    return render_template('empresas.html', form=form, oferta_form=oferta_form)

@app.route('/comunidad')
def comunidad():
    return render_template('comunidad.html')

@app.route('/asociaciones')
def asociaciones():
    return render_template('asociaciones.html')

@app.route('/metricool-verification')
def metricool_verification():
    return render_template('metricool_verification.html')

@app.route('/politica-privacidad')
def politica_privacidad():
    return render_template('politica-privacidad.html')

@app.route('/terminos-condiciones')
def terminos_condiciones():
    return render_template('terminos-condiciones.html')

@app.route('/aviso-legal')
def aviso_legal():
    return render_template('aviso-legal.html')

@app.route('/politica-cookies')
def politica_cookies():
    return render_template('politica_cookies.html')

@app.route('/sobre-nosotros')
def sobre_nosotros():
    return render_template('sobre-nosotros.html')

@app.route('/contacto')
def contacto():
    return render_template('contacto.html')

@app.route('/crm')
def crm_dashboard():
    try:
        from flask import session, redirect, flash
        if 'admin_id' not in session:
            flash('Debes iniciar sesión como administrador para acceder al CRM.', 'error')
            return redirect('/admin/login')
        return render_template('crm-dashboard.html')
    except Exception as e:
        print(f"Error en CRM dashboard: {e}")
        flash('Error interno del servidor. Inténtalo de nuevo.', 'error')
        return redirect('/')

# Rutas para formularios del CRM
@app.route('/admin/create-task')
def create_task():
    from flask import session, redirect, flash
    if 'admin_id' not in session:
        flash('Debes iniciar sesión como administrador.', 'error')
        return redirect('/admin/login')
    return render_template('admin/create_task.html')

@app.route('/admin/create-employee')
def create_employee():
    from flask import session, redirect, flash
    if 'admin_id' not in session:
        flash('Debes iniciar sesión como administrador.', 'error')
        return redirect('/admin/login')
    return render_template('admin/create_employee.html')

@app.route('/admin/edit-employee')
def edit_employee():
    from flask import session, redirect, flash
    if 'admin_id' not in session:
        flash('Debes iniciar sesión como administrador.', 'error')
        return redirect('/admin/login')
    return render_template('admin/edit_employee.html')

@app.route('/admin/edit-task')
def edit_task():
    from flask import session, redirect, flash
    if 'admin_id' not in session:
        flash('Debes iniciar sesión como administrador.', 'error')
        return redirect('/admin/login')
    return render_template('admin/edit_task.html')

@app.route('/admin/edit-contact')
def edit_contact():
    from flask import session, redirect, flash
    if 'admin_id' not in session:
        flash('Debes iniciar sesión como administrador.', 'error')
        return redirect('/admin/login')
    return render_template('admin/edit_contact.html')

@app.route('/admin/edit-company')
def edit_company():
    from flask import session, redirect, flash
    if 'admin_id' not in session:
        flash('Debes iniciar sesión como administrador.', 'error')
        return redirect('/admin/login')
    return render_template('admin/edit_company.html')

@app.route('/enviar-contacto', methods=['POST'])
def enviar_contacto():
    try:
        nombre = request.form.get('nombre')
        email = request.form.get('email')
        asunto = request.form.get('asunto')
        mensaje = request.form.get('mensaje')
        
        if not all([nombre, email, asunto, mensaje]):
            flash('Por favor completa todos los campos requeridos.', 'error')
            return redirect(url_for('contacto'))
        
        # Enviar notificación por email
        try:
            from sendgrid_helper import send_contact_notification
            success = send_contact_notification(nombre, email, asunto, mensaje)
        except ImportError:
            success = False
        
        if success:
            flash('¡Mensaje enviado correctamente! Te responderemos en 24-48 horas.', 'success')
        else:
            flash('Hubo un problema al enviar el mensaje. Por favor contacta directamente a diversiaeternals@gmail.com', 'warning')
            
    except Exception as e:
        flash('Error al enviar el mensaje. Por favor intenta de nuevo.', 'error')
    
    return redirect(url_for('contacto'))

@app.route('/registro', methods=['GET', 'POST'])
def registro():
    form = RegistroGeneralForm()
    if form.validate_on_submit():
        user = User(
            nombre=form.nombre.data,
            apellidos=form.apellidos.data,
            email=form.email.data,
            fecha_nacimiento=form.fecha_nacimiento.data,
            telefono=form.telefono.data,
            ciudad=form.ciudad.data,
            tipo_neurodivergencia=form.tipo_neurodivergencia.data,
            diagnostico_formal=form.diagnostico_formal.data,
            experiencia_laboral=form.experiencia_laboral.data,
            formacion_academica=form.formacion_academica.data,
            habilidades=form.habilidades.data,
            intereses_laborales=form.intereses_laborales.data,
            adaptaciones_necesarias=form.adaptaciones_necesarias.data
        )
        db.session.add(user)
        db.session.commit()
        
        # Enviar email de notificación
        user_data = {
            'nombre': form.nombre.data,
            'apellidos': form.apellidos.data,
            'email': form.email.data,
            'telefono': form.telefono.data,
            'ciudad': form.ciudad.data,
            'fecha_nacimiento': form.fecha_nacimiento.data,
            'tipo_neurodivergencia': form.tipo_neurodivergencia.data,
            'diagnostico_formal': form.diagnostico_formal.data,
            'experiencia_laboral': form.experiencia_laboral.data,
            'formacion_academica': form.formacion_academica.data,
            'habilidades': form.habilidades.data,
            'intereses_laborales': form.intereses_laborales.data,
            'adaptaciones_necesarias': form.adaptaciones_necesarias.data
        }
        send_registration_notification(user_data, "Registro General")
        
        flash('¡Registro completado exitosamente!', 'success')
        return redirect(url_for('index'))
    return render_template('registro.html', form=form)

@app.route('/registro-tdah', methods=['GET', 'POST'])
def registro_tdah():
    form = RegistroTDAHForm()
    if form.validate_on_submit():
        user = User(
            nombre=form.nombre.data,
            apellidos=form.apellidos.data,
            email=form.email.data,
            fecha_nacimiento=form.fecha_nacimiento.data,
            telefono=form.telefono.data,
            ciudad=form.ciudad.data,
            tipo_neurodivergencia='tdah',
            diagnostico_formal=form.diagnostico_formal.data,
            experiencia_laboral=form.experiencia_laboral.data,
            formacion_academica=form.formacion_academica.data,
            habilidades=form.habilidades.data,
            intereses_laborales=form.intereses_laborales.data,
            adaptaciones_necesarias=form.adaptaciones_necesarias.data
        )
        db.session.add(user)
        db.session.commit()
        
        # Enviar email de notificación
        user_data = {
            'nombre': form.nombre.data,
            'apellidos': form.apellidos.data,
            'email': form.email.data,
            'telefono': form.telefono.data,
            'ciudad': form.ciudad.data,
            'fecha_nacimiento': form.fecha_nacimiento.data,
            'tipo_neurodivergencia': 'TDAH',
            'diagnostico_formal': form.diagnostico_formal.data,
            'experiencia_laboral': form.experiencia_laboral.data,
            'formacion_academica': form.formacion_academica.data,
            'habilidades': form.habilidades.data,
            'intereses_laborales': form.intereses_laborales.data,
            'adaptaciones_necesarias': form.adaptaciones_necesarias.data
        }
        send_registration_notification(user_data, "Registro TDAH")
        
        flash('¡Registro de TDAH completado exitosamente!', 'success')
        return redirect(url_for('index'))
    return render_template('registro-tdah.html', form=form)

@app.route('/registro-dislexia', methods=['GET', 'POST'])
def registro_dislexia():
    form = RegistroDislexiaForm()
    if form.validate_on_submit():
        user = User(
            nombre=form.nombre.data,
            apellidos=form.apellidos.data,
            email=form.email.data,
            fecha_nacimiento=form.fecha_nacimiento.data,
            telefono=form.telefono.data,
            ciudad=form.ciudad.data,
            tipo_neurodivergencia='dislexia',
            diagnostico_formal=form.diagnostico_formal.data,
            experiencia_laboral=form.experiencia_laboral.data,
            formacion_academica=form.formacion_academica.data,
            habilidades=form.habilidades.data,
            intereses_laborales=form.intereses_laborales.data,
            adaptaciones_necesarias=form.adaptaciones_necesarias.data
        )
        db.session.add(user)
        db.session.commit()
        
        # Enviar email de notificación
        user_data = {
            'nombre': form.nombre.data,
            'apellidos': form.apellidos.data,
            'email': form.email.data,
            'telefono': form.telefono.data,
            'ciudad': form.ciudad.data,
            'fecha_nacimiento': form.fecha_nacimiento.data,
            'tipo_neurodivergencia': 'Dislexia',
            'diagnostico_formal': form.diagnostico_formal.data,
            'experiencia_laboral': form.experiencia_laboral.data,
            'formacion_academica': form.formacion_academica.data,
            'habilidades': form.habilidades.data,
            'intereses_laborales': form.intereses_laborales.data,
            'adaptaciones_necesarias': form.adaptaciones_necesarias.data
        }
        send_registration_notification(user_data, "Registro Dislexia")
        
        flash('¡Registro de Dislexia completado exitosamente!', 'success')
        return redirect(url_for('index'))
    return render_template('registro-dislexia.html', form=form)

@app.route('/registro-tea', methods=['GET', 'POST'])
def registro_tea():
    form = RegistroTEAForm()
    if form.validate_on_submit():
        user = User(
            nombre=form.nombre.data,
            apellidos=form.apellidos.data,
            email=form.email.data,
            fecha_nacimiento=form.fecha_nacimiento.data,
            telefono=form.telefono.data,
            ciudad=form.ciudad.data,
            tipo_neurodivergencia='tea',
            diagnostico_formal=form.diagnostico_formal.data,
            experiencia_laboral=form.experiencia_laboral.data,
            formacion_academica=form.formacion_academica.data,
            habilidades=form.habilidades.data,
            intereses_laborales=form.intereses_laborales.data,
            adaptaciones_necesarias=form.adaptaciones_necesarias.data
        )
        db.session.add(user)
        db.session.commit()
        
        # Enviar email de notificación
        user_data = {
            'nombre': form.nombre.data,
            'apellidos': form.apellidos.data,
            'email': form.email.data,
            'telefono': form.telefono.data,
            'ciudad': form.ciudad.data,
            'fecha_nacimiento': form.fecha_nacimiento.data,
            'tipo_neurodivergencia': 'TEA (Trastorno del Espectro Autista)',
            'diagnostico_formal': form.diagnostico_formal.data,
            'experiencia_laboral': form.experiencia_laboral.data,
            'formacion_academica': form.formacion_academica.data,
            'habilidades': form.habilidades.data,
            'intereses_laborales': form.intereses_laborales.data,
            'adaptaciones_necesarias': form.adaptaciones_necesarias.data
        }
        send_registration_notification(user_data, "Registro TEA")
        
        flash('¡Registro de TEA completado exitosamente!', 'success')
        return redirect(url_for('index'))
    return render_template('registro-tea.html', form=form)

@app.route('/registro-discalculia', methods=['GET', 'POST'])
def registro_discalculia():
    form = RegistroDiscalculiaForm()
    if form.validate_on_submit():
        user = User(
            nombre=form.nombre.data,
            apellidos=form.apellidos.data,
            email=form.email.data,
            fecha_nacimiento=form.fecha_nacimiento.data,
            telefono=form.telefono.data,
            ciudad=form.ciudad.data,
            tipo_neurodivergencia='discalculia',
            diagnostico_formal=form.diagnostico_formal.data,
            experiencia_laboral=form.experiencia_laboral.data,
            formacion_academica=form.formacion_academica.data,
            habilidades=form.habilidades.data,
            intereses_laborales=form.intereses_laborales.data,
            adaptaciones_necesarias=form.adaptaciones_necesarias.data
        )
        db.session.add(user)
        db.session.commit()
        
        # Enviar email de notificación
        user_data = {
            'nombre': form.nombre.data,
            'apellidos': form.apellidos.data,
            'email': form.email.data,
            'telefono': form.telefono.data,
            'ciudad': form.ciudad.data,
            'fecha_nacimiento': form.fecha_nacimiento.data,
            'tipo_neurodivergencia': 'Discalculia',
            'diagnostico_formal': form.diagnostico_formal.data,
            'experiencia_laboral': form.experiencia_laboral.data,
            'formacion_academica': form.formacion_academica.data,
            'habilidades': form.habilidades.data,
            'intereses_laborales': form.intereses_laborales.data,
            'adaptaciones_necesarias': form.adaptaciones_necesarias.data
        }
        send_registration_notification(user_data, "Registro Discalculia")
        
        flash('¡Registro de Discalculia completado exitosamente!', 'success')
        return redirect(url_for('index'))
    return render_template('registro-discalculia.html', form=form)

@app.route('/registro-tourette', methods=['GET', 'POST'])
def registro_tourette():
    form = RegistroTouretteForm()
    if form.validate_on_submit():
        user = User(
            nombre=form.nombre.data,
            apellidos=form.apellidos.data,
            email=form.email.data,
            fecha_nacimiento=form.fecha_nacimiento.data,
            telefono=form.telefono.data,
            ciudad=form.ciudad.data,
            tipo_neurodivergencia='tourette',
            diagnostico_formal=form.diagnostico_formal.data,
            experiencia_laboral=form.experiencia_laboral.data,
            formacion_academica=form.formacion_academica.data,
            habilidades=form.habilidades.data,
            intereses_laborales=form.intereses_laborales.data,
            adaptaciones_necesarias=form.adaptaciones_necesarias.data
        )
        db.session.add(user)
        db.session.commit()
        
        # Enviar email de notificación
        user_data = {
            'nombre': form.nombre.data,
            'apellidos': form.apellidos.data,
            'email': form.email.data,
            'telefono': form.telefono.data,
            'ciudad': form.ciudad.data,
            'fecha_nacimiento': form.fecha_nacimiento.data,
            'tipo_neurodivergencia': 'Síndrome de Tourette',
            'diagnostico_formal': form.diagnostico_formal.data,
            'experiencia_laboral': form.experiencia_laboral.data,
            'formacion_academica': form.formacion_academica.data,
            'habilidades': form.habilidades.data,
            'intereses_laborales': form.intereses_laborales.data,
            'adaptaciones_necesarias': form.adaptaciones_necesarias.data
        }
        send_registration_notification(user_data, "Registro Síndrome de Tourette")
        
        flash('¡Registro de Síndrome de Tourette completado exitosamente!', 'success')
        return redirect(url_for('index'))
    return render_template('registro-tourette.html', form=form)

@app.route('/registro-dispraxia', methods=['GET', 'POST'])
def registro_dispraxia():
    form = RegistroDispraxiaForm()
    if form.validate_on_submit():
        user = User(
            nombre=form.nombre.data,
            apellidos=form.apellidos.data,
            email=form.email.data,
            fecha_nacimiento=form.fecha_nacimiento.data,
            telefono=form.telefono.data,
            ciudad=form.ciudad.data,
            tipo_neurodivergencia='dispraxia',
            diagnostico_formal=form.diagnostico_formal.data,
            experiencia_laboral=form.experiencia_laboral.data,
            formacion_academica=form.formacion_academica.data,
            habilidades=form.habilidades.data,
            intereses_laborales=form.intereses_laborales.data,
            adaptaciones_necesarias=form.adaptaciones_necesarias.data
        )
        db.session.add(user)
        db.session.commit()
        
        # Enviar email de notificación
        user_data = {
            'nombre': form.nombre.data,
            'apellidos': form.apellidos.data,
            'email': form.email.data,
            'telefono': form.telefono.data,
            'ciudad': form.ciudad.data,
            'fecha_nacimiento': form.fecha_nacimiento.data,
            'tipo_neurodivergencia': 'Dispraxia',
            'diagnostico_formal': form.diagnostico_formal.data,
            'experiencia_laboral': form.experiencia_laboral.data,
            'formacion_academica': form.formacion_academica.data,
            'habilidades': form.habilidades.data,
            'intereses_laborales': form.intereses_laborales.data,
            'adaptaciones_necesarias': form.adaptaciones_necesarias.data
        }
        send_registration_notification(user_data, "Registro Dispraxia")
        
        flash('¡Registro de Dispraxia completado exitosamente!', 'success')
        return redirect(url_for('index'))
    return render_template('registro-dispraxia.html', form=form)

@app.route('/registro-ansiedad', methods=['GET', 'POST'])
def registro_ansiedad():
    form = RegistroAnsiedadForm()
    if form.validate_on_submit():
        user = User(
            nombre=form.nombre.data,
            apellidos=form.apellidos.data,
            email=form.email.data,
            fecha_nacimiento=form.fecha_nacimiento.data,
            telefono=form.telefono.data,
            ciudad=form.ciudad.data,
            tipo_neurodivergencia='ansiedad',
            diagnostico_formal=form.diagnostico_formal.data,
            experiencia_laboral=form.experiencia_laboral.data,
            formacion_academica=form.formacion_academica.data,
            habilidades=form.habilidades.data,
            intereses_laborales=form.intereses_laborales.data,
            adaptaciones_necesarias=form.adaptaciones_necesarias.data
        )
        db.session.add(user)
        db.session.commit()
        
        # Enviar email de notificación
        user_data = {
            'nombre': form.nombre.data,
            'apellidos': form.apellidos.data,
            'email': form.email.data,
            'telefono': form.telefono.data,
            'ciudad': form.ciudad.data,
            'fecha_nacimiento': form.fecha_nacimiento.data,
            'tipo_neurodivergencia': 'Trastornos de Ansiedad',
            'diagnostico_formal': form.diagnostico_formal.data,
            'experiencia_laboral': form.experiencia_laboral.data,
            'formacion_academica': form.formacion_academica.data,
            'habilidades': form.habilidades.data,
            'intereses_laborales': form.intereses_laborales.data,
            'adaptaciones_necesarias': form.adaptaciones_necesarias.data
        }
        send_registration_notification(user_data, "Registro Trastornos de Ansiedad")
        
        flash('¡Registro de Trastornos de Ansiedad completado exitosamente!', 'success')
        return redirect(url_for('index'))
    return render_template('registro-ansiedad.html', form=form)

@app.route('/registro-bipolar', methods=['GET', 'POST'])
def registro_bipolar():
    form = RegistroBipolarForm()
    if form.validate_on_submit():
        user = User(
            nombre=form.nombre.data,
            apellidos=form.apellidos.data,
            email=form.email.data,
            fecha_nacimiento=form.fecha_nacimiento.data,
            telefono=form.telefono.data,
            ciudad=form.ciudad.data,
            tipo_neurodivergencia='bipolar',
            diagnostico_formal=form.diagnostico_formal.data,
            experiencia_laboral=form.experiencia_laboral.data,
            formacion_academica=form.formacion_academica.data,
            habilidades=form.habilidades.data,
            intereses_laborales=form.intereses_laborales.data,
            adaptaciones_necesarias=form.adaptaciones_necesarias.data
        )
        db.session.add(user)
        db.session.commit()
        
        # Enviar email de notificación
        user_data = {
            'nombre': form.nombre.data,
            'apellidos': form.apellidos.data,
            'email': form.email.data,
            'telefono': form.telefono.data,
            'ciudad': form.ciudad.data,
            'fecha_nacimiento': form.fecha_nacimiento.data,
            'tipo_neurodivergencia': 'Trastorno Bipolar',
            'diagnostico_formal': form.diagnostico_formal.data,
            'experiencia_laboral': form.experiencia_laboral.data,
            'formacion_academica': form.formacion_academica.data,
            'habilidades': form.habilidades.data,
            'intereses_laborales': form.intereses_laborales.data,
            'adaptaciones_necesarias': form.adaptaciones_necesarias.data
        }
        send_registration_notification(user_data, "Registro Trastorno Bipolar")
        
        flash('¡Registro de Trastorno Bipolar completado exitosamente!', 'success')
        return redirect(url_for('index'))
    return render_template('registro-bipolar.html', form=form)

@app.route('/registro-altas-capacidades', methods=['GET', 'POST'])
def registro_altas_capacidades():
    form = RegistroAltasCapacidadesForm()
    if form.validate_on_submit():
        user = User(
            nombre=form.nombre.data,
            apellidos=form.apellidos.data,
            email=form.email.data,
            fecha_nacimiento=form.fecha_nacimiento.data,
            telefono=form.telefono.data,
            ciudad=form.ciudad.data,
            tipo_neurodivergencia='altas_capacidades',
            diagnostico_formal=form.diagnostico_formal.data,
            experiencia_laboral=form.experiencia_laboral.data,
            formacion_academica=form.formacion_academica.data,
            habilidades=form.habilidades.data,
            intereses_laborales=form.intereses_laborales.data,
            adaptaciones_necesarias=form.adaptaciones_necesarias.data
        )
        db.session.add(user)
        db.session.commit()
        
        # Enviar email de notificación
        user_data = {
            'nombre': form.nombre.data,
            'apellidos': form.apellidos.data,
            'email': form.email.data,
            'telefono': form.telefono.data,
            'ciudad': form.ciudad.data,
            'fecha_nacimiento': form.fecha_nacimiento.data,
            'tipo_neurodivergencia': 'Altas Capacidades',
            'diagnostico_formal': form.diagnostico_formal.data,
            'experiencia_laboral': form.experiencia_laboral.data,
            'formacion_academica': form.formacion_academica.data,
            'habilidades': form.habilidades.data,
            'intereses_laborales': form.intereses_laborales.data,
            'adaptaciones_necesarias': form.adaptaciones_necesarias.data
        }
        send_registration_notification(user_data, "Registro Altas Capacidades")
        
        flash('¡Registro de Altas Capacidades completado exitosamente!', 'success')
        return redirect(url_for('index'))
    return render_template('registro-altas-capacidades.html', form=form)

@app.route('/descargar-guia-laboral')
def descargar_guia_laboral():
    """Ruta para descargar la guía de preparación laboral"""
    try:
        with open('static/resources/guia-preparacion-laboral.md', 'r', encoding='utf-8') as file:
            content = file.read()
        
        # Crear respuesta con el contenido del archivo
        response = app.response_class(
            content,
            mimetype='text/markdown',
            headers={'Content-Disposition': 'attachment; filename=Guia_Preparacion_Laboral_DiversIA.md'}
        )
        return response
    except FileNotFoundError:
        flash('La guía no está disponible en este momento. Por favor, inténtalo más tarde.', 'error')
        return redirect(url_for('personas_nd'))

@app.route('/videos-informativos')
def videos_informativos():
    """Página con videos informativos sobre neurodiversidad"""
    videos = [
        {
            'titulo': 'Neurodiversidad y Empleo - NeurodiverSí',
            'descripcion': 'Serie educativa sobre inclusión laboral para personas neurodivergentes',
            'url': 'https://neurodiversi.org/neurovideo/',
            'categoria': 'Educativo'
        },
        {
            'titulo': 'Microsoft: El futuro del trabajo es neurodiverso',
            'descripcion': 'Iniciativas de inclusión laboral de Microsoft para personas neurodivergentes',
            'url': 'https://news.microsoft.com/source/latam/noticias-de-microsoft/el-futuro-del-trabajo-es-neurodiverso/',
            'categoria': 'Casos de éxito'
        },
        {
            'titulo': 'Fundación Neurodiversidad - Capacitaciones',
            'descripcion': 'Cursos gratuitos y congresos sobre neurodiversidad e inclusión',
            'url': 'https://fundacionneurodiversidad.tiendup.com/',
            'categoria': 'Formación'
        },
        {
            'titulo': 'FLEDNI - Diplomatura en Neurodiversidad',
            'descripcion': 'Formación profesional sobre neurodiversidad desde perspectiva crítica',
            'url': 'https://fledni.org/',
            'categoria': 'Profesional'
        }
    ]
    return render_template('videos-informativos.html', videos=videos)

@app.route('/podcast-diversia')
def podcast_diversia():
    """Página del podcast DiversIA"""
    return render_template('podcast-diversia.html')

@app.route('/registro-asociacion', methods=['GET', 'POST'])
def registro_asociacion():
    """Formulario para registro de nuevas asociaciones"""
    from forms import AsociacionForm
    from models import Asociacion
    import json
    from flask import request
    
    form = AsociacionForm()
    
    if form.validate_on_submit():
        try:
            # Crear nueva asociación
            nueva_asociacion = Asociacion()
            
            # Información básica
            nueva_asociacion.nombre_asociacion = form.nombre_asociacion.data
            nueva_asociacion.acronimo = form.acronimo.data
            nueva_asociacion.pais = form.pais.data
            nueva_asociacion.otro_pais = form.otro_pais.data if form.pais.data == 'OTHER' else None
            
            # Información legal
            nueva_asociacion.tipo_documento = form.tipo_documento.data
            nueva_asociacion.numero_documento = form.numero_documento.data
            nueva_asociacion.descripcion_otro_documento = form.descripcion_otro_documento.data
            
            # Servicios y neurodivergencias (convertir listas a JSON)
            nueva_asociacion.neurodivergencias_atendidas = json.dumps(form.neurodivergencias_atendidas.data)
            nueva_asociacion.servicios = json.dumps(form.servicios.data)
            nueva_asociacion.certificaciones = json.dumps(form.certificaciones.data) if form.certificaciones.data else None
            
            # Información de contacto
            nueva_asociacion.ciudad = form.ciudad.data
            nueva_asociacion.direccion = form.direccion.data
            nueva_asociacion.telefono = form.telefono.data
            nueva_asociacion.email = form.email.data
            nueva_asociacion.sitio_web = form.sitio_web.data
            nueva_asociacion.descripcion = form.descripcion.data
            
            # Información operativa
            nueva_asociacion.años_funcionamiento = form.años_funcionamiento.data
            nueva_asociacion.numero_socios = form.numero_socios.data
            
            # Contacto responsable
            nueva_asociacion.contacto_nombre = form.contacto_nombre.data
            nueva_asociacion.contacto_cargo = form.contacto_cargo.data
            
            # Información de auditoría
            nueva_asociacion.ip_solicitud = request.remote_addr
            nueva_asociacion.user_agent = request.user_agent.string[:500]
            nueva_asociacion.estado = 'pendiente'  # Por defecto pendiente de verificación
            
            # Guardar en base de datos
            db.session.add(nueva_asociacion)
            db.session.commit()
            
            # Enviar notificación por email
            try:
                from sendgrid_helper import send_notification_email
                
                # Preparar datos para la notificación
                asociacion_data = {
                    'nombre_asociacion': nueva_asociacion.nombre_asociacion,
                    'pais': nueva_asociacion.pais,
                    'ciudad': nueva_asociacion.ciudad,
                    'email': nueva_asociacion.email,
                    'telefono': nueva_asociacion.telefono,
                    'neurodivergencias': ', '.join(form.neurodivergencias_atendidas.data),
                    'servicios': ', '.join(form.servicios.data),
                    'contacto_nombre': nueva_asociacion.contacto_nombre,
                    'contacto_cargo': nueva_asociacion.contacto_cargo,
                    'tipo_documento': nueva_asociacion.tipo_documento,
                    'numero_documento': nueva_asociacion.numero_documento,
                    'años_funcionamiento': nueva_asociacion.años_funcionamiento,
                    'numero_socios': nueva_asociacion.numero_socios
                }
                
                send_notification_email(asociacion_data, "Nueva Solicitud de Asociación")
                
            except ImportError:
                print("SendGrid no disponible - notificación no enviada")
            except Exception as e:
                print(f"Error enviando notificación: {e}")
            
            flash('¡Solicitud de asociación enviada exitosamente! La revisaremos y nos pondremos en contacto contigo pronto.', 'success')
            return redirect(url_for('asociaciones'))
            
        except Exception as e:
            db.session.rollback()
            flash('Error al procesar la solicitud. Por favor, inténtalo de nuevo.', 'error')
            print(f"Error en registro de asociación: {e}")
    
    return render_template('registro-asociacion.html', form=form)

@app.route('/empresa-registro', methods=['POST'])
def empresa_registro():
    form = EmpresaRegistroForm()
    if form.validate_on_submit():
        company = Company(
            nombre_empresa=form.nombre_empresa.data,
            email_contacto=form.email_contacto.data,
            telefono=form.telefono.data,
            sector=form.sector.data,
            tamano_empresa=form.tamano_empresa.data,
            ciudad=form.ciudad.data
        )
        db.session.add(company)
        db.session.commit()
        
        # Enviar email de notificación
        company_data = {
            'nombre': form.nombre_empresa.data,
            'contacto_email': form.email_contacto.data,
            'contacto_telefono': form.telefono.data,
            'sector': form.sector.data,
            'tamaño': form.tamano_empresa.data,
            'ubicacion': form.ciudad.data,
            'sitio_web': 'N/A',
            'contacto_nombre': 'N/A',
            'experiencia_neurodivergentes': False,
            'politicas_inclusion': 'N/A',
            'adaptaciones_disponibles': 'N/A'
        }
        send_company_registration_notification(company_data)
        
        flash('¡Empresa registrada exitosamente!', 'success')
    return redirect(url_for('empresas'))

@app.route('/ofertas-empleo', methods=['POST'])
def crear_oferta():
    form = OfertaEmpleoForm()
    if form.validate_on_submit():
        # For simplicity, using company_id = 1. In production, this would come from authentication
        offer = JobOffer(
            company_id=1,
            titulo_puesto=form.titulo_puesto.data,
            descripcion=form.descripcion.data,
            tipo_contrato=form.tipo_contrato.data,
            modalidad_trabajo=form.modalidad_trabajo.data,
            salario_min=form.salario_min.data,
            salario_max=form.salario_max.data,
            requisitos=form.requisitos.data,
            adaptaciones_disponibles=form.adaptaciones_disponibles.data,
            neurodivergencias_target=','.join(form.neurodivergencias_target.data or [])
        )
        db.session.add(offer)
        db.session.commit()
        flash('¡Oferta de empleo creada exitosamente!', 'success')
    return redirect(url_for('empresas'))

@app.route('/api/ofertas')
def api_ofertas():
    ofertas = JobOffer.query.filter_by(activa=True).all()
    return jsonify([{
        'id': oferta.id,
        'titulo': oferta.titulo_puesto,
        'empresa': oferta.company.nombre_empresa,
        'modalidad': oferta.modalidad_trabajo,
        'fecha': oferta.created_at.strftime('%d/%m/%Y')
    } for oferta in ofertas])

# Error handlers
@app.errorhandler(404)
def not_found_error(error):
    return render_template('404.html'), 404

@app.errorhandler(500)
def internal_error(error):
    db.session.rollback()
    return render_template('500.html'), 500
