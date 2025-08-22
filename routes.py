from flask import render_template, request, redirect, url_for, flash, jsonify
from datetime import datetime
from app import app, db
from models import User, Company, JobOffer, TestResult
from forms import (RegistroGeneralForm, RegistroTDAHForm, RegistroDislexiaForm, RegistroTEAForm, 
                  RegistroDiscalculiaForm, RegistroTouretteForm, RegistroDispraxiaForm, 
                  RegistroAnsiedadForm, RegistroBipolarForm, RegistroAltasCapacidadesForm,
                  EmpresaForm, OfertaTrabajoForm)
from sendgrid_helper import send_registration_notification, send_company_registration_notification

# Importar CSV Manager
try:
    from csv_manager import create_csv_routes
    create_csv_routes(app)
except ImportError:
    print("⚠️ CSV Manager no disponible")

# CRM Neurodivergentes eliminado para evitar conflictos

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/personas-nd')
def personas_nd():
    return render_template('personas-nd.html')

@app.route('/empresas', methods=['GET', 'POST'])
def empresas():
    form = EmpresaForm()
    oferta_form = OfertaTrabajoForm()
    
    if request.method == 'POST':
        try:
            # Debug: imprimir todos los datos del formulario
            print("=== DATOS RECIBIDOS EN FORMULARIO ===")
            for key, value in request.form.items():
                print(f"{key}: {value}")
            print("=====================================")
            
            # Obtener datos del formulario usando los nombres correctos del template
            data = {
                'nombre': request.form.get('nombre_empresa'),  # Campo del template
                'email': request.form.get('email_contacto'),   # Campo del template  
                'telefono': request.form.get('telefono'),
                'sector': request.form.get('sector'),
                'tamaño': request.form.get('tamano_empresa'),  # Campo del template
                'ciudad': request.form.get('ciudad'),
                'web': request.form.get('sitio_web'),          # Campo del template
                'descripcion': request.form.get('descripcion_empresa'),  # Campo del template
                'inclusivo': request.form.get('aceptar_privacidad'),  # Checkbox privacidad
                'created_at': datetime.now().isoformat()
            }
            
            print(f"Datos procesados: {data}")
            
            # Guardar directamente en SQLite
            company = Company(
                nombre_empresa=data['nombre'],
                email_contacto=data['email'],
                telefono=data['telefono'],
                sector=data['sector'],
                tamano_empresa=data['tamaño'],
                ciudad=data['ciudad'],
                sitio_web=data.get('web'),
                descripcion_empresa=data.get('descripcion')
            )
            db.session.add(company)
            db.session.commit()
            
            # Enviar email de notificación
            from sendgrid_helper import send_email
            subject = f"Nueva Empresa Registrada - {data['nombre']}"
            html_content = f"""
            <h2>🏢 Nueva Empresa Registrada</h2>
            <p><strong>Empresa:</strong> {data['nombre']}</p>
            <p><strong>Email:</strong> {data['email']}</p>
            <p><strong>Teléfono:</strong> {data['telefono']}</p>
            <p><strong>Sector:</strong> {data['sector']}</p>
            <p><strong>Tamaño:</strong> {data['tamaño']}</p>
            <p><strong>Ciudad:</strong> {data['ciudad']}</p>
            <p><strong>Web:</strong> {data.get('web', 'No especificado')}</p>
            <hr>
            <p>Panel admin: <a href="http://localhost:5000/admin/login-new">CRM</a></p>
            """
            email_success = send_email('diversiaeternals@gmail.com', subject, html_content)
            print(f"✅ Email empresa enviado: {email_success}")
            success = True
            
            if success:
                flash(f'Empresa {data["nombre"]} registrada exitosamente', 'success')
                return redirect(url_for('empresas'))
            else:
                flash('Error al registrar la empresa. Los datos han sido guardados en respaldo.', 'warning')
                return redirect(url_for('empresas'))
            
        except Exception as e:
            print(f"❌ Error procesando formulario empresa: {e}")
            flash('Error al registrar la empresa. Inténtalo de nuevo.', 'error')
    
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

# Rutas para los botones principales del inicio
@app.route('/test')
def test():
    """Ruta para "Haz mi test" - redirige al registro general"""
    return redirect(url_for('registro'))

@app.route('/comenzar')
def comenzar():
    """Ruta para "Comenzar ahora" - redirige a personas neurodivergentes"""
    return redirect(url_for('personas_nd'))

