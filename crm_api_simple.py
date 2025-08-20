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
            
            # Enviar email de bienvenida al empleado
            try:
                from employee_email_service import send_employee_welcome_email, send_admin_notification
                
                # Enviar email de bienvenida
                email_sent = send_employee_welcome_email(new_employee)
                
                # Notificar a administradores
                admin_notified = send_admin_notification(new_employee)
                
                response_message = 'Empleado creado correctamente'
                if email_sent:
                    response_message += ' - Email de activación enviado'
                if admin_notified:
                    response_message += ' - Administradores notificados'
                    
            except Exception as e:
                print(f"⚠️ Error enviando emails: {e}")
                response_message = 'Empleado creado correctamente (sin notificación por email)'
                
            return add_cors_headers(jsonify({'message': response_message, 'id': new_id})), 201
            
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

# API CONTACTOS
@app.route('/api/contacts', methods=['GET', 'POST'])
def api_contacts():
    if not require_admin():
        return jsonify({'error': 'No autorizado'}), 401
    
    if request.method == 'GET':
        return add_cors_headers(jsonify(SAMPLE_CRM_DATA.get('contacts', [])))
    
    elif request.method == 'POST':
        try:
            data = request.get_json()
            new_id = max([c['id'] for c in SAMPLE_CRM_DATA['contacts']], default=0) + 1
            
            new_contact = {
                'id': new_id,
                'name': data.get('name'),
                'email': data.get('email'),
                'phone': data.get('phone', ''),
                'city': data.get('city', ''),
                'neurodivergence': data.get('neurodivergence', 'TDAH'),
                'formal_diagnosis': data.get('formal_diagnosis', False),
                'created_at': '2024-12-20T10:00:00',
                'source': 'Manual'
            }
            
            SAMPLE_CRM_DATA['contacts'].append(new_contact)
            return add_cors_headers(jsonify({'message': 'Contacto creado', 'id': new_id})), 201
        except Exception as e:
            return add_cors_headers(jsonify({'error': str(e)})), 500

@app.route('/api/contacts/<int:contact_id>', methods=['PUT', 'DELETE'])
def manage_contact(contact_id):
    if not require_admin():
        return jsonify({'error': 'No autorizado'}), 401
    
    if request.method == 'DELETE':
        initial_count = len(SAMPLE_CRM_DATA['contacts'])
        SAMPLE_CRM_DATA['contacts'] = [c for c in SAMPLE_CRM_DATA['contacts'] if c['id'] != contact_id]
        
        if len(SAMPLE_CRM_DATA['contacts']) < initial_count:
            return add_cors_headers(jsonify({'message': 'Contacto eliminado'}))
        else:
            return add_cors_headers(jsonify({'error': 'No encontrado'})), 404
    
    elif request.method == 'PUT':
        data = request.get_json()
        contact = next((c for c in SAMPLE_CRM_DATA['contacts'] if c['id'] == contact_id), None)
        
        if contact:
            contact.update({
                'name': data.get('name', contact['name']),
                'email': data.get('email', contact['email']),
                'phone': data.get('phone', contact['phone']),
                'city': data.get('city', contact['city']),
                'neurodivergence': data.get('neurodivergence', contact['neurodivergence']),
                'formal_diagnosis': data.get('formal_diagnosis', contact['formal_diagnosis'])
            })
            return add_cors_headers(jsonify({'message': 'Contacto actualizado'}))
        else:
            return add_cors_headers(jsonify({'error': 'No encontrado'})), 404

# API EMPRESAS
@app.route('/api/companies', methods=['GET', 'POST'])
def api_companies():
    if not require_admin():
        return jsonify({'error': 'No autorizado'}), 401
    
    if request.method == 'GET':
        return add_cors_headers(jsonify(SAMPLE_CRM_DATA.get('companies', [])))
    
    elif request.method == 'POST':
        try:
            data = request.get_json()
            new_id = max([c['id'] for c in SAMPLE_CRM_DATA['companies']], default=0) + 1
            
            new_company = {
                'id': new_id,
                'name': data.get('name'),
                'sector': data.get('sector', 'Tecnología'),
                'email': data.get('email'),
                'phone': data.get('phone', ''),
                'city': data.get('city', ''),
                'size': data.get('size', '1-10'),
                'website': data.get('website', ''),
                'created_at': '2024-12-20T10:00:00'
            }
            
            SAMPLE_CRM_DATA['companies'].append(new_company)
            return add_cors_headers(jsonify({'message': 'Empresa creada', 'id': new_id})), 201
        except Exception as e:
            return add_cors_headers(jsonify({'error': str(e)})), 500

@app.route('/api/companies/<int:company_id>', methods=['PUT', 'DELETE'])
def manage_company(company_id):
    if not require_admin():
        return jsonify({'error': 'No autorizado'}), 401
    
    if request.method == 'DELETE':
        initial_count = len(SAMPLE_CRM_DATA['companies'])
        SAMPLE_CRM_DATA['companies'] = [c for c in SAMPLE_CRM_DATA['companies'] if c['id'] != company_id]
        
        if len(SAMPLE_CRM_DATA['companies']) < initial_count:
            return add_cors_headers(jsonify({'message': 'Empresa eliminada'}))
        else:
            return add_cors_headers(jsonify({'error': 'No encontrada'})), 404
    
    elif request.method == 'PUT':
        data = request.get_json()
        company = next((c for c in SAMPLE_CRM_DATA['companies'] if c['id'] == company_id), None)
        
        if company:
            company.update({
                'name': data.get('name', company['name']),
                'sector': data.get('sector', company['sector']),
                'email': data.get('email', company['email']),
                'phone': data.get('phone', company['phone']),
                'city': data.get('city', company['city']),
                'size': data.get('size', company['size']),
                'website': data.get('website', company['website'])
            })
            return add_cors_headers(jsonify({'message': 'Empresa actualizada'}))
        else:
            return add_cors_headers(jsonify({'error': 'No encontrada'})), 404

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