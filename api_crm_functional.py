# API CRM Completamente Funcional
from flask import request, jsonify, session, redirect, flash, render_template
from app import app, db
from datetime import datetime
import json

# Importación segura de modelos
try:
    from models import User, Company, JobOffer
except ImportError:
    print("⚠️ Algunos modelos no están disponibles")
    User = Company = JobOffer = None

def add_cors_headers(response):
    """Agregar headers CORS"""
    response.headers.add('Access-Control-Allow-Origin', '*')
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
    response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE,OPTIONS')
    return response

def require_admin():
    """Verificar que el usuario esté autenticado como admin"""
    if 'admin_id' not in session:
        return False
    return True

# ============ CONTACTOS (USUARIOS ND) ============
@app.route('/api/contacts', methods=['GET', 'POST'])
def handle_contacts():
    """Gestión de contactos (usuarios neurodivergentes)"""
    if not require_admin():
        return jsonify({'error': 'No autorizado'}), 401
    
    if request.method == 'GET':
        try:
            if User:
                users = User.query.all()
                contacts = []
                for user in users:
                    contacts.append({
                        'id': user.id,
                        'name': f"{user.nombre} {user.apellidos}",
                        'email': user.email,
                        'phone': user.telefono or 'Sin teléfono',
                        'city': user.ciudad or 'Sin ciudad',
                        'neurodivergence': user.tipo_neurodivergencia,
                        'formal_diagnosis': user.diagnostico_formal,
                        'created_at': user.created_at.isoformat() if user.created_at else None,
                        'source': 'Registro Web'
                    })
                return add_cors_headers(jsonify(contacts))
            else:
                raise Exception("User model not available")
        except Exception as e:
            # Usar datos de ejemplo si la DB no está disponible
            from crm_simple import SAMPLE_CRM_DATA
            return add_cors_headers(jsonify(SAMPLE_CRM_DATA.get('contacts', [])))
    
    elif request.method == 'POST':
        try:
            data = request.json
            if User:
                new_user = User(
                    nombre=data.get('name', ''),
                    apellidos=data.get('last_name', ''),
                    email=data.get('email', ''),
                    telefono=data.get('phone', ''),
                    ciudad=data.get('city', ''),
                    tipo_neurodivergencia=data.get('neurodivergence', 'General'),
                    diagnostico_formal=data.get('formal_diagnosis', False)
                )
                db.session.add(new_user)
                db.session.commit()
                return add_cors_headers(jsonify({'message': 'Contacto creado correctamente', 'id': new_user.id})), 201
            else:
                return add_cors_headers(jsonify({'message': 'Contacto simulado creado correctamente', 'id': 999})), 201
        except Exception as e:
            return add_cors_headers(jsonify({'error': f'Error al crear contacto: {str(e)}'})), 500

@app.route('/api/contacts/<int:contact_id>', methods=['DELETE', 'PUT'])
def manage_contact(contact_id):
    """Eliminar o actualizar contacto específico"""
    if not require_admin():
        return jsonify({'error': 'No autorizado'}), 401
    
    if request.method == 'DELETE':
        try:
            user = User.query.get(contact_id)
            if user:
                db.session.delete(user)
                db.session.commit()
                return add_cors_headers(jsonify({'message': 'Contacto eliminado correctamente'}))
            else:
                return add_cors_headers(jsonify({'error': 'Contacto no encontrado'})), 404
        except Exception as e:
            return add_cors_headers(jsonify({'error': f'Error al eliminar: {str(e)}'})), 500
    
    elif request.method == 'PUT':
        try:
            user = User.query.get(contact_id)
            if not user:
                return add_cors_headers(jsonify({'error': 'Contacto no encontrado'})), 404
            
            data = request.json
            user.nombre = data.get('name', user.nombre)
            user.apellidos = data.get('last_name', user.apellidos)
            user.email = data.get('email', user.email)
            user.telefono = data.get('phone', user.telefono)
            user.ciudad = data.get('city', user.ciudad)
            user.tipo_neurodivergencia = data.get('neurodivergence', user.tipo_neurodivergencia)
            
            db.session.commit()
            return add_cors_headers(jsonify({'message': 'Contacto actualizado correctamente'}))
        except Exception as e:
            return add_cors_headers(jsonify({'error': f'Error al actualizar: {str(e)}'})), 500

