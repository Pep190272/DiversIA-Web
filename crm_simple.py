"""
CRM simplificado que funciona independientemente de la base de datos
Para casos donde PostgreSQL no esté disponible
"""

from flask import jsonify, request, session, redirect, flash, render_template
from app import app
import json
import hashlib
from datetime import datetime

# Sistema de admin simple en memoria
ADMIN_USERS = {
    'DiversiaEternals': {
        'password_hash': hashlib.sha256('diversia3ternal$2025'.encode()).hexdigest(),
        'email': 'diversiaeternals@gmail.com',
        'is_super_admin': True
    }
}

# Cargar datos persistentes del gestor
try:
    from data_persistence_manager import persistence_manager
    SAMPLE_CRM_DATA = persistence_manager.load_data()
    print(f"✅ Datos CRM cargados desde archivo persistente: {len(SAMPLE_CRM_DATA.get('tasks', []))} tareas")
except ImportError:
    print("⚠️ Gestor de persistencia no disponible, usando datos por defecto")
    # Datos de ejemplo para el CRM
    SAMPLE_CRM_DATA = {
    'employees': [
        {
            'id': 1,
            'first_name': 'Ana',
            'last_name': 'García',
            'email': 'ana.garcia@diversia.com',
            'position': 'Desarrolladora Frontend',
            'department': 'Desarrollo',
            'role': 'empleado',
            'hire_date': '2024-01-15',
            'is_active': True,
            'salary': 35000
        },
        {
            'id': 2,
            'first_name': 'Carlos',
            'last_name': 'López',
            'email': 'carlos.lopez@diversia.com',
            'position': 'Especialista en Marketing',
            'department': 'Marketing',
            'role': 'colaborador',
            'hire_date': '2024-02-01',
            'is_active': True,
            'salary': 32000
        },
        {
            'id': 3,
            'first_name': 'María',
            'last_name': 'Rodríguez',
            'email': 'maria.rodriguez@diversia.com',
            'position': 'Diseñadora UX/UI',
            'department': 'Diseño',
            'role': 'empleado',
            'hire_date': '2024-03-01',
            'is_active': True,
            'salary': 34000
        }
    ],
    'tasks': [
        {
            'id': 1,
            'title': 'Actualizar diseño de landing page',
            'description': 'Mejorar la accesibilidad del sitio web principal',
            'priority': 'high',
            'status': 'in_progress',
            'category': 'diseño',
            'assigned_to': 'Ana García',
            'assigned_to_id': 1,
            'estimated_hours': 8,
            'actual_hours': 4,
            'due_date': '2024-12-30',
            'created_at': '2024-12-15T10:00:00'
        },
        {
            'id': 2,
            'title': 'Campaña de redes sociales',
            'description': 'Crear contenido para promover la inclusión laboral',
            'priority': 'medium',
            'status': 'pending',
            'category': 'marketing',
            'assigned_to': 'Carlos López',
            'assigned_to_id': 2,
            'estimated_hours': 6,
            'actual_hours': 0,
            'due_date': '2025-01-05',
            'created_at': '2024-12-16T14:00:00'
        }
    ],
    'old_employees': [
        {
            'id': 1,
            'first_name': 'Ana',
            'last_name': 'Martínez',
            'email': 'ana.martinez@diversia.com',
            'position': 'Desarrolladora Frontend',
            'department': 'Desarrollo',
            'role': 'empleado',
            'hire_date': '2024-01-15',
            'is_active': True,
            'tasks_count': 3,
            'completed_tasks': 1
        },
        {
            'id': 2,
            'first_name': 'Carlos',
            'last_name': 'Ruiz',
            'email': 'carlos.ruiz@diversia.com',
            'position': 'Community Manager',
            'department': 'Marketing',
            'role': 'colaborador',
            'hire_date': '2024-02-01',
            'is_active': True,
            'tasks_count': 2,
            'completed_tasks': 2
        }
    ],
    'tasks': [
        {
            'id': 1,
            'title': 'Mejorar accesibilidad web',
            'description': 'Implementar mejoras de accesibilidad en formularios',
            'assigned_to': 'Ana Martínez',
            'assigned_to_id': 1,
            'priority': 'high',
            'status': 'in_progress',
            'category': 'development',
            'estimated_hours': 8.0,
            'actual_hours': 4.5,
            'due_date': '2025-08-25',
            'created_at': '2025-08-20'
        },
        {
            'id': 2,
            'title': 'Campaña redes sociales',
            'description': 'Crear contenido para campaña de inclusión',
            'assigned_to': 'Carlos Ruiz',
            'assigned_to_id': 2,
            'priority': 'medium',
            'status': 'completed',
            'category': 'marketing',
            'estimated_hours': 6.0,
            'actual_hours': 5.5,
            'due_date': '2025-08-22',
            'created_at': '2025-08-18'
        }
    ],
    'contacts': [
        {
            'id': 1,
            'name': 'María García',
            'email': 'maria.garcia@example.com',
            'phone': '+34 666 123 456',
            'city': 'Madrid',
            'neurodivergence': 'TDAH',
            'source': 'Registro Web',
            'type': 'Usuario ND',
            'created_at': '2025-01-15T10:30:00',
            'exported_to_crm': False
        },
        {
            'id': 2,
            'name': 'Carlos Rodríguez',
            'email': 'carlos.rodriguez@tech.com',
            'phone': '+34 677 789 012',
            'city': 'Barcelona',
            'neurodivergence': 'TEA',
            'source': 'Registro Web',
            'type': 'Usuario ND',
            'created_at': '2025-01-16T14:20:00',
            'exported_to_crm': False
        }
    ],
    'companies': [
        {
            'id': 1,
            'name': 'TechInclusive SA',
            'email': 'rrhh@techinclusive.com',
            'phone': '+34 912 345 678',
            'sector': 'Tecnología',
            'size': '50-200 empleados',
            'city': 'Madrid',
            'description': 'Empresa tecnológica comprometida con la inclusión',
            'job_offers_count': 3,
            'created_at': '2025-01-14T09:15:00',
            'exported_to_crm': False
        },
        {
            'id': 2,
            'name': 'Diversidad Corp',
            'email': 'contacto@diversidadcorp.es',
            'phone': '+34 933 456 789',
            'sector': 'Consultoría',
            'size': '10-50 empleados',
            'city': 'Barcelona',
            'description': 'Consultoría especializada en diversidad e inclusión',
            'job_offers_count': 1,
            'created_at': '2025-01-17T11:45:00',
            'exported_to_crm': False
        }
    ],
    'job_offers': [
        {
            'id': 1,
            'title': 'Desarrollador Frontend Inclusivo',
            'company_name': 'TechInclusive SA',
            'company_id': 1,
            'location': 'Madrid (Remoto posible)',
            'salary': '35.000-45.000€',
            'description': 'Buscamos desarrollador frontend con ganas de crear interfaces accesibles',
            'accepted_neurodivergences': 'TDAH, TEA, Dislexia',
            'active': True,
            'created_at': '2025-01-15T16:30:00',
            'exported_to_crm': False
        },
        {
            'id': 2,
            'title': 'Consultor Junior Diversidad',
            'company_name': 'Diversidad Corp',
            'company_id': 2,
            'location': 'Barcelona',
            'salary': '28.000-35.000€',
            'description': 'Posición junior para apoyar proyectos de inclusión laboral',
            'accepted_neurodivergences': 'Todas',
            'active': True,
            'created_at': '2025-01-18T12:00:00',
            'exported_to_crm': False
        }
    ],
    'associations': [
        {
            'id': 1,
            'name': 'Fundación TDAH Madrid',
            'acronym': 'FTDAH-M',
            'country': 'España',
            'document_type': 'CIF',
            'document_number': 'G12345678'
        },
        {
            'id': 2,
            'name': 'Asociación TEA Barcelona',
            'acronym': 'ATEAB',
            'country': 'España',
            'document_type': 'CIF',
            'document_number': 'G87654321'
        }
    ]
}

