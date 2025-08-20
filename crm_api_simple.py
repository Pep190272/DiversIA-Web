# API CRM Simple y Funcional
from flask import request, jsonify, session
from app import app

# Importar datos del CRM simple
from crm_simple import SAMPLE_CRM_DATA

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
        return add_cors_headers(jsonify(SAMPLE_CRM_DATA.get('employees', [])))
    
    elif request.method == 'POST':
        try:
            data = request.get_json()
            
            if not data or not data.get('first_name') or not data.get('email'):
                return add_cors_headers(jsonify({'error': 'Nombre y email son obligatorios'})), 400
            
            new_id = max([e['id'] for e in SAMPLE_CRM_DATA['employees']], default=0) + 1
            
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
            
            SAMPLE_CRM_DATA['employees'].append(new_employee)
            return add_cors_headers(jsonify({'message': 'Empleado creado correctamente', 'id': new_id})), 201
            
        except Exception as e:
            return add_cors_headers(jsonify({'error': f'Error al crear empleado: {str(e)}'})), 500

@app.route('/api/employees/<int:employee_id>', methods=['DELETE', 'PUT'])
def manage_employee(employee_id):
    if not require_admin():
        return jsonify({'error': 'No autorizado'}), 401
    
    if request.method == 'DELETE':
        try:
            initial_count = len(SAMPLE_CRM_DATA['employees'])
            SAMPLE_CRM_DATA['employees'] = [e for e in SAMPLE_CRM_DATA['employees'] if e['id'] != employee_id]
            
            if len(SAMPLE_CRM_DATA['employees']) < initial_count:
                return add_cors_headers(jsonify({'message': 'Empleado eliminado correctamente'}))
            else:
                return add_cors_headers(jsonify({'error': 'Empleado no encontrado'})), 404
                
        except Exception as e:
            return add_cors_headers(jsonify({'error': f'Error al eliminar: {str(e)}'})), 500
    
    elif request.method == 'PUT':
        try:
            data = request.get_json()
            employee = next((e for e in SAMPLE_CRM_DATA['employees'] if e['id'] == employee_id), None)
            
            if employee:
                employee.update({
                    'first_name': data.get('first_name', employee['first_name']),
                    'last_name': data.get('last_name', employee['last_name']),
                    'email': data.get('email', employee['email']),
                    'position': data.get('position', employee['position']),
                    'department': data.get('department', employee['department']),
                    'role': data.get('role', employee['role']),
                    'hire_date': data.get('hire_date', employee['hire_date']),
                    'salary': data.get('salary', employee['salary']),
                    'is_active': data.get('is_active', employee['is_active'])
                })
                return add_cors_headers(jsonify({'message': 'Empleado actualizado correctamente'}))
            else:
                return add_cors_headers(jsonify({'error': 'Empleado no encontrado'})), 404
                
        except Exception as e:
            return add_cors_headers(jsonify({'error': f'Error al actualizar: {str(e)}'})), 500

# API TAREAS
@app.route('/api/tasks', methods=['GET', 'POST'])
def api_tasks():
    if not require_admin():
        return jsonify({'error': 'No autorizado'}), 401
    
    if request.method == 'GET':
        return add_cors_headers(jsonify(SAMPLE_CRM_DATA.get('tasks', [])))
    
    elif request.method == 'POST':
        try:
            data = request.get_json()
            
            if not data or not data.get('title') or not data.get('assigned_to_id'):
                return add_cors_headers(jsonify({'error': 'Título y empleado asignado son obligatorios'})), 400
            
            # Buscar empleado asignado
            assigned_employee = next((e for e in SAMPLE_CRM_DATA['employees'] if e['id'] == data.get('assigned_to_id')), None)
            assigned_to = f"{assigned_employee['first_name']} {assigned_employee['last_name']}" if assigned_employee else 'Sin asignar'
            
            new_id = max([t['id'] for t in SAMPLE_CRM_DATA['tasks']], default=0) + 1
            
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
            
            SAMPLE_CRM_DATA['tasks'].append(new_task)
            return add_cors_headers(jsonify({'message': 'Tarea creada correctamente', 'id': new_id})), 201
            
        except Exception as e:
            return add_cors_headers(jsonify({'error': f'Error al crear tarea: {str(e)}'})), 500

