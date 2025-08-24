#!/usr/bin/env python3
"""
Routes simplificado - Solo funcionalidades esenciales
"""

from flask import render_template, request, flash, redirect, url_for, jsonify
from app import app, db
from models import User, Company, Admin, JobOffer
from forms import (RegistroGeneralForm, RegistroTDAHForm, RegistroDislexiaForm, RegistroTEAForm, 
                  RegistroDiscalculiaForm, RegistroTouretteForm, RegistroDispraxiaForm, 
                  RegistroAnsiedadForm, RegistroBipolarForm, RegistroAltasCapacidadesForm,
                  EmpresaForm)
from datetime import datetime

# Importar CSV Manager
try:
    from csv_manager import create_csv_routes
    create_csv_routes(app)
    print("✅ Rutas CSV completas: exportar e importar datos")
except Exception as e:
    print(f"⚠️ Error cargando CSV manager: {e}")

# Ruta principal movida a main.py

@app.route('/personas-nd')
def personas_nd():
    return render_template('personas-nd.html')

@app.route('/empresas', methods=['GET', 'POST'])
def empresas():
    try:
        print("🔍 DEBUG: Iniciando función empresas")
        form = EmpresaForm()
        print("🔍 DEBUG: EmpresaForm creado")
        
        if request.method == 'POST':
            try:
                # Obtener datos del formulario
                data = {
                    'nombre': request.form.get('nombre_empresa'),
                    'email': request.form.get('email_contacto'),
                    'telefono': request.form.get('telefono'),
                    'sector': request.form.get('sector'),
                    'tamaño': request.form.get('tamano_empresa'),
                    'ciudad': request.form.get('ciudad'),
                    'web': request.form.get('sitio_web'),
                    'descripcion': request.form.get('descripcion_empresa'),
                    'created_at': datetime.now().isoformat()
                }
                
                print(f"Datos procesados: {data}")
                
                # Guardar en SQLite
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
                
                # También guardar en CRM Minimal
                try:
                    from crm_minimal import load_data, save_data
                    
                    crm_data = load_data()
                    companies = crm_data.get('companies', [])
                    new_id = max([c.get('id', 0) for c in companies], default=0) + 1
                    
                    crm_company = {
                        'id': new_id,
                        'nombre': data['nombre'],
                        'email': data['email'],
                        'telefono': data['telefono'],
                        'sector': data['sector'],
                        'ciudad': data['ciudad'],
                        'tamano': data['tamaño'],
                        'web': data.get('web', ''),
                        'descripcion': data.get('descripcion', ''),
                        'origen': 'web_registro',
                        'created_at': datetime.now().isoformat()
                    }
                    
                    companies.append(crm_company)
                    crm_data['companies'] = companies
                    save_data(crm_data)
                    
                    print(f"✅ Empresa guardada en SQLite y CRM: {data['nombre']}")
                    
                except Exception as e:
                    print(f"⚠️ Error guardando en CRM: {e}")
                
                flash(f'Empresa {data["nombre"]} registrada exitosamente', 'success')
                return redirect(url_for('empresas'))
                
            except Exception as e:
                print(f"❌ Error procesando formulario: {e}")
                flash('Error al registrar la empresa. Inténtalo de nuevo.', 'error')
        
        print("🔍 DEBUG: Enviando template empresas.html")
        return render_template('empresas.html', form=form)
    except Exception as e:
        print(f"❌ ERROR EN EMPRESAS: {e}")
        import traceback
        traceback.print_exc()
        return f"Error en /empresas: {e}", 500

@app.route('/comunidad')
def comunidad():
    return render_template('comunidad.html')

@app.route('/contacto')
def contacto():
    return render_template('contacto.html')

@app.route('/asociaciones')
def asociaciones():
    return render_template('asociaciones.html')

