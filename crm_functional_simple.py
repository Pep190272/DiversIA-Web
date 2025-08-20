# CRM FUNCIONAL SIMPLE - Sin errores
from flask import request, jsonify, session
from app import app

# Datos en memoria para demostración
CRM_DATA = {
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
    'contacts': [
        {
            'id': 1,
            'name': 'Juan Pérez Martínez',
            'email': 'juan.perez@email.com',
            'phone': '+34 600 123 456',
            'city': 'Madrid',
            'neurodivergence': 'TDAH',
            'formal_diagnosis': True,
            'created_at': '2024-12-10T09:00:00',
            'source': 'Registro Web'
        }
    ]
}

def add_cors_headers(response):
    response.headers.add('Access-Control-Allow-Origin', '*')
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
    response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE,OPTIONS')
    return response

def require_admin():
    return 'admin_id' in session

# API EMPLEADOS
@app.route('/api/employees', methods=['GET', 'POST'])
def api_employees():
    if not require_admin():
        return jsonify({'error': 'No autorizado'}), 401
    
    if request.method == 'GET':
        return add_cors_headers(jsonify(CRM_DATA['employees']))
    
    elif request.method == 'POST':
        try:
            data = request.get_json()
            
            if not data.get('first_name') or not data.get('email'):
                return add_cors_headers(jsonify({'error': 'Nombre y email son obligatorios'})), 400
            
            new_id = max([e['id'] for e in CRM_DATA['employees']], default=0) + 1
            
            new_employee = {
                'id': new_id,
                'first_name': data.get('first_name'),
                'last_name': data.get('last_name', ''),
                'email': data.get('email'),
                'position': data.get('position', ''),
                'department': data.get('department', 'General'),
                'role': data.get('role', 'empleado'),
                'hire_date': data.get('hire_date'),
                'is_active': True,
                'salary': data.get('salary', 0)
            }
            
            CRM_DATA['employees'].append(new_employee)
            return add_cors_headers(jsonify({'message': 'Empleado creado correctamente', 'id': new_id})), 201
            
        except Exception as e:
            return add_cors_headers(jsonify({'error': f'Error al crear empleado: {str(e)}'})), 500

@app.route('/api/employees/<int:employee_id>', methods=['DELETE'])
def delete_employee(employee_id):
    if not require_admin():
        return jsonify({'error': 'No autorizado'}), 401
    
    try:
        initial_count = len(CRM_DATA['employees'])
        CRM_DATA['employees'] = [e for e in CRM_DATA['employees'] if e['id'] != employee_id]
        
        if len(CRM_DATA['employees']) < initial_count:
            return add_cors_headers(jsonify({'message': 'Empleado eliminado correctamente'}))
        else:
            return add_cors_headers(jsonify({'error': 'Empleado no encontrado'})), 404
            
    except Exception as e:
        return add_cors_headers(jsonify({'error': f'Error al eliminar: {str(e)}'})), 500

# API TAREAS
@app.route('/api/tasks', methods=['GET', 'POST'])
def api_tasks():
    if not require_admin():
        return jsonify({'error': 'No autorizado'}), 401
    
    if request.method == 'GET':
        return add_cors_headers(jsonify(CRM_DATA['tasks']))
    
    elif request.method == 'POST':
        try:
            data = request.get_json()
            
            if not data.get('title') or not data.get('assigned_to_id'):
                return add_cors_headers(jsonify({'error': 'Título y empleado asignado son obligatorios'})), 400
            
            # Buscar empleado asignado
            assigned_employee = next((e for e in CRM_DATA['employees'] if e['id'] == data.get('assigned_to_id')), None)
            assigned_to = f"{assigned_employee['first_name']} {assigned_employee['last_name']}" if assigned_employee else 'Sin asignar'
            
            new_id = max([t['id'] for t in CRM_DATA['tasks']], default=0) + 1
            
            new_task = {
                'id': new_id,
                'title': data.get('title'),
                'description': data.get('description', ''),
                'priority': data.get('priority', 'medium'),
                'status': 'pending',
                'category': data.get('category', 'general'),
                'assigned_to': assigned_to,
                'assigned_to_id': data.get('assigned_to_id'),
                'estimated_hours': data.get('estimated_hours', 0),
                'actual_hours': 0,
                'due_date': data.get('due_date'),
                'created_at': '2024-12-20T10:00:00'
            }
            
            CRM_DATA['tasks'].append(new_task)
            return add_cors_headers(jsonify({'message': 'Tarea creada correctamente', 'id': new_id})), 201
            
        except Exception as e:
            return add_cors_headers(jsonify({'error': f'Error al crear tarea: {str(e)}'})), 500

@app.route('/api/tasks/<int:task_id>', methods=['DELETE', 'PUT'])
def manage_task(task_id):
    if not require_admin():
        return jsonify({'error': 'No autorizado'}), 401
    
    if request.method == 'DELETE':
        try:
            initial_count = len(CRM_DATA['tasks'])
            CRM_DATA['tasks'] = [t for t in CRM_DATA['tasks'] if t['id'] != task_id]
            
            if len(CRM_DATA['tasks']) < initial_count:
                return add_cors_headers(jsonify({'message': 'Tarea eliminada correctamente'}))
            else:
                return add_cors_headers(jsonify({'error': 'Tarea no encontrada'})), 404
                
        except Exception as e:
            return add_cors_headers(jsonify({'error': f'Error al eliminar: {str(e)}'})), 500
    
    elif request.method == 'PUT':
        try:
            data = request.get_json()
            task = next((t for t in CRM_DATA['tasks'] if t['id'] == task_id), None)
            
            if task:
                task['status'] = data.get('status', task['status'])
                task['actual_hours'] = data.get('actual_hours', task['actual_hours'])
                return add_cors_headers(jsonify({'message': 'Tarea actualizada correctamente'}))
            else:
                return add_cors_headers(jsonify({'error': 'Tarea no encontrada'})), 404
                
        except Exception as e:
            return add_cors_headers(jsonify({'error': f'Error al actualizar: {str(e)}'})), 500

# API ESTADÍSTICAS
@app.route('/api/stats')
def api_stats():
    if not require_admin():
        return jsonify({'error': 'No autorizado'}), 401
    
    try:
        stats = {
            'total_users': len(CRM_DATA['contacts']),
            'total_companies': 5,  # Datos de ejemplo
            'total_job_offers': 8,
            'active_job_offers': 6,
            'total_employees': len(CRM_DATA['employees']),
            'total_tasks': len(CRM_DATA['tasks']),
            'completed_tasks': len([t for t in CRM_DATA['tasks'] if t['status'] == 'completed']),
            'pending_tasks': len([t for t in CRM_DATA['tasks'] if t['status'] == 'pending'])
        }
        return add_cors_headers(jsonify(stats))
    except Exception as e:
        return add_cors_headers(jsonify({'error': f'Error al cargar estadísticas: {str(e)}'})), 500

print("✅ CRM Funcional Simple cargado correctamente")