# ============ RUTAS DE AUTENTICACIÓN SIMPLE ============
@app.route('/admin/login', methods=['GET', 'POST'])
def admin_login_simple():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        if username in ADMIN_USERS:
            password_hash = hashlib.sha256(password.encode()).hexdigest()
            if ADMIN_USERS[username]['password_hash'] == password_hash:
                session['admin_id'] = username
                session['admin_username'] = username
                session['is_super_admin'] = ADMIN_USERS[username]['is_super_admin']
                
                flash(f'Bienvenido {username}', 'success')
                return redirect('/crm')
        
        flash('Credenciales incorrectas.', 'error')
    
    return render_template('admin/login.html')

@app.route('/admin/logout')
def admin_logout_simple():
    session.pop('admin_id', None)
    session.pop('admin_username', None)
    session.pop('is_super_admin', None)
    flash('Sesión cerrada correctamente.', 'success')
    return redirect('/')

# ============ API CRM SIMPLE ============
@app.route('/api/contacts')
def api_contacts_simple():
    if 'admin_id' not in session:
        return jsonify({'error': 'No autorizado'}), 401
    return jsonify(SAMPLE_CRM_DATA['contacts'])

@app.route('/api/companies')
def api_companies_simple():
    if 'admin_id' not in session:
        return jsonify({'error': 'No autorizado'}), 401
    return jsonify(SAMPLE_CRM_DATA['companies'])