@app.route('/registro-discalculia', methods=['GET', 'POST'])
def registro_discalculia():
    form = RegistroDiscalculiaForm()
    if form.validate_on_submit():
        user = User(
            nombre=form.nombre.data,
            apellidos=form.apellidos.data,
            email=form.email.data,
            tipo_neurodivergencia='Discalculia'
        )
        db.session.add(user)
        db.session.commit()
        flash('¡Registro Discalculia completado!', 'success')
    return render_template('registro-discalculia.html', form=form)

@app.route('/registro-tourette', methods=['GET', 'POST'])
def registro_tourette():
    form = RegistroTouretteForm()
    if form.validate_on_submit():
        user = User(
            nombre=form.nombre.data,
            apellidos=form.apellidos.data,
            email=form.email.data,
            tipo_neurodivergencia='Tourette'
        )
        db.session.add(user)
        db.session.commit()
        flash('¡Registro Tourette completado!', 'success')
    return render_template('registro-tourette.html', form=form)

@app.route('/registro-dispraxia', methods=['GET', 'POST'])
def registro_dispraxia():
    form = RegistroDispraxiaForm()
    if form.validate_on_submit():
        user = User(
            nombre=form.nombre.data,
            apellidos=form.apellidos.data,
            email=form.email.data,
            tipo_neurodivergencia='Dispraxia'
        )
        db.session.add(user)
        db.session.commit()
        flash('¡Registro Dispraxia completado!', 'success')
    return render_template('registro-dispraxia.html', form=form)

@app.route('/registro-ansiedad', methods=['GET', 'POST'])
def registro_ansiedad():
    form = RegistroAnsiedadForm()
    if form.validate_on_submit():
        user = User(
            nombre=form.nombre.data,
            apellidos=form.apellidos.data,
            email=form.email.data,
            tipo_neurodivergencia='Ansiedad'
        )
        db.session.add(user)
        db.session.commit()
        flash('¡Registro Ansiedad completado!', 'success')
    return render_template('registro-ansiedad.html', form=form)

@app.route('/registro-bipolar', methods=['GET', 'POST'])
def registro_bipolar():
    form = RegistroBipolarForm()
    if form.validate_on_submit():
        user = User(
            nombre=form.nombre.data,
            apellidos=form.apellidos.data,
            email=form.email.data,
            tipo_neurodivergencia='Bipolar'
        )
        db.session.add(user)
        db.session.commit()
        flash('¡Registro Bipolar completado!', 'success')
    return render_template('registro-bipolar.html', form=form)

@app.route('/registro-altas-capacidades', methods=['GET', 'POST'])
def registro_altas_capacidades():
    form = RegistroAltasCapacidadesForm()
    if form.validate_on_submit():
        user = User(
            nombre=form.nombre.data,
            apellidos=form.apellidos.data,
            email=form.email.data,
            tipo_neurodivergencia='Altas Capacidades'
        )
        db.session.add(user)
        db.session.commit()
        flash('¡Registro Altas Capacidades completado!', 'success')
    return render_template('registro-altas-capacidades.html', form=form)

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
        
        flash('¡Registro completado exitosamente!', 'success')
        return redirect(url_for('registro'))
    
    return render_template('registro.html', form=form)