# API del Chat Inteligente
@app.route('/api/chat', methods=['POST'])
def chat_endpoint():
    """Endpoint para el chat inteligente"""
    try:
        from chat_simple import get_chat_response
        
        data = request.get_json()
        message = data.get('message', '')
        context = data.get('context', {})
        
        if not message:
            return jsonify({'error': 'Mensaje requerido'}), 400
        
        response = get_chat_response(message, context)
        return jsonify(response)
        
    except Exception as e:
        return jsonify({
            'error': 'Error en el chat',
            'response': 'Lo siento, hay un problema técnico. Intenta de nuevo.',
            'source': 'error'
        }), 500

# API del Motor de Emparejamiento
@app.route('/api/matching', methods=['POST'])
def matching_endpoint():
    """Endpoint para encontrar coincidencias de trabajo"""
    try:
        from matching_engine_simple import find_job_matches
        
        data = request.get_json()
        user_profile = data.get('user_profile', {})
        job_offers = data.get('job_offers', [])
        top_n = data.get('top_n', 5)
        
        if not user_profile:
            return jsonify({'error': 'Perfil de usuario requerido'}), 400
        
        matches = find_job_matches(user_profile, job_offers, top_n)
        
        return jsonify({
            'success': True,
            'matches': matches,
            'total_jobs_analyzed': len(job_offers),
            'top_matches_returned': len(matches)
        })
        
    except Exception as e:
        return jsonify({
            'error': 'Error en el motor de emparejamiento',
            'message': str(e)
        }), 500

@app.route('/contacto', methods=['GET', 'POST'])
def contacto():
    if request.method == 'POST':
        try:
            # Obtener datos del formulario
            nombre = request.form.get('nombre')
            email = request.form.get('email')
            asunto = request.form.get('asunto')
            mensaje = request.form.get('mensaje')
            
            # Validar campos requeridos
            if not all([nombre, email, mensaje]):
                flash('Por favor completa todos los campos obligatorios.', 'error')
                return render_template('contacto.html')
            
            # Enviar email de notificación
            from email_system_reliable import send_contact_notification
            success = send_contact_notification(nombre, email, asunto, mensaje)
            
            # Guardar en CRM
            try:
                from form_integration_service import process_form_submission
                contact_data = {
                    'nombre': nombre,
                    'email': email,
                    'mensaje': mensaje,
                    'tipo_interes': asunto,
                    'created_at': datetime.now().isoformat()
                }
                crm_id = process_form_submission('contacto', contact_data, 'web_form_contacto')
                if crm_id:
                    print(f"✅ Contacto añadido al CRM con ID: {crm_id}")
            except Exception as e:
                print(f"⚠️ Error añadiendo contacto al CRM: {e}")
            
            if success:
                flash('¡Mensaje enviado correctamente! Te responderemos en 24-48 horas.', 'success')
            else:
                flash('Hubo un problema al enviar el mensaje. Por favor contacta directamente a diversiaeternals@gmail.com', 'warning')
                
        except Exception as e:
            flash('Error al enviar el mensaje. Por favor intenta de nuevo.', 'error')
        
        return redirect(url_for('contacto'))
    
    return render_template('contacto.html')

@app.route('/crm')
def crm_dashboard():
    try:
        from flask import session, redirect, flash
        if 'admin_user_id' not in session:
            flash('Debes iniciar sesión como administrador para acceder al CRM.', 'error')
            return redirect('/admin/login-new')
        return render_template('crm-dashboard.html')
    except Exception as e:
        print(f"Error en CRM dashboard: {e}")
        flash('Error interno del servidor. Inténtalo de nuevo.', 'error')
        return redirect('/')

@app.route('/crm/neurodivergentes')
def crm_neurodivergentes():
    """Panel CRM especializado para personas neurodivergentes"""
    try:
        from flask import session, redirect, flash
        if 'admin_user_id' not in session:
            flash('Debes iniciar sesión como administrador para acceder al CRM.', 'error')
            return redirect('/admin/login-new')
        return render_template('crm-neurodivergentes.html')
    except Exception as e:
        print(f"Error en CRM neurodivergentes: {e}")
        flash('Error interno del servidor. Inténtalo de nuevo.', 'error')
        return redirect('/crm')

@app.route('/crm/funnel')
def crm_funnel_dashboard():
    from flask import session, redirect, flash
    if 'admin_logged_in' not in session or not session['admin_logged_in']:
        flash('Debes iniciar sesión como administrador.', 'error')
        return redirect('/admin/login')
    return render_template('crm-dashboard-funnel.html')

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

