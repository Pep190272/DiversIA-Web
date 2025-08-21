#!/usr/bin/env python3
"""
Sistema CRM para gestionar personas neurodivergentes
Incluye todas las categorías y tipos de neurodivergencias
"""

import sqlite3
import json
from datetime import datetime
from flask import jsonify

class CRMNeurodivergentes:
    """Gestor CRM especializado para personas neurodivergentes"""
    
    def __init__(self, db_path='diversia.db'):
        self.db_path = db_path
        self.neurodivergence_types = [
            'TDAH', 'TEA', 'Dislexia', 'Discalculia', 'Tourette', 
            'Dispraxia', 'Ansiedad', 'Bipolar', 'Altas Capacidades'
        ]
    
    def get_stats_by_neurodivergence(self):
        """Obtener estadísticas por tipo de neurodivergencia"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Verificar si tabla users existe
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='users'")
        if not cursor.fetchone():
            return {'total': 0, 'by_type': {}}
        
        cursor.execute('''
        SELECT tipo_neurodivergencia, COUNT(*) as count
        FROM users 
        GROUP BY tipo_neurodivergencia
        ORDER BY count DESC
        ''')
        
        results = cursor.fetchall()
        by_type = dict(results)
        
        cursor.execute('SELECT COUNT(*) FROM users')
        total = cursor.fetchone()[0]
        
        conn.close()
        
        return {
            'total': total,
            'by_type': by_type
        }
    
    def get_users_by_type(self, neurodivergence_type):
        """Obtener usuarios por tipo de neurodivergencia"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
        SELECT id, nombre, apellidos, email, telefono, ciudad,
               diagnostico_formal, experiencia_laboral, habilidades,
               created_at
        FROM users 
        WHERE tipo_neurodivergencia = ?
        ORDER BY created_at DESC
        ''', (neurodivergence_type,))
        
        users = []
        for row in cursor.fetchall():
            users.append({
                'id': row[0],
                'nombre_completo': f"{row[1]} {row[2]}",
                'email': row[3],
                'telefono': row[4],
                'ciudad': row[5],
                'diagnostico_formal': row[6],
                'experiencia_laboral': row[7],
                'habilidades': row[8],
                'fecha_registro': row[9]
            })
        
        conn.close()
        return users
    
    def get_detailed_user(self, user_id):
        """Obtener información detallada de un usuario"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
        SELECT * FROM users WHERE id = ?
        ''', (user_id,))
        
        row = cursor.fetchone()
        if not row:
            return None
        
        # Mapear campos según el modelo User
        user_data = {
            'id': row[0],
            'nombre': row[1],
            'apellidos': row[2],
            'email': row[3],
            'telefono': row[4],
            'ciudad': row[5],
            'fecha_nacimiento': row[6],
            'tipo_neurodivergencia': row[7],
            'diagnostico_formal': row[8],
            'experiencia_laboral': row[9],
            'formacion_academica': row[10],
            'habilidades': row[11],
            'intereses_laborales': row[12],
            'adaptaciones_necesarias': row[13],
            'created_at': row[14]
        }
        
        conn.close()
        return user_data
    
    def export_neurodivergence_report(self):
        """Exportar reporte completo de neurodivergencias"""
        stats = self.get_stats_by_neurodivergence()
        
        report = {
            'generated_at': datetime.now().isoformat(),
            'total_users': stats['total'],
            'distribution': stats['by_type'],
            'detailed_data': {}
        }
        
        # Agregar datos detallados por tipo
        for nd_type in self.neurodivergence_types:
            users = self.get_users_by_type(nd_type)
            report['detailed_data'][nd_type] = {
                'count': len(users),
                'users': users[:10]  # Primeros 10 usuarios
            }
        
        return report

# Instancia global
crm_nd = CRMNeurodivergentes()

def create_neurodivergentes_api(app):
    """Crear APIs para gestión de personas neurodivergentes"""
    
    @app.route('/api/neurodivergentes/stats')
    def api_nd_stats():
        """API para estadísticas de neurodivergentes"""
        try:
            stats = crm_nd.get_stats_by_neurodivergence()
            return jsonify(stats)
        except Exception as e:
            return jsonify({'error': str(e)}), 500
    
    @app.route('/api/neurodivergentes/<nd_type>')
    def api_nd_by_type(nd_type):
        """API para obtener usuarios por tipo de neurodivergencia"""
        try:
            users = crm_nd.get_users_by_type(nd_type)
            return jsonify({
                'type': nd_type,
                'count': len(users),
                'users': users
            })
        except Exception as e:
            return jsonify({'error': str(e)}), 500
    
    @app.route('/api/neurodivergentes/user/<int:user_id>')
    def api_nd_user_detail(user_id):
        """API para obtener detalle de usuario"""
        try:
            user = crm_nd.get_detailed_user(user_id)
            if user:
                return jsonify(user)
            else:
                return jsonify({'error': 'Usuario no encontrado'}), 404
        except Exception as e:
            return jsonify({'error': str(e)}), 500
    
    @app.route('/api/neurodivergentes/export')
    def api_nd_export():
        """API para exportar reporte completo"""
        try:
            report = crm_nd.export_neurodivergence_report()
            return jsonify(report)
        except Exception as e:
            return jsonify({'error': str(e)}), 500
    
    print("✅ APIs de neurodivergentes creadas: /api/neurodivergentes/*")

if __name__ == "__main__":
    # Test
    crm = CRMNeurodivergentes()
    stats = crm.get_stats_by_neurodivergence()
    print(f"📊 Estadísticas ND: {stats}")
    
    report = crm.export_neurodivergence_report()
    print(f"📋 Reporte generado para {report['total_users']} usuarios")