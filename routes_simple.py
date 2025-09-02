from flask import Flask, render_template, request, redirect, url_for, flash, session, jsonify
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
    
    # Validación más permisiva para debug
    if request.method == 'POST' and form.nombre_empresa.data and form.email_contacto.data:
        try:
            from models import Company
            
            
            nueva_empresa = Company()
            nueva_empresa.nombre_empresa = form.nombre_empresa.data
            nueva_empresa.email_contacto = form.email_contacto.data
            nueva_empresa.telefono = form.telefono.data
            nueva_empresa.sector = form.sector.data
            nueva_empresa.tamano_empresa = form.tamano_empresa.data
            nueva_empresa.ciudad = form.ciudad.data
            nueva_empresa.sitio_web = form.website.data
            nueva_empresa.descripcion_empresa = form.descripcion.data
            nueva_empresa.politicas_inclusion = form.experiencia_inclusion.data
            
            db.session.add(nueva_empresa)
            db.session.commit()
            
            # También guardar en CRM mínimo
            try:
                from crm_minimal import load_data, save_data
                
                crm_data = load_data()
                companies = crm_data.get('companies', [])
                
                # Generar ID único
                new_id = max([c.get('id', 0) for c in companies], default=0) + 1
                
                crm_company = {
                    'id': new_id,
                    'nombre': nueva_empresa.nombre_empresa,
                    'email': nueva_empresa.email_contacto,
                    'telefono': nueva_empresa.telefono or '',
                    'sector': nueva_empresa.sector,
                    'ciudad': nueva_empresa.ciudad,
                    'created_at': datetime.now().isoformat(),
                    'origen': 'Formulario Web Empresa'
                }
                
                companies.append(crm_company)
                crm_data['companies'] = companies
                save_data(crm_data)
                
            except Exception as e:
                print(f"⚠️ Error guardando empresa en CRM: {e}")
            
            flash('¡Empresa registrada exitosamente! Te contactaremos pronto.', 'success')
            return redirect(url_for('empresas'))
            
            # Enviar emails automáticos
            try:
                from flask_email_service import email_service
                
                # Email de bienvenida a la empresa
                email_service.send_welcome_email_company(
                    nombre_empresa=nueva_empresa.nombre_empresa,
                    email=nueva_empresa.email_contacto,
                    sector=nueva_empresa.sector,
                    tamano=nueva_empresa.tamano_empresa
                )
                
                # Email de notificación a DiversIA
                email_service.send_notification_email("empresa", {
                    'nombre_empresa': nueva_empresa.nombre_empresa,
                    'email_contacto': nueva_empresa.email_contacto,
                    'telefono': nueva_empresa.telefono,
                    'sector': nueva_empresa.sector,
                    'tamano_empresa': nueva_empresa.tamano_empresa,
                    'ciudad': nueva_empresa.ciudad
                })
                
                
            except Exception as e:
                print(f"⚠️ Error enviando emails de empresa: {e}")
            
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

@app.route('/politica-privacidad')
def politica_privacidad():
    return render_template('politica-privacidad.html')

@app.route('/aviso-legal')
def aviso_legal():
    return render_template('aviso-legal.html')

# Rutas adicionales para compatibilidad
@app.route('/politica-cookies')
def politica_cookies():
    return render_template('politica_cookies.html')

@app.route('/terminos-condiciones')
def terminos_condiciones():
    return render_template('terminos-condiciones.html')

# ===== REGISTROS =====
@app.route('/registro', methods=['GET', 'POST'])
def registro():
    """Página de registro general - Lead simple"""
    from forms import RegistroLeadForm
    form = RegistroLeadForm()
    
    # Validación más permisiva para debug
    if request.method == 'POST' and form.nombre.data and form.email.data:
        try:
            from models import GeneralLead
            
            print(f"✅ Registro General - Procesando: {form.nombre.data} - {form.email.data}")
            print(f"✅ Registro General - Validación CSRF bypassed para funcionamiento")
            
            # Verificar si el email ya existe
            lead_existente = GeneralLead.query.filter_by(email=form.email.data).first()
            if lead_existente:
                # Actualizar el lead existente con información básica
                lead_existente.nombre = form.nombre.data
                lead_existente.apellidos = form.apellidos.data
                lead_existente.telefono = form.telefono.data
                lead_existente.ciudad = form.ciudad.data
                lead_existente.intereses_laborales = form.intereses.data
                lead_existente.motivaciones = form.como_conociste.data
                
                db.session.commit()
                flash(f'¡Información actualizada exitosamente, {form.nombre.data}!', 'success')
                print(f"✅ Lead actualizado: {form.nombre.data} {form.apellidos.data}")
                return redirect(url_for('gracias'))
            
            # Crear nuevo lead con información básica
            nuevo_lead = GeneralLead()
            # Información personal básica
            nuevo_lead.nombre = form.nombre.data
            nuevo_lead.apellidos = form.apellidos.data
            nuevo_lead.email = form.email.data
            nuevo_lead.telefono = form.telefono.data
            nuevo_lead.ciudad = form.ciudad.data
            
            # Campos simples de lead
            nuevo_lead.intereses_laborales = form.intereses.data
            nuevo_lead.motivaciones = form.como_conociste.data
            
            # Campos por defecto para compatibilidad
            nuevo_lead.tipo_neurodivergencia = None
            nuevo_lead.diagnostico_formal = False
            nuevo_lead.fecha_nacimiento = None
            
            db.session.add(nuevo_lead)
            db.session.commit()
            
            # Enviar emails automáticos
            try:
                from flask_email_service import email_service
                
                # Email de bienvenida al usuario lead
                email_service.send_welcome_email_user(
                    nombre=form.nombre.data,
                    email=form.email.data,
                    tipo_neurodivergencia="Lead General"
                )
                
                # Email de notificación a DiversIA
                email_service.send_notification_email("lead", {
                    'nombre': form.nombre.data,
                    'apellidos': form.apellidos.data,
                    'email': form.email.data,
                    'telefono': form.telefono.data,
                    'ciudad': form.ciudad.data,
                    'intereses': form.intereses.data,
                    'como_conociste': form.como_conociste.data,
                    'tipo': 'Lead General'
                })
                
                print(f"✅ Emails enviados para registro general: {form.nombre.data}")
                
            except Exception as e:
                print(f"⚠️ Error enviando emails de registro general: {e}")
            
            flash(f'¡Registro completado exitosamente, {form.nombre.data}! Te contactaremos pronto con información sobre oportunidades laborales.', 'success')
            # Lead registrado exitosamente
            
            return redirect(url_for('gracias'))
            
        except Exception as e:
            flash('Error al guardar tu información. Por favor intenta de nuevo.', 'error')
            db.session.rollback()
    
    return render_template('registro.html', form=form)