@app.route('/admin/edit-offer')
def edit_offer():
    from flask import session, redirect, flash
    if 'admin_id' not in session:
        flash('Debes iniciar sesión como administrador.', 'error')
        return redirect('/admin/login')
    return render_template('admin/edit_offer.html')

@app.route('/admin/edit-association')
def edit_association():
    from flask import session, redirect, flash
    if 'admin_id' not in session:
        flash('Debes iniciar sesión como administrador.', 'error')
        return redirect('/admin/login')
    return render_template('admin/edit_association.html')

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
        
        # Intentar enviar email, usar sistema de respaldo si falla
        email_sent = False
        try:
            from email_system_reliable import send_contact_notification
            email_sent = send_contact_notification(nombre, email, asunto, mensaje)
            if email_sent:
                print(f"✅ Email de contacto enviado exitosamente a diversiaeternals@gmail.com")
        except ImportError:
            print(f"⚠️ Sistema de email principal no disponible")
        
        # Sistema de respaldo - siempre guarda la notificación
        try:
            from email_fallback_system import send_contact_notification_fallback
            fallback_saved = send_contact_notification_fallback(nombre, email, asunto, mensaje)
            if not email_sent and fallback_saved:
                print(f"✅ Notificación guardada para revisión manual en el CRM")
        except ImportError:
            print(f"⚠️ Sistema de respaldo no disponible")
        
        # NUEVA FUNCIONALIDAD: Añadir formulario de contacto al CRM
        try:
            from form_integration_service import process_form_submission
            contact_data = {
                'nombre': nombre,
                'email': email,
                'mensaje': mensaje,
                'tipo_interes': asunto
            }
            crm_id = process_form_submission('contacto', contact_data, 'web_form_contacto')
            if crm_id:
                print(f"✅ Mensaje de contacto añadido al CRM para seguimiento")
        except Exception as e:
            print(f"⚠️ Error añadiendo contacto al CRM: {e}")
        
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
        
        # NUEVA FUNCIONALIDAD: Integración automática con CRM
        try:
            from form_integration_service import process_form_submission
            crm_id = process_form_submission('registro_persona', user_data, 'web_form_registro_general')
            if crm_id:
                print(f"✅ Usuario añadido automáticamente al CRM con ID: {crm_id}")
        except Exception as e:
            print(f"⚠️ Error integrando con CRM: {e}")
        
        flash('¡Registro completado exitosamente! Tu información se ha añadido a nuestra base de datos para conectarte con oportunidades laborales.', 'success')
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
    form = AsociacionForm()
    
    if request.method == 'POST' and form.validate_on_submit():
        try:
            # Verificar y convertir años_funcionamiento
            años_funcionamiento_valor = form.años_funcionamiento.data
            try:
                años_funcionamiento_int = int(años_funcionamiento_valor) if años_funcionamiento_valor else None
            except (ValueError, TypeError):
                años_funcionamiento_int = None
            
            # Crear nueva asociación en base de datos
            nueva_asociacion = Asociacion(
                nombre_asociacion=form.nombre_asociacion.data,
                acronimo=form.acronimo.data,
                pais=form.pais.data,
                ciudad=form.ciudad.data,
                email=form.email.data,
                telefono=form.telefono.data,
                tipo_documento=form.tipo_documento.data,
                numero_documento=form.numero_documento.data,
                neurodivergencias_atendidas=','.join(form.neurodivergencias_atendidas.data or []),
                servicios=','.join(form.servicios.data or []),
                descripcion=form.descripcion.data,
                años_funcionamiento=años_funcionamiento_int,
                contacto_nombre=form.contacto_nombre.data,
                contacto_cargo=form.contacto_cargo.data,
                estado='verificando_documentacion',
                ip_solicitud=request.remote_addr,
                user_agent=request.user_agent.string[:500] if request.user_agent else None
            )
            
            db.session.add(nueva_asociacion)
            db.session.commit()
            
            # Recoger datos para email y CRM
            data = {
                'id': nueva_asociacion.id,
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
                'descripcion': nueva_asociacion.descripcion,
                'años_funcionamiento': años_funcionamiento_int,
                'contacto_nombre': nueva_asociacion.contacto_nombre,
                'contacto_cargo': nueva_asociacion.contacto_cargo,
                'estado': nueva_asociacion.estado
            }
            
            # Crear asociación en SQLite
            from models import Asociacion
            from app import db
            
            asociacion = Asociacion(
                nombre_asociacion=data['nombre_asociacion'],
                acronimo=data['acronimo'],
                pais=data['pais'],
                ciudad=data['ciudad'],
                email=data['email'],
                telefono=data['telefono'],
                tipo_documento=data['tipo_documento'],
                numero_documento=data['numero_documento'],
                neurodivergencias_atendidas=data['neurodivergencias_atendidas'],
                servicios=data['servicios'],
                descripcion=data['descripcion'],
                años_funcionamiento=int(data['años_funcionamiento']) if data['años_funcionamiento'] else None,
                contacto_nombre=data['contacto_nombre'],
                contacto_cargo=data['contacto_cargo']
            )
            
            db.session.add(asociacion)
            db.session.commit()
            
            # Enviar email de notificación
            from sendgrid_helper import send_email
            subject = f"Nueva Asociación Registrada - {data['nombre_asociacion']}"
            html_content = f"""
            <h2>🏢 Nueva Asociación Registrada</h2>
            <p><strong>Nombre:</strong> {data['nombre_asociacion']}</p>
            <p><strong>País:</strong> {data['pais']}</p>
            <p><strong>Ciudad:</strong> {data['ciudad']}</p>
            <p><strong>Email:</strong> {data['email']}</p>
            <p><strong>Neurodivergencias:</strong> {data['neurodivergencias_atendidas']}</p>
            <p><strong>Servicios:</strong> {data['servicios']}</p>
            <hr>
            <p>Panel: <a href="http://localhost:5000/admin/login-new">CRM</a></p>
            """
            
            email_success = send_email('diversiaeternals@gmail.com', subject, html_content)
            print(f"✅ Email asociación enviado: {email_success}")
            
            # Guardar en CRM
            try:
                from form_integration_service import process_form_submission
                crm_id = process_form_submission('registro_asociacion', data, 'web_form_asociacion')
                if crm_id:
                    print(f"✅ Asociación añadida al CRM con ID: {crm_id}")
            except Exception as e:
                print(f"⚠️ Error integrando asociación con CRM: {e}")
            
            flash('¡Asociación registrada exitosamente! Te contactaremos pronto.', 'success')
            return redirect(url_for('verificacion_documentos'))
            
        except Exception as e:
            print(f"❌ Error registrando asociación: {e}")
            flash('Error al registrar la asociación. Por favor intenta de nuevo.', 'error')
    
    return render_template('registro-asociacion.html', form=form)

