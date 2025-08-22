"""
Sistema de Gestión de Tareas para DiversIA
Gestión completa de tareas de empleados
"""

import csv
import io
from datetime import datetime
from flask import request, jsonify, render_template_string, flash, redirect, session
from app import app, db
from models import Task, Employee

@app.route('/tasks')
def tasks_dashboard():
    """Dashboard principal de gestión de tareas"""
    # Verificar autenticación admin
    if 'admin_ok' not in session or not session.get('admin_ok'):
        return redirect('/diversia-admin')
    
    # Obtener todas las tareas y empleados
    tasks = Task.query.all()
    employees = Employee.query.filter_by(active=True).all()
    total_tasks = len(tasks)
    
    return render_template_string(TASKS_TABLE_TEMPLATE, 
                                tasks=tasks,
                                employees=employees,
                                total_tasks=total_tasks)

@app.route('/tasks/analytics')
def tasks_analytics():
    """Dashboard de análisis con gráficos"""
    # Verificar autenticación admin
    if 'admin_ok' not in session or not session.get('admin_ok'):
        return redirect('/diversia-admin')
    
    # Estadísticas de tareas
    total_tasks = Task.query.count()
    pendientes = Task.query.filter_by(estado='Pendiente').count()
    en_curso = Task.query.filter_by(estado='En curso').count()
    completadas = Task.query.filter_by(estado='Completado').count()
    
    # Tareas por colaborador
    tasks_by_collaborator = db.session.query(
        Task.colaborador,
        db.func.count(Task.id).label('total_tasks'),
        db.func.sum(db.case((Task.estado == 'Completado', 1), else_=0)).label('completed'),
        db.func.sum(db.case((Task.estado == 'En curso', 1), else_=0)).label('in_progress'),
        db.func.sum(db.case((Task.estado == 'Pendiente', 1), else_=0)).label('pending')
    ).group_by(Task.colaborador).all()
    
    # Productividad por estado
    productivity_data = {
        'pendientes': pendientes,
        'en_curso': en_curso, 
        'completadas': completadas
    }
    
    # Empleados activos
    employees = Employee.query.filter_by(active=True).all()
    
    return render_template_string(TASKS_ANALYTICS_TEMPLATE,
                                total_tasks=total_tasks,
                                pendientes=pendientes,
                                en_curso=en_curso,
                                completadas=completadas,
                                tasks_by_collaborator=tasks_by_collaborator,
                                productivity_data=productivity_data,
                                employees=employees)

@app.route('/tasks/import', methods=['POST'])
def import_tasks_csv():
    """Importar CSV de tareas"""
    if 'file' not in request.files:
        flash('No se seleccionó archivo', 'error')
        return redirect('/tasks')
    
    file = request.files['file']
    if file.filename == '':
        flash('No se seleccionó archivo', 'error')
        return redirect('/tasks')
    
    try:
        content = file.read().decode('utf-8')
        csv_reader = csv.DictReader(io.StringIO(content))
        
        imported_count = 0
        updated_count = 0
        
        for row in csv_reader:
            tarea_name = row.get('Tarea', '').strip()
            
            if not tarea_name:
                continue
            
            # Buscar tarea existente
            existing = Task.query.filter_by(tarea=tarea_name).first()
            
            if existing:
                # Actualizar tarea existente
                existing.colaborador = row.get('Colaborador', '').strip()
                existing.fecha_inicio = row.get('Fecha de inicio', '').strip()
                existing.fecha_final = row.get('Fecha final', '').strip()
                existing.estado = row.get('Pendiente', 'Pendiente').strip()
                existing.updated_at = datetime.now()
                updated_count += 1
            else:
                # Crear nueva tarea
                new_task = Task(
                    tarea = tarea_name,
                    colaborador = row.get('Colaborador', '').strip(),
                    fecha_inicio = row.get('Fecha de inicio', '').strip(),
                    fecha_final = row.get('Fecha final', '').strip(),
                    estado = row.get('Pendiente', 'Pendiente').strip(),
                    notas = ''
                )
                db.session.add(new_task)
                imported_count += 1
        
        db.session.commit()
        flash(f'Importación exitosa: {imported_count} tareas nuevas, {updated_count} actualizadas', 'success')
        
    except Exception as e:
        db.session.rollback()
        flash(f'Error al importar CSV: {str(e)}', 'error')
    
    return redirect('/tasks')