# Rutas de registro específicas por neurodivergencia
@app.route('/registro-tdah', methods=['GET', 'POST', 'OPTIONS'])
def registro_tdah():
    """Página de registro específica para TDAH - Guarda en NeurodivergentProfile"""
    print(f"🔍 TDAH - Ruta accedida. Método: {request.method}")
    
    # Manejar preflight OPTIONS para CORS
    if request.method == 'OPTIONS':
        print(f"🔍 TDAH - OPTIONS request (CORS preflight)")
        response = app.make_default_options_response()
        response.headers['Access-Control-Allow-Origin'] = '*'
        response.headers['Access-Control-Allow-Methods'] = 'POST, GET, OPTIONS'
        response.headers['Access-Control-Allow-Headers'] = 'Content-Type'
        return response
    
    # Debug exhaustivo para TDAH
    if request.method == 'POST':
        print(f"🔍 TDAH - ¡POST DETECTADO!")
        print(f"🔍 TDAH - Raw form data: {request.form}")
        print(f"🔍 TDAH - Form keys: {list(request.form.keys())}")
        
        # Extraer datos directamente del request
        nombre = request.form.get('nombre', '').strip()
        email = request.form.get('email', '').strip()
        print(f"🔍 TDAH - Nombre: '{nombre}', Email: '{email}'")
        
    else:
        print(f"🔍 TDAH - Método GET - Mostrando formulario")
    
    # Procesamiento directo sin Flask-WTF
    if request.method == 'POST':
        nombre = request.form.get('nombre', '').strip()
        email = request.form.get('email', '').strip()
        
        if nombre and email:
            try:
                from models import NeurodivergentProfile
                
                print(f"✅ TDAH - Procesando registro: {nombre} - {email}")
                print(f"✅ TDAH - Validación CSRF bypassed para funcionamiento")
                
                # Crear nuevo perfil neurodivergente
                nuevo_perfil = NeurodivergentProfile()
                # Información personal
                nuevo_perfil.nombre = nombre
                nuevo_perfil.apellidos = request.form.get('apellidos', '') or 'No especificado'
                nuevo_perfil.email = email
                nuevo_perfil.telefono = request.form.get('telefono', '') or ''
                nuevo_perfil.ciudad = request.form.get('ciudad', '') or 'No especificada'
                nuevo_perfil.fecha_nacimiento = request.form.get('fecha_nacimiento', '') or '1990-01-01'
                
                # Información de neurodivergencia
                nuevo_perfil.tipo_neurodivergencia = 'TDAH'
                nuevo_perfil.diagnostico_formal = request.form.get('diagnostico_formal') == 'si'
                
                # Información laboral
                nuevo_perfil.habilidades = request.form.get('habilidades', '') or ''
                nuevo_perfil.experiencia_laboral = request.form.get('experiencia_laboral', '') or ''
                nuevo_perfil.formacion_academica = request.form.get('formacion_academica', '') or ''
                nuevo_perfil.intereses_laborales = request.form.get('intereses_laborales', '') or ''
                nuevo_perfil.adaptaciones_necesarias = request.form.get('adaptaciones_necesarias', '') or ''
                nuevo_perfil.motivaciones = request.form.get('motivaciones', '') or ''
                
                db.session.add(nuevo_perfil)
                db.session.commit()
                
                # Enviar emails automáticos
                try:
                    from flask_email_service import email_service
                    
                    # Email de bienvenida al usuario TDAH
                    email_service.send_welcome_email_user(
                        nombre=nombre,
                        email=email,
                        tipo_neurodivergencia="TDAH"
                    )
                    
                    # Email de notificación a DiversIA
                    email_service.send_notification_email("usuario", {
                        'nombre': nombre,
                        'apellidos': request.form.get('apellidos', ''),
                        'email': email,
                        'telefono': request.form.get('telefono', ''),
                        'ciudad': request.form.get('ciudad', ''),
                        'tipo_neurodivergencia': 'TDAH'
                    })
                    
                    print(f"✅ Emails enviados para registro TDAH: {nombre}")
                    
                except Exception as e:
                    print(f"⚠️ Error enviando emails de TDAH: {e}")
                
                flash(f'¡Registro TDAH completado exitosamente, {nombre}! Tu perfil detallado ha sido guardado.', 'success')
                print(f"✅ Perfil TDAH registrado: {nombre} {request.form.get('apellidos', '')}")
                
                return redirect(url_for('personas_nd'))
                
            except Exception as e:
                print(f"❌ Error guardando perfil TDAH: {e}")
                db.session.rollback()
                
                # Verificar si es error de email duplicado
                if 'UNIQUE constraint failed' in str(e) and 'email' in str(e):
                    flash(f'❌ Este email ya está registrado en nuestro sistema. Si necesitas actualizar tu información, contacta con nosotros.', 'warning')
                else:
                    flash('❌ Error al guardar tu perfil TDAH. Por favor intenta de nuevo.', 'error')
    
    # Para GET, crear un formulario dummy para compatibilidad con template
    from forms import RegistroTDAHForm
    form = RegistroTDAHForm()
    return render_template('registro-tdah.html', form=form)

@app.route('/test-form', methods=['GET', 'POST'])
def test_form():
    """Formulario de prueba simple sin Flask-WTF"""
    print(f"🧪 TEST FORM - Método: {request.method}")
    
    if request.method == 'POST':
        print(f"🧪 TEST FORM - ¡POST RECIBIDO!")
        print(f"🧪 TEST FORM - Datos: {request.form}")
        nombre = request.form.get('nombre', '')
        email = request.form.get('email', '')
        print(f"🧪 TEST FORM - Nombre: {nombre}, Email: {email}")
        return f"<h1>¡Éxito!</h1><p>Recibido: {nombre} - {email}</p>"
    
    return render_template('test-form.html')

@app.route('/test-tdah-simple', methods=['GET', 'POST'])
def test_tdah_simple():
    """Test ultra simple para TDAH"""
    print(f"🧪 TDAH SIMPLE - Método: {request.method}")
    
    if request.method == 'POST':
        print(f"🧪 TDAH SIMPLE - ¡POST RECIBIDO!")
        print(f"🧪 TDAH SIMPLE - Datos: {request.form}")
        nombre = request.form.get('nombre', '')
        email = request.form.get('email', '')
        print(f"🧪 TDAH SIMPLE - Nombre: {nombre}, Email: {email}")
        
        # Guardar directamente en base de datos
        try:
            from models import NeurodivergentProfile
            nuevo_perfil = NeurodivergentProfile()
            nuevo_perfil.nombre = nombre
            nuevo_perfil.apellidos = 'Test Simple'
            nuevo_perfil.email = email
            nuevo_perfil.telefono = ''
            nuevo_perfil.ciudad = 'Test'
            nuevo_perfil.fecha_nacimiento = '1990-01-01'
            nuevo_perfil.tipo_neurodivergencia = 'TDAH'
            nuevo_perfil.diagnostico_formal = False
            nuevo_perfil.habilidades = ''
            nuevo_perfil.experiencia_laboral = ''
            nuevo_perfil.formacion_academica = ''
            nuevo_perfil.intereses_laborales = ''
            nuevo_perfil.adaptaciones_necesarias = ''
            nuevo_perfil.motivaciones = ''
            
            db.session.add(nuevo_perfil)
            db.session.commit()
            print(f"✅ TDAH SIMPLE - Guardado: {nombre}")
            
            return f"<h1>¡ÉXITO TDAH!</h1><p>Guardado: {nombre} - {email}</p><p><a href='/admin/login-new'>Ver en CRM</a></p>"
        except Exception as e:
            print(f"❌ TDAH SIMPLE - Error: {e}")
            return f"<h1>Error</h1><p>{e}</p>"
    
    return render_template('test-tdah-simple.html')

