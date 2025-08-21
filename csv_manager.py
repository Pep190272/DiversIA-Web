#!/usr/bin/env python3
"""
Gestor CSV para importar/exportar datos de DiversIA
Maneja empresas, contactos, asociaciones y ofertas
"""

import csv
import sqlite3
import json
import os
from datetime import datetime
from io import StringIO
from flask import Response

class CSVManager:
    """Gestor de CSV para importar y exportar datos"""
    
    def __init__(self, db_path='diversia.db'):
        self.db_path = db_path
    
    def export_companies_csv(self):
        """Exportar empresas a CSV"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
        SELECT id, nombre_empresa, email_contacto, telefono, sector, 
               tamano_empresa, ciudad, sitio_web, descripcion_empresa, 
               created_at
        FROM companies ORDER BY created_at DESC
        ''')
        
        companies = cursor.fetchall()
        conn.close()
        
        output = StringIO()
        writer = csv.writer(output)
        
        # Headers
        writer.writerow([
            'ID', 'Nombre Empresa', 'Email', 'Teléfono', 'Sector',
            'Tamaño', 'Ciudad', 'Sitio Web', 'Descripción', 'Fecha Registro'
        ])
        
        # Data
        for company in companies:
            writer.writerow(company)
        
        output.seek(0)
        return output.getvalue()
    
    def export_job_offers_csv(self):
        """Exportar ofertas de trabajo a CSV"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
        SELECT jo.id, c.nombre_empresa, jo.titulo_puesto, jo.descripcion,
               jo.tipo_contrato, jo.modalidad_trabajo, jo.salario_min, 
               jo.salario_max, jo.requisitos, jo.adaptaciones_disponibles,
               jo.neurodivergencias_target, jo.activa, jo.created_at
        FROM job_offers jo
        JOIN companies c ON jo.company_id = c.id
        ORDER BY jo.created_at DESC
        ''')
        
        offers = cursor.fetchall()
        conn.close()
        
        output = StringIO()
        writer = csv.writer(output)
        
        # Headers
        writer.writerow([
            'ID', 'Empresa', 'Título Puesto', 'Descripción', 'Tipo Contrato',
            'Modalidad', 'Salario Mín', 'Salario Máx', 'Requisitos', 
            'Adaptaciones', 'Neurodivergencias', 'Activa', 'Fecha Creación'
        ])
        
        # Data
        for offer in offers:
            writer.writerow(offer)
        
        output.seek(0)
        return output.getvalue()
    
    def import_companies_csv(self, csv_content):
        """Importar empresas desde CSV"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        reader = csv.DictReader(StringIO(csv_content))
        imported_count = 0
        
        for row in reader:
            try:
                cursor.execute('''
                INSERT INTO companies (
                    nombre_empresa, email_contacto, telefono, sector,
                    tamano_empresa, ciudad, sitio_web, descripcion_empresa
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                ''', (
                    row.get('Nombre Empresa'),
                    row.get('Email'),
                    row.get('Teléfono'),
                    row.get('Sector'),
                    row.get('Tamaño'),
                    row.get('Ciudad'),
                    row.get('Sitio Web'),
                    row.get('Descripción')
                ))
                imported_count += 1
            except Exception as e:
                print(f"Error importando empresa {row.get('Nombre Empresa')}: {e}")
        
        conn.commit()
        conn.close()
        return imported_count
    
    def export_users_csv(self):
        """Exportar usuarios neurodivergentes a CSV"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
        SELECT id, nombre, apellidos, email, telefono, ciudad, 
               fecha_nacimiento, tipo_neurodivergencia, diagnostico_formal,
               experiencia_laboral, formacion_academica, habilidades,
               intereses_laborales, adaptaciones_necesarias, created_at
        FROM users ORDER BY created_at DESC
        ''')
        
        users = cursor.fetchall()
        conn.close()
        
        output = StringIO()
        writer = csv.writer(output)
        
        # Headers
        writer.writerow([
            'ID', 'Nombre', 'Apellidos', 'Email', 'Teléfono', 'Ciudad',
            'Fecha Nacimiento', 'Neurodivergencia', 'Diagnóstico Formal', 
            'Experiencia Laboral', 'Formación', 'Habilidades',
            'Intereses Laborales', 'Adaptaciones', 'Fecha Registro'
        ])
        
        # Data
        for user in users:
            writer.writerow(user)
        
        output.seek(0)
        return output.getvalue()
    
    def export_associations_csv(self):
        """Exportar asociaciones a CSV"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Verificar si tabla existe
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='asociaciones'")
        if not cursor.fetchone():
            return "ID,Nombre,Email,Ciudad,Estado\n# No hay asociaciones registradas"
        
        cursor.execute('''
        SELECT id, nombre_asociacion, email, ciudad, pais, 
               neurodivergencias_atendidas, servicios, estado, created_at
        FROM asociaciones ORDER BY created_at DESC
        ''')
        
        associations = cursor.fetchall()
        conn.close()
        
        output = StringIO()
        writer = csv.writer(output)
        
        # Headers
        writer.writerow([
            'ID', 'Nombre Asociación', 'Email', 'Ciudad', 'País',
            'Neurodivergencias', 'Servicios', 'Estado', 'Fecha Registro'
        ])
        
        # Data
        for assoc in associations:
            writer.writerow(assoc)
        
        output.seek(0)
        return output.getvalue()
    
    def export_stats_json(self):
        """Exportar estadísticas en JSON"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Contar empresas
        cursor.execute('SELECT COUNT(*) FROM companies')
        companies_count = cursor.fetchone()[0]
        
        # Contar ofertas
        cursor.execute('SELECT COUNT(*) FROM job_offers WHERE activa = 1')
        active_offers = cursor.fetchone()[0]
        
        # Empresas por sector
        cursor.execute('''
        SELECT sector, COUNT(*) 
        FROM companies 
        GROUP BY sector 
        ORDER BY COUNT(*) DESC
        ''')
        sectors = dict(cursor.fetchall())
        
        # Ofertas por modalidad
        cursor.execute('''
        SELECT modalidad_trabajo, COUNT(*) 
        FROM job_offers 
        WHERE activa = 1 
        GROUP BY modalidad_trabajo
        ''')
        modalities = dict(cursor.fetchall())
        
        conn.close()
        
        stats = {
            'timestamp': datetime.now().isoformat(),
            'total_companies': companies_count,
            'active_job_offers': active_offers,
            'companies_by_sector': sectors,
            'offers_by_modality': modalities
        }
        
        return json.dumps(stats, indent=2)

