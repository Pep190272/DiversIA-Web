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
        if 'admin_user_id' not in session:
            return redirect('/admin/login-new')
        return render_template('crm-minimal.html')
    
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
    
    print("CRM Minimal inicializado correctamente")