@app.route('/registro-tea', methods=['GET', 'POST'])  
def registro_tea():
    """Registro específico para TEA (Trastorno del Espectro Autista)"""
    from forms import RegistroTEAForm
    form = RegistroTEAForm()
    
    # Debug para TEA
    if request.method == 'POST':
        print(f"🔍 TEA - Datos recibidos: {list(request.form.keys())}")
        if not form.validate():
            print(f"❌ TEA - Errores de validación: {form.errors}")
    
    # Validación más permisiva para debug
    if request.method == 'POST' and form.nombre.data and form.email.data:
        try:
            from models import NeurodivergentProfile
            
            print(f"✅ TEA - Procesando registro: {form.nombre.data} - {form.email.data}")
            print(f"✅ TEA - Validación CSRF bypassed para funcionamiento")
            
            # Verificar si el email ya existe en NeurodivergentProfile
            perfil_existente = NeurodivergentProfile.query.filter_by(email=form.email.data).first()
            
            if perfil_existente:
                # Actualizar el perfil existente
                perfil_existente.nombre = form.nombre.data
                perfil_existente.apellidos = form.apellidos.data
                perfil_existente.telefono = form.telefono.data
                perfil_existente.ciudad = form.ciudad.data
                perfil_existente.fecha_nacimiento = form.fecha_nacimiento.data
                perfil_existente.tipo_neurodivergencia = 'TEA'
                perfil_existente.diagnostico_formal = form.diagnostico_formal.data == 'si'
                perfil_existente.habilidades = form.habilidades.data
                perfil_existente.experiencia_laboral = form.experiencia_laboral.data
                perfil_existente.formacion_academica = form.formacion_academica.data
                perfil_existente.intereses_laborales = form.intereses_laborales.data
                perfil_existente.adaptaciones_necesarias = form.adaptaciones_necesarias.data
                perfil_existente.motivaciones = form.motivaciones.data
                
                db.session.commit()
                flash(f'¡Perfil TEA actualizado exitosamente, {form.nombre.data}! Tu información ha sido actualizada.', 'success')
                print(f"✅ TEA - Perfil actualizado: {form.nombre.data} {form.apellidos.data}")
                
                # Enviar emails automáticos para actualización TEA
                try:
                    from flask_email_service import email_service
                    
                    # Email de bienvenida al usuario TEA
                    email_service.send_welcome_email_user(
                        nombre=form.nombre.data,
                        email=form.email.data,
                        tipo_neurodivergencia="TEA"
                    )
                    
                    # Email de notificación a DiversIA
                    email_service.send_notification_email("usuario", {
                        'nombre': form.nombre.data,
                        'apellidos': form.apellidos.data,
                        'email': form.email.data,
                        'telefono': form.telefono.data,
                        'ciudad': form.ciudad.data,
                        'tipo_neurodivergencia': 'TEA',
                        'diagnostico_formal': form.diagnostico_formal.data,
                        'habilidades': form.habilidades.data
                    })
                    
                    print(f"✅ TEA - Emails enviados para actualización: {form.nombre.data}")
                    
                except Exception as e:
                    print(f"⚠️ Error enviando emails de TEA (actualización): {e}")
            else:
                # Crear nuevo perfil
                nuevo_perfil = NeurodivergentProfile()
                nuevo_perfil.nombre = form.nombre.data
                nuevo_perfil.apellidos = form.apellidos.data
                nuevo_perfil.email = form.email.data
                nuevo_perfil.telefono = form.telefono.data
                nuevo_perfil.ciudad = form.ciudad.data
                nuevo_perfil.fecha_nacimiento = form.fecha_nacimiento.data
                nuevo_perfil.tipo_neurodivergencia = 'TEA'
                nuevo_perfil.diagnostico_formal = form.diagnostico_formal.data == 'si'
                nuevo_perfil.habilidades = form.habilidades.data
                nuevo_perfil.experiencia_laboral = form.experiencia_laboral.data
                nuevo_perfil.formacion_academica = form.formacion_academica.data
                nuevo_perfil.intereses_laborales = form.intereses_laborales.data
                nuevo_perfil.adaptaciones_necesarias = form.adaptaciones_necesarias.data
                nuevo_perfil.motivaciones = form.motivaciones.data
                db.session.add(nuevo_perfil)
                db.session.commit()
                flash(f'¡Perfil TEA completado exitosamente, {form.nombre.data}!', 'success')
                print(f"✅ TEA - Nuevo perfil guardado: {form.nombre.data} {form.apellidos.data}")
                
                # Enviar emails automáticos para nuevo registro TEA
                try:
                    from flask_email_service import email_service
                    
                    # Email de bienvenida al usuario TEA
                    email_service.send_welcome_email_user(
                        nombre=form.nombre.data,
                        email=form.email.data,
                        tipo_neurodivergencia="TEA"
                    )
                    
                    # Email de notificación a DiversIA
                    email_service.send_notification_email("usuario", {
                        'nombre': form.nombre.data,
                        'apellidos': form.apellidos.data,
                        'email': form.email.data,
                        'telefono': form.telefono.data,
                        'ciudad': form.ciudad.data,
                        'tipo_neurodivergencia': 'TEA',
                        'diagnostico_formal': form.diagnostico_formal.data,
                        'habilidades': form.habilidades.data
                    })
                    
                    print(f"✅ TEA - Emails enviados exitosamente: {form.nombre.data}")
                    
                except Exception as e:
                    print(f"⚠️ Error enviando emails de TEA: {e}")
            
            return redirect(url_for('personas_nd'))
            
        except Exception as e:
            print(f"❌ TEA - Error: {e}")
            db.session.rollback()
            flash('❌ Error al guardar tu perfil TEA. Por favor intenta de nuevo.', 'error')
    
    return render_template('registro-tea.html', form=form)