# Instancia global
csv_manager = CSVManager()

def create_csv_routes(app):
    """Crear rutas CSV para la app Flask"""
    
    @app.route('/admin/export/companies.csv')
    def export_companies():
        csv_data = csv_manager.export_companies_csv()
        response = Response(
            csv_data,
            mimetype='text/csv',
            headers={'Content-Disposition': 'attachment; filename=companies.csv'}
        )
        return response
    
    @app.route('/admin/export/offers.csv')  
    def export_offers():
        csv_data = csv_manager.export_job_offers_csv()
        response = Response(
            csv_data,
            mimetype='text/csv',
            headers={'Content-Disposition': 'attachment; filename=job_offers.csv'}
        )
        return response
    
    @app.route('/admin/export/stats.json')
    def export_stats():
        json_data = csv_manager.export_stats_json()
        response = Response(
            json_data,
            mimetype='application/json',
            headers={'Content-Disposition': 'attachment; filename=diversia_stats.json'}
        )
        return response
    
    @app.route('/admin/export/users.csv')
    def export_users():
        csv_data = csv_manager.export_users_csv()
        response = Response(
            csv_data,
            mimetype='text/csv',
            headers={'Content-Disposition': 'attachment; filename=users_neurodivergentes.csv'}
        )
        return response
    
    @app.route('/admin/export/associations.csv')
    def export_associations():
        csv_data = csv_manager.export_associations_csv()
        response = Response(
            csv_data,
            mimetype='text/csv',
            headers={'Content-Disposition': 'attachment; filename=asociaciones.csv'}
        )
        return response
    
    @app.route('/admin/import/companies', methods=['POST'])
    def import_companies():
        if 'file' not in request.files:
            return jsonify({'error': 'No file provided'}), 400
        
        file = request.files['file']
        if file.filename == '':
            return jsonify({'error': 'No file selected'}), 400
        
        if file and file.filename.endswith('.csv'):
            csv_content = file.read().decode('utf-8')
            imported_count = csv_manager.import_companies_csv(csv_content)
            return jsonify({'message': f'{imported_count} companies imported successfully'})
        
        return jsonify({'error': 'Invalid file format. Please upload CSV'}), 400
    
    print("✅ Rutas CSV completas: exportar e importar datos")

if __name__ == "__main__":
    # Test
    manager = CSVManager()
    print("📊 Exportando empresas...")
    companies_csv = manager.export_companies_csv()
    companies_count = len(companies_csv.split('\n')) - 1
    print(f"✅ {companies_count} empresas exportadas")
    
    print("📊 Exportando estadísticas...")
    stats = manager.export_stats_json()
    print(f"✅ Estadísticas: {stats}")