# Rutas de registro específicas por neurodivergencia
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
            tipo_neurodivergencia='TDAH',
            diagnostico_formal=form.diagnostico_formal.data,
            experiencia_laboral=form.experiencia_laboral.data,
            formacion_academica=form.formacion_academica.data,
            habilidades=form.habilidades.data,
            intereses_laborales=form.intereses_laborales.data,
            adaptaciones_necesarias=form.adaptaciones_necesarias.data,
            sintomas_tdah=form.sintomas_tdah.data,
            medicacion_actual=form.medicacion_actual.data,
            estrategias_organizacion=form.estrategias_organizacion.data
        )
        db.session.add(user)
        db.session.commit()
        
        flash('¡Registro TDAH completado exitosamente!', 'success')
        return redirect(url_for('registro_tdah'))
    
    return render_template('registro-tdah.html', form=form)

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
            tipo_neurodivergencia='TEA',
            diagnostico_formal=form.diagnostico_formal.data,
            experiencia_laboral=form.experiencia_laboral.data,
            formacion_academica=form.formacion_academica.data,
            habilidades=form.habilidades.data,
            intereses_laborales=form.intereses_laborales.data,
            adaptaciones_necesarias=form.adaptaciones_necesarias.data,
            nivel_soporte_tea=form.nivel_soporte_tea.data,
            sensibilidades_sensoriales=form.sensibilidades_sensoriales.data,
            intereses_especificos=form.intereses_especificos.data
        )
        db.session.add(user)
        db.session.commit()
        
        flash('¡Registro TEA completado exitosamente!', 'success')
        return redirect(url_for('registro_tea'))
    
    return render_template('registro-tea.html', form=form)

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
            tipo_neurodivergencia='Dislexia',
            diagnostico_formal=form.diagnostico_formal.data,
            experiencia_laboral=form.experiencia_laboral.data,
            formacion_academica=form.formacion_academica.data,
            habilidades=form.habilidades.data,
            intereses_laborales=form.intereses_laborales.data,
            adaptaciones_necesarias=form.adaptaciones_necesarias.data,
            dificultades_lectura=form.dificultades_lectura.data,
            herramientas_asistivas=form.herramientas_asistivas.data,
            estrategias_aprendizaje=form.estrategias_aprendizaje.data
        )
        db.session.add(user)
        db.session.commit()
        
        flash('¡Registro Dislexia completado exitosamente!', 'success')
        return redirect(url_for('registro_dislexia'))
    
    return render_template('registro-dislexia.html', form=form)

# Rutas básicas adicionales
@app.route('/test')
def test():
    return render_template('test.html')

@app.route('/comenzar')
def comenzar():
    return render_template('comenzar.html')

@app.route('/sobre-nosotros')
def sobre_nosotros():
    return render_template('sobre-nosotros.html')

@app.route('/crm-dashboard')
def crm_dashboard():
    # Redireccionar al CRM Minimal
    return redirect('/crm-minimal')

@app.route('/privacidad')
def privacidad():
    return render_template('privacidad.html')

@app.route('/terminos')
def terminos():
    return render_template('terminos.html')

@app.route('/aviso-legal')
def aviso_legal():
    return render_template('aviso-legal.html')

@app.route('/enviar-contacto', methods=['POST'])
def enviar_contacto():
    try:
        nombre = request.form.get('nombre')
        email = request.form.get('email')
        asunto = request.form.get('asunto')
        mensaje = request.form.get('mensaje')
        
        if nombre and email and asunto and mensaje:
            print(f"📧 Contacto recibido de {nombre} ({email}): {asunto}")
            flash('¡Mensaje enviado correctamente! Te responderemos pronto.', 'success')
        else:
            flash('Por favor completa todos los campos.', 'error')
    except Exception as e:
        print(f"Error en contacto: {e}")
        flash('Error al enviar el mensaje. Intenta de nuevo.', 'error')
    
    return redirect(url_for('contacto'))

# Ruta para descargar la guía laboral
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

# Ruta para videos informativos
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

# Ruta para podcast
@app.route('/podcast-diversia')
def podcast_diversia():
    """Página del podcast DiversIA"""
    return render_template('podcast-diversia.html')

# Ruta para registro de asociaciones
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
            from models import Asociacion
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
    
    from models import Asociacion
    
    # Obtener todas las asociaciones pendientes de verificación
    asociaciones_pendientes = Asociacion.query.filter(
        Asociacion.estado.in_(['verificando_documentacion', 'pendiente', 'documentos_requeridos'])
    ).order_by(Asociacion.created_at.desc()).all()
    
    return render_template('admin/verificar-asociaciones.html', 
                         asociaciones=asociaciones_pendientes)

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

# Las rutas de admin están en admin_final.py - no redefinir aquí

print("✅ Routes simplificado cargado correctamente")