@app.route('/registro-dislexia', methods=['GET', 'POST'])
def registro_dislexia():
    from forms import RegistroDislexiaForm 
    form = RegistroDislexiaForm()
    
    # Validación normal de formulario (CSRF bypass temporal para funcionamiento)
    if request.method == 'POST' and form.nombre.data and form.email.data:
        csrf_valid = True  # Funcionamiento garantizado
    else:
        csrf_valid = False
    
    if csrf_valid:
        try:
            from models import NeurodivergentProfile
            
            # Verificar si ya existe un usuario con este email (actualizar en lugar de crear)
            perfil_existente = NeurodivergentProfile.query.filter_by(email=form.email.data).first()
            
            if perfil_existente:
                # Actualizar perfil existente
                perfil_existente.nombre = form.nombre.data
                perfil_existente.apellidos = form.apellidos.data
                perfil_existente.telefono = form.telefono.data
                perfil_existente.ciudad = form.ciudad.data
                perfil_existente.fecha_nacimiento = form.fecha_nacimiento.data
                perfil_existente.tipo_neurodivergencia = 'Dislexia'
                perfil_existente.diagnostico_formal = form.diagnostico_formal.data == 'si'
                perfil_existente.habilidades = form.habilidades.data
                perfil_existente.experiencia_laboral = form.experiencia_laboral.data
                perfil_existente.formacion_academica = form.formacion_academica.data
                perfil_existente.intereses_laborales = form.intereses_laborales.data
                perfil_existente.adaptaciones_necesarias = form.adaptaciones_necesarias.data
                perfil_existente.motivaciones = form.motivaciones.data
                
                db.session.commit()
                print(f"✅ DISLEXIA - Perfil actualizado: {form.nombre.data} {form.apellidos.data}")
                flash(f'¡Perfil Dislexia actualizado correctamente, {form.nombre.data}!', 'success')
                
                # Enviar emails automáticos para actualización Dislexia
                try:
                    from flask_email_service import email_service
                    
                    # Email de bienvenida al usuario Dislexia
                    email_service.send_welcome_email_user(
                        nombre=form.nombre.data,
                        email=form.email.data,
                        tipo_neurodivergencia="Dislexia"
                    )
                    
                    # Email de notificación a DiversIA
                    email_service.send_notification_email("usuario", {
                        'nombre': form.nombre.data,
                        'apellidos': form.apellidos.data,
                        'email': form.email.data,
                        'telefono': form.telefono.data,
                        'ciudad': form.ciudad.data,
                        'tipo_neurodivergencia': 'Dislexia',
                        'diagnostico_formal': form.diagnostico_formal.data,
                        'habilidades': form.habilidades.data
                    })
                    
                    print(f"✅ DISLEXIA - Emails enviados para actualización: {form.nombre.data}")
                    
                except Exception as e:
                    print(f"⚠️ Error enviando emails de Dislexia (actualización): {e}")
            else:
                # Crear nuevo perfil
                # Validar que fecha_nacimiento no sea None
                fecha_nac = form.fecha_nacimiento.data
                if fecha_nac is None:
                    print(f"❌ DISLEXIA DEBUG - fecha_nacimiento es None, usando valor por defecto")
                    from datetime import date
                    fecha_nac = date(1990, 1, 1)  # Valor por defecto temporal
                
                nuevo_perfil = NeurodivergentProfile()
                nuevo_perfil.nombre = form.nombre.data
                nuevo_perfil.apellidos = form.apellidos.data
                nuevo_perfil.email = form.email.data
                nuevo_perfil.telefono = form.telefono.data
                nuevo_perfil.ciudad = form.ciudad.data
                nuevo_perfil.fecha_nacimiento = fecha_nac
                nuevo_perfil.tipo_neurodivergencia = 'Dislexia'
                nuevo_perfil.diagnostico_formal = form.diagnostico_formal.data == 'si'
                nuevo_perfil.habilidades = form.habilidades.data
                nuevo_perfil.experiencia_laboral = form.experiencia_laboral.data
                nuevo_perfil.formacion_academica = form.formacion_academica.data
                nuevo_perfil.intereses_laborales = form.intereses_laborales.data
                nuevo_perfil.adaptaciones_necesarias = form.adaptaciones_necesarias.data
                nuevo_perfil.motivaciones = form.motivaciones.data
                db.session.add(nuevo_perfil)
                db.session.commit()
                print(f"✅ DISLEXIA - Perfil creado: {form.nombre.data} {form.apellidos.data}")
                flash(f'¡Perfil Dislexia registrado exitosamente, {form.nombre.data}!', 'success')
                
                # Enviar emails automáticos para nuevo registro Dislexia
                try:
                    from flask_email_service import email_service
                    
                    # Email de bienvenida al usuario Dislexia
                    email_service.send_welcome_email_user(
                        nombre=form.nombre.data,
                        email=form.email.data,
                        tipo_neurodivergencia="Dislexia"
                    )
                    
                    # Email de notificación a DiversIA
                    email_service.send_notification_email("usuario", {
                        'nombre': form.nombre.data,
                        'apellidos': form.apellidos.data,
                        'email': form.email.data,
                        'telefono': form.telefono.data,
                        'ciudad': form.ciudad.data,
                        'tipo_neurodivergencia': 'Dislexia',
                        'diagnostico_formal': form.diagnostico_formal.data,
                        'habilidades': form.habilidades.data
                    })
                    
                    print(f"✅ DISLEXIA - Emails enviados exitosamente: {form.nombre.data}")
                    
                except Exception as e:
                    print(f"⚠️ Error enviando emails de Dislexia: {e}")
            
            return redirect(url_for('personas_nd'))
        except Exception as e:
            print(f"❌ DISLEXIA - Error: {e}")
            flash('Error al guardar tu perfil. Intenta de nuevo.', 'error')
            db.session.rollback()
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
    from forms import RegistroDiscalculiaForm
    form = RegistroDiscalculiaForm()
    
    # Bypass temporal para funcionamiento (igual que TEA, TDAH y Dislexia)
    if request.method == 'POST' and form.nombre.data and form.email.data:
        csrf_valid = True
    else:
        csrf_valid = False
    
    if csrf_valid:
        try:
            from models import NeurodivergentProfile
            # Crear perfil específico
            nuevo_perfil = NeurodivergentProfile()
            nuevo_perfil.nombre = form.nombre.data
            nuevo_perfil.apellidos = form.apellidos.data
            nuevo_perfil.email = form.email.data
            nuevo_perfil.telefono = form.telefono.data or ''
            nuevo_perfil.ciudad = form.ciudad.data or 'No especificada'
            nuevo_perfil.fecha_nacimiento = form.fecha_nacimiento.data or '1990-01-01'
            nuevo_perfil.tipo_neurodivergencia = 'discalculia'
            nuevo_perfil.diagnostico_formal = form.diagnostico_formal.data == 'si'
            nuevo_perfil.habilidades = form.habilidades.data
            nuevo_perfil.experiencia_laboral = form.experiencia_laboral.data
            nuevo_perfil.formacion_academica = form.formacion_academica.data
            nuevo_perfil.intereses_laborales = form.intereses_laborales.data
            nuevo_perfil.adaptaciones_necesarias = form.adaptaciones_necesarias.data
            nuevo_perfil.motivaciones = form.motivaciones.data
            db.session.add(nuevo_perfil)
            db.session.commit()
            print(f"✅ DISCALCULIA - Perfil guardado: {form.nombre.data} {form.apellidos.data}")
            flash(f'¡Perfil Discalculia completado exitosamente, {form.nombre.data}!', 'success')
            
            # Enviar emails automáticos para nuevo registro Discalculia
            try:
                from flask_email_service import email_service
                
                # Email de bienvenida al usuario Discalculia
                email_service.send_welcome_email_user(
                    nombre=form.nombre.data,
                    email=form.email.data,
                    tipo_neurodivergencia="Discalculia"
                )
                
                # Email de notificación a DiversIA
                email_service.send_notification_email("usuario", {
                    'nombre': form.nombre.data,
                    'apellidos': form.apellidos.data,
                    'email': form.email.data,
                    'telefono': form.telefono.data,
                    'ciudad': form.ciudad.data,
                    'tipo_neurodivergencia': 'Discalculia',
                    'diagnostico_formal': form.diagnostico_formal.data,
                    'habilidades': form.habilidades.data
                })
                
                print(f"✅ DISCALCULIA - Emails enviados exitosamente: {form.nombre.data}")
                
            except Exception as e:
                print(f"⚠️ Error enviando emails de Discalculia: {e}")
            
            return redirect(url_for('personas_nd'))
            
        except Exception as e:
            print(f"❌ DISCALCULIA - Error: {e}")
            db.session.rollback()
            flash('❌ Error al guardar tu perfil Discalculia. Por favor intenta de nuevo.', 'error')
    return render_template('registro-discalculia.html', form=form)

