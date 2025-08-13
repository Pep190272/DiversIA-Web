from flask import render_template, request, redirect, url_for, flash, jsonify
from app import app, db
from models import User, Company, JobOffer, TestResult
from forms import RegistroGeneralForm, RegistroTDAHForm, RegistroDislexiaForm, RegistroTEAForm, EmpresaRegistroForm, OfertaEmpleoForm
from sendgrid_helper import send_registration_notification, send_company_registration_notification

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/personas-nd')
def personas_nd():
    return render_template('personas-nd.html')

@app.route('/empresas')
def empresas():
    form = EmpresaRegistroForm()
    oferta_form = OfertaEmpleoForm()
    return render_template('empresas.html', form=form, oferta_form=oferta_form)

@app.route('/comunidad')
def comunidad():
    return render_template('comunidad.html')

@app.route('/asociaciones')
def asociaciones():
    return render_template('asociaciones.html')

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