@app.route('/verificacion-documentos')
def verificacion_documentos():
    """Página de confirmación y subida de documentos para asociaciones"""
    return render_template('verificacion-documentos.html')

# API para obtener asociaciones (para CRM)
@app.route('/api/associations')
def api_associations():
    """API para obtener todas las asociaciones"""
    from models import Asociacion
    try:
        asociaciones = Asociacion.query.all()
        data = []
        
        for asoc in asociaciones:
            data.append({
                'id': asoc.id,
                'name': asoc.nombre_asociacion,
                'acronym': asoc.acronimo,
                'country': asoc.pais,
                'city': asoc.ciudad,
                'email': asoc.email,
                'neurodivergences': asoc.neurodivergencias_atendidas,
                'status': asoc.estado,
                'created_at': asoc.created_at.isoformat() if asoc.created_at else None
            })
        
        return jsonify(data)
    except Exception as e:
        print(f"Error en API associations: {e}")
        return jsonify([])  # Devolver lista vacía si hay error

# API para importar CSV
@app.route('/api/import-csv', methods=['POST'])
def api_import_csv():
    """API para importar datos desde CSV al CRM"""
    try:
        if 'csv_file' not in request.files:
            return jsonify({'success': False, 'message': 'No se encontró archivo CSV'})
        
        file = request.files['csv_file']
        import_type = request.form.get('import_type')
        update_existing = request.form.get('update_existing') == 'true'
        
        if file.filename == '':
            return jsonify({'success': False, 'message': 'No se seleccionó archivo'})
        
        if not file.filename.lower().endswith('.csv'):
            return jsonify({'success': False, 'message': 'El archivo debe ser CSV'})
        
        # Leer CSV
        import csv
        import io
        
        # Leer contenido del archivo
        file_content = file.read().decode('utf-8')
        csv_reader = csv.DictReader(io.StringIO(file_content))
        
        processed = 0
        created = 0
        updated = 0
        errors = 0
        
        # Procesar según tipo de importación
        if import_type == 'companies':
            for row in csv_reader:
                try:
                    # Verificar campos requeridos
                    required_fields = ['nombre_empresa', 'email_contacto']
                    if not all(field in row and row[field].strip() for field in required_fields):
                        errors += 1
                        continue
                    
                    # Buscar empresa existente si se debe actualizar
                    existing_company = None
                    if update_existing:
                        existing_company = Company.query.filter_by(email_contacto=row['email_contacto']).first()
                    
                    if existing_company:
                        # Actualizar empresa existente
                        existing_company.nombre_empresa = row.get('nombre_empresa', existing_company.nombre_empresa)
                        existing_company.telefono = row.get('telefono', existing_company.telefono)
                        existing_company.sector = row.get('sector', existing_company.sector)
                        existing_company.ciudad = row.get('ciudad', existing_company.ciudad)
                        if not existing_company.tamano_empresa:
                            existing_company.tamano_empresa = 'No especificado'
                        updated += 1
                    else:
                        # Crear nueva empresa
                        new_company = Company(
                            nombre_empresa=row['nombre_empresa'],
                            email_contacto=row['email_contacto'],
                            telefono=row.get('telefono', ''),
                            sector=row.get('sector', 'General'),
                            tamano_empresa='No especificado',
                            ciudad=row.get('ciudad', '')
                        )
                        db.session.add(new_company)
                        created += 1
                    
                    processed += 1
                    
                except Exception as e:
                    print(f"Error procesando fila de empresa: {e}")
                    errors += 1
        
        elif import_type == 'contacts':
            for row in csv_reader:
                try:
                    # Verificar campos requeridos
                    required_fields = ['nombre', 'email']
                    if not all(field in row and row[field].strip() for field in required_fields):
                        errors += 1
                        continue
                    
                    # Buscar usuario existente si se debe actualizar
                    existing_user = None
                    if update_existing:
                        existing_user = User.query.filter_by(email=row['email']).first()
                    
                    if existing_user:
                        # Actualizar usuario existente
                        existing_user.nombre = row.get('nombre', existing_user.nombre)
                        existing_user.apellidos = row.get('apellidos', existing_user.apellidos)
                        existing_user.telefono = row.get('telefono', existing_user.telefono)
                        existing_user.ciudad = row.get('ciudad', existing_user.ciudad)
                        existing_user.tipo_neurodivergencia = row.get('tipo_neurodivergencia', existing_user.tipo_neurodivergencia)
                        updated += 1
                    else:
                        # Crear nuevo usuario
                        new_user = User(
                            nombre=row['nombre'],
                            apellidos=row.get('apellidos', ''),
                            email=row['email'],
                            telefono=row.get('telefono', ''),
                            ciudad=row.get('ciudad', ''),
                            tipo_neurodivergencia=row.get('tipo_neurodivergencia', 'otro')
                        )
                        db.session.add(new_user)
                        created += 1
                    
                    processed += 1
                    
                except Exception as e:
                    print(f"Error procesando fila de contacto: {e}")
                    errors += 1
        
        else:
            return jsonify({'success': False, 'message': 'Tipo de importación no válido'})
        
        # Guardar cambios en base de datos
        db.session.commit()
        
        # También actualizar CRM persistente
        try:
            import json
            import os
            
            crm_file = 'crm_persistent_data.json'
            if os.path.exists(crm_file):
                with open(crm_file, 'r', encoding='utf-8') as f:
                    crm_data = json.load(f)
                
                # Agregar datos al CRM según el tipo
                if import_type == 'companies':
                    if 'companies' not in crm_data:
                        crm_data['companies'] = []
                    
                    # Obtener empresas de la base de datos
                    companies = Company.query.all()
                    crm_data['companies'] = []
                    for company in companies:
                        crm_data['companies'].append({
                            'id': company.id,
                            'nombre_empresa': company.nombre_empresa,
                            'email_contacto': company.email_contacto,
                            'telefono': company.telefono,
                            'sector': company.sector,
                            'ciudad': company.ciudad,
                            'created_at': company.created_at.isoformat() if company.created_at else None
                        })
                
                elif import_type == 'contacts':
                    if 'contacts' not in crm_data:
                        crm_data['contacts'] = []
                    
                    # Obtener usuarios de la base de datos
                    users = User.query.all()
                    crm_data['contacts'] = []
                    for user in users:
                        crm_data['contacts'].append({
                            'id': user.id,
                            'nombre': user.nombre,
                            'apellidos': user.apellidos,
                            'email': user.email,
                            'telefono': user.telefono,
                            'ciudad': user.ciudad,
                            'tipo_neurodivergencia': user.tipo_neurodivergencia,
                            'created_at': user.created_at.isoformat() if user.created_at else None
                        })
                
                # Guardar CRM actualizado
                with open(crm_file, 'w', encoding='utf-8') as f:
                    json.dump(crm_data, f, ensure_ascii=False, indent=2)
                    
        except Exception as e:
            print(f"Error actualizando CRM persistente: {e}")
        
        # Enviar email de confirmación
        try:
            from sendgrid_helper import send_email
            
            email_content = f'''
            <h2>📁 IMPORTACIÓN CSV COMPLETADA</h2>
            
            <h3>📊 Resultados:</h3>
            <ul>
            <li>✅ Registros procesados: {processed}</li>
            <li>✅ Registros creados: {created}</li>
            <li>✅ Registros actualizados: {updated}</li>
            <li>⚠️ Errores: {errors}</li>
            </ul>
            
            <h3>🗂️ Tipo de importación:</h3>
            <p><strong>{import_type}</strong></p>
            
            <h3>⏰ Fecha:</h3>
            <p>{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
            '''
            
            send_email('diversiaeternals@gmail.com', f'📁 CSV IMPORTADO - {import_type}', email_content)
        except Exception as e:
            print(f"Error enviando email: {e}")
        
        return jsonify({
            'success': True,
            'processed': processed,
            'created': created,
            'updated': updated,
            'errors': errors,
            'message': f'Importación completada: {created} creados, {updated} actualizados'
        })
        
    except Exception as e:
        print(f"Error en importación CSV: {e}")
        return jsonify({'success': False, 'message': f'Error al procesar CSV: {str(e)}'})