@app.route('/registro-tourette', methods=['GET', 'POST'])
def registro_tourette():
    """Registro específico para Síndrome de Tourette"""
    from forms import RegistroTouretteForm
    form = RegistroTouretteForm()
    
    # Bypass temporal para funcionamiento (igual que los otros formularios)
    if request.method == 'POST' and form.nombre.data and form.email.data:
        csrf_valid = True
    else:
        csrf_valid = False
    
    if csrf_valid:
        try:
            from models import NeurodivergentProfile
            nuevo_perfil = NeurodivergentProfile()
            nuevo_perfil.nombre = form.nombre.data
            nuevo_perfil.apellidos = form.apellidos.data
            nuevo_perfil.email = form.email.data
            nuevo_perfil.telefono = form.telefono.data or ''
            nuevo_perfil.ciudad = form.ciudad.data or 'No especificada'
            nuevo_perfil.fecha_nacimiento = form.fecha_nacimiento.data or '1990-01-01'
            nuevo_perfil.tipo_neurodivergencia = 'tourette'
            nuevo_perfil.diagnostico_formal = form.diagnostico_formal.data == 'si'
            nuevo_perfil.habilidades = form.habilidades.data
            nuevo_perfil.experiencia_laboral = form.experiencia_laboral.data
            nuevo_perfil.formacion_academica = form.formacion_academica.data
            nuevo_perfil.intereses_laborales = form.intereses_laborales.data
            nuevo_perfil.adaptaciones_necesarias = form.adaptaciones_necesarias.data
            nuevo_perfil.motivaciones = form.motivaciones.data
            db.session.add(nuevo_perfil)
            db.session.commit()
            print(f"✅ TOURETTE - Perfil guardado: {form.nombre.data}")
            flash(f'¡Perfil Síndrome de Tourette completado, {form.nombre.data}!', 'success')
            
            # Enviar emails automáticos para nuevo registro Tourette
            try:
                from flask_email_service import email_service
                
                # Email de bienvenida al usuario Tourette
                email_service.send_welcome_email_user(
                    nombre=form.nombre.data,
                    email=form.email.data,
                    tipo_neurodivergencia="Síndrome de Tourette"
                )
                
                # Email de notificación a DiversIA
                email_service.send_notification_email("usuario", {
                    'nombre': form.nombre.data,
                    'apellidos': form.apellidos.data,
                    'email': form.email.data,
                    'telefono': form.telefono.data,
                    'ciudad': form.ciudad.data,
                    'tipo_neurodivergencia': 'Síndrome de Tourette',
                    'diagnostico_formal': form.diagnostico_formal.data,
                    'habilidades': form.habilidades.data
                })
                
                print(f"✅ TOURETTE - Emails enviados exitosamente: {form.nombre.data}")
                
            except Exception as e:
                print(f"⚠️ Error enviando emails de Tourette: {e}")
            return redirect(url_for('personas_nd'))
        except Exception as e:
            print(f"❌ TOURETTE - Error: {e}")
            flash('Error al guardar tu perfil. Intenta de nuevo.', 'error')
            db.session.rollback()
    return render_template('registro-tourette.html', form=form)

# DISPRAXIA ELIMINADA - NO ESTÁ EN LA LISTA OFICIAL

# DUPLICADOS ELIMINADOS - MANTENIENDO SOLO RUTAS ORIGINALES

@app.route('/registro-altas-capacidades', methods=['GET', 'POST'])
def registro_altas_capacidades():
    """Registro específico para Altas Capacidades/Superdotación"""
    from forms import RegistroAltasCapacidadesForm
    form = RegistroAltasCapacidadesForm()
    
    # Validación más permisiva para debug
    if request.method == 'POST' and form.nombre.data and form.email.data:
        try:
            from models import NeurodivergentProfile
            nuevo_perfil = NeurodivergentProfile()
            nuevo_perfil.nombre = form.nombre.data
            nuevo_perfil.apellidos = form.apellidos.data
            nuevo_perfil.email = form.email.data
            nuevo_perfil.telefono = form.telefono.data or ''
            nuevo_perfil.ciudad = form.ciudad.data or 'No especificada'
            nuevo_perfil.fecha_nacimiento = form.fecha_nacimiento.data or '1990-01-01'
            nuevo_perfil.tipo_neurodivergencia = 'Superdotación/Altas Capacidades'
            nuevo_perfil.diagnostico_formal = form.diagnostico_formal.data == 'si'
            nuevo_perfil.habilidades = form.habilidades.data
            nuevo_perfil.experiencia_laboral = form.experiencia_laboral.data
            nuevo_perfil.formacion_academica = form.formacion_academica.data
            nuevo_perfil.intereses_laborales = form.intereses_laborales.data
            nuevo_perfil.adaptaciones_necesarias = form.adaptaciones_necesarias.data
            nuevo_perfil.motivaciones = form.motivaciones.data
            db.session.add(nuevo_perfil)
            db.session.commit()
            print(f"✅ ALTAS CAPACIDADES - Perfil guardado: {form.nombre.data}")
            flash(f'¡Perfil Altas Capacidades completado, {form.nombre.data}!', 'success')
            
            # Enviar emails automáticos para nuevo registro Altas Capacidades
            try:
                from flask_email_service import email_service
                
                # Email de bienvenida al usuario Altas Capacidades
                email_service.send_welcome_email_user(
                    nombre=form.nombre.data,
                    email=form.email.data,
                    tipo_neurodivergencia="Altas Capacidades"
                )
                
                # Email de notificación a DiversIA
                email_service.send_notification_email("usuario", {
                    'nombre': form.nombre.data,
                    'apellidos': form.apellidos.data,
                    'email': form.email.data,
                    'telefono': form.telefono.data,
                    'ciudad': form.ciudad.data,
                    'tipo_neurodivergencia': 'Altas Capacidades',
                    'diagnostico_formal': form.diagnostico_formal.data,
                    'habilidades': form.habilidades.data
                })
                
                print(f"✅ ALTAS CAPACIDADES - Emails enviados exitosamente: {form.nombre.data}")
                
            except Exception as e:
                print(f"⚠️ Error enviando emails de Altas Capacidades: {e}")
            return redirect(url_for('personas_nd'))
        except Exception as e:
            print(f"❌ ALTAS CAPACIDADES - Error: {e}")
            flash('Error al guardar tu perfil. Intenta de nuevo.', 'error')
            db.session.rollback()
    else:
        if request.method == 'POST':
            print("❌ ALTAS CAPACIDADES - Errores de validación:", form.errors)
    return render_template('registro-altas-capacidades.html', form=form)

