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

# Importar CRM Neurodivergentes
try:
    from crm_neurodivergentes import create_neurodivergentes_api
    create_neurodivergentes_api(app)
except ImportError:
    print("⚠️ CRM Neurodivergentes no disponible")

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
            # Recoger datos del formulario
            data = {
                'nombre_asociacion': form.nombre_asociacion.data,
                'acronimo': form.acronimo.data,
                'pais': form.pais.data,
                'ciudad': form.ciudad.data,
                'email': form.email.data,
                'telefono': form.telefono.data,
                'tipo_documento': form.tipo_documento.data,
                'numero_documento': form.numero_documento.data,
                'neurodivergencias_atendidas': ','.join(form.neurodivergencias_atendidas.data or []),
                'servicios': ','.join(form.servicios.data or []),
                'descripcion': form.descripcion.data,
                'años_funcionamiento': form.anos_funcionamiento.data,
                'contacto_nombre': form.contacto_nombre.data,
                'contacto_cargo': form.contacto_cargo.data
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
            return redirect(url_for('registro_asociacion'))
            
        except Exception as e:
            print(f"❌ Error registrando asociación: {e}")
            flash('Error al registrar la asociación. Por favor intenta de nuevo.', 'error')
    
    return render_template('registro-asociacion.html', form=form)