@app.route('/tasks/edit/<int:task_id>', methods=['POST'])
def edit_task(task_id):
    """Editar una tarea específica inline"""
    if 'admin_ok' not in session or not session.get('admin_ok'):
        return jsonify({'error': 'No autorizado'}), 403
    
    data = request.get_json()
    
    try:
        task = Task.query.get_or_404(task_id)
        
        # Actualizar campos editables
        field = data.get('field')
        value = data.get('value', '').strip()
        
        if field == 'tarea':
            task.tarea = value
        elif field == 'colaborador':
            task.colaborador = value
        elif field == 'fecha_inicio':
            task.fecha_inicio = value
        elif field == 'fecha_final':
            task.fecha_final = value
        elif field == 'estado':
            task.estado = value
        elif field == 'notas':
            task.notas = value
        else:
            return jsonify({'error': 'Campo no válido'}), 400
        
        task.updated_at = datetime.now()
        db.session.commit()
        
        return jsonify({'success': True, 'value': value})
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@app.route('/tasks/delete/<int:task_id>', methods=['DELETE'])
def delete_task(task_id):
    """Eliminar una tarea específica"""
    if 'admin_ok' not in session or not session.get('admin_ok'):
        return jsonify({'error': 'No autorizado'}), 403
    
    try:
        task = Task.query.get_or_404(task_id)
        db.session.delete(task)
        db.session.commit()
        
        return jsonify({'success': True, 'message': 'Tarea eliminada'})
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@app.route('/tasks/delete-all', methods=['DELETE'])
def delete_all_tasks():
    """Eliminar todas las tareas"""
    if 'admin_ok' not in session or not session.get('admin_ok'):
        return jsonify({'error': 'No autorizado'}), 403
    
    try:
        count = Task.query.count()
        Task.query.delete()
        db.session.commit()
        
        return jsonify({'success': True, 'message': f'{count} tareas eliminadas'})
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@app.route('/tasks/export')
def export_tasks_csv():
    """Exportar datos de tareas"""
    tasks = Task.query.all()
    
    output = io.StringIO()
    writer = csv.writer(output)
    
    # Headers
    writer.writerow([
        'Tarea', 'Colaborador', 'Fecha de inicio', 'Fecha final', 'Pendiente'
    ])
    
    # Data
    for task in tasks:
        writer.writerow([
            task.tarea,
            task.colaborador or '',
            task.fecha_inicio or '',
            task.fecha_final or '',
            task.estado or 'Pendiente'
        ])
    
    output.seek(0)
    return output.getvalue(), 200, {
        'Content-Type': 'text/csv',
        'Content-Disposition': 'attachment; filename=tareas_diversia.csv'
    }

@app.route('/employees', methods=['GET', 'POST'])
def manage_employees():
    """Gestionar empleados"""
    if 'admin_ok' not in session or not session.get('admin_ok'):
        return redirect('/diversia-admin')
    
    if request.method == 'POST':
        data = request.get_json()
        try:
            new_employee = Employee(
                name=data.get('name', '').strip(),
                email=data.get('email', '').strip(),
                rol=data.get('rol', '').strip(),
                department=data.get('department', '').strip()
            )
            db.session.add(new_employee)
            db.session.commit()
            return jsonify({'success': True, 'message': 'Empleado añadido correctamente'})
        except Exception as e:
            db.session.rollback()
            return jsonify({'success': False, 'error': str(e)}), 500
    
    # GET: mostrar empleados
    employees = Employee.query.filter_by(active=True).all()
    return jsonify([{
        'id': emp.id,
        'name': emp.name,
        'email': emp.email,
        'rol': emp.rol,
        'department': emp.department
    } for emp in employees])

@app.route('/employees/<int:employee_id>', methods=['DELETE'])
def delete_employee(employee_id):
    """Eliminar empleado"""
    if 'admin_ok' not in session or not session.get('admin_ok'):
        return jsonify({'error': 'No autorizado'}), 403
    
    try:
        employee = Employee.query.get_or_404(employee_id)
        employee.active = False  # Soft delete
        db.session.commit()
        return jsonify({'success': True, 'message': 'Empleado eliminado'})
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