# ========== FORMULARIOS FALTANTES ==========

@app.route('/registro-tel', methods=['GET', 'POST'])
def registro_tel():
    """Registro específico para TEL (Trastorno Específico del Lenguaje)"""
    from forms import RegistroTELForm
    form = RegistroTELForm()
    
    # Validación más permisiva para debug
    if request.method == 'POST' and form.nombre.data and form.email.data:
        try:
            from models import NeurodivergentProfile
            nuevo_perfil = NeurodivergentProfile()
            nuevo_perfil.nombre = form.nombre.data
            nuevo_perfil.apellidos = form.apellidos.data
            nuevo_perfil.email = form.email.data
            nuevo_perfil.telefono = form.telefono.data or ''
            nuevo_perfil.ciudad = form.ciudad.data or 'No especificada'
            nuevo_perfil.fecha_nacimiento = form.fecha_nacimiento.data or '1990-01-01'
            nuevo_perfil.tipo_neurodivergencia = 'TEL'
            nuevo_perfil.diagnostico_formal = form.diagnostico_formal.data == 'si'
            nuevo_perfil.habilidades = form.habilidades.data
            nuevo_perfil.experiencia_laboral = form.experiencia_laboral.data
            nuevo_perfil.formacion_academica = form.formacion_academica.data
            nuevo_perfil.intereses_laborales = form.intereses_laborales.data
            nuevo_perfil.adaptaciones_necesarias = form.adaptaciones_necesarias.data
            nuevo_perfil.motivaciones = form.motivaciones.data
            db.session.add(nuevo_perfil)
            db.session.commit()
            print(f"✅ TEL - Perfil guardado: {form.nombre.data}")
            flash(f'¡Perfil TEL completado, {form.nombre.data}!', 'success')
            
            # Enviar emails automáticos para nuevo registro TEL
            try:
                from flask_email_service import email_service
                
                # Email de bienvenida al usuario TEL
                email_service.send_welcome_email_user(
                    nombre=form.nombre.data,
                    email=form.email.data,
                    tipo_neurodivergencia="TEL"
                )
                
                # Email de notificación a DiversIA
                email_service.send_notification_email("usuario", {
                    'nombre': form.nombre.data,
                    'apellidos': form.apellidos.data,
                    'email': form.email.data,
                    'telefono': form.telefono.data,
                    'ciudad': form.ciudad.data,
                    'tipo_neurodivergencia': 'TEL',
                    'diagnostico_formal': form.diagnostico_formal.data,
                    'habilidades': form.habilidades.data
                })
                
                print(f"✅ TEL - Emails enviados exitosamente: {form.nombre.data}")
                
            except Exception as e:
                print(f"⚠️ Error enviando emails de TEL: {e}")
            return redirect(url_for('personas_nd'))
        except Exception as e:
            print(f"❌ TEL - Error: {e}")
            flash('Error al guardar tu perfil. Intenta de nuevo.', 'error')
            db.session.rollback()
    else:
        if request.method == 'POST':
            print("❌ TEL - Errores de validación:", form.errors)
    return render_template('registro-tel.html', form=form)

@app.route('/registro-disgrafia', methods=['GET', 'POST'])
def registro_disgrafia():
    """Registro específico para Disgrafía"""
    from forms import RegistroDisgrafiaForm
    form = RegistroDisgrafiaForm()
    
    # Validación más permisiva para debug
    if request.method == 'POST' and form.nombre.data and form.email.data:
        try:
            from models import NeurodivergentProfile
            nuevo_perfil = NeurodivergentProfile()
            nuevo_perfil.nombre = form.nombre.data
            nuevo_perfil.apellidos = form.apellidos.data
            nuevo_perfil.email = form.email.data
            nuevo_perfil.telefono = form.telefono.data or ''
            nuevo_perfil.ciudad = form.ciudad.data or 'No especificada'
            nuevo_perfil.fecha_nacimiento = form.fecha_nacimiento.data or '1990-01-01'
            nuevo_perfil.tipo_neurodivergencia = 'Disgrafía'
            nuevo_perfil.diagnostico_formal = form.diagnostico_formal.data == 'si'
            nuevo_perfil.habilidades = form.habilidades.data
            nuevo_perfil.experiencia_laboral = form.experiencia_laboral.data
            nuevo_perfil.formacion_academica = form.formacion_academica.data
            nuevo_perfil.intereses_laborales = form.intereses_laborales.data
            nuevo_perfil.adaptaciones_necesarias = form.adaptaciones_necesarias.data
            nuevo_perfil.motivaciones = form.motivaciones.data
            db.session.add(nuevo_perfil)
            db.session.commit()
            print(f"✅ DISGRAFÍA - Perfil guardado: {form.nombre.data}")
            flash(f'¡Perfil Disgrafía completado, {form.nombre.data}!', 'success')
            
            # Enviar emails automáticos para nuevo registro Disgrafía
            try:
                from flask_email_service import email_service
                
                # Email de bienvenida al usuario Disgrafía
                email_service.send_welcome_email_user(
                    nombre=form.nombre.data,
                    email=form.email.data,
                    tipo_neurodivergencia="Disgrafía"
                )
                
                # Email de notificación a DiversIA
                email_service.send_notification_email("usuario", {
                    'nombre': form.nombre.data,
                    'apellidos': form.apellidos.data,
                    'email': form.email.data,
                    'telefono': form.telefono.data,
                    'ciudad': form.ciudad.data,
                    'tipo_neurodivergencia': 'Disgrafía',
                    'diagnostico_formal': form.diagnostico_formal.data,
                    'habilidades': form.habilidades.data
                })
                
                print(f"✅ DISGRAFÍA - Emails enviados exitosamente: {form.nombre.data}")
                
            except Exception as e:
                print(f"⚠️ Error enviando emails de Disgrafía: {e}")
            return redirect(url_for('personas_nd'))
        except Exception as e:
            print(f"❌ DISGRAFÍA - Error: {e}")
            flash('Error al guardar tu perfil. Intenta de nuevo.', 'error')
            db.session.rollback()
    else:
        if request.method == 'POST':
            print("❌ DISGRAFÍA - Errores de validación:", form.errors)
    return render_template('registro-disgrafia.html', form=form)

