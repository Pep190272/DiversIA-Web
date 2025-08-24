#!/usr/bin/env python3
"""
CRM Minimal - Sistema simple que funciona sin complicaciones
"""

from flask import jsonify, request, render_template, session, redirect
import json
import os
from datetime import datetime
import csv
import io

# Archivo de datos simple
DATA_FILE = 'crm_data.json'

def init_data_file():
    """Inicializar archivo de datos si no existe"""
    if not os.path.exists(DATA_FILE):
        data = {
            'companies': [],
            'contacts': [],
            'stats': {
                'total_companies': 0,
                'total_contacts': 0,
                'last_updated': datetime.now().isoformat()
            }
        }
        with open(DATA_FILE, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)

def load_data():
    """Cargar datos del archivo"""
    init_data_file()
    with open(DATA_FILE, 'r', encoding='utf-8') as f:
        return json.load(f)

def save_data(data):
    """Guardar datos al archivo"""
    data['stats']['last_updated'] = datetime.now().isoformat()
    data['stats']['total_companies'] = len(data.get('companies', []))
    data['stats']['total_contacts'] = len(data.get('contacts', []))
    
    with open(DATA_FILE, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

def create_minimal_crm_routes(app):
    """Crear rutas del CRM minimal"""
    
    @app.route('/crm-minimal')
    def crm_minimal_dashboard():
        """Dashboard del CRM minimal - requiere autenticación"""
        # Verificar si está autenticado como admin
        if 'admin_ok' not in session or not session.get('admin_ok'):
            return redirect('/diversia-admin')
        return render_template('crm-minimal.html')
    
    @app.route('/empresas')
    def empresas_cards():
        """Vista de tarjetas de empresas para edición individual"""
        if 'admin_ok' not in session or not session.get('admin_ok'):
            return redirect('/diversia-admin')
        
        data = load_data()
        companies = data.get('companies', [])
        return render_template('empresas-cards.html', companies=companies)
    
    @app.route('/asociaciones-crm')
    def asociaciones_crm():
        """Dashboard de asociaciones del CRM - requiere autenticación"""
        if 'admin_ok' not in session or not session.get('admin_ok'):
            return redirect('/diversia-admin')
        return render_template('asociaciones-crm.html')
    
    @app.route('/usuarios-neurodivergentes')
    def usuarios_neurodivergentes():
        """Dashboard de usuarios neurodivergentes del CRM - requiere autenticación"""
        if 'admin_ok' not in session or not session.get('admin_ok'):
            return redirect('/diversia-admin')
        return render_template('crm-neurodivergentes.html')
    
    @app.route('/leads-generales')
    def leads_generales():
        """Dashboard de leads generales del test 'Haz mi test' - requiere autenticación"""
        if 'admin_ok' not in session or not session.get('admin_ok'):
            return redirect('/diversia-admin')
        return render_template('crm-leads-generales.html')
    
    @app.route('/api/minimal/companies')
    def get_companies_minimal():
        """Obtener todas las empresas"""
        data = load_data()
        return jsonify(data.get('companies', []))
    
    @app.route('/api/minimal/companies', methods=['POST'])
    def create_company_minimal():
        """Crear nueva empresa"""
        try:
            company_data = request.get_json()
            
            data = load_data()
            companies = data.get('companies', [])
            
            # Generar ID
            new_id = max([c.get('id', 0) for c in companies], default=0) + 1
            
            new_company = {
                'id': new_id,
                'nombre': company_data.get('nombre', ''),
                'email': company_data.get('email', ''),
                'telefono': company_data.get('telefono', ''),
                'sector': company_data.get('sector', ''),
                'ciudad': company_data.get('ciudad', ''),
                'created_at': datetime.now().isoformat()
            }
            
            companies.append(new_company)
            data['companies'] = companies
            save_data(data)
            
            return jsonify({'success': True, 'company': new_company})
        except Exception as e:
            return jsonify({'success': False, 'error': str(e)}), 500
    
    @app.route('/api/minimal/companies/<int:company_id>')
    def get_company_minimal(company_id):
        """Obtener una empresa específica"""
        try:
            data = load_data()
            companies = data.get('companies', [])
            
            company = next((c for c in companies if c.get('id') == company_id), None)
            if not company:
                return jsonify({'success': False, 'error': 'Empresa no encontrada'}), 404
            
            return jsonify({'success': True, 'company': company})
        except Exception as e:
            return jsonify({'success': False, 'error': str(e)}), 500
    
    @app.route('/api/minimal/companies/<int:company_id>', methods=['PUT'])
    def update_company_minimal(company_id):
        """Actualizar empresa específica"""
        try:
            update_data = request.get_json()
            
            data = load_data()
            companies = data.get('companies', [])
            
            # Encontrar empresa
            company_index = next((i for i, c in enumerate(companies) if c.get('id') == company_id), None)
            if company_index is None:
                return jsonify({'success': False, 'error': 'Empresa no encontrada'}), 404
            
            # Actualizar campos
            company = companies[company_index]
            company.update({
                'nombre': update_data.get('nombre', company.get('nombre', '')),
                'email': update_data.get('email', company.get('email', '')),
                'telefono': update_data.get('telefono', company.get('telefono', '')),
                'sector': update_data.get('sector', company.get('sector', '')),
                'ciudad': update_data.get('ciudad', company.get('ciudad', '')),
                'fecha_contacto': update_data.get('fecha_contacto', company.get('fecha_contacto', '')),
                'notas': update_data.get('notas', company.get('notas', '')),
                'updated_at': datetime.now().isoformat()
            })
            
            companies[company_index] = company
            data['companies'] = companies
            save_data(data)
            
            return jsonify({'success': True, 'company': company})
        except Exception as e:
            return jsonify({'success': False, 'error': str(e)}), 500

    @app.route('/api/minimal/companies/<int:company_id>', methods=['DELETE'])
    def delete_company_minimal(company_id):
        """Eliminar empresa"""
        try:
            data = load_data()
            companies = data.get('companies', [])
            
            # Filtrar empresa a eliminar
            companies = [c for c in companies if c.get('id') != company_id]
            data['companies'] = companies
            save_data(data)
            
            return jsonify({'success': True, 'message': 'Empresa eliminada'})
        except Exception as e:
            return jsonify({'success': False, 'error': str(e)}), 500
    
    @app.route('/api/minimal/companies/clear', methods=['POST'])
    def clear_companies_minimal():
        """Eliminar todas las empresas"""
        try:
            data = load_data()
            count = len(data.get('companies', []))
            data['companies'] = []
            save_data(data)
            
            return jsonify({'success': True, 'message': f'{count} empresas eliminadas'})
        except Exception as e:
            return jsonify({'success': False, 'error': str(e)}), 500
    
    @app.route('/api/minimal/import-csv', methods=['POST'])
    def import_csv_minimal():
        """Importar CSV con formato específico de DiversIA"""
        try:
            if 'csv_file' not in request.files:
                return jsonify({'success': False, 'error': 'No se proporcionó archivo'})
            
            file = request.files['csv_file']
            if file.filename == '':
                return jsonify({'success': False, 'error': 'No se seleccionó archivo'})
            
            # Leer CSV con formato específico
            content = file.stream.read().decode("UTF8")
            stream = io.StringIO(content, newline=None)
            reader = csv.DictReader(stream)
            
            data = load_data()
            companies = data.get('companies', [])
            
            created = 0
            skipped = 0
            
            for row in reader:
                # Mapear columnas específicas del CSV de DiversIA
                empresa = row.get('Empresa', '').strip()
                email = row.get('Email', '').strip()
                telefono = row.get('Telefono', '').strip()
                sector = row.get('Sector', '').strip()
                ciudad = row.get('Ciudad', '').strip()
                fecha = row.get('Fecha', '').strip()
                acciones = row.get('Acciones', '').strip()
                
                # Validar que tenga al menos empresa
                if not empresa:
                    skipped += 1
                    continue
                
                # Limpiar email si tiene formato mailto:
                if email.startswith('mailto:'):
                    email = email.replace('mailto:', '')
                
                # Generar ID único
                new_id = max([c.get('id', 0) for c in companies], default=0) + 1
                
                new_company = {
                    'id': new_id,
                    'nombre': empresa,
                    'email': email,
                    'telefono': telefono,
                    'sector': sector,
                    'ciudad': ciudad,
                    'fecha_contacto': fecha,
                    'notas': acciones,
                    'created_at': datetime.now().isoformat()
                }
                
                companies.append(new_company)
                created += 1
            
            data['companies'] = companies
            save_data(data)
            
            message = f'Importación completada: {created} empresas creadas'
            if skipped > 0:
                message += f', {skipped} filas omitidas'
            
            return jsonify({
                'success': True,
                'message': message,
                'created': created,
                'skipped': skipped
            })
            
        except Exception as e:
            return jsonify({'success': False, 'error': f'Error procesando CSV: {str(e)}'}), 500
    
    # Ruta adicional para exportar datos
    @app.route('/api/minimal/export-csv')
    def export_csv_minimal():
        """Exportar datos a CSV"""
        try:
            from flask import make_response
            
            data = load_data()
            companies = data.get('companies', [])
            
            if not companies:
                return jsonify({'success': False, 'error': 'No hay datos para exportar'})
            
            # Crear CSV
            output = io.StringIO()
            writer = csv.writer(output)
            
            # Escribir encabezados
            writer.writerow(['Empresa', 'Email', 'Telefono', 'Sector', 'Ciudad', 'Fecha', 'Acciones'])
            
            # Escribir datos
            for company in companies:
                writer.writerow([
                    company.get('nombre', ''),
                    company.get('email', ''),
                    company.get('telefono', ''),
                    company.get('sector', ''),
                    company.get('ciudad', ''),
                    company.get('fecha_contacto', ''),
                    company.get('notas', '')
                ])
            
            # Preparar respuesta
            output.seek(0)
            response = make_response(output.getvalue())
            response.headers['Content-Type'] = 'text/csv'
            response.headers['Content-Disposition'] = f'attachment; filename=diversia_empresas_{datetime.now().strftime("%Y%m%d")}.csv'
            
            return response
            
        except Exception as e:
            return jsonify({'success': False, 'error': str(e)}), 500
    
    # ==================== RUTAS PARA USUARIOS NEURODIVERGENTES ====================
    
    @app.route('/api/neurodivergent-profiles')
    def get_neurodivergent_profiles():
        """Obtener todos los perfiles neurodivergentes detallados de la base de datos"""
        try:
            from models import NeurodivergentProfile
            from app import db
            
            profiles = NeurodivergentProfile.query.all()
            
            profiles_data = []
            for profile in profiles:
                profiles_data.append({
                    'id': profile.id,
                    'nombre': profile.nombre,
                    'apellidos': profile.apellidos,
                    'email': profile.email,
                    'telefono': profile.telefono,
                    'ciudad': profile.ciudad,
                    'fecha_nacimiento': profile.fecha_nacimiento.isoformat() if profile.fecha_nacimiento else None,
                    'tipo_neurodivergencia': profile.tipo_neurodivergencia,
                    'diagnostico_formal': profile.diagnostico_formal,
                    'habilidades': profile.habilidades,
                    'experiencia_laboral': profile.experiencia_laboral,
                    'formacion_academica': profile.formacion_academica,
                    'intereses_laborales': profile.intereses_laborales,
                    'adaptaciones_necesarias': profile.adaptaciones_necesarias,
                    'motivaciones': profile.motivaciones,
                    # Campos específicos TDAH
                    'tipo_tdah': profile.tipo_tdah,
                    'nivel_atencion': profile.nivel_atencion,
                    'impulsividad': profile.impulsividad,
                    'hiperactividad': profile.hiperactividad,
                    'medicacion': profile.medicacion,
                    'medicacion_actual': profile.medicacion_actual,
                    'dosis_medicacion': profile.dosis_medicacion,
                    'efectos_secundarios': profile.efectos_secundarios,
                    'estrategias_organizacion': profile.estrategias_organizacion,
                    # Campos específicos TEA
                    'nivel_comunicacion': profile.nivel_comunicacion,
                    'sensibilidades': profile.sensibilidades,
                    'rutinas_importantes': profile.rutinas_importantes,
                    'intereses_especiales': profile.intereses_especiales,
                    'dificultades_sociales': profile.dificultades_sociales,
                    # Campos específicos Dislexia
                    'areas_dificultad': profile.areas_dificultad,
                    'herramientas_apoyo': profile.herramientas_apoyo,
                    'estrategias_lectura': profile.estrategias_lectura,
                    'created_at': profile.created_at.isoformat() if profile.created_at else None
                })
            
            return jsonify(profiles_data)
        except Exception as e:
            return jsonify({'success': False, 'error': str(e)}), 500

    # ==================== MIGRACIÓN DE USUARIOS LEGACY A LEADS ====================
    
    @app.route('/api/migrate-users-to-leads', methods=['POST'])
    def migrate_users_to_leads():
        """Migrar usuarios de la tabla User legacy a GeneralLead"""
        try:
            from models import NeurodivergentProfile, GeneralLead
            from app import db
            
            # Obtener todos los usuarios de la tabla legacy
            usuarios_legacy = User.query.all()
            migrados = 0
            
            for usuario in usuarios_legacy:
                # Verificar si ya existe en GeneralLead
                lead_existente = GeneralLead.query.filter_by(email=usuario.email).first()
                
                if not lead_existente:
                    # Migrar a GeneralLead
                    nuevo_lead = GeneralLead(
                        nombre=usuario.nombre,
                        apellidos=usuario.apellidos,
                        email=usuario.email,
                        telefono=usuario.telefono,
                        ciudad=usuario.ciudad,
                        fecha_nacimiento=usuario.fecha_nacimiento,
                        tipo_neurodivergencia=usuario.tipo_neurodivergencia,
                        diagnostico_formal=usuario.diagnostico_formal,
                        habilidades=usuario.habilidades,
                        experiencia_laboral=usuario.experiencia_laboral,
                        formacion_academica=usuario.formacion_academica,
                        intereses_laborales=usuario.intereses_laborales,
                        adaptaciones_necesarias=usuario.adaptaciones_necesarias,
                        motivaciones=usuario.motivaciones,
                        convertido_a_perfil=False,  # Viene del test general
                        created_at=usuario.created_at,
                        updated_at=usuario.updated_at
                    )
                    
                    db.session.add(nuevo_lead)
                    migrados += 1
            
            # Limpiar tabla legacy después de migrar
            if migrados > 0:
                User.query.delete()
                db.session.commit()
                
            return jsonify({
                'success': True, 
                'message': f'Migrados {migrados} usuarios de legacy a leads generales',
                'migrados': migrados
            })
            
        except Exception as e:
            db.session.rollback()
            return jsonify({'success': False, 'error': str(e)}), 500

    # ==================== RUTAS PARA LEADS GENERALES (TEST "HAZ MI TEST") ====================
    
    @app.route('/api/leads-generales')
    def get_leads_generales():
        """Obtener todos los leads del test general"""
        try:
            from models import GeneralLead
            from app import db
            
            leads = GeneralLead.query.all()
            
            leads_data = []
            for lead in leads:
                leads_data.append({
                    'id': lead.id,
                    'nombre': lead.nombre,
                    'apellidos': lead.apellidos,
                    'email': lead.email,
                    'telefono': lead.telefono,
                    'ciudad': lead.ciudad,
                    'fecha_nacimiento': lead.fecha_nacimiento.isoformat() if lead.fecha_nacimiento else None,
                    'tipo_neurodivergencia': lead.tipo_neurodivergencia,
                    'diagnostico_formal': lead.diagnostico_formal,
                    'habilidades': lead.habilidades,
                    'experiencia_laboral': lead.experiencia_laboral,
                    'formacion_academica': lead.formacion_academica,
                    'intereses_laborales': lead.intereses_laborales,
                    'adaptaciones_necesarias': lead.adaptaciones_necesarias,
                    'motivaciones': lead.motivaciones,
                    'convertido_a_perfil': lead.convertido_a_perfil,
                    'created_at': lead.created_at.isoformat() if lead.created_at else None
                })
            
            return jsonify(leads_data)
        except Exception as e:
            return jsonify({'success': False, 'error': str(e)}), 500
    
    @app.route('/api/leads-generales/<int:lead_id>')
    def get_lead_general(lead_id):
        """Obtener un lead específico para edición"""
        try:
            from models import GeneralLead
            
            lead = GeneralLead.query.get_or_404(lead_id)
            
            lead_data = {
                'id': lead.id,
                'nombre': lead.nombre,
                'apellidos': lead.apellidos,
                'email': lead.email,
                'telefono': lead.telefono,
                'ciudad': lead.ciudad,
                'fecha_nacimiento': lead.fecha_nacimiento.isoformat() if lead.fecha_nacimiento else None,
                'tipo_neurodivergencia': lead.tipo_neurodivergencia,
                'diagnostico_formal': lead.diagnostico_formal,
                'habilidades': lead.habilidades,
                'experiencia_laboral': lead.experiencia_laboral,
                'formacion_academica': lead.formacion_academica,
                'intereses_laborales': lead.intereses_laborales,
                'adaptaciones_necesarias': lead.adaptaciones_necesarias,
                'motivaciones': lead.motivaciones,
                'convertido_a_perfil': lead.convertido_a_perfil,
                'created_at': lead.created_at.isoformat() if lead.created_at else None
            }
            
            return jsonify(lead_data)
        except Exception as e:
            return jsonify({'success': False, 'error': str(e)}), 500
    
    @app.route('/api/leads-generales/<int:lead_id>', methods=['PUT'])
    def update_lead_general(lead_id):
        """Actualizar información de un lead"""
        try:
            from models import GeneralLead
            from app import db
            
            lead = GeneralLead.query.get_or_404(lead_id)
            data = request.get_json()
            
            # Actualizar campos
            if 'nombre' in data:
                lead.nombre = data['nombre']
            if 'apellidos' in data:
                lead.apellidos = data['apellidos']
            if 'telefono' in data:
                lead.telefono = data['telefono']
            if 'ciudad' in data:
                lead.ciudad = data['ciudad']
            if 'habilidades' in data:
                lead.habilidades = data['habilidades']
            if 'experiencia_laboral' in data:
                lead.experiencia_laboral = data['experiencia_laboral']
            if 'formacion_academica' in data:
                lead.formacion_academica = data['formacion_academica']
            if 'intereses_laborales' in data:
                lead.intereses_laborales = data['intereses_laborales']
            if 'adaptaciones_necesarias' in data:
                lead.adaptaciones_necesarias = data['adaptaciones_necesarias']
            if 'motivaciones' in data:
                lead.motivaciones = data['motivaciones']
            if 'convertido_a_perfil' in data:
                lead.convertido_a_perfil = data['convertido_a_perfil']
            
            db.session.commit()
            
            return jsonify({'success': True, 'message': 'Lead actualizado correctamente'})
        except Exception as e:
            return jsonify({'success': False, 'error': str(e)}), 500

    # ==================== APIS SEPARADAS POR TIPO DE USUARIO ====================""
    
    @app.route('/api/usuarios-neurodivergentes')
    def get_usuarios_neurodivergentes():
        """Obtener SOLO usuarios de formularios específicos ND (NeurodivergentProfile)"""
        try:
            from models import NeurodivergentProfile
            from app import db
            
            usuarios_data = []
            
            # Solo usuarios de la tabla NeurodivergentProfile (formularios específicos)
            try:
                usuarios_profile = NeurodivergentProfile.query.all()
                print(f"🔍 CRM ND - Encontrados {len(usuarios_profile)} perfiles neurodivergentes específicos")
                
                for profile in usuarios_profile:
                    print(f"📋 CRM ND - Perfil: {profile.nombre} {profile.apellidos} ({profile.tipo_neurodivergencia})")
                    usuarios_data.append({
                        'id': f'profile_{profile.id}',
                        'fuente': 'NeurodivergentProfile (formulario específico)',
                        'nombre': profile.nombre,
                        'apellidos': profile.apellidos,
                        'nombre_completo': f"{profile.nombre} {profile.apellidos}",
                        'email': profile.email,
                        'telefono': profile.telefono,
                        'ciudad': profile.ciudad,
                        'fecha_nacimiento': profile.fecha_nacimiento.isoformat() if profile.fecha_nacimiento else None,
                        'tipo_neurodivergencia': profile.tipo_neurodivergencia,
                        'diagnostico_formal': profile.diagnostico_formal,
                        'habilidades': profile.habilidades,
                        'experiencia_laboral': profile.experiencia_laboral,
                        'formacion_academica': profile.formacion_academica,
                        'intereses_laborales': profile.intereses_laborales,
                        'adaptaciones_necesarias': profile.adaptaciones_necesarias,
                        'motivaciones': profile.motivaciones,
                        'created_at': profile.created_at.isoformat() if profile.created_at else None
                    })
            except Exception as e:
                print(f"⚠️ Error cargando perfiles ND específicos: {e}")
            
            print(f"📊 CRM ND - Total perfiles ND específicos: {len(usuarios_data)}")
            return jsonify(usuarios_data)
            
        except Exception as e:
            print(f"❌ Error en API usuarios-neurodivergentes: {e}")
            return jsonify([])

    @app.route('/api/leads-generales')
    def get_leads_generales():
        """Obtener SOLO leads del test general (GeneralLead)"""
        try:
            from models import GeneralLead
            from app import db
            
            leads_data = []
            
            # Solo leads de la tabla GeneralLead (test general)
            try:
                leads = GeneralLead.query.all()
                print(f"🔍 CRM Leads - Encontrados {len(leads)} leads del test general")
                
                for lead in leads:
                    print(f"📋 CRM Leads - Lead: {lead.nombre} {lead.apellidos}")
                    leads_data.append({
                        'id': f'lead_{lead.id}',
                        'fuente': 'GeneralLead (test general)',
                        'nombre': lead.nombre,
                        'apellidos': lead.apellidos,
                        'email': lead.email,
                        'telefono': getattr(lead, 'telefono', ''),
                        'ciudad': getattr(lead, 'ciudad', ''),
                        'fecha_nacimiento': getattr(lead, 'fecha_nacimiento', None),
                        'tipo_neurodivergencia': getattr(lead, 'resultado_test', 'En proceso'),
                        'created_at': lead.created_at.isoformat() if lead.created_at else None
                    })
            except Exception as e:
                print(f"⚠️ Error cargando leads generales: {e}")
            
            print(f"📊 CRM Leads - Total leads generales: {len(leads_data)}")
            return jsonify(leads_data)
            
        except Exception as e:
            print(f"❌ Error en API leads-generales: {e}")
            return jsonify([])

    # ==================== RUTAS PARA USUARIOS GENERALES (LEGACY) ====================""
    
    @app.route('/api/usuarios')
    def get_usuarios():
        """Obtener TODOS los usuarios neurodivergentes (tabla User + nuevos perfiles)"""
        try:
            from models import User, NeurodivergentProfile
            from app import db
            
            usuarios_data = []
            
            # 1. Obtener usuarios de la tabla User original
            try:
                usuarios_user = User.query.all()
                for user in usuarios_user:
                    usuarios_data.append({
                        'id': f'user_{user.id}',
                        'fuente': 'User (original)',
                        'nombre': user.nombre,
                        'apellidos': user.apellidos,
                        'email': user.email,
                        'telefono': user.telefono,
                        'ciudad': user.ciudad,
                        'fecha_nacimiento': user.fecha_nacimiento.isoformat() if user.fecha_nacimiento else None,
                        'tipo_neurodivergencia': user.tipo_neurodivergencia,
                        'diagnostico_formal': user.diagnostico_formal,
                        'habilidades': user.habilidades,
                        'experiencia_laboral': user.experiencia_laboral,
                        'formacion_academica': user.formacion_academica,
                        'intereses_laborales': user.intereses_laborales,
                        'adaptaciones_necesarias': user.adaptaciones_necesarias,
                        'motivaciones': user.motivaciones,
                        'created_at': user.created_at.isoformat() if user.created_at else None
                    })
            except Exception as e:
                print(f"⚠️ Error cargando tabla User: {e}")
            
            # 2. Obtener usuarios de la tabla NeurodivergentProfile nueva  
            try:
                usuarios_profile = NeurodivergentProfile.query.all()
                print(f"🔍 CRM - Encontrados {len(usuarios_profile)} perfiles neurodivergentes")
                
                for profile in usuarios_profile:
                    print(f"📋 CRM - Perfil: {profile.nombre} {profile.apellidos} ({profile.tipo_neurodivergencia})")
                    usuarios_data.append({
                        'id': f'profile_{profile.id}',
                        'fuente': 'NeurodivergentProfile (nuevo)',
                        'nombre': profile.nombre,
                        'apellidos': profile.apellidos,
                        'email': profile.email,
                        'telefono': profile.telefono,
                        'ciudad': profile.ciudad,
                        'fecha_nacimiento': profile.fecha_nacimiento.isoformat() if profile.fecha_nacimiento else None,
                        'tipo_neurodivergencia': profile.tipo_neurodivergencia,
                        'diagnostico_formal': profile.diagnostico_formal,
                        'habilidades': profile.habilidades,
                        'experiencia_laboral': profile.experiencia_laboral,
                        'formacion_academica': profile.formacion_academica,
                        'intereses_laborales': profile.intereses_laborales,
                        'adaptaciones_necesarias': profile.adaptaciones_necesarias,
                        'motivaciones': profile.motivaciones,
                        'created_at': profile.created_at.isoformat() if profile.created_at else None
                    })
            except Exception as e:
                print(f"⚠️ Error cargando tabla NeurodivergentProfile: {e}")
            
            print(f"📊 CRM - Total usuarios combinados: {len(usuarios_data)}")
            
            return jsonify(usuarios_data)
        except Exception as e:
            return jsonify({'success': False, 'error': str(e)}), 500
    
    @app.route('/api/usuarios/<int:user_id>')
    def get_usuario(user_id):
        """Obtener un usuario específico"""
        try:
            from models import User  # Restaurar User original
            
            user = User.query.get_or_404(user_id)
            
            user_data = {
                'id': user.id,
                'nombre': user.nombre,
                'apellidos': user.apellidos,
                'email': user.email,
                'telefono': user.telefono,
                'ciudad': user.ciudad,
                'fecha_nacimiento': user.fecha_nacimiento.isoformat() if user.fecha_nacimiento else None,
                'tipo_neurodivergencia': user.tipo_neurodivergencia,
                'diagnostico_formal': user.diagnostico_formal,
                'habilidades': user.habilidades,
                'experiencia_laboral': user.experiencia_laboral,
                'formacion_academica': user.formacion_academica,
                'intereses_laborales': user.intereses_laborales,
                'adaptaciones_necesarias': user.adaptaciones_necesarias,
                'motivaciones': user.motivaciones,
                'created_at': user.created_at.isoformat() if user.created_at else None
            }
            
            return jsonify(user_data)
        except Exception as e:
            return jsonify({'success': False, 'error': str(e)}), 500

    # ==================== RUTAS PARA ASOCIACIONES ====================
    
    @app.route('/api/asociaciones')
    def get_asociaciones():
        """Obtener todas las asociaciones de la base de datos"""
        try:
            from models import Asociacion
            from app import db
            
            asociaciones = Asociacion.query.all()
            
            asociaciones_data = []
            for asoc in asociaciones:
                # Procesar neurodivergencias y servicios desde JSON
                import json
                try:
                    neurodivergencias = json.loads(asoc.neurodivergencias_atendidas) if asoc.neurodivergencias_atendidas else []
                except:
                    neurodivergencias = []
                
                try:
                    servicios = json.loads(asoc.servicios) if asoc.servicios else []
                except:
                    servicios = []
                
                asociaciones_data.append({
                    'id': asoc.id,
                    'nombre_asociacion': asoc.nombre_asociacion,
                    'acronimo': asoc.acronimo,
                    'pais': asoc.pais,
                    'ciudad': asoc.ciudad,
                    'telefono': asoc.telefono,
                    'email': asoc.email,
                    'sitio_web': asoc.sitio_web,
                    'contacto_nombre': asoc.contacto_nombre,
                    'contacto_cargo': asoc.contacto_cargo,
                    'estado': asoc.estado,
                    'años_funcionamiento': asoc.años_funcionamiento,
                    'numero_socios': asoc.numero_socios,
                    'neurodivergencias_atendidas': ', '.join(neurodivergencias) if neurodivergencias else '',
                    'servicios': ', '.join(servicios) if servicios else '',
                    'descripcion': asoc.descripcion,
                    'created_at': asoc.created_at.isoformat() if asoc.created_at else None
                })
            
            return jsonify(asociaciones_data)
        except Exception as e:
            return jsonify({'success': False, 'error': str(e)}), 500
    
    @app.route('/api/asociaciones/<int:asociacion_id>')
    def get_asociacion(asociacion_id):
        """Obtener una asociación específica"""
        try:
            from models import Asociacion
            
            asociacion = Asociacion.query.get_or_404(asociacion_id)
            
            # Procesar campos JSON
            import json
            try:
                neurodivergencias = json.loads(asociacion.neurodivergencias_atendidas) if asociacion.neurodivergencias_atendidas else []
            except:
                neurodivergencias = []
            
            try:
                servicios = json.loads(asociacion.servicios) if asociacion.servicios else []
            except:
                servicios = []
                
            data = {
                'id': asociacion.id,
                'nombre_asociacion': asociacion.nombre_asociacion,
                'acronimo': asociacion.acronimo,
                'pais': asociacion.pais,
                'ciudad': asociacion.ciudad,
                'direccion': asociacion.direccion,
                'telefono': asociacion.telefono,
                'email': asociacion.email,
                'sitio_web': asociacion.sitio_web,
                'contacto_nombre': asociacion.contacto_nombre,
                'contacto_cargo': asociacion.contacto_cargo,
                'estado': asociacion.estado,
                'años_funcionamiento': asociacion.años_funcionamiento,
                'numero_socios': asociacion.numero_socios,
                'neurodivergencias_atendidas': neurodivergencias,
                'servicios': servicios,
                'descripcion': asociacion.descripcion,
                'tipo_documento': asociacion.tipo_documento,
                'numero_documento': asociacion.numero_documento
            }
            
            return jsonify({'success': True, 'asociacion': data})
        except Exception as e:
            return jsonify({'success': False, 'error': str(e)}), 500
    
    @app.route('/api/asociaciones/<int:asociacion_id>', methods=['PUT'])
    def update_asociacion(asociacion_id):
        """Actualizar asociación específica"""
        try:
            from models import Asociacion
            from app import db
            
            asociacion = Asociacion.query.get_or_404(asociacion_id)
            update_data = request.get_json()
            
            # Actualizar campos básicos
            if 'nombre_asociacion' in update_data:
                asociacion.nombre_asociacion = update_data['nombre_asociacion']
            if 'acronimo' in update_data:
                asociacion.acronimo = update_data['acronimo']
            if 'pais' in update_data:
                asociacion.pais = update_data['pais']
            if 'ciudad' in update_data:
                asociacion.ciudad = update_data['ciudad']
            if 'direccion' in update_data:
                asociacion.direccion = update_data['direccion']
            if 'telefono' in update_data:
                asociacion.telefono = update_data['telefono']
            if 'email' in update_data:
                asociacion.email = update_data['email']
            if 'sitio_web' in update_data:
                asociacion.sitio_web = update_data['sitio_web']
            if 'contacto_nombre' in update_data:
                asociacion.contacto_nombre = update_data['contacto_nombre']
            if 'contacto_cargo' in update_data:
                asociacion.contacto_cargo = update_data['contacto_cargo']
            if 'estado' in update_data:
                asociacion.estado = update_data['estado']
            if 'años_funcionamiento' in update_data:
                try:
                    asociacion.años_funcionamiento = int(update_data['años_funcionamiento']) if update_data['años_funcionamiento'] else None
                except:
                    pass
            if 'numero_socios' in update_data:
                try:
                    asociacion.numero_socios = int(update_data['numero_socios']) if update_data['numero_socios'] else None
                except:
                    pass
            if 'descripcion' in update_data:
                asociacion.descripcion = update_data['descripcion']
            
            # Actualizar timestamp
            from datetime import datetime
            asociacion.updated_at = datetime.now()
            
            db.session.commit()
            
            return jsonify({'success': True, 'message': 'Asociación actualizada correctamente'})
        except Exception as e:
            db.session.rollback()
            return jsonify({'success': False, 'error': str(e)}), 500
    
    @app.route('/api/asociaciones/<int:asociacion_id>', methods=['DELETE'])
    def delete_asociacion(asociacion_id):
        """Eliminar asociación"""
        try:
            from models import Asociacion
            from app import db
            
            asociacion = Asociacion.query.get_or_404(asociacion_id)
            db.session.delete(asociacion)
            db.session.commit()
            
            return jsonify({'success': True, 'message': 'Asociación eliminada correctamente'})
        except Exception as e:
            db.session.rollback()
            return jsonify({'success': False, 'error': str(e)}), 500
    
    @app.route('/api/asociaciones/export-csv')
    def export_asociaciones_csv():
        """Exportar asociaciones a CSV"""
        try:
            from models import Asociacion
            from flask import make_response
            import json
            
            asociaciones = Asociacion.query.all()
            
            if not asociaciones:
                return jsonify({'success': False, 'error': 'No hay asociaciones para exportar'})
            
            # Crear CSV
            output = io.StringIO()
            writer = csv.writer(output)
            
            # Escribir encabezados
            writer.writerow([
                'ID', 'Nombre Asociación', 'Acrónimo', 'País', 'Ciudad', 'Teléfono', 
                'Email', 'Sitio Web', 'Contacto', 'Cargo', 'Estado', 'Años Funcionamiento',
                'Número Socios', 'Neurodivergencias', 'Servicios', 'Descripción'
            ])
            
            # Escribir datos
            for asoc in asociaciones:
                try:
                    neurodivergencias = json.loads(asoc.neurodivergencias_atendidas) if asoc.neurodivergencias_atendidas else []
                except:
                    neurodivergencias = []
                
                try:
                    servicios = json.loads(asoc.servicios) if asoc.servicios else []
                except:
                    servicios = []
                
                writer.writerow([
                    asoc.id,
                    asoc.nombre_asociacion,
                    asoc.acronimo or '',
                    asoc.pais,
                    asoc.ciudad,
                    asoc.telefono or '',
                    asoc.email,
                    asoc.sitio_web or '',
                    asoc.contacto_nombre or '',
                    asoc.contacto_cargo or '',
                    asoc.estado,
                    asoc.años_funcionamiento or '',
                    asoc.numero_socios or '',
                    ', '.join(neurodivergencias),
                    ', '.join(servicios),
                    asoc.descripcion or ''
                ])
            
            # Preparar respuesta
            output.seek(0)
            response = make_response(output.getvalue())
            response.headers['Content-Type'] = 'text/csv'
            response.headers['Content-Disposition'] = f'attachment; filename=diversia_asociaciones_{datetime.now().strftime("%Y%m%d")}.csv'
            
            return response
            
        except Exception as e:
            return jsonify({'success': False, 'error': str(e)}), 500

    # ==================== FUNCIONALIDAD DE EDICIÓN ====================
    
    @app.route('/api/usuario/<user_id>/editar', methods=['GET', 'POST'])
    def editar_usuario(user_id):
        """Editar un usuario específico (User o NeurodivergentProfile)"""
        try:
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
                'nombre': usuario.nombre,
                'apellidos': usuario.apellidos,
                'email': usuario.email,
                'telefono': usuario.telefono,
                'ciudad': usuario.ciudad,
                'fecha_nacimiento': usuario.fecha_nacimiento.isoformat() if usuario.fecha_nacimiento else None,
                'tipo_neurodivergencia': usuario.tipo_neurodivergencia,
                'diagnostico_formal': usuario.diagnostico_formal,
                'habilidades': usuario.habilidades,
                'experiencia_laboral': usuario.experiencia_laboral,
                'formacion_academica': usuario.formacion_academica,
                'intereses_laborales': usuario.intereses_laborales,
                'adaptaciones_necesarias': usuario.adaptaciones_necesarias,
                'motivaciones': usuario.motivaciones
            }
            
            return jsonify(usuario_data)
            
        except Exception as e:
            print(f"❌ Error editando usuario {user_id}: {e}")
            return jsonify({'success': False, 'error': str(e)}), 500
    
    @app.route('/crm-editar/<user_id>')
    def crm_editar_usuario(user_id):
        """Página de edición de usuario"""
        try:
            # Verificar que es administrador
            if 'admin_ok' not in session or not session.get('admin_ok'):
                flash('Acceso restringido. Inicia sesión como administrador.', 'error')
                return redirect('/admin/login-new')
            
            return render_template('crm-editar-usuario.html', user_id=user_id)
            
        except Exception as e:
            flash('Error cargando editor de usuario.', 'error')
            return redirect('/crm-minimal')
    
    print("CRM Minimal inicializado correctamente")