# Template para tabla de tareas
TASKS_TABLE_TEMPLATE = '''
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Gestión de Tareas - DiversIA</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
    <style>
        .table-responsive { max-height: 70vh; overflow-y: auto; }
        .btn-sm { font-size: 0.8rem; }
        .editable-field {
            cursor: pointer;
            padding: 3px 6px;
            border-radius: 3px;
            transition: background-color 0.2s;
            display: inline-block;
            min-width: 60px;
            min-height: 20px;
        }
        .editable-field:hover {
            background-color: #e3f2fd;
            border: 1px solid #2196f3;
        }
        .editing {
            background-color: #fff3cd !important;
            border: 2px solid #ffc107 !important;
        }
        .edit-input {
            border: 2px solid #007bff;
            font-size: 0.9rem;
            padding: 2px 6px;
            width: 100%;
            min-width: 80px;
        }
        .edit-select {
            border: 2px solid #007bff;
            font-size: 0.9rem;
            padding: 2px 6px;
            width: 100%;
        }
        .edit-textarea {
            border: 2px solid #007bff;
            font-size: 0.9rem;
            padding: 5px;
            width: 100%;
            min-height: 60px;
            resize: vertical;
        }
        .save-cancel-buttons {
            margin-top: 5px;
        }
        .status-pendiente { background-color: #fff3cd; }
        .status-en-curso { background-color: #d1ecf1; }
        .status-completado { background-color: #d4edda; }
    </style>
</head>
<body class="bg-light">
    <div class="container-fluid">
        <div class="row">
            <div class="col-12">
                <div class="d-flex justify-content-between align-items-center mb-4">
                    <h2>📋 Gestión de Tareas - DiversIA ({{ total_tasks }})</h2>
                    <div>
                        <a href="/tasks/analytics" class="btn btn-info me-2">📊 Analytics</a>
                        <a href="/crm-minimal" class="btn btn-outline-secondary me-2">← CRM</a>
                        <a href="/diversia-admin-logout" class="btn btn-outline-danger">Salir</a>
                    </div>
                </div>
                
                <!-- Acciones rápidas -->
                <div class="row mb-3">
                    <div class="col-md-4">
                        <form action="/tasks/import" method="post" enctype="multipart/form-data" class="d-flex">
                            <input type="file" name="file" class="form-control me-2" accept=".csv" required>
                            <button type="submit" class="btn btn-success">Importar CSV</button>
                        </form>
                    </div>
                    <div class="col-md-4">
                        <div class="input-group">
                            <input type="text" id="searchInput" class="form-control" placeholder="Buscar por tarea o colaborador...">
                            <button class="btn btn-outline-secondary" type="button" onclick="clearSearch()">
                                <span id="clearIcon">🔍</span>
                            </button>
                        </div>
                    </div>
                    <div class="col-md-4 text-end">
                        <button class="btn btn-primary me-2" onclick="showAddEmployeeForm()">👤 Añadir Colaborador</button>
                        <a href="/tasks/export" class="btn btn-warning me-2">Exportar CSV</a>
                        <button onclick="deleteAllTasks()" class="btn btn-danger">🗑️ Eliminar Todo</button>
                    </div>
                </div>
                
                <!-- Contador de resultados -->
                <div class="row mb-2">
                    <div class="col-12">
                        <small class="text-muted">
                            Mostrando <span id="visibleCount">{{ total_tasks }}</span> de {{ total_tasks }} tareas
                        </small>
                    </div>
                </div>
                
                <!-- Formulario añadir empleado -->
                <div id="addEmployeeForm" class="card mb-4" style="display: none;">
                    <div class="card-header">
                        <h5>Añadir Nuevo Colaborador</h5>
                    </div>
                    <div class="card-body">
                        <form id="employeeForm">
                            <div class="row">
                                <div class="col-md-6">
                                    <div class="mb-3">
                                        <label class="form-label">Nombre Completo *</label>
                                        <input type="text" class="form-control" id="empName" required>
                                    </div>
                                </div>
                                <div class="col-md-6">
                                    <div class="mb-3">
                                        <label class="form-label">Email *</label>
                                        <input type="email" class="form-control" id="empEmail" required>
                                    </div>
                                </div>
                                <div class="col-md-6">
                                    <div class="mb-3">
                                        <label class="form-label">Rol *</label>
                                        <select class="form-control" id="empRol" required>
                                            <option value="">Seleccionar rol...</option>
                                            <option value="Developer">Developer</option>
                                            <option value="Designer">Designer</option>
                                            <option value="Marketing">Marketing</option>
                                            <option value="Manager">Manager</option>
                                            <option value="Analyst">Analyst</option>
                                            <option value="Support">Support</option>
                                        </select>
                                    </div>
                                </div>
                                <div class="col-md-6">
                                    <div class="mb-3">
                                        <label class="form-label">Departamento</label>
                                        <input type="text" class="form-control" id="empDepartment">
                                    </div>
                                </div>
                            </div>
                            <div class="d-flex gap-2">
                                <button type="submit" class="btn btn-success">Añadir Colaborador</button>
                                <button type="button" class="btn btn-secondary" onclick="hideAddEmployeeForm()">Cancelar</button>
                            </div>
                        </form>
                    </div>
                </div>
                
                <!-- Tabla de tareas -->
                <div class="card">
                    <div class="card-body p-0">
                        <div class="table-responsive">
                            <table class="table table-striped table-hover mb-0">
                                <thead class="table-dark">
                                    <tr>
                                        <th>ID</th>
                                        <th>Tarea <small>(click para editar)</small></th>
                                        <th>Colaborador <small>(click para editar)</small></th>
                                        <th>Fecha Inicio <small>(click para editar)</small></th>
                                        <th>Fecha Final <small>(click para editar)</small></th>
                                        <th>Estado <small>(click para editar)</small></th>
                                        <th>Acciones</th>
                                    </tr>
                                </thead>
                                <tbody>
                                    {% for task in tasks %}
                                    <tr class="status-{{ task.estado.lower().replace(' ', '-') }}">
                                        <td>{{ task.id }}</td>
                                        <td>
                                            <span class="editable-field" 
                                                  data-field="tarea" 
                                                  data-id="{{ task.id }}"
                                                  title="Click para editar">{{ task.tarea }}</span>
                                        </td>
                                        <td>
                                            <span class="editable-field editable-collaborator" 
                                                  data-field="colaborador" 
                                                  data-id="{{ task.id }}"
                                                  title="Click para editar">{{ task.colaborador or '-' }}</span>
                                        </td>
                                        <td>
                                            <span class="editable-field" 
                                                  data-field="fecha_inicio" 
                                                  data-id="{{ task.id }}"
                                                  title="Click para editar">{{ task.fecha_inicio or '-' }}</span>
                                        </td>
                                        <td>
                                            <span class="editable-field" 
                                                  data-field="fecha_final" 
                                                  data-id="{{ task.id }}"
                                                  title="Click para editar">{{ task.fecha_final or '-' }}</span>
                                        </td>
                                        <td>
                                            <span class="editable-field editable-status" 
                                                  data-field="estado" 
                                                  data-id="{{ task.id }}"
                                                  title="Click para editar">{{ task.estado }}</span>
                                        </td>
                                        <td>
                                            <button class="btn btn-sm btn-danger" onclick="deleteTask({{ task.id }})">Eliminar</button>
                                        </td>
                                    </tr>
                                    {% endfor %}
                                </tbody>
                            </table>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </div>
    
    <script>
        function deleteTask(id) {
            if (confirm('¿Estás seguro de que quieres eliminar esta tarea?')) {
                fetch(`/tasks/delete/${id}`, {
                    method: 'DELETE'
                })
                .then(response => response.json())
                .then(data => {
                    if (data.success) {
                        location.reload();
                    } else {
                        alert('Error al eliminar: ' + data.error);
                    }
                })
                .catch(error => {
                    alert('Error de conexión: ' + error);
                });
            }
        }
        
        function showAddEmployeeForm() {
            document.getElementById('addEmployeeForm').style.display = 'block';
            document.getElementById('empName').focus();
        }
        
        function hideAddEmployeeForm() {
            document.getElementById('addEmployeeForm').style.display = 'none';
            document.getElementById('employeeForm').reset();
        }
        
        // Gestión de empleados
        document.getElementById('employeeForm').addEventListener('submit', function(e) {
            e.preventDefault();
            
            const formData = {
                name: document.getElementById('empName').value.trim(),
                email: document.getElementById('empEmail').value.trim(),
                rol: document.getElementById('empRol').value.trim(),
                department: document.getElementById('empDepartment').value.trim()
            };
            
            if (!formData.name || !formData.email || !formData.rol) {
                alert('Por favor, completa todos los campos obligatorios');
                return;
            }
            
            fetch('/employees', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(formData)
            })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    alert('✅ Colaborador añadido correctamente');
                    hideAddEmployeeForm();
                    loadEmployeeOptions(); // Actualizar opciones
                } else {
                    alert('❌ Error: ' + data.error);
                }
            })
            .catch(error => {
                alert('❌ Error de conexión: ' + error);
            });
        });
        
        function loadEmployeeOptions() {
            fetch('/employees')
            .then(response => response.json())
            .then(employees => {
                // Actualizar opciones disponibles para asignación
                window.availableEmployees = employees;
            })
            .catch(error => console.error('Error loading employees:', error));
        }
        
        function deleteAllTasks() {
            if (confirm('⚠️ ATENCIÓN: ¿Estás COMPLETAMENTE SEGURO de eliminar TODAS las tareas?')) {
                if (confirm('🛑 ÚLTIMA CONFIRMACIÓN: Esto eliminará TODAS las tareas. ¿Confirmas?')) {
                    fetch('/tasks/delete-all', {
                        method: 'DELETE'
                    })
                    .then(response => response.json())
                    .then(data => {
                        if (data.success) {
                            alert('✅ ' + data.message);
                            location.reload();
                        } else {
                            alert('❌ Error al eliminar todo: ' + data.error);
                        }
                    })
                    .catch(error => {
                        alert('❌ Error de conexión: ' + error);
                    });
                }
            }
        }

        // Sistema de búsqueda
        let allRows = [];
        
        function initializeSearch() {
            allRows = Array.from(document.querySelectorAll('tbody tr'));
            const searchInput = document.getElementById('searchInput');
            
            searchInput.addEventListener('input', function() {
                performSearch(this.value);
            });
            
            searchInput.addEventListener('keydown', function(e) {
                if (e.key === 'Escape') {
                    clearSearch();
                }
            });
        }
        
        function performSearch(searchTerm) {
            const term = searchTerm.toLowerCase().trim();
            let visibleCount = 0;
            
            allRows.forEach(row => {
                const tarea = row.cells[1].textContent.toLowerCase();
                const colaborador = row.cells[2].textContent.toLowerCase();
                const estado = row.cells[5].textContent.toLowerCase();
                
                const matches = tarea.includes(term) || 
                              colaborador.includes(term) || 
                              estado.includes(term);
                
                if (matches || term === '') {
                    row.style.display = '';
                    visibleCount++;
                } else {
                    row.style.display = 'none';
                }
            });
            
            document.getElementById('visibleCount').textContent = visibleCount;
            document.getElementById('clearIcon').textContent = term ? '✗' : '🔍';
        }
        
        function clearSearch() {
            document.getElementById('searchInput').value = '';
            performSearch('');
            document.getElementById('searchInput').focus();
        }

        // Sistema de edición inline
        document.addEventListener('DOMContentLoaded', function() {
            let currentlyEditing = null;
            
            // Inicializar búsqueda y cargar empleados
            initializeSearch();
            loadEmployeeOptions();

            // Hacer todos los campos editables
            document.querySelectorAll('.editable-field').forEach(field => {
                field.addEventListener('click', function() {
                    if (currentlyEditing && currentlyEditing !== this) {
                        cancelEdit(currentlyEditing);
                    }
                    startEdit(this);
                });
            });

            function startEdit(element) {
                if (currentlyEditing === element) return;

                currentlyEditing = element;
                const originalValue = element.textContent.trim();
                const field = element.getAttribute('data-field');
                const taskId = element.getAttribute('data-id');
                
                element.classList.add('editing');
                
                // Crear input apropiado según el campo
                let inputElement;
                if (field === 'colaborador') {
                    inputElement = document.createElement('select');
                    inputElement.className = 'edit-select';
                    inputElement.innerHTML = '<option value="">Sin asignar</option>';
                    
                    // Añadir empleados disponibles
                    if (window.availableEmployees) {
                        window.availableEmployees.forEach(emp => {
                            const option = document.createElement('option');
                            option.value = emp.name;
                            option.textContent = `${emp.name} (${emp.rol})`;
                            inputElement.appendChild(option);
                        });
                    }
                    
                    inputElement.value = originalValue === '-' ? '' : originalValue;
                } else if (field === 'estado') {
                    inputElement = document.createElement('select');
                    inputElement.className = 'edit-select';
                    inputElement.innerHTML = `
                        <option value="Pendiente">Pendiente</option>
                        <option value="En curso">En curso</option>
                        <option value="Completado">Completado</option>
                    `;
                    inputElement.value = originalValue;
                } else if (field === 'notas') {
                    inputElement = document.createElement('textarea');
                    inputElement.className = 'edit-textarea';
                    inputElement.rows = 3;
                    inputElement.value = originalValue === '-' ? '' : originalValue;
                } else {
                    inputElement = document.createElement('input');
                    inputElement.className = 'edit-input';
                    inputElement.type = 'text';
                    inputElement.value = originalValue === '-' ? '' : originalValue;
                }
                
                // Crear botones de acción
                const buttonContainer = document.createElement('div');
                buttonContainer.className = 'save-cancel-buttons';
                
                const saveBtn = document.createElement('button');
                saveBtn.className = 'btn btn-sm btn-success me-1';
                saveBtn.textContent = '✓';
                saveBtn.onclick = () => saveEdit(element, inputElement, taskId, field, originalValue);
                
                const cancelBtn = document.createElement('button');
                cancelBtn.className = 'btn btn-sm btn-secondary';
                cancelBtn.textContent = '✗';
                cancelBtn.onclick = () => cancelEdit(element, originalValue);
                
                buttonContainer.appendChild(saveBtn);
                buttonContainer.appendChild(cancelBtn);
                
                // Reemplazar contenido
                element.innerHTML = '';
                element.appendChild(inputElement);
                element.appendChild(buttonContainer);
                
                inputElement.focus();
                if (inputElement.select) inputElement.select();
                
                // Guardar con Enter, cancelar con Escape
                inputElement.addEventListener('keydown', function(e) {
                    if (e.key === 'Enter' && !e.shiftKey) {
                        e.preventDefault();
                        saveEdit(element, inputElement, taskId, field, originalValue);
                    } else if (e.key === 'Escape') {
                        e.preventDefault();
                        cancelEdit(element, originalValue);
                    }
                });
            }

            function saveEdit(element, inputElement, taskId, field, originalValue) {
                const newValue = inputElement.value.trim();
                
                // Mostrar loading
                element.innerHTML = '<div class="spinner-border spinner-border-sm" role="status"></div>';
                
                fetch(`/tasks/edit/${taskId}`, {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify({
                        field: field,
                        value: newValue
                    })
                })
                .then(response => response.json())
                .then(data => {
                    if (data.success) {
                        // Mostrar valor actualizado
                        const displayValue = newValue || '-';
                        element.textContent = displayValue;
                        element.classList.remove('editing');
                        currentlyEditing = null;
                        
                        // Actualizar clase de estado si es necesario
                        if (field === 'estado') {
                            const row = element.closest('tr');
                            row.className = row.className.replace(/status-[\\w-]+/g, '');
                            row.classList.add('status-' + newValue.toLowerCase().replace(' ', '-'));
                        }
                        
                        // Efecto visual de éxito
                        element.style.backgroundColor = '#d4edda';
                        setTimeout(() => {
                            element.style.backgroundColor = '';
                        }, 1000);
                    } else {
                        alert('Error al guardar: ' + data.error);
                        cancelEdit(element, originalValue);
                    }
                })
                .catch(error => {
                    alert('Error de conexión: ' + error);
                    cancelEdit(element, originalValue);
                });
            }

            function cancelEdit(element, originalValue = null) {
                if (originalValue !== null) {
                    element.textContent = originalValue;
                }
                element.classList.remove('editing');
                currentlyEditing = null;
            }
        });
    </script>
</body>
</html>
'''