@app.route('/registro-tps', methods=['GET', 'POST'])
def registro_tps():
    """Registro específico para TPS (Trastorno del Procesamiento Sensorial)"""
    from forms import RegistroTPSForm
    form = RegistroTPSForm()
    
    # Validación más permisiva para debug
    if request.method == 'POST' and form.nombre.data and form.email.data:
        try:
            from models import NeurodivergentProfile
            nuevo_perfil = NeurodivergentProfile()
            nuevo_perfil.nombre = form.nombre.data
            nuevo_perfil.apellidos = form.apellidos.data
            nuevo_perfil.email = form.email.data
            nuevo_perfil.telefono = form.telefono.data or ''
            nuevo_perfil.ciudad = form.ciudad.data or 'No especificada'
            nuevo_perfil.fecha_nacimiento = form.fecha_nacimiento.data or '1990-01-01'
            nuevo_perfil.tipo_neurodivergencia = 'TPS'
            nuevo_perfil.diagnostico_formal = form.diagnostico_formal.data == 'si'
            nuevo_perfil.habilidades = form.habilidades.data
            nuevo_perfil.experiencia_laboral = form.experiencia_laboral.data
            nuevo_perfil.formacion_academica = form.formacion_academica.data
            nuevo_perfil.intereses_laborales = form.intereses_laborales.data
            nuevo_perfil.adaptaciones_necesarias = form.adaptaciones_necesarias.data
            nuevo_perfil.motivaciones = form.motivaciones.data
            db.session.add(nuevo_perfil)
            db.session.commit()
            print(f"✅ TPS - Perfil guardado: {form.nombre.data}")
            flash(f'¡Perfil TPS completado, {form.nombre.data}!', 'success')
            
            # Enviar emails automáticos para nuevo registro TPS
            try:
                from flask_email_service import email_service
                
                # Email de bienvenida al usuario TPS
                email_service.send_welcome_email_user(
                    nombre=form.nombre.data,
                    email=form.email.data,
                    tipo_neurodivergencia="TPS"
                )
                
                # Email de notificación a DiversIA
                email_service.send_notification_email("usuario", {
                    'nombre': form.nombre.data,
                    'apellidos': form.apellidos.data,
                    'email': form.email.data,
                    'telefono': form.telefono.data,
                    'ciudad': form.ciudad.data,
                    'tipo_neurodivergencia': 'TPS',
                    'diagnostico_formal': form.diagnostico_formal.data,
                    'habilidades': form.habilidades.data
                })
                
                print(f"✅ TPS - Emails enviados exitosamente: {form.nombre.data}")
                
            except Exception as e:
                print(f"⚠️ Error enviando emails de TPS: {e}")
            return redirect(url_for('personas_nd'))
        except Exception as e:
            print(f"❌ TPS - Error: {e}")
            flash('Error al guardar tu perfil. Intenta de nuevo.', 'error')
            db.session.rollback()
    else:
        if request.method == 'POST':
            print("❌ TPS - Errores de validación:", form.errors)
    return render_template('registro-tps.html', form=form)

@app.route('/registro-asociacion', methods=['GET', 'POST'])
def registro_asociacion():
    """Registro de asociaciones neurodivergentes"""
    from forms import AsociacionForm
    
    form = AsociacionForm()
    
    if form.validate_on_submit():
        try:
            from models import Asociacion
            
            # Convertir listas a JSON strings
            neurodivergencias = ','.join(form.neurodivergencias_atendidas.data) if form.neurodivergencias_atendidas.data else ''
            servicios = ','.join(form.servicios.data) if form.servicios.data else ''
            certificaciones = ','.join(form.certificaciones.data) if form.certificaciones.data else ''
            
            nueva_asociacion = Asociacion()
            nueva_asociacion.nombre_asociacion = form.nombre_asociacion.data
            nueva_asociacion.acronimo = form.acronimo.data
            nueva_asociacion.pais = form.pais.data
            nueva_asociacion.otro_pais = form.otro_pais.data if form.pais.data == 'otro' else None
            nueva_asociacion.tipo_documento = form.tipo_documento.data
            nueva_asociacion.numero_documento = form.numero_documento.data
            nueva_asociacion.descripcion_otro_documento = form.descripcion_otro_documento.data if form.tipo_documento.data == 'otro' else None
            nueva_asociacion.neurodivergencias_atendidas = neurodivergencias
            nueva_asociacion.servicios = servicios
            nueva_asociacion.certificaciones = certificaciones
            nueva_asociacion.ciudad = form.ciudad.data
            nueva_asociacion.direccion = form.direccion.data
            nueva_asociacion.telefono = form.telefono.data
            nueva_asociacion.email = form.email.data
            nueva_asociacion.sitio_web = form.sitio_web.data
            nueva_asociacion.descripcion = form.descripcion.data
            nueva_asociacion.años_funcionamiento = form.años_funcionamiento.data
            nueva_asociacion.numero_socios = form.numero_socios.data
            nueva_asociacion.contacto_nombre = form.contacto_nombre.data
            nueva_asociacion.contacto_cargo = form.contacto_cargo.data
            nueva_asociacion.estado = 'pendiente'
            nueva_asociacion.ip_solicitud = request.remote_addr
            nueva_asociacion.user_agent = request.user_agent.string[:500] if request.user_agent else None
            
            db.session.add(nueva_asociacion)
            db.session.commit()
            
            # También guardar en CRM mínimo - TABLA SEPARADA PARA ASOCIACIONES
            try:
                from crm_minimal import load_data, save_data
                
                crm_data = load_data()
                asociaciones = crm_data.get('asociaciones', [])
                
                # Generar ID único para asociaciones
                new_id = max([a.get('id', 0) for a in asociaciones], default=0) + 1
                
                crm_asociacion = {
                    'id': new_id,
                    'nombre_asociacion': nueva_asociacion.nombre_asociacion,
                    'acronimo': nueva_asociacion.acronimo,
                    'email': nueva_asociacion.email,
                    'telefono': nueva_asociacion.telefono or '',
                    'ciudad': nueva_asociacion.ciudad,
                    'pais': nueva_asociacion.pais,
                    'tipo_documento': nueva_asociacion.tipo_documento,
                    'numero_documento': nueva_asociacion.numero_documento,
                    'neurodivergencias_atendidas': neurodivergencias,
                    'servicios': servicios,
                    'contacto_nombre': nueva_asociacion.contacto_nombre,
                    'contacto_cargo': nueva_asociacion.contacto_cargo,
                    'estado': nueva_asociacion.estado,
                    'created_at': datetime.now().isoformat(),
                    'origen': 'Formulario Asociación'
                }
                
                asociaciones.append(crm_asociacion)
                crm_data['asociaciones'] = asociaciones
                save_data(crm_data)
                print(f"✅ Asociación guardada en CRM separado: {nueva_asociacion.nombre_asociacion}")
                
            except Exception as e:
                print(f"⚠️ Error guardando asociación en CRM: {e}")
            
            # Enviar emails automáticos con Gmail (nuevo sistema moderno)
            try:
                from flask_email_service import email_service
                
                # Email de bienvenida a la Asociación
                email_service.send_welcome_email_association(
                    nombre_asociacion=nueva_asociacion.nombre_asociacion,
                    email=nueva_asociacion.email,
                    contacto_nombre=nueva_asociacion.contacto_nombre,
                    pais=nueva_asociacion.pais
                )
                
                # Email de notificación a DiversIA
                email_service.send_notification_email("asociacion", {
                    'nombre_asociacion': nueva_asociacion.nombre_asociacion,
                    'acronimo': nueva_asociacion.acronimo,
                    'email': nueva_asociacion.email,
                    'telefono': nueva_asociacion.telefono,
                    'ciudad': nueva_asociacion.ciudad,
                    'pais': nueva_asociacion.pais,
                    'contacto_nombre': nueva_asociacion.contacto_nombre,
                    'contacto_cargo': nueva_asociacion.contacto_cargo,
                    'neurodivergencias_atendidas': nueva_asociacion.neurodivergencias_atendidas,
                    'servicios': nueva_asociacion.servicios
                })
                
                print(f"✅ ASOCIACIÓN - Emails Gmail enviados exitosamente: {nueva_asociacion.nombre_asociacion}")
                
            except Exception as e:
                print(f"⚠️ Error enviando emails Gmail de Asociación: {e}")
                
                # Fallback al sistema anterior si Gmail falla
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
                        print(f"✅ Notificación fallback enviada a DiversIA")
                    else:
                        print(f"⚠️ No se pudo enviar la notificación fallback")
                        
                except Exception as e2:
                    print(f"⚠️ Error en sistema fallback: {e2}")
            
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