@app.route('/api/tasks/<int:task_id>', methods=['DELETE', 'PUT'])
def manage_task(task_id):
    if not require_admin():
        return jsonify({'error': 'No autorizado'}), 401
    
    if request.method == 'DELETE':
        try:
            initial_count = len(SAMPLE_CRM_DATA['tasks'])
            SAMPLE_CRM_DATA['tasks'] = [t for t in SAMPLE_CRM_DATA['tasks'] if t['id'] != task_id]
            
            if len(SAMPLE_CRM_DATA['tasks']) < initial_count:
                return add_cors_headers(jsonify({'message': 'Tarea eliminada correctamente'}))
            else:
                return add_cors_headers(jsonify({'error': 'Tarea no encontrada'})), 404
                
        except Exception as e:
            return add_cors_headers(jsonify({'error': f'Error al eliminar: {str(e)}'})), 500
    
    elif request.method == 'PUT':
        try:
            data = request.get_json()
            task = next((t for t in SAMPLE_CRM_DATA['tasks'] if t['id'] == task_id), None)
            
            if task:
                # Buscar empleado asignado si cambió
                if 'assigned_to_id' in data:
                    assigned_employee = next((e for e in SAMPLE_CRM_DATA['employees'] if e['id'] == data['assigned_to_id']), None)
                    if assigned_employee:
                        task['assigned_to'] = f"{assigned_employee['first_name']} {assigned_employee['last_name']}"
                        task['assigned_to_id'] = data['assigned_to_id']
                
                # Actualizar otros campos
                task.update({
                    'title': data.get('title', task['title']),
                    'description': data.get('description', task['description']),
                    'priority': data.get('priority', task['priority']),
                    'status': data.get('status', task['status']),
                    'category': data.get('category', task['category']),
                    'estimated_hours': data.get('estimated_hours', task['estimated_hours']),
                    'actual_hours': data.get('actual_hours', task['actual_hours']),
                    'due_date': data.get('due_date', task['due_date'])
                })
                
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
            'total_users': len(SAMPLE_CRM_DATA.get('contacts', [])),
            'total_companies': len(SAMPLE_CRM_DATA.get('companies', [])),
            'total_job_offers': len(SAMPLE_CRM_DATA.get('job_offers', [])),
            'active_job_offers': len([o for o in SAMPLE_CRM_DATA.get('job_offers', []) if o.get('active', False)]),
            'total_employees': len(SAMPLE_CRM_DATA.get('employees', [])),
            'total_tasks': len(SAMPLE_CRM_DATA.get('tasks', [])),
            'completed_tasks': len([t for t in SAMPLE_CRM_DATA.get('tasks', []) if t.get('status') == 'completed']),
            'pending_tasks': len([t for t in SAMPLE_CRM_DATA.get('tasks', []) if t.get('status') == 'pending'])
        }
        return add_cors_headers(jsonify(stats))
    except Exception as e:
        return add_cors_headers(jsonify({'error': f'Error al cargar estadísticas: {str(e)}'})), 500

# API CONTACTOS (para compatibilidad)
@app.route('/api/contacts')
def api_contacts():
    if not require_admin():
        return jsonify({'error': 'No autorizado'}), 401
    return add_cors_headers(jsonify(SAMPLE_CRM_DATA.get('contacts', [])))

# API EMPRESAS (para compatibilidad)  
@app.route('/api/companies')
def api_companies():
    if not require_admin():
        return jsonify({'error': 'No autorizado'}), 401
    return add_cors_headers(jsonify(SAMPLE_CRM_DATA.get('companies', [])))

# API OFERTAS (para compatibilidad)
@app.route('/api/offers')
def api_offers():
    if not require_admin():
        return jsonify({'error': 'No autorizado'}), 401
    return add_cors_headers(jsonify(SAMPLE_CRM_DATA.get('job_offers', [])))

# API ASOCIACIONES (para compatibilidad)
@app.route('/api/associations')
def api_associations():
    if not require_admin():
        return jsonify({'error': 'No autorizado'}), 401
    return add_cors_headers(jsonify(SAMPLE_CRM_DATA.get('associations', [])))

print("✅ API CRM Simple cargada correctamente")