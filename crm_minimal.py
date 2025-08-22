#!/usr/bin/env python3
"""
CRM Minimal - Sistema simple que funciona sin complicaciones
"""

from flask import jsonify, request, render_template, session, redirect, url_for, flash
import json
import os
from datetime import datetime
from werkzeug.utils import secure_filename
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
        """Dashboard del CRM minimal"""
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
        """Importar CSV"""
        try:
            if 'csv_file' not in request.files:
                return jsonify({'success': False, 'error': 'No se proporcionó archivo'})
            
            file = request.files['csv_file']
            if file.filename == '':
                return jsonify({'success': False, 'error': 'No se seleccionó archivo'})
            
            # Leer CSV
            stream = io.StringIO(file.stream.read().decode("UTF8"), newline=None)
            reader = csv.DictReader(stream)
            
            data = load_data()
            companies = data.get('companies', [])
            
            created = 0
            for row in reader:
                # Generar ID
                new_id = max([c.get('id', 0) for c in companies], default=0) + 1
                
                new_company = {
                    'id': new_id,
                    'nombre': row.get('nombre_empresa', row.get('nombre', '')),
                    'email': row.get('email_contacto', row.get('email', '')),
                    'telefono': row.get('telefono', ''),
                    'sector': row.get('sector', ''),
                    'ciudad': row.get('ciudad', ''),
                    'created_at': datetime.now().isoformat()
                }
                
                companies.append(new_company)
                created += 1
            
            data['companies'] = companies
            save_data(data)
            
            return jsonify({
                'success': True,
                'message': f'Importación completada: {created} empresas creadas',
                'created': created
            })
            
        except Exception as e:
            return jsonify({'success': False, 'error': str(e)}), 500
    
    print("✅ CRM Minimal inicializado correctamente")