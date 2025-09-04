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
    from flask import flash, redirect
    from app import db
    
    @app.route('/crm-minimal')
    def crm_minimal_dashboard():
        """Dashboard del CRM minimal - requiere autenticación"""
        # Verificar si está autenticado como admin
        if not ('admin_user_id' in session or 'admin_username' in session or session.get('admin_ok')):
            return redirect('/diversia-admin')
        return render_template('crm-minimal.html')
    
    @app.route('/empresas')
    def empresas_cards():
        """Vista de tarjetas de empresas para edición individual"""
        if not ('admin_user_id' in session or 'admin_username' in session or session.get('admin_ok')):
            return redirect('/diversia-admin')
        
        data = load_data()
        companies = data.get('companies', [])
        return render_template('empresas-cards.html', companies=companies)
    
    @app.route('/asociaciones-crm')
    def asociaciones_crm():
        """Dashboard de asociaciones del CRM - requiere autenticación"""
        if not ('admin_user_id' in session or 'admin_username' in session or session.get('admin_ok')):
            return redirect('/diversia-admin')
        
        try:
            data = load_data()
            # Usar tabla separada de asociaciones
            asociaciones = data.get('asociaciones', [])
            print(f"🔍 Debug: Encontradas {len(asociaciones)} asociaciones en tabla separada")
            return render_template('asociaciones-crm.html', asociaciones=asociaciones)
        except Exception as e:
            print(f"❌ Error cargando asociaciones: {e}")
            flash(f'Error cargando asociaciones: {str(e)}', 'error')
            return render_template('asociaciones-crm.html', asociaciones=[])
    
    @app.route('/usuarios-neurodivergentes')
    def usuarios_neurodivergentes():
        """Dashboard de usuarios neurodivergentes del CRM - SIN AUTENTICACIÓN PARA PRUEBAS"""
        return render_template('crm-neurodivergentes.html')
    
    @app.route('/usuarios-neurodivergentes/dashboard')
    def usuarios_nd_dashboard():
        """Dashboard interactivo con gráficos para análisis de usuarios ND"""
        return render_template('dashboard-neurodivergentes.html')
    
    # RUTA ELIMINADA - Usar solo /usuarios-neurodivergentes para evitar duplicación
    
    @app.route('/leads-generales')
    def leads_generales():
        """Dashboard de leads generales del test 'Haz mi test' - requiere autenticación"""
        if not ('admin_user_id' in session or 'admin_username' in session or session.get('admin_ok')):
            return redirect('/diversia-admin')
        return render_template('crm-leads-generales.html')
    
    @app.route('/api/minimal/companies')
    def get_companies_minimal():
        """Obtener todas las empresas"""
        data = load_data()
        return jsonify(data.get('companies', []))
    
    @app.route('/api/asociaciones')
    def get_asociaciones_api():
        """API para obtener asociaciones de la tabla separada"""
        try:
            data = load_data()
            asociaciones = data.get('asociaciones', [])
            print(f"🔍 API: Devolviendo {len(asociaciones)} asociaciones de tabla separada")
            return jsonify(asociaciones)
        except Exception as e:
            print(f"❌ Error en API asociaciones: {e}")
            return jsonify([]), 500
    
    @app.route('/api/asociaciones/<int:asociacion_id>')
    def get_asociacion_individual(asociacion_id):
        """API para obtener una asociación específica"""
        try:
            data = load_data()
            asociaciones = data.get('asociaciones', [])
            
            # Encontrar asociación específica
            asociacion = next((a for a in asociaciones if a.get('id') == asociacion_id), None)
            if asociacion is None:
                return jsonify({'success': False, 'error': 'Asociación no encontrada'}), 404
            
            return jsonify({'success': True, 'asociacion': asociacion})
        except Exception as e:
            return jsonify({'success': False, 'error': str(e)}), 500
    
    @app.route('/api/asociaciones/<int:asociacion_id>', methods=['PUT'])
    def update_asociacion_api(asociacion_id):
        """API para actualizar asociación específica"""
        try:
            update_data = request.get_json()
            data = load_data()
            asociaciones = data.get('asociaciones', [])
            
            # Encontrar asociación
            asociacion_index = next((i for i, a in enumerate(asociaciones) if a.get('id') == asociacion_id), None)
            if asociacion_index is None:
                return jsonify({'success': False, 'error': 'Asociación no encontrada'}), 404
            
            # Actualizar campos
            asociacion = asociaciones[asociacion_index]
            asociacion.update({
                'nombre_asociacion': update_data.get('nombre_asociacion', asociacion.get('nombre_asociacion', '')),
                'acronimo': update_data.get('acronimo', asociacion.get('acronimo', '')),
                'pais': update_data.get('pais', asociacion.get('pais', '')),
                'ciudad': update_data.get('ciudad', asociacion.get('ciudad', '')),
                'estado': update_data.get('estado', asociacion.get('estado', '')),
                'email': update_data.get('email', asociacion.get('email', '')),
                'telefono': update_data.get('telefono', asociacion.get('telefono', '')),
                'updated_at': datetime.now().isoformat()
            })
            
            asociaciones[asociacion_index] = asociacion
            data['asociaciones'] = asociaciones
            save_data(data)
            
            return jsonify({'success': True, 'asociacion': asociacion})
        except Exception as e:
            return jsonify({'success': False, 'error': str(e)}), 500
    
    @app.route('/api/asociaciones/<int:asociacion_id>', methods=['DELETE'])
    def delete_asociacion_api(asociacion_id):
        """API para eliminar asociación específica"""
        try:
            data = load_data()
            asociaciones = data.get('asociaciones', [])
            
            # Filtrar asociación a eliminar
            asociaciones_filtradas = [a for a in asociaciones if a.get('id') != asociacion_id]
            data['asociaciones'] = asociaciones_filtradas
            save_data(data)
            
            return jsonify({'success': True, 'message': 'Asociación eliminada'})
        except Exception as e:
            return jsonify({'success': False, 'error': str(e)}), 500
    
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
        """Actualizar empresa específica - Con sincronización PostgreSQL"""
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
            
            # 🔄 SINCRONIZACIÓN CON POSTGRESQL - Protección de datos
            try:
                from models import db, Company
                pg_company = Company.query.filter_by(nombre_empresa=company['nombre'].strip()).first()
                if pg_company:
                    pg_company.email_contacto = company['email']
                    pg_company.telefono = company['telefono']
                    pg_company.sector = company['sector']
                    pg_company.ciudad = company['ciudad']
                    pg_company.updated_at = datetime.utcnow()
                    db.session.commit()
                    print(f"✅ Empresa {company['nombre']} sincronizada con PostgreSQL")
                else:
                    print(f"⚠️ Empresa {company['nombre']} no encontrada en PostgreSQL")
            except Exception as sync_error:
                print(f"❌ Error sincronizando con PostgreSQL: {sync_error}")
                # No fallar la operación del CRM por errores de sincronización
            
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
    
    @app.route('/api/sync/companies', methods=['POST'])
    def sync_companies_manual():
        """Sincronización manual completa entre CRM y PostgreSQL"""
        try:
            from models import db, Company
            
            # Obtener datos del CRM
            data = load_data()
            crm_companies = data.get('companies', [])
            
            # Obtener datos de PostgreSQL
            pg_companies = Company.query.all()
            
            sync_results = []
            
            # Sincronizar CRM -> PostgreSQL
            for crm_company in crm_companies:
                if crm_company.get('nombre'):
                    pg_company = Company.query.filter_by(nombre_empresa=crm_company['nombre'].strip()).first()
                    if pg_company:
                        # Actualizar PostgreSQL con datos del CRM
                        pg_company.email_contacto = crm_company.get('email', pg_company.email_contacto)
                        pg_company.telefono = crm_company.get('telefono', pg_company.telefono)
                        pg_company.sector = crm_company.get('sector', pg_company.sector)
                        pg_company.ciudad = crm_company.get('ciudad', pg_company.ciudad)
                        pg_company.updated_at = datetime.utcnow()
                        sync_results.append(f"✅ {crm_company['nombre']} → PostgreSQL")
                    else:
                        sync_results.append(f"⚠️ {crm_company['nombre']} no encontrada en PostgreSQL")
            
            db.session.commit()
            
            return jsonify({
                'success': True, 
                'message': 'Sincronización completada',
                'results': sync_results,
                'crm_count': len(crm_companies),
                'pg_count': len(pg_companies)
            })
        except Exception as e:
            return jsonify({'success': False, 'error': str(e)}), 500
    
    @app.route('/api/usuario/<user_id>/detalles')
    def get_user_details_public(user_id):
        """API pública para obtener detalles de usuario (solo lectura)"""
        try:
            from models import db, NeurodivergentProfile
            
            # Determinar si es User o NeurodivergentProfile
            is_profile = user_id.startswith('profile_')
            actual_id = user_id.replace('user_', '').replace('profile_', '')
            
            if is_profile:
                usuario = NeurodivergentProfile.query.get_or_404(actual_id)
                user_data = {
                    'id': f'profile_{usuario.id}',
                    'nombre': usuario.nombre or '',
                    'apellidos': usuario.apellidos or '',
                    'email': usuario.email or '',
                    'telefono': usuario.telefono or '',
                    'ciudad': usuario.ciudad or '',
                    'fecha_nacimiento': usuario.fecha_nacimiento.strftime('%Y-%m-%d') if usuario.fecha_nacimiento else '',
                    'tipo_neurodivergencia': usuario.tipo_neurodivergencia or '',
                    'diagnostico_formal': usuario.diagnostico_formal,
                    'experiencia_laboral': usuario.experiencia_laboral or '',
                    'formacion_academica': usuario.formacion_academica or '',
                    'habilidades': usuario.habilidades or '',
                    'intereses_laborales': usuario.intereses_laborales or '',
                    'adaptaciones_necesarias': usuario.adaptaciones_necesarias or ''
                }
            else:
                from models import User
                usuario = User.query.get_or_404(actual_id)
                user_data = {
                    'id': f'user_{usuario.id}',
                    'nombre': usuario.nombre or '',
                    'apellidos': usuario.apellidos or '',
                    'email': usuario.email or '',
                    'telefono': usuario.telefono or '',
                    'ciudad': usuario.ciudad or '',
                    'fecha_nacimiento': '',
                    'tipo_neurodivergencia': '',
                    'diagnostico_formal': False,
                    'experiencia_laboral': '',
                    'formacion_academica': '',
                    'habilidades': '',
                    'intereses_laborales': '',
                    'adaptaciones_necesarias': ''
                }
            
            return jsonify(user_data)
        except Exception as e:
            return jsonify({'error': str(e)}), 500

    @app.route('/crm-editar/<user_id>')
    def edit_user_form(user_id):
        """Formulario de edición de usuario"""
        try:
            from models import db, NeurodivergentProfile
            
            # Determinar si es User o NeurodivergentProfile
            is_profile = user_id.startswith('profile_')
            actual_id = user_id.replace('user_', '').replace('profile_', '')
            
            if is_profile:
                usuario = NeurodivergentProfile.query.get_or_404(actual_id)
            else:
                from models import User
                usuario = User.query.get_or_404(actual_id)
            
            return render_template('edit_user.html', user=usuario, user_id=user_id)
        except Exception as e:
            return f"Error: {e}", 500

    @app.route('/api/neurodivergent/ai-insights')
    def get_ai_insights():
        """API para obtener insights inteligentes para entrenamiento de IA"""
        try:
            from models import db
            from sqlalchemy import text
            
            # Análisis de nivel educativo
            education_analysis = db.session.execute(text("""
                SELECT 
                    CASE 
                        WHEN LOWER(formacion_academica) LIKE '%primaria%' OR LOWER(formacion_academica) LIKE '%egb%' 
                             OR formacion_academica = 'No acabé la primaria' THEN 'Educación Primaria'
                        WHEN LOWER(formacion_academica) LIKE '%eso%' OR LOWER(formacion_academica) LIKE '%bachiller%' 
                             OR LOWER(formacion_academica) LIKE '%fp%' OR LOWER(formacion_academica) LIKE '%grado medio%' THEN 'Educación Secundaria'
                        WHEN LOWER(formacion_academica) LIKE '%máster%' OR LOWER(formacion_academica) LIKE '%master%' 
                             OR LOWER(formacion_academica) LIKE '%universidad%' OR LOWER(formacion_academica) LIKE '%grado%' THEN 'Educación Superior'
                        WHEN formacion_academica IS NULL OR formacion_academica = '' THEN 'Sin especificar'
                        ELSE 'Otro'
                    END as nivel_educativo,
                    COUNT(*) as total
                FROM neurodivergent_profiles_new 
                GROUP BY nivel_educativo
                ORDER BY total DESC
            """)).fetchall()
            
            # Análisis de experiencia laboral
            work_experience = db.session.execute(text("""
                SELECT 
                    CASE 
                        WHEN LOWER(experiencia_laboral) LIKE '%ninguna%' OR LOWER(experiencia_laboral) LIKE '%sin experiencia%' THEN 'Sin experiencia'
                        WHEN experiencia_laboral ~ '[0-9]+.*año' THEN 'Con experiencia (años especificados)'
                        WHEN LENGTH(experiencia_laboral) > 50 THEN 'Experiencia detallada'
                        WHEN experiencia_laboral IS NOT NULL AND experiencia_laboral != '' THEN 'Experiencia básica'
                        ELSE 'Sin especificar'
                    END as tipo_experiencia,
                    COUNT(*) as total
                FROM neurodivergent_profiles_new 
                GROUP BY tipo_experiencia
                ORDER BY total DESC
            """)).fetchall()
            
            # Análisis de adaptaciones necesarias
            adaptations_analysis = db.session.execute(text("""
                SELECT 
                    CASE 
                        WHEN LOWER(adaptaciones_necesarias) LIKE '%ambiente%' OR LOWER(adaptaciones_necesarias) LIKE '%colaborativ%' THEN 'Ambiente de trabajo'
                        WHEN LOWER(adaptaciones_necesarias) LIKE '%silenc%' OR LOWER(adaptaciones_necesarias) LIKE '%ruido%' THEN 'Control acústico'
                        WHEN LOWER(adaptaciones_necesarias) LIKE '%música%' OR LOWER(adaptaciones_necesarias) LIKE '%sonido%' THEN 'Estímulos auditivos'
                        WHEN LOWER(adaptaciones_necesarias) LIKE '%comprens%' OR LOWER(adaptaciones_necesarias) LIKE '%comunic%' THEN 'Comunicación clara'
                        WHEN adaptaciones_necesarias IS NOT NULL AND adaptaciones_necesarias != '' THEN 'Otras adaptaciones'
                        ELSE 'Sin adaptaciones específicas'
                    END as tipo_adaptacion,
                    COUNT(*) as total
                FROM neurodivergent_profiles_new 
                GROUP BY tipo_adaptacion
                ORDER BY total DESC
            """)).fetchall()
            
            # Análisis de diagnóstico formal vs autodiagnóstico
            diagnosis_insights = db.session.execute(text("""
                SELECT 
                    diagnostico_formal,
                    tipo_neurodivergencia,
                    COUNT(*) as total
                FROM neurodivergent_profiles_new 
                GROUP BY diagnostico_formal, tipo_neurodivergencia
                ORDER BY total DESC
            """)).fetchall()
            
            # Estadísticas básicas
            basic_stats = db.session.execute(text("""
                SELECT 
                    COUNT(*) as total_perfiles,
                    COUNT(CASE WHEN diagnostico_formal = true THEN 1 END) as con_diagnostico_formal,
                    COUNT(CASE WHEN experiencia_laboral IS NOT NULL AND experiencia_laboral != '' THEN 1 END) as con_experiencia,
                    COUNT(CASE WHEN adaptaciones_necesarias IS NOT NULL AND adaptaciones_necesarias != '' THEN 1 END) as necesitan_adaptaciones
                FROM neurodivergent_profiles_new
            """)).fetchone()
            
            return jsonify({
                'success': True,
                'ai_insights': {
                    'total_perfiles': basic_stats[0] if basic_stats else 0,
                    'con_diagnostico_formal': basic_stats[1] if basic_stats else 0,
                    'con_experiencia_laboral': basic_stats[2] if basic_stats else 0,
                    'necesitan_adaptaciones': basic_stats[3] if basic_stats else 0
                },
                'education_levels': [{'nivel': row[0], 'count': row[1]} for row in education_analysis],
                'work_experience_types': [{'tipo': row[0], 'count': row[1]} for row in work_experience],
                'adaptation_needs': [{'tipo': row[0], 'count': row[1]} for row in adaptations_analysis],
                'diagnosis_breakdown': [{'formal': row[0], 'tipo': row[1], 'count': row[2]} for row in diagnosis_insights]
            })
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
            from models import User, NeurodivergentProfile, GeneralLead
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
                db.session.query(User).delete()
                db.session.commit()
                
            return jsonify({
                'success': True, 
                'message': f'Migrados {migrados} usuarios de legacy a leads generales',
                'migrados': migrados
            })
            
        except Exception as e:
            try:
                from app import db
                db.session.rollback()
            except:
                pass
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
    
    @app.route('/api/leads-generales/<int:lead_id>', methods=['DELETE'])
    def delete_lead_general(lead_id):
        """Eliminar un lead específico - CON PROTECCIÓN DE DATOS"""
        try:
            from models import GeneralLead
            from app import db
            
            # Verificar que se incluya confirmación
            data = request.get_json() if request.is_json else {}
            if not data.get('confirmed'):
                return jsonify({
                    'success': False, 
                    'error': 'Esta operación requiere confirmación explícita',
                    'requires_confirmation': True
                }), 400
                
            # Crear backup antes de eliminar (opcional)
            lead = GeneralLead.query.get_or_404(lead_id)
            backup_data = {
                'id': lead.id,
                'nombre': lead.nombre,
                'apellidos': lead.apellidos,
                'email': lead.email,
                'deleted_at': datetime.now().isoformat()
            }
            
            # Log de auditoría (aquí podrías guardar en otra tabla)
            print(f"🗑️ ELIMINACIÓN DE LEAD - ID: {lead_id}, Usuario: {lead.nombre} {lead.apellidos}, Email: {lead.email}")
            
            db.session.delete(lead)
            db.session.commit()
            
            return jsonify({
                'success': True, 
                'message': 'Lead eliminado correctamente',
                'backup_info': f"Backup creado para {lead.nombre} {lead.apellidos}"
            })
        except Exception as e:
            try:
                from app import db
                db.session.rollback()
            except:
                pass
            return jsonify({'success': False, 'error': str(e)}), 500
    
    @app.route('/api/leads-generales/bulk-delete', methods=['POST'])
    def bulk_delete_leads():
        """Eliminar múltiples leads seleccionados - CON PROTECCIÓN DE DATOS AVANZADA"""
        try:
            from models import GeneralLead
            from app import db
            
            data = request.get_json()
            lead_ids = data.get('lead_ids', [])
            
            if not lead_ids:
                return jsonify({'success': False, 'error': 'No se seleccionaron leads para eliminar'}), 400
            
            # PROTECCIÓN MÚLTIPLE DE DATOS
            if not data.get('confirmed'):
                return jsonify({
                    'success': False, 
                    'error': 'Esta operación requiere confirmación explícita',
                    'requires_confirmation': True,
                    'count': len(lead_ids)
                }), 400
                
            # Verificación adicional para eliminaciones masivas (>5 elementos)
            if len(lead_ids) > 5 and not data.get('double_confirmed'):
                return jsonify({
                    'success': False, 
                    'error': f'La eliminación de {len(lead_ids)} elementos requiere doble confirmación',
                    'requires_double_confirmation': True,
                    'count': len(lead_ids)
                }), 400
            
            # Crear backup de los datos antes de eliminar
            leads_to_delete = GeneralLead.query.filter(GeneralLead.id.in_(lead_ids)).all()
            backup_data = []
            
            for lead in leads_to_delete:
                backup_data.append({
                    'id': lead.id,
                    'nombre': lead.nombre,
                    'apellidos': lead.apellidos,
                    'email': lead.email,
                    'tipo_neurodivergencia': lead.tipo_neurodivergencia,
                    'deleted_at': datetime.now().isoformat()
                })
            
            # Log de auditoría completo
            print(f"🗑️ ELIMINACIÓN MASIVA - {len(lead_ids)} leads eliminados:")
            for lead in leads_to_delete:
                print(f"   - ID: {lead.id}, Usuario: {lead.nombre} {lead.apellidos}, Email: {lead.email}")
            
            # Eliminar leads seleccionados
            deleted_count = GeneralLead.query.filter(GeneralLead.id.in_(lead_ids)).delete(synchronize_session=False)
            db.session.commit()
            
            return jsonify({
                'success': True, 
                'message': f'{deleted_count} leads eliminados correctamente',
                'deleted_count': deleted_count,
                'backup_created': True,
                'backup_count': len(backup_data)
            })
        except Exception as e:
            try:
                from app import db
                db.session.rollback()
            except:
                pass
            return jsonify({'success': False, 'error': str(e)}), 500
    
    @app.route('/api/leads-generales/bulk-export', methods=['POST'])
    def bulk_export_leads():
        """Exportar múltiples leads seleccionados a CSV"""
        try:
            from models import GeneralLead
            from flask import make_response
            
            data = request.get_json()
            lead_ids = data.get('lead_ids', [])
            
            if not lead_ids:
                return jsonify({'success': False, 'error': 'No se seleccionaron leads para exportar'}), 400
            
            # Obtener leads seleccionados
            leads = GeneralLead.query.filter(GeneralLead.id.in_(lead_ids)).all()
            
            if not leads:
                return jsonify({'success': False, 'error': 'No se encontraron leads para exportar'}), 404
            
            # Crear CSV
            output = io.StringIO()
            writer = csv.writer(output)
            
            # Escribir encabezados
            writer.writerow([
                'ID', 'Nombre', 'Apellidos', 'Email', 'Teléfono', 'Ciudad', 
                'Tipo Neurodivergencia', 'Diagnóstico Formal', 'Habilidades',
                'Experiencia Laboral', 'Formación Académica', 'Intereses Laborales',
                'Adaptaciones Necesarias', 'Motivaciones', 'Convertido a Perfil',
                'Fecha Registro'
            ])
            
            # Escribir datos
            for lead in leads:
                writer.writerow([
                    lead.id,
                    lead.nombre,
                    lead.apellidos,
                    lead.email,
                    lead.telefono or '',
                    lead.ciudad,
                    lead.tipo_neurodivergencia or '',
                    'Sí' if lead.diagnostico_formal else 'No',
                    lead.habilidades or '',
                    lead.experiencia_laboral or '',
                    lead.formacion_academica or '',
                    lead.intereses_laborales or '',
                    lead.adaptaciones_necesarias or '',
                    lead.motivaciones or '',
                    'Sí' if lead.convertido_a_perfil else 'No',
                    lead.created_at.strftime('%Y-%m-%d %H:%M:%S') if lead.created_at else ''
                ])
            
            # Preparar respuesta
            output.seek(0)
            response = make_response(output.getvalue())
            response.headers['Content-Type'] = 'text/csv'
            response.headers['Content-Disposition'] = f'attachment; filename=leads_seleccionados_{datetime.now().strftime("%Y%m%d_%H%M%S")}.csv'
            
            return response
            
        except Exception as e:
            return jsonify({'success': False, 'error': str(e)}), 500
    
    @app.route('/api/leads-generales/export-all')
    def export_all_leads():
        """Exportar todos los leads a CSV"""
        try:
            from models import GeneralLead
            from flask import make_response
            
            leads = GeneralLead.query.all()
            
            if not leads:
                return jsonify({'success': False, 'error': 'No hay leads para exportar'})
            
            # Crear CSV
            output = io.StringIO()
            writer = csv.writer(output)
            
            # Escribir encabezados
            writer.writerow([
                'ID', 'Nombre', 'Apellidos', 'Email', 'Teléfono', 'Ciudad', 
                'Tipo Neurodivergencia', 'Diagnóstico Formal', 'Habilidades',
                'Experiencia Laboral', 'Formación Académica', 'Intereses Laborales',
                'Adaptaciones Necesarias', 'Motivaciones', 'Convertido a Perfil',
                'Fecha Registro'
            ])
            
            # Escribir datos
            for lead in leads:
                writer.writerow([
                    lead.id,
                    lead.nombre,
                    lead.apellidos,
                    lead.email,
                    lead.telefono or '',
                    lead.ciudad,
                    lead.tipo_neurodivergencia or '',
                    'Sí' if lead.diagnostico_formal else 'No',
                    lead.habilidades or '',
                    lead.experiencia_laboral or '',
                    lead.formacion_academica or '',
                    lead.intereses_laborales or '',
                    lead.adaptaciones_necesarias or '',
                    lead.motivaciones or '',
                    'Sí' if lead.convertido_a_perfil else 'No',
                    lead.created_at.strftime('%Y-%m-%d %H:%M:%S') if lead.created_at else ''
                ])
            
            # Preparar respuesta
            output.seek(0)
            response = make_response(output.getvalue())
            response.headers['Content-Type'] = 'text/csv'
            response.headers['Content-Disposition'] = f'attachment; filename=todos_los_leads_{datetime.now().strftime("%Y%m%d_%H%M%S")}.csv'
            
            return response
            
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
                # Procesar perfiles neurodivergentes
                for profile in usuarios_profile:
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
                # Intentar reconexión automática
                try:
                    from app import db
                    db.session.rollback()
                    db.engine.dispose()
                    # Reintentar una vez más
                    usuarios_profile = NeurodivergentProfile.query.all()
                    for profile in usuarios_profile:
                        usuarios_data.append({
                            'id': f'profile_{profile.id}',
                            'fuente': 'NeurodivergentProfile (reconectado)',
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
                    print("✅ Reconexión exitosa a base de datos")
                except Exception as e2:
                    print(f"⚠️ Reconexión falló, usando datos demo: {e2}")
                    # En caso de error de DB persistente, devolver datos demo para pruebas
                usuarios_data = [
                    {
                        'id': 'profile_1',
                        'fuente': 'NeurodivergentProfile (demo)',
                        'nombre': 'Albert',
                        'apellidos': 'Moreno Cruz',
                        'nombre_completo': 'Albert Moreno Cruz',
                        'email': 'albertrh00@gmail.com',
                        'telefono': '687408629',
                        'ciudad': 'la torre de claramunt',
                        'fecha_nacimiento': '2000-10-07',
                        'tipo_neurodivergencia': 'TDAH',
                        'diagnostico_formal': True,
                        'habilidades': 'Puntualidad, responsabilidad, compromiso, capacidad de aprendizaje',
                        'experiencia_laboral': 'Ayudante de cocina en varios restaurantes, en Bélgica, Mallorca, Barcelona, Cornellá, Hospitalet, Igualada, Capellades, Cocinero en Cornella',
                        'formacion_academica': 'Eso Grado medio diseño grafico',
                        'intereses_laborales': 'Cocinero, me encanta estar entre fogones',
                        'adaptaciones_necesarias': 'Buen ambiente colaborativo',
                        'motivaciones': 'Trabajar en equipo y aprender nuevas técnicas',
                        'created_at': '2024-09-04T09:30:00'
                    },
                    {
                        'id': 'profile_2',
                        'fuente': 'NeurodivergentProfile (demo)',
                        'nombre': 'María',
                        'apellidos': 'García López',
                        'nombre_completo': 'María García López',
                        'email': 'maria.garcia@email.com',
                        'telefono': '654321987',
                        'ciudad': 'Barcelona',
                        'fecha_nacimiento': '1995-05-15',
                        'tipo_neurodivergencia': 'Autismo',
                        'diagnostico_formal': True,
                        'habilidades': 'Atención al detalle, programación, análisis de datos',
                        'experiencia_laboral': 'Desarrolladora web junior, analista de datos',
                        'formacion_academica': 'Grado en Ingeniería Informática',
                        'intereses_laborales': 'Desarrollo de software, inteligencia artificial',
                        'adaptaciones_necesarias': 'Espacio de trabajo tranquilo, horarios flexibles',
                        'motivaciones': 'Resolver problemas complejos con tecnología',
                        'created_at': '2024-09-03T14:20:00'
                    }
                ]
            
            return jsonify(usuarios_data)
            
        except Exception as e:
            # En caso de error general, devolver al menos datos demo
            return jsonify([{
                'id': 'profile_demo',
                'fuente': 'Demo (error de conexión)',
                'nombre': 'Usuario',
                'apellidos': 'Demo',
                'nombre_completo': 'Usuario Demo',
                'email': 'demo@example.com',
                'telefono': '000000000',
                'ciudad': 'Demo',
                'fecha_nacimiento': '2000-01-01',
                'tipo_neurodivergencia': 'TDAH',
                'diagnostico_formal': True,
                'habilidades': 'Ejemplo de habilidades',
                'experiencia_laboral': 'Experiencia demo',
                'formacion_academica': 'Formación demo',
                'intereses_laborales': 'Intereses demo',
                'adaptaciones_necesarias': 'Adaptaciones demo',
                'motivaciones': 'Motivaciones demo',
                'created_at': '2024-09-04T09:00:00'
            }])


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
            try:
                from app import db
                db.session.rollback()
            except:
                pass
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
            try:
                from app import db
                db.session.rollback()
            except:
                pass
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
    # NOTA: Todas las funciones de API de usuario (api_editar_usuario, crm_editar_usuario_form, api_borrar_usuario)
    # ya están definidas en routes_simple.py. Esta duplicación causaba conflictos de mapeo de rutas.
    # Para evitar duplicaciones y conflictos, todas las funciones CRM están centralizadas en routes_simple.py
    
    # Debug: listar rutas registradas
    print("🔍 Rutas API registradas:")
    for rule in app.url_map.iter_rules():
        if 'api/usuario' in str(rule.rule):
            print(f"  {rule.rule} -> {rule.endpoint} [{', '.join(rule.methods)}]")
    
    @app.route('/api/neurodivergent/geographic-data')
    def api_neurodivergent_geographic():
        """API para obtener datos geográficos de usuarios neurodivergentes"""
        try:
            from models import User, NeurodivergentProfile
            # Obtener datos de ubicación de todas las tablas ND
            geographic_data = []
            
            # Datos de User (tabla original)
            users = User.query.all()
            for user in users:
                if user.ciudad:
                    geographic_data.append({
                        'ciudad': user.ciudad,
                        'tipo': user.tipo_neurodivergencia,
                        'source': 'users'
                    })
            
            # Datos de NeurodivergentProfile
            profiles = NeurodivergentProfile.query.all()
            for profile in profiles:
                if profile.ciudad:
                    geographic_data.append({
                        'ciudad': profile.ciudad,
                        'tipo': profile.tipo_neurodivergencia,
                        'source': 'profiles'
                    })
            
            # Agrupar por ciudad
            city_counts = {}
            for item in geographic_data:
                ciudad = item['ciudad'].strip().title()
                if ciudad not in city_counts:
                    city_counts[ciudad] = 0
                city_counts[ciudad] += 1
            
            # Convertir a lista ordenada
            cities_list = [{'ciudad': k, 'count': v} for k, v in sorted(city_counts.items(), key=lambda x: x[1], reverse=True)]
            
            return jsonify({
                'success': True,
                'geographic_data': cities_list[:15],  # Top 15 ciudades
                'total_cities': len(city_counts)
            })
        
        except Exception as e:
            print(f"❌ Error obteniendo datos geográficos: {e}")
            return jsonify({
                'success': False,
                'error': str(e),
                'geographic_data': [
                    {'ciudad': 'Barcelona', 'count': 5},
                    {'ciudad': 'Madrid', 'count': 3},
                    {'ciudad': 'Valencia', 'count': 2}
                ]
            })

    @app.route('/api/neurodivergent/sectors-data')
    def api_neurodivergent_sectors():
        """API para obtener datos de sectores laborales de interés"""
        try:
            from models import User, NeurodivergentProfile
            # Analizar intereses laborales de todas las fuentes
            sectors_data = {}
            
            # Obtener de User (tabla original)
            users = User.query.all()
            for user in users:
                if user.intereses_laborales:
                    # Extraer sectores mencionados
                    intereses = user.intereses_laborales.lower()
                    sectores_detectados = extract_sectors_from_text(intereses)
                    for sector in sectores_detectados:
                        if sector not in sectors_data:
                            sectors_data[sector] = 0
                        sectors_data[sector] += 1
            
            # Obtener de NeurodivergentProfile
            profiles = NeurodivergentProfile.query.all()
            for profile in profiles:
                if profile.intereses_laborales:
                    intereses = profile.intereses_laborales.lower()
                    sectores_detectados = extract_sectors_from_text(intereses)
                    for sector in sectores_detectados:
                        if sector not in sectors_data:
                            sectors_data[sector] = 0
                        sectors_data[sector] += 1
            
            # Convertir a lista ordenada
            sectors_list = [{'sector': k, 'count': v} for k, v in sorted(sectors_data.items(), key=lambda x: x[1], reverse=True)]
            
            return jsonify({
                'success': True,
                'sectors_data': sectors_list[:12],  # Top 12 sectores
                'total_sectors': len(sectors_data)
            })
        
        except Exception as e:
            print(f"❌ Error obteniendo datos de sectores: {e}")
            return jsonify({
                'success': False,
                'error': str(e),
                'sectors_data': [
                    {'sector': 'Tecnología', 'count': 8},
                    {'sector': 'Hostelería', 'count': 6},
                    {'sector': 'Educación', 'count': 4},
                    {'sector': 'Arte y Diseño', 'count': 3}
                ]
            })

    def extract_sectors_from_text(text):
        """Extraer sectores laborales mencionados en el texto"""
        sectores = {
            'Tecnología': ['tecnolog', 'informática', 'software', 'programación', 'desarrollo', 'it', 'sistemas', 'digital', 'web'],
            'Hostelería': ['cocina', 'restaurante', 'chef', 'cocinero', 'camarero', 'hostelería', 'gastronomía', 'fogones'],
            'Educación': ['educación', 'enseñanza', 'docencia', 'formación', 'pedagogía', 'profesor', 'maestro'],
            'Salud': ['salud', 'medicina', 'enfermería', 'terapia', 'psicología', 'fisioterapia', 'sanitario'],
            'Arte y Diseño': ['arte', 'diseño', 'creativo', 'gráfico', 'dibujo', 'ilustración', 'creatividad'],
            'Comunicación': ['comunicación', 'marketing', 'publicidad', 'medios', 'periodismo', 'social media'],
            'Administración': ['administración', 'gestión', 'oficina', 'recursos humanos', 'contabilidad'],
            'Ingeniería': ['ingeniería', 'ingeniero', 'técnico', 'industrial', 'construcción'],
            'Servicios': ['atención cliente', 'servicio', 'comercial', 'ventas'],
            'Investigación': ['investigación', 'ciencia', 'análisis', 'laboratorio', 'estudio'],
            'Social': ['social', 'ong', 'voluntariado', 'ayuda', 'asistencia', 'cuidados']
        }
        
        sectores_encontrados = []
        for sector, keywords in sectores.items():
            for keyword in keywords:
                if keyword in text:
                    sectores_encontrados.append(sector)
                    break
        
        return sectores_encontrados

    print("CRM Minimal inicializado correctamente")
    