# Template para analytics con gráficos
TASKS_ANALYTICS_TEMPLATE = '''
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Analytics de Tareas - DiversIA</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
    <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
    <style>
        .metric-card { 
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            border: none;
            border-radius: 15px;
        }
        .chart-container { 
            height: 400px; 
            position: relative;
        }
        .analytics-card {
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
            border-radius: 10px;
        }
    </style>
</head>
<body class="bg-light">
    <div class="container-fluid py-4">
        <div class="d-flex justify-content-between align-items-center mb-4">
            <h1>📊 Analytics de Tareas - DiversIA</h1>
            <div>
                <a href="/tasks" class="btn btn-outline-primary me-2">← Ver Tareas</a>
                <a href="/crm-minimal" class="btn btn-outline-secondary me-2">CRM</a>
            </div>
        </div>
        
        <!-- Métricas principales -->
        <div class="row mb-4">
            <div class="col-md-3">
                <div class="card metric-card">
                    <div class="card-body text-center">
                        <h3>{{ total_tasks }}</h3>
                        <p class="mb-0">Total Tareas</p>
                    </div>
                </div>
            </div>
            <div class="col-md-3">
                <div class="card metric-card">
                    <div class="card-body text-center">
                        <h3>{{ completadas }}</h3>
                        <p class="mb-0">Completadas</p>
                        <small>{% if total_tasks > 0 %}{{ (completadas / total_tasks * 100)|round(1) }}%{% else %}0%{% endif %}</small>
                    </div>
                </div>
            </div>
            <div class="col-md-3">
                <div class="card metric-card">
                    <div class="card-body text-center">
                        <h3>{{ en_curso }}</h3>
                        <p class="mb-0">En Progreso</p>
                        <small>{% if total_tasks > 0 %}{{ (en_curso / total_tasks * 100)|round(1) }}%{% else %}0%{% endif %}</small>
                    </div>
                </div>
            </div>
            <div class="col-md-3">
                <div class="card metric-card">
                    <div class="card-body text-center">
                        <h3>{{ pendientes }}</h3>
                        <p class="mb-0">Pendientes</p>
                        <small>{% if total_tasks > 0 %}{{ (pendientes / total_tasks * 100)|round(1) }}%{% else %}0%{% endif %}</small>
                    </div>
                </div>
            </div>
        </div>
        
        <!-- Gráficos -->
        <div class="row">
            <div class="col-md-6">
                <div class="card analytics-card">
                    <div class="card-header">
                        <h5>📈 Estado General de Tareas</h5>
                    </div>
                    <div class="card-body">
                        <div class="chart-container">
                            <canvas id="statusChart"></canvas>
                        </div>
                    </div>
                </div>
            </div>
            
            <div class="col-md-6">
                <div class="card analytics-card">
                    <div class="card-header">
                        <h5>👥 Productividad por Colaborador</h5>
                    </div>
                    <div class="card-body">
                        <div class="chart-container">
                            <canvas id="collaboratorChart"></canvas>
                        </div>
                    </div>
                </div>
            </div>
        </div>
        
        <!-- Tabla de rendimiento -->
        <div class="row mt-4">
            <div class="col-12">
                <div class="card analytics-card">
                    <div class="card-header">
                        <h5>📋 Rendimiento Detallado por Colaborador</h5>
                    </div>
                    <div class="card-body">
                        <div class="table-responsive">
                            <table class="table table-striped">
                                <thead>
                                    <tr>
                                        <th>Colaborador</th>
                                        <th>Total Tareas</th>
                                        <th>Completadas</th>
                                        <th>En Progreso</th>
                                        <th>Pendientes</th>
                                        <th>% Completado</th>
                                        <th>Eficiencia</th>
                                    </tr>
                                </thead>
                                <tbody>
                                    {% for collab in tasks_by_collaborator %}
                                    <tr>
                                        <td><strong>{{ collab.colaborador or 'Sin asignar' }}</strong></td>
                                        <td><span class="badge bg-primary">{{ collab.total_tasks }}</span></td>
                                        <td><span class="badge bg-success">{{ collab.completed }}</span></td>
                                        <td><span class="badge bg-warning">{{ collab.in_progress }}</span></td>
                                        <td><span class="badge bg-danger">{{ collab.pending }}</span></td>
                                        <td>
                                            {% set completion_rate = (collab.completed / collab.total_tasks * 100) if collab.total_tasks > 0 else 0 %}
                                            {{ completion_rate|round(1) }}%
                                        </td>
                                        <td>
                                            {% if completion_rate >= 80 %}
                                                <span class="badge bg-success">Excelente</span>
                                            {% elif completion_rate >= 60 %}
                                                <span class="badge bg-warning">Bueno</span>
                                            {% elif completion_rate >= 40 %}
                                                <span class="badge bg-secondary">Regular</span>
                                            {% else %}
                                                <span class="badge bg-danger">Necesita Mejora</span>
                                            {% endif %}
                                        </td>
                                    </tr>
                                    {% endfor %}
                                </tbody>
                            </table>
                        </div>
                    </div>
                </div>
            </div>
        </div>
        
        <!-- Insights de optimización -->
        <div class="row mt-4">
            <div class="col-12">
                <div class="card analytics-card">
                    <div class="card-header">
                        <h5>💡 Insights de Optimización</h5>
                    </div>
                    <div class="card-body">
                        <div class="row">
                            <div class="col-md-4">
                                <h6>🎯 Recomendaciones</h6>
                                <ul class="list-unstyled">
                                    {% if pendientes > en_curso + completadas %}
                                    <li><i class="text-warning">⚠️</i> Alto número de tareas pendientes</li>
                                    <li><i class="text-info">💡</i> Considerar reasignar recursos</li>
                                    {% endif %}
                                    {% if en_curso > completadas * 2 %}
                                    <li><i class="text-warning">⚠️</i> Muchas tareas en progreso</li>
                                    <li><i class="text-info">💡</i> Revisar bloqueos o dependencias</li>
                                    {% endif %}
                                    {% if completadas > total_tasks * 0.7 %}
                                    <li><i class="text-success">✅</i> Excelente productividad general</li>
                                    {% endif %}
                                </ul>
                            </div>
                            <div class="col-md-4">
                                <h6>📊 Métricas Clave</h6>
                                <ul class="list-unstyled">
                                    <li>Tasa de Finalización: <strong>{% if total_tasks > 0 %}{{ (completadas / total_tasks * 100)|round(1) }}%{% else %}0%{% endif %}</strong></li>
                                    <li>Tareas Activas: <strong>{{ en_curso }}</strong></li>
                                    <li>Backlog: <strong>{{ pendientes }}</strong></li>
                                    <li>Colaboradores Activos: <strong>{{ tasks_by_collaborator|length }}</strong></li>
                                </ul>
                            </div>
                            <div class="col-md-4">
                                <h6>🚀 Próximos Pasos</h6>
                                <ul class="list-unstyled">
                                    <li><i class="text-primary">📋</i> Revisar tareas sin asignar</li>
                                    <li><i class="text-primary">⏰</i> Establecer fechas límite</li>
                                    <li><i class="text-primary">👥</i> Equilibrar carga de trabajo</li>
                                    <li><i class="text-primary">📈</i> Monitorear progreso semanal</li>
                                </ul>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </div>
    
    <script>
        // Gráfico de estado general
        const statusCtx = document.getElementById('statusChart').getContext('2d');
        new Chart(statusCtx, {
            type: 'doughnut',
            data: {
                labels: ['Completadas', 'En Progreso', 'Pendientes'],
                datasets: [{
                    data: [{{ completadas }}, {{ en_curso }}, {{ pendientes }}],
                    backgroundColor: ['#28a745', '#ffc107', '#dc3545'],
                    borderWidth: 2,
                    borderColor: '#fff'
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                    legend: {
                        position: 'bottom'
                    }
                }
            }
        });
        
        // Gráfico de productividad por colaborador
        const collaboratorCtx = document.getElementById('collaboratorChart').getContext('2d');
        const collaboratorData = {
            labels: [{% for collab in tasks_by_collaborator %}'{{ collab.colaborador or "Sin asignar" }}'{% if not loop.last %},{% endif %}{% endfor %}],
            datasets: [{
                label: 'Completadas',
                data: [{% for collab in tasks_by_collaborator %}{{ collab.completed }}{% if not loop.last %},{% endif %}{% endfor %}],
                backgroundColor: '#28a745'
            }, {
                label: 'En Progreso',
                data: [{% for collab in tasks_by_collaborator %}{{ collab.in_progress }}{% if not loop.last %},{% endif %}{% endfor %}],
                backgroundColor: '#ffc107'
            }, {
                label: 'Pendientes',
                data: [{% for collab in tasks_by_collaborator %}{{ collab.pending }}{% if not loop.last %},{% endif %}{% endfor %}],
                backgroundColor: '#dc3545'
            }]
        };
        
        new Chart(collaboratorCtx, {
            type: 'bar',
            data: collaboratorData,
            options: {
                responsive: true,
                maintainAspectRatio: false,
                scales: {
                    x: {
                        stacked: true
                    },
                    y: {
                        stacked: true,
                        beginAtZero: true
                    }
                },
                plugins: {
                    legend: {
                        position: 'top'
                    }
                }
            }
        });
    </script>
</body>
</html>
'''

print("✅ Task Manager cargado")