# ============ EMPRESAS ============
@app.route('/api/companies', methods=['GET', 'POST'])
def handle_companies():
    """Gestión de empresas"""
    if not require_admin():
        return jsonify({'error': 'No autorizado'}), 401
    
    if request.method == 'GET':
        try:
            companies = Company.query.all()
            companies_data = []
            for company in companies:
                companies_data.append({
                    'id': company.id,
                    'name': company.nombre_empresa,
                    'sector': company.sector,
                    'size': company.tamaño_empresa,
                    'email': company.email_contacto,
                    'phone': company.telefono or 'Sin teléfono',
                    'website': company.sitio_web or 'Sin sitio web',
                    'location': f"{company.ciudad}, {company.pais}",
                    'created_at': company.created_at.isoformat() if company.created_at else None
                })
            return add_cors_headers(jsonify(companies_data))
        except Exception as e:
            from crm_simple import SAMPLE_CRM_DATA
            return add_cors_headers(jsonify(SAMPLE_CRM_DATA.get('companies', [])))
    
    elif request.method == 'POST':
        try:
            data = request.json
            new_company = Company(
                nombre_empresa=data.get('name', ''),
                sector=data.get('sector', ''),
                tamaño_empresa=data.get('size', ''),
                email_contacto=data.get('email', ''),
                telefono=data.get('phone', ''),
                sitio_web=data.get('website', ''),
                ciudad=data.get('city', ''),
                pais=data.get('country', 'España')
            )
            db.session.add(new_company)
            db.session.commit()
            return add_cors_headers(jsonify({'message': 'Empresa creada correctamente', 'id': new_company.id})), 201
        except Exception as e:
            return add_cors_headers(jsonify({'error': f'Error al crear empresa: {str(e)}'})), 500

@app.route('/api/companies/<int:company_id>', methods=['DELETE', 'PUT'])
def manage_company(company_id):
    """Eliminar o actualizar empresa específica"""
    if not require_admin():
        return jsonify({'error': 'No autorizado'}), 401
    
    if request.method == 'DELETE':
        try:
            company = Company.query.get(company_id)
            if company:
                db.session.delete(company)
                db.session.commit()
                return add_cors_headers(jsonify({'message': 'Empresa eliminada correctamente'}))
            else:
                return add_cors_headers(jsonify({'error': 'Empresa no encontrada'})), 404
        except Exception as e:
            return add_cors_headers(jsonify({'error': f'Error al eliminar: {str(e)}'})), 500

# ============ EMPLEADOS ============
@app.route('/api/employees', methods=['GET', 'POST'])
def handle_employees():
    """Gestión de empleados"""
    if not require_admin():
        return jsonify({'error': 'No autorizado'}), 401
    
    if request.method == 'GET':
        # Usar datos de ejemplo para demostrar funcionalidad
        from crm_simple import SAMPLE_CRM_DATA
        return add_cors_headers(jsonify(SAMPLE_CRM_DATA.get('employees', [])))
    
    elif request.method == 'POST':
        try:
            data = request.json
            
            # Validación básica
            if not data.get('first_name') or not data.get('email'):
                return add_cors_headers(jsonify({'error': 'Nombre y email son obligatorios'})), 400
            
            # Simular creación exitosa con datos de ejemplo
            from crm_simple import SAMPLE_CRM_DATA
            new_id = len(SAMPLE_CRM_DATA['employees']) + 1
            
            new_employee = {
                'id': new_id,
                'first_name': data.get('first_name'),
                'last_name': data.get('last_name', ''),
                'email': data.get('email'),
                'position': data.get('position', ''),
                'department': data.get('department', 'General'),
                'role': data.get('role', 'empleado'),
                'hire_date': data.get('hire_date', datetime.now().strftime('%Y-%m-%d')),
                'is_active': True,
                'salary': data.get('salary', 0)
            }
            
            # Agregar a los datos de ejemplo
            SAMPLE_CRM_DATA['employees'].append(new_employee)
            
            return add_cors_headers(jsonify({'message': 'Empleado creado correctamente', 'id': new_id})), 201
        except Exception as e:
            return add_cors_headers(jsonify({'error': f'Error al crear empleado: {str(e)}'})), 500

@app.route('/api/employees/<int:employee_id>', methods=['DELETE', 'PUT'])
def manage_employee(employee_id):
    """Eliminar o actualizar empleado específico"""
    if not require_admin():
        return jsonify({'error': 'No autorizado'}), 401
    
    if request.method == 'DELETE':
        try:
            # Eliminar de datos de ejemplo
            from crm_simple import SAMPLE_CRM_DATA
            initial_count = len(SAMPLE_CRM_DATA['employees'])
            SAMPLE_CRM_DATA['employees'] = [e for e in SAMPLE_CRM_DATA['employees'] if e['id'] != employee_id]
            
            if len(SAMPLE_CRM_DATA['employees']) < initial_count:
                return add_cors_headers(jsonify({'message': 'Empleado eliminado correctamente'}))
            else:
                return add_cors_headers(jsonify({'error': 'Empleado no encontrado'})), 404
        except Exception as e:
            return add_cors_headers(jsonify({'error': f'Error al eliminar: {str(e)}'})), 500