@app.route('/api/job-offers')
def api_job_offers_simple():
    if 'admin_id' not in session:
        return jsonify({'error': 'No autorizado'}), 401
    return jsonify(SAMPLE_CRM_DATA['job_offers'])

@app.route('/api/associations')
def api_associations_simple():
    if 'admin_id' not in session:
        return jsonify({'error': 'No autorizado'}), 401
    return jsonify(SAMPLE_CRM_DATA['associations'])

@app.route('/api/stats')
def api_stats_simple():
    if 'admin_id' not in session:
        return jsonify({'error': 'No autorizado'}), 401
    
    stats = {
        'total_users': len(SAMPLE_CRM_DATA['contacts']),
        'total_companies': len(SAMPLE_CRM_DATA['companies']),
        'total_job_offers': len(SAMPLE_CRM_DATA['job_offers']),
        'active_job_offers': len([offer for offer in SAMPLE_CRM_DATA['job_offers'] if offer['active']]),
        'total_associations': len(SAMPLE_CRM_DATA['associations']),
        'total_employees': len(SAMPLE_CRM_DATA['employees']),
        'total_tasks': len(SAMPLE_CRM_DATA['tasks']),
        'completed_tasks': len([task for task in SAMPLE_CRM_DATA['tasks'] if task['status'] == 'completed']),
        'pending_tasks': len([task for task in SAMPLE_CRM_DATA['tasks'] if task['status'] == 'pending']),
        'users_by_neurodivergence': {
            'TDAH': 1,
            'TEA': 1,
            'Dislexia': 0
        },
        'companies_by_sector': {
            'Tecnología': 1,
            'Consultoría': 1
        },
        'recent_registrations': 2
    }
    
    return jsonify(stats)

# ============ EMPLEADOS ============
@app.route('/api/employees')
def api_employees_simple():
    if 'admin_id' not in session:
        return jsonify({'error': 'No autorizado'}), 401
    return jsonify(SAMPLE_CRM_DATA['employees'])

@app.route('/api/employees/<int:employee_id>', methods=['DELETE'])
def delete_employee_simple(employee_id):
    if 'admin_id' not in session:
        return jsonify({'error': 'No autorizado'}), 401
    
    # Simular eliminación
    SAMPLE_CRM_DATA['employees'] = [e for e in SAMPLE_CRM_DATA['employees'] if e['id'] != employee_id]
    return jsonify({'message': 'Employee deleted successfully'})