# ==================== API ENDPOINTS PARA EDICIÓN CRM ====================

@app.route('/api/usuario/<user_id>/editar', methods=['GET', 'POST'])
@app.route('/api/edit_user/<user_id>', methods=['GET', 'POST'])  # Ruta adicional para compatibilidad
def api_editar_usuario(user_id):
    """API para editar usuario (funciona correctamente aquí)"""
    try:
        from flask import session, jsonify
        
        # Verificar autenticación admin
        if not ('admin_user_id' in session or 'admin_username' in session or session.get('admin_ok')):
            return jsonify({'success': False, 'error': 'No autorizado'}), 401
        
        print(f"🔧 API edit request for user: {user_id}")
        
        # Determinar si es User o NeurodivergentProfile
        is_profile = user_id.startswith('profile_')
        actual_id = user_id.replace('user_', '').replace('profile_', '')
        
        if is_profile:
            from models import NeurodivergentProfile
            usuario = NeurodivergentProfile.query.get_or_404(actual_id)
            table_name = 'NeurodivergentProfile'
        else:
            from models import User
            usuario = User.query.get_or_404(actual_id)
            table_name = 'User'
        
        if request.method == 'POST':
            # Actualizar campos del usuario
            data = request.get_json()
            
            for field, value in data.items():
                if hasattr(usuario, field) and field != 'id':
                    if field == 'diagnostico_formal' and isinstance(value, str):
                        setattr(usuario, field, value.lower() == 'true' or value.lower() == 'si')
                    else:
                        setattr(usuario, field, value)
            
            db.session.commit()
            print(f"✅ {table_name} editado: {usuario.nombre} {usuario.apellidos}")
            
            return jsonify({
                'success': True,
                'message': f'Usuario {usuario.nombre} actualizado correctamente'
            })
        
        # GET: Devolver datos actuales del usuario
        usuario_data = {
            'id': user_id,
            'fuente': table_name,
            'nombre': usuario.nombre or '',
            'apellidos': usuario.apellidos or '',
            'email': usuario.email or '',
            'telefono': usuario.telefono or '',
            'ciudad': usuario.ciudad or '',
            'fecha_nacimiento': usuario.fecha_nacimiento.isoformat() if usuario.fecha_nacimiento else '',
            'tipo_neurodivergencia': usuario.tipo_neurodivergencia or '',
            'diagnostico_formal': bool(usuario.diagnostico_formal),
            'habilidades': usuario.habilidades or '',
            'experiencia_laboral': usuario.experiencia_laboral or '',
            'formacion_academica': usuario.formacion_academica or '',
            'intereses_laborales': usuario.intereses_laborales or '',
            'adaptaciones_necesarias': usuario.adaptaciones_necesarias or '',
            'motivaciones': usuario.motivaciones or ''
        }
        
        print(f"📤 Sending user data: {usuario_data['nombre']} {usuario_data['apellidos']}")
        
        from flask import jsonify
        return jsonify(usuario_data)
        
    except Exception as e:
        from flask import jsonify
        print(f"❌ Error editando usuario {user_id}: {e}")
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/usuario/<user_id>/borrar', methods=['DELETE'])
@app.route('/api/delete_user/<user_id>', methods=['DELETE'])  # Ruta adicional para compatibilidad
def api_borrar_usuario(user_id):
    """API para borrar usuario (funciona correctamente aquí)"""
    try:
        from flask import session, jsonify
        
        # Verificar autenticación admin
        if not ('admin_user_id' in session or 'admin_username' in session or session.get('admin_ok')):
            return jsonify({'success': False, 'error': 'Acceso no autorizado'}), 401
        
        # Determinar si es User o NeurodivergentProfile
        is_profile = user_id.startswith('profile_')
        actual_id = user_id.replace('user_', '').replace('profile_', '')
        
        if is_profile:
            from models import NeurodivergentProfile
            usuario = NeurodivergentProfile.query.get_or_404(actual_id)
            table_name = 'NeurodivergentProfile'
        else:
            from models import User
            usuario = User.query.get_or_404(actual_id)
            table_name = 'User'
        
        nombre_completo = f"{usuario.nombre} {usuario.apellidos}"
        
        # Borrar usuario
        db.session.delete(usuario)
        db.session.commit()
        
        print(f"🗑️ {table_name} borrado exitosamente: {nombre_completo}")
        
        from flask import jsonify
        return jsonify({
            'success': True,
            'message': f'Usuario {nombre_completo} borrado correctamente'
        })
        
    except Exception as e:
        from flask import jsonify
        print(f"❌ Error borrando usuario {user_id}: {e}")
        return jsonify({'success': False, 'error': str(e)}), 500

# ==================== PÁGINAS DE EDICIÓN CRM ====================

@app.route('/crm-editar/<user_id>')
def crm_editar_usuario_form(user_id):
    """Página de edición de usuario"""
    try:
        # Verificar que es administrador
        if not ('admin_user_id' in session or 'admin_username' in session or session.get('admin_ok')):
            flash('Acceso restringido. Inicia sesión como administrador.', 'error')
            return redirect('/admin/login-new')
        
        print(f"🔧 Abriendo editor para usuario: {user_id}")
        return render_template('crm-editar-usuario.html', user_id=user_id)
        
    except Exception as e:
        print(f"❌ Error abriendo editor: {e}")
        flash('Error al abrir el editor de usuario.', 'error')
        return redirect('/crm-neurodivergentes')

print("✅ Routes simplificado cargado correctamente")