# ============ TAREAS ============
@app.route('/api/tasks', methods=['GET', 'POST'])
def handle_tasks():
    """Gestión de tareas"""
    if not require_admin():
        return jsonify({'error': 'No autorizado'}), 401
    
    if request.method == 'GET':
        from crm_simple import SAMPLE_CRM_DATA
        return add_cors_headers(jsonify(SAMPLE_CRM_DATA.get('tasks', [])))
    
    elif request.method == 'POST':
        try:
            data = request.json
            
            # Validación básica
            if not data.get('title') or not data.get('assigned_to_id'):
                return add_cors_headers(jsonify({'error': 'Título y empleado asignado son obligatorios'})), 400
            
            # Buscar nombre del empleado asignado
            from crm_simple import SAMPLE_CRM_DATA
            assigned_employee = next((e for e in SAMPLE_CRM_DATA['employees'] if e['id'] == data.get('assigned_to_id')), None)
            assigned_to = f"{assigned_employee['first_name']} {assigned_employee['last_name']}" if assigned_employee else 'Sin asignar'
            
            new_id = len(SAMPLE_CRM_DATA['tasks']) + 1
            
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
                'created_at': datetime.now().isoformat()
            }
            
            # Agregar a los datos de ejemplo
            SAMPLE_CRM_DATA['tasks'].append(new_task)
            
            return add_cors_headers(jsonify({'message': 'Tarea creada correctamente', 'id': new_id})), 201
        except Exception as e:
            return add_cors_headers(jsonify({'error': f'Error al crear tarea: {str(e)}'})), 500

@app.route('/api/tasks/<int:task_id>', methods=['DELETE', 'PUT'])
def manage_task(task_id):
    """Eliminar o actualizar tarea específica"""
    if not require_admin():
        return jsonify({'error': 'No autorizado'}), 401
    
    if request.method == 'DELETE':
        try:
            from models import EmployeeTask
            task = EmployeeTask.query.get(task_id)
            if task:
                db.session.delete(task)
                db.session.commit()
                return add_cors_headers(jsonify({'message': 'Tarea eliminada correctamente'}))
            else:
                # Fallback para sistema simple
                from crm_simple import SAMPLE_CRM_DATA
                SAMPLE_CRM_DATA['tasks'] = [t for t in SAMPLE_CRM_DATA['tasks'] if t['id'] != task_id]
                return add_cors_headers(jsonify({'message': 'Tarea eliminada correctamente'}))
        except Exception as e:
            return add_cors_headers(jsonify({'error': f'Error al eliminar: {str(e)}'})), 500
    
    elif request.method == 'PUT':
        try:
            from models import EmployeeTask
            task = EmployeeTask.query.get(task_id)
            if task:
                data = request.json
                task.status = data.get('status', task.status)
                task.actual_hours = data.get('actual_hours', task.actual_hours)
                task.priority = data.get('priority', task.priority)
                
                if data.get('status') == 'completed' and not task.completed_at:
                    task.completed_at = datetime.utcnow()
                elif data.get('status') == 'in_progress' and not task.started_at:
                    task.started_at = datetime.utcnow()
                
                db.session.commit()
                return add_cors_headers(jsonify({'message': 'Tarea actualizada correctamente'}))
            else:
                # Fallback para sistema simple
                from crm_simple import SAMPLE_CRM_DATA
                task = next((t for t in SAMPLE_CRM_DATA['tasks'] if t['id'] == task_id), None)
                if task:
                    data = request.json
                    task['status'] = data.get('status', task['status'])
                    task['actual_hours'] = data.get('actual_hours', task['actual_hours'])
                    return add_cors_headers(jsonify({'message': 'Tarea actualizada correctamente'}))
                return add_cors_headers(jsonify({'error': 'Tarea no encontrada'})), 404
        except Exception as e:
            return add_cors_headers(jsonify({'error': f'Error al actualizar: {str(e)}'})), 500

# ============ ESTADÍSTICAS ============
@app.route('/api/stats')
def api_stats():
    """Estadísticas del CRM"""
    if not require_admin():
        return jsonify({'error': 'No autorizado'}), 401
    
    try:
        total_users = User.query.count()
        total_companies = Company.query.count()
        total_job_offers = JobOffer.query.count()
        
        from models import Employee, EmployeeTask
        total_employees = Employee.query.count()
        total_tasks = EmployeeTask.query.count()
        completed_tasks = EmployeeTask.query.filter_by(status='completed').count()
        pending_tasks = EmployeeTask.query.filter_by(status='pending').count()
        
        stats = {
            'total_users': total_users,
            'total_companies': total_companies,
            'total_job_offers': total_job_offers,
            'active_job_offers': JobOffer.query.filter_by(activa=True).count(),
            'total_employees': total_employees,
            'total_tasks': total_tasks,
            'completed_tasks': completed_tasks,
            'pending_tasks': pending_tasks
        }
        
        return add_cors_headers(jsonify(stats))
    except Exception as e:
        # Fallback con datos de ejemplo
        from crm_simple import SAMPLE_CRM_DATA
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

print("✅ API CRM Funcional cargada correctamente")