# ============ TAREAS ============
@app.route('/api/tasks')
def api_tasks_simple():
    if 'admin_id' not in session:
        return jsonify({'error': 'No autorizado'}), 401
    return jsonify(SAMPLE_CRM_DATA['tasks'])

@app.route('/api/tasks', methods=['POST'])
def create_task_simple():
    if 'admin_id' not in session:
        return jsonify({'error': 'No autorizado'}), 401
    
    data = request.json
    new_task = {
        'id': len(SAMPLE_CRM_DATA['tasks']) + 1,
        'title': data.get('title', ''),
        'description': data.get('description', ''),
        'assigned_to_id': data.get('assigned_to_id'),
        'assigned_to': next((e['first_name'] + ' ' + e['last_name'] for e in SAMPLE_CRM_DATA['employees'] if e['id'] == data.get('assigned_to_id')), 'Sin asignar'),
        'priority': data.get('priority', 'medium'),
        'status': 'pending',
        'category': data.get('category', 'general'),
        'estimated_hours': data.get('estimated_hours', 0),
        'actual_hours': 0,
        'due_date': data.get('due_date'),
        'created_at': datetime.now().strftime('%Y-%m-%d')
    }
    
    SAMPLE_CRM_DATA['tasks'].append(new_task)
    return jsonify({'message': 'Task created successfully', 'task': new_task}), 201

@app.route('/api/tasks/<int:task_id>', methods=['PUT'])
def update_task_simple(task_id):
    if 'admin_id' not in session:
        return jsonify({'error': 'No autorizado'}), 401
    
    data = request.json
    task = next((t for t in SAMPLE_CRM_DATA['tasks'] if t['id'] == task_id), None)
    
    if not task:
        return jsonify({'error': 'Task not found'}), 404
    
    # Actualizar campos
    task['status'] = data.get('status', task['status'])
    task['actual_hours'] = data.get('actual_hours', task['actual_hours'])
    task['priority'] = data.get('priority', task['priority'])
    
    return jsonify({'message': 'Task updated successfully', 'task': task})

@app.route('/api/tasks/<int:task_id>', methods=['DELETE'])
def delete_task_simple(task_id):
    if 'admin_id' not in session:
        return jsonify({'error': 'No autorizado'}), 401
    
    # Simular eliminación
    SAMPLE_CRM_DATA['tasks'] = [t for t in SAMPLE_CRM_DATA['tasks'] if t['id'] != task_id]
    return jsonify({'message': 'Task deleted successfully'})

# ============ ENDPOINTS PARA ELIMINAR (SIMULADO) ============
@app.route('/api/contacts/<int:contact_id>', methods=['DELETE'])
def delete_contact_simple(contact_id):
    if 'admin_id' not in session:
        return jsonify({'error': 'No autorizado'}), 401
    
    # Simular eliminación
    SAMPLE_CRM_DATA['contacts'] = [c for c in SAMPLE_CRM_DATA['contacts'] if c['id'] != contact_id]
    return jsonify({'message': 'Contact deleted successfully'})

@app.route('/api/companies/<int:company_id>', methods=['DELETE'])
def delete_company_simple(company_id):
    if 'admin_id' not in session:
        return jsonify({'error': 'No autorizado'}), 401
    
    # Simular eliminación
    SAMPLE_CRM_DATA['companies'] = [c for c in SAMPLE_CRM_DATA['companies'] if c['id'] != company_id]
    return jsonify({'message': 'Company deleted successfully'})

@app.route('/api/job-offers/<int:offer_id>', methods=['DELETE'])
def delete_offer_simple(offer_id):
    if 'admin_id' not in session:
        return jsonify({'error': 'No autorizado'}), 401
    
    # Simular eliminación
    SAMPLE_CRM_DATA['job_offers'] = [o for o in SAMPLE_CRM_DATA['job_offers'] if o['id'] != offer_id]
    return jsonify({'message': 'Job offer deleted successfully'})

print("✅ CRM simple inicializado - funciona sin base de datos")
print("Credenciales: DiversiaEternals / diversia3ternal$2025")