# ============== API CRM SIMPLE SIN CONFLICTOS ==============
@app.route('/api/companies-fixed')
def api_companies_fixed():
    try:
        companies = Company.query.all()
        companies_list = []
        for company in companies:
            companies_list.append({
                'id': company.id,
                'nombre_empresa': company.nombre_empresa,
                'email_contacto': company.email_contacto,
                'telefono': company.telefono,
                'sector': company.sector,
                'ciudad': company.ciudad,
                'created_at': company.created_at.isoformat() if company.created_at else None
            })
        return jsonify(companies_list)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/contacts-fixed')
def api_contacts_fixed():
    try:
        users = User.query.all()
        users_list = []
        for user in users:
            users_list.append({
                'id': user.id,
                'nombre': user.nombre,
                'apellidos': user.apellidos,
                'email': user.email,
                'telefono': user.telefono,
                'tipo_neurodivergencia': user.tipo_neurodivergencia,
                'ciudad': user.ciudad,
                'created_at': user.created_at.isoformat() if user.created_at else None
            })
        return jsonify(users_list)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/offers-fixed')
def api_offers_fixed():
    try:
        offers = JobOffer.query.all()
        offers_list = []
        for offer in offers:
            offers_list.append({
                'id': offer.id,
                'titulo': offer.titulo,
                'descripcion': offer.descripcion,
                'salario': offer.salario,
                'ubicacion': offer.ubicacion,
                'created_at': offer.created_at.isoformat() if offer.created_at else None
            })
        return jsonify(offers_list)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/employees-fixed')
def api_employees_fixed():
    return jsonify([])

@app.route('/api/tasks-fixed')
def api_tasks_fixed():
    return jsonify([])

@app.route('/api/companies-fixed/<int:company_id>', methods=['DELETE'])
def delete_company_fixed(company_id):
    try:
        company = Company.query.get(company_id)
        if not company:
            return jsonify({'error': 'Empresa no encontrada'}), 404
        
        # Guardar nombre para confirmación
        company_name = company.nombre_empresa
        
        # Eliminar de base de datos
        db.session.delete(company)
        db.session.commit()
        
        return jsonify({
            'success': True, 
            'message': f'Empresa {company_name} eliminada correctamente'
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/companies-fixed/clear', methods=['POST'])
def clear_all_companies():
    try:
        # Eliminar todas las empresas
        count = Company.query.count()
        Company.query.delete()
        db.session.commit()
        
        return jsonify({
            'success': True, 
            'message': f'{count} empresas eliminadas correctamente'
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500
