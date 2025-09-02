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
from email_notifications import send_employee_notification, send_task_assignment_notification

# Google Drive imports
try:
    from google_auth_oauthlib.flow import Flow
    from google.auth.transport.requests import Request
    from google.oauth2.credentials import Credentials
    from googleapiclient.discovery import build
    from googleapiclient.errors import HttpError
    import json
    import os
    import secrets
    GOOGLE_DRIVE_AVAILABLE = True
except ImportError:
    GOOGLE_DRIVE_AVAILABLE = False

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
                # Buscar estado en diferentes posibles nombres de columna
                estado_value = (row.get('Estado', '') or 
                               row.get('Pendiente', '') or 
                               row.get('Status', '') or 
                               'Pendiente').strip()
                existing.estado = estado_value
                existing.updated_at = datetime.now()
                updated_count += 1
            else:
                # Crear nueva tarea
                new_task = Task(
                    tarea = tarea_name,
                    colaborador = row.get('Colaborador', '').strip(),
                    fecha_inicio = row.get('Fecha de inicio', '').strip(),
                    fecha_final = row.get('Fecha final', '').strip(),
                    estado = (row.get('Estado', '') or 
                             row.get('Pendiente', '') or 
                             row.get('Status', '') or 
                             'Pendiente').strip(),
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
            old_collaborator = task.colaborador
            task.colaborador = value
            
            # Si se asigna un nuevo colaborador, enviar notificación
            if value and value != old_collaborator:
                employee = Employee.query.filter_by(name=value, active=True).first()
                if employee:
                    task_data = {
                        'tarea': task.tarea,
                        'estado': task.estado,
                        'fecha_inicio': task.fecha_inicio,
                        'fecha_final': task.fecha_final
                    }
                    send_task_assignment_notification(task_data, employee.email)
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

@app.route('/tasks/add', methods=['POST'])
def add_task_manual():
    """Añadir tarea manualmente"""
    if 'admin_ok' not in session or not session.get('admin_ok'):
        return jsonify({'error': 'No autorizado'}), 403
    
    data = request.get_json()
    try:
        new_task = Task(
            tarea=data.get('tarea', '').strip(),
            colaborador=data.get('colaborador', '').strip(),
            fecha_inicio=data.get('fecha_inicio', '').strip(),
            fecha_final=data.get('fecha_final', '').strip(),
            estado=data.get('estado', 'Pendiente').strip(),
            notas=data.get('notas', '').strip()
        )
        db.session.add(new_task)
        db.session.commit()
        
        # Si se asigna a un colaborador, enviar notificación
        if new_task.colaborador:
            employee = Employee.query.filter_by(name=new_task.colaborador, active=True).first()
            if employee:
                task_data = {
                    'tarea': new_task.tarea,
                    'estado': new_task.estado,
                    'fecha_inicio': new_task.fecha_inicio,
                    'fecha_final': new_task.fecha_final
                }
                send_task_assignment_notification(task_data, employee.email)
        
        return jsonify({'success': True, 'message': 'Tarea añadida correctamente'})
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
            
            # Enviar notificaciones por email
            employee_data = {
                'name': new_employee.name,
                'email': new_employee.email,
                'rol': new_employee.rol,
                'department': new_employee.department
            }
            
            email_sent = send_employee_notification(employee_data)
            
            if email_sent:
                return jsonify({'success': True, 'message': 'Empleado añadido y notificaciones enviadas'})
            else:
                return jsonify({'success': True, 'message': 'Empleado añadido (error en notificaciones por email)'})
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
                        <a href="/colaboradores" class="btn btn-primary me-2">👥 Colaboradores</a>
                        <a href="/crm-minimal" class="btn btn-outline-secondary me-2">← CRM</a>
                        <a href="/diversia-admin-logout" class="btn btn-outline-danger">Salir</a>
                    </div>
                </div>
                
                <!-- Acciones rápidas -->
                <div class="row mb-3">
                    <div class="col-md-6">
                        <div class="card">
                            <div class="card-header">
                                <h6 class="mb-0">📁 Importar Tareas</h6>
                            </div>
                            <div class="card-body">
                                <!-- Importar desde archivo local -->
                                <form action="/tasks/import" method="post" enctype="multipart/form-data" class="d-flex mb-2">
                                    <input type="file" name="file" class="form-control me-2" accept=".csv" required>
                                    <button type="submit" class="btn btn-success btn-sm">📂 Local</button>
                                </form>
                                
                                <!-- Importar desde Google Drive -->
                                <div class="d-flex">
                                    <button class="btn btn-primary btn-sm" onclick="showGoogleDriveModal()">
                                        🌐 Google Drive
                                    </button>
                                    <small class="text-muted ms-2 align-self-center">CSV y Google Sheets</small>
                                </div>
                            </div>
                        </div>
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
                        <button class="btn btn-success me-2" onclick="showAddTaskForm()">➕ Añadir Tarea</button>
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
                
                <!-- Formulario añadir tarea -->
                <div id="addTaskForm" class="card mb-4" style="display: none;">
                    <div class="card-header">
                        <h5>Añadir Nueva Tarea</h5>
                    </div>
                    <div class="card-body">
                        <form id="taskForm">
                            <div class="row">
                                <div class="col-md-12">
                                    <div class="mb-3">
                                        <label class="form-label">Descripción de la Tarea *</label>
                                        <textarea class="form-control" id="taskTarea" rows="2" required 
                                                placeholder="Describe la tarea a realizar..."></textarea>
                                    </div>
                                </div>
                                <div class="col-md-6">
                                    <div class="mb-3">
                                        <label class="form-label">Asignar a Colaborador</label>
                                        <select class="form-control" id="taskColaborador">
                                            <option value="">Sin asignar</option>
                                            {% for emp in employees %}
                                            <option value="{{ emp.name }}">{{ emp.name }} ({{ emp.rol }})</option>
                                            {% endfor %}
                                        </select>
                                    </div>
                                </div>
                                <div class="col-md-6">
                                    <div class="mb-3">
                                        <label class="form-label">Estado</label>
                                        <select class="form-control" id="taskEstado">
                                            <option value="Pendiente">Pendiente</option>
                                            <option value="En curso">En curso</option>
                                            <option value="Completado">Completado</option>
                                        </select>
                                    </div>
                                </div>
                                <div class="col-md-6">
                                    <div class="mb-3">
                                        <label class="form-label">Fecha de Inicio</label>
                                        <input type="date" class="form-control" id="taskFechaInicio">
                                    </div>
                                </div>
                                <div class="col-md-6">
                                    <div class="mb-3">
                                        <label class="form-label">Fecha Límite</label>
                                        <input type="date" class="form-control" id="taskFechaFinal">
                                    </div>
                                </div>
                                <div class="col-md-12">
                                    <div class="mb-3">
                                        <label class="form-label">Notas Adicionales</label>
                                        <textarea class="form-control" id="taskNotas" rows="2" 
                                                placeholder="Notas opcionales sobre la tarea..."></textarea>
                                    </div>
                                </div>
                            </div>
                            <div class="d-flex gap-2">
                                <button type="submit" class="btn btn-success">Crear Tarea</button>
                                <button type="button" class="btn btn-secondary" onclick="hideAddTaskForm()">Cancelar</button>
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
    
    <!-- Modal de Google Drive -->
    <div class="modal fade" id="googleDriveModal" tabindex="-1">
        <div class="modal-dialog modal-lg">
            <div class="modal-content">
                <div class="modal-header">
                    <h5 class="modal-title">🌐 Importar desde Google Drive</h5>
                    <button type="button" class="btn-close" data-bs-dismiss="modal"></button>
                </div>
                <div class="modal-body">
                    <div id="gdrive-loading" class="text-center py-4">
                        <div class="spinner-border text-primary" role="status"></div>
                        <p class="mt-2">Cargando archivos de Google Drive...</p>
                    </div>
                    
                    <div id="gdrive-error" class="alert alert-warning d-none">
                        <h6>⚠️ Google Drive no configurado</h6>
                        <p>Para usar esta función necesitas configurar las credenciales de Google Drive.</p>
                        <small>Contacta al administrador para obtener acceso.</small>
                    </div>
                    
                    <div id="gdrive-files" class="d-none">
                        <h6>📁 Archivos disponibles (CSV y Google Sheets):</h6>
                        <div id="files-list" class="mt-3">
                            <!-- Los archivos se cargarán aquí dinámicamente -->
                        </div>
                    </div>
                </div>
                <div class="modal-footer">
                    <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Cerrar</button>
                    <button type="button" class="btn btn-primary" id="refresh-files" onclick="loadGoogleDriveFiles()">🔄 Actualizar</button>
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
        
        function showAddTaskForm() {
            document.getElementById('addTaskForm').style.display = 'block';
            document.getElementById('taskTarea').focus();
        }
        
        function hideAddTaskForm() {
            document.getElementById('addTaskForm').style.display = 'none';
            document.getElementById('taskForm').reset();
        }
        
        // ===== GOOGLE DRIVE FUNCTIONS =====
        function showGoogleDriveModal() {
            // Primero intentar autenticar con Google
            authenticateWithGoogle();
        }
        
        function authenticateWithGoogle() {
            fetch('/auth/google-drive')
                .then(response => response.json())
                .then(data => {
                    if (data.success && data.configured && data.auth_url) {
                        // Abrir ventana de autenticación de Google
                        window.open(data.auth_url, 'google-auth', 'width=500,height=600,scrollbars=yes,resizable=yes');
                    } else {
                        // Mostrar modal con mensaje de configuración
                        showGoogleDriveConfigModal(data.message || 'Configuración necesaria');
                    }
                })
                .catch(error => {
                    console.error('Error de autenticación:', error);
                    showGoogleDriveConfigModal('Error de conexión');
                });
        }
        
        function showGoogleDriveConfigModal(message = 'Configuración necesaria') {
            const modal = new bootstrap.Modal(document.getElementById('googleDriveModal'));
            
            // Mostrar mensaje de configuración
            document.getElementById('gdrive-loading').classList.add('d-none');
            document.getElementById('gdrive-files').classList.add('d-none');
            document.getElementById('gdrive-error').classList.remove('d-none');
            document.getElementById('gdrive-error').innerHTML = `
                <div class="alert alert-info">
                    <h6>🔧 Google Drive - Configuración Pendiente</h6>
                    <p><strong>La función de Google Drive no está completamente configurada aún.</strong></p>
                    <p>Mientras tanto, puedes usar la opción <strong>"📂 Local"</strong> para subir archivos CSV desde tu computadora, que funciona perfectamente.</p>
                    
                    <hr>
                    <small class="text-muted">
                        <strong>Para el administrador:</strong> Para habilitar Google Drive, configura las variables GOOGLE_CLIENT_ID y GOOGLE_CLIENT_SECRET.
                    </small>
                </div>
            `;
            
            modal.show();
        }
        
        function loadGoogleDriveFiles() {
            const loading = document.getElementById('gdrive-loading');
            const error = document.getElementById('gdrive-error');
            const files = document.getElementById('gdrive-files');
            
            // Mostrar loading, ocultar otros
            loading.classList.remove('d-none');
            error.classList.add('d-none');
            files.classList.add('d-none');
            
            fetch('/tasks/google-drive-files')
                .then(response => response.json())
                .then(data => {
                    loading.classList.add('d-none');
                    
                    if (data.success) {
                        displayGoogleDriveFiles(data.files);
                        files.classList.remove('d-none');
                    } else {
                        error.classList.remove('d-none');
                    }
                })
                .catch(err => {
                    loading.classList.add('d-none');
                    error.classList.remove('d-none');
                    console.error('Error cargando archivos de Google Drive:', err);
                });
        }
        
        function displayGoogleDriveFiles(fileList) {
            const container = document.getElementById('files-list');
            
            if (fileList.length === 0) {
                container.innerHTML = '<div class="alert alert-info">No se encontraron archivos CSV o Google Sheets</div>';
                return;
            }
            
            let html = '';
            fileList.forEach(file => {
                const typeIcon = file.type === 'Google Sheets' ? '📊' : '📄';
                const typeClass = file.type === 'Google Sheets' ? 'text-success' : 'text-primary';
                
                html += `
                    <div class="card mb-2">
                        <div class="card-body py-2">
                            <div class="row align-items-center">
                                <div class="col-md-6">
                                    <h6 class="mb-1">${typeIcon} ${file.name}</h6>
                                    <small class="${typeClass}">${file.type}</small>
                                </div>
                                <div class="col-md-3">
                                    <small class="text-muted">
                                        ${file.created ? new Date(file.created).toLocaleDateString('es-ES') : 'N/A'}
                                    </small>
                                </div>
                                <div class="col-md-3 text-end">
                                    <button class="btn btn-sm btn-primary me-1" 
                                            onclick="importFromGoogleDrive('${file.id}', '${file.name}')">
                                        📥 Importar
                                    </button>
                                    ${file.view_link ? `<a href="${file.view_link}" target="_blank" class="btn btn-sm btn-outline-secondary">👁️</a>` : ''}
                                </div>
                            </div>
                        </div>
                    </div>
                `;
            });
            
            container.innerHTML = html;
        }
        
        function importFromGoogleDrive(fileId, fileName) {
            if (!confirm(`¿Importar tareas desde "${fileName}"?`)) {
                return;
            }
            
            // Mostrar loading en el botón
            const buttons = document.querySelectorAll('button');
            buttons.forEach(btn => btn.disabled = true);
            
            fetch('/tasks/import-from-google-drive', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ file_id: fileId })
            })
            .then(response => response.json())
            .then(data => {
                buttons.forEach(btn => btn.disabled = false);
                
                if (data.success) {
                    alert(`✅ ${data.message}`);
                    // Cerrar modal y recargar página
                    bootstrap.Modal.getInstance(document.getElementById('googleDriveModal')).hide();
                    location.reload();
                } else {
                    alert(`❌ Error: ${data.error}`);
                }
            })
            .catch(error => {
                buttons.forEach(btn => btn.disabled = false);
                alert(`❌ Error de conexión: ${error}`);
                console.error('Error importando desde Google Drive:', error);
            });
        }

        
        // Gestión de tareas manuales
        document.getElementById('taskForm').addEventListener('submit', function(e) {
            e.preventDefault();
            
            const formData = {
                tarea: document.getElementById('taskTarea').value.trim(),
                colaborador: document.getElementById('taskColaborador').value.trim(),
                estado: document.getElementById('taskEstado').value.trim(),
                fecha_inicio: document.getElementById('taskFechaInicio').value.trim(),
                fecha_final: document.getElementById('taskFechaFinal').value.trim(),
                notas: document.getElementById('taskNotas').value.trim()
            };
            
            if (!formData.tarea) {
                alert('Por favor, describe la tarea');
                return;
            }
            
            fetch('/tasks/add', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(formData)
            })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    alert('✅ Tarea añadida correctamente');
                    hideAddTaskForm();
                    location.reload(); // Actualizar la tabla
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

# ============================================
# GOOGLE DRIVE INTEGRATION
# ============================================

# Configuración OAuth2 para Google Drive
SCOPES = [
    'https://www.googleapis.com/auth/drive.readonly',
    'https://www.googleapis.com/auth/spreadsheets.readonly'
]

# Configuración OAuth2 simplificada (usar variables de entorno en producción)
def get_client_config():
    """Obtener configuración de cliente desde variables de entorno"""
    client_id = os.environ.get('GOOGLE_CLIENT_ID')
    client_secret = os.environ.get('GOOGLE_CLIENT_SECRET')
    
    if not client_id or not client_secret:
        return None
    
    return {
        "web": {
            "client_id": client_id,
            "client_secret": client_secret,
            "auth_uri": "https://accounts.google.com/o/oauth2/auth",
            "token_uri": "https://oauth2.googleapis.com/token",
            "redirect_uris": [request.url_root.rstrip('/') + '/oauth2callback'] if request else ["http://localhost:5000/oauth2callback"]
        }
    }

@app.route('/auth/google-drive')
def auth_google_drive():
    """Iniciar autenticación OAuth2 con Google Drive"""
    if not GOOGLE_DRIVE_AVAILABLE:
        return jsonify({'error': 'Google Drive no disponible', 'configured': False}), 400
    
    # Verificar si están configuradas las credenciales
    client_config = get_client_config()
    if not client_config:
        return jsonify({
            'error': 'Credenciales de Google no configuradas', 
            'configured': False,
            'message': 'Necesitas configurar GOOGLE_CLIENT_ID y GOOGLE_CLIENT_SECRET'
        }), 400
    
    try:
        # Crear flow OAuth2
        flow = Flow.from_client_config(
            client_config,
            scopes=SCOPES
        )
        flow.redirect_uri = request.url_root.rstrip('/') + '/oauth2callback'
        
        # Generar estado para seguridad
        state = secrets.token_urlsafe(32)
        session['oauth_state'] = state
        
        # Obtener URL de autorización
        authorization_url, _ = flow.authorization_url(
            access_type='offline',
            include_granted_scopes='true',
            state=state,
            prompt='select_account'  # Esto fuerza la selección de cuenta
        )
        
        return jsonify({
            'success': True,
            'configured': True,
            'auth_url': authorization_url
        })
        
    except Exception as e:
        return jsonify({'error': f'Error de autenticación: {str(e)}', 'configured': False}), 500

@app.route('/oauth2callback')
def oauth2callback():
    """Callback para completar autenticación OAuth2"""
    if not GOOGLE_DRIVE_AVAILABLE:
        return "Google Drive no disponible", 400
    
    try:
        # Verificar estado para seguridad
        state = request.args.get('state')
        if state != session.get('oauth_state'):
            return "Estado de OAuth inválido", 400
        
        # Completar flujo OAuth2
        flow = Flow.from_client_config(
            CLIENT_CONFIG,
            scopes=SCOPES,
            state=state
        )
        flow.redirect_uri = request.url_root.rstrip('/') + '/oauth2callback'
        
        # Obtener token
        flow.fetch_token(authorization_response=request.url)
        
        # Guardar credenciales en sesión
        credentials = flow.credentials
        session['google_credentials'] = {
            'token': credentials.token,
            'refresh_token': credentials.refresh_token,
            'token_uri': credentials.token_uri,
            'client_id': credentials.client_id,
            'client_secret': credentials.client_secret,
            'scopes': credentials.scopes
        }
        
        # Redirigir de vuelta a tareas con éxito
        return '''
        <script>
            alert('✅ Autenticación exitosa con Google Drive');
            window.location.href = '/tasks';
        </script>
        '''
        
    except Exception as e:
        return f"Error en callback: {str(e)}", 500

def get_google_drive_service():
    """Obtener servicio de Google Drive usando credenciales de sesión"""
    if not GOOGLE_DRIVE_AVAILABLE:
        return None
    
    try:
        # Obtener credenciales de la sesión
        creds_data = session.get('google_credentials')
        if not creds_data:
            return None
        
        # Crear objeto de credenciales
        credentials = Credentials(
            token=creds_data['token'],
            refresh_token=creds_data.get('refresh_token'),
            token_uri=creds_data['token_uri'],
            client_id=creds_data['client_id'],
            client_secret=creds_data['client_secret'],
            scopes=creds_data['scopes']
        )
        
        # Refrescar token si es necesario
        if credentials.expired and credentials.refresh_token:
            credentials.refresh(Request())
            # Actualizar sesión con nuevo token
            session['google_credentials']['token'] = credentials.token
        
        # Construir servicio
        service = build('drive', 'v3', credentials=credentials)
        return service
        
    except Exception as e:
        print(f"Error inicializando Google Drive: {e}")
        return None

def get_google_sheets_service():
    """Obtener servicio de Google Sheets usando credenciales de sesión"""
    if not GOOGLE_DRIVE_AVAILABLE:
        return None
        
    try:
        # Obtener credenciales de la sesión
        creds_data = session.get('google_credentials')
        if not creds_data:
            return None
        
        # Crear objeto de credenciales
        credentials = Credentials(
            token=creds_data['token'],
            refresh_token=creds_data.get('refresh_token'),
            token_uri=creds_data['token_uri'],
            client_id=creds_data['client_id'],
            client_secret=creds_data['client_secret'],
            scopes=creds_data['scopes']
        )
        
        # Refrescar token si es necesario
        if credentials.expired and credentials.refresh_token:
            credentials.refresh(Request())
            # Actualizar sesión con nuevo token
            session['google_credentials']['token'] = credentials.token
        
        # Construir servicio
        service = build('sheets', 'v4', credentials=credentials)
        return service
        
    except Exception as e:
        print(f"Error inicializando Google Sheets: {e}")
        return None

@app.route('/tasks/google-drive-files')
def list_google_drive_files():
    """Listar archivos CSV y hojas de cálculo de Google Drive"""
    if 'admin_ok' not in session or not session.get('admin_ok'):
        return jsonify({'error': 'No autorizado'}), 403
        
    if not GOOGLE_DRIVE_AVAILABLE:
        return jsonify({'error': 'Google Drive no disponible'}), 400
    
    try:
        service = get_google_drive_service()
        if not service:
            return jsonify({'error': 'No se pudo conectar a Google Drive. Verifica las credenciales.'}), 400
        
        # Buscar archivos CSV y hojas de cálculo
        query = "mimeType='text/csv' or mimeType='application/vnd.google-apps.spreadsheet'"
        results = service.files().list(
            q=query,
            fields="files(id, name, mimeType, createdTime, webViewLink, size)",
            orderBy='createdTime desc',
            pageSize=50
        ).execute()
        
        files = results.get('files', [])
        
        # Formatear información de archivos
        formatted_files = []
        for file in files:
            formatted_files.append({
                'id': file['id'],
                'name': file['name'],
                'type': 'Google Sheets' if file['mimeType'] == 'application/vnd.google-apps.spreadsheet' else 'CSV',
                'created': file.get('createdTime', ''),
                'view_link': file.get('webViewLink', ''),
                'size': file.get('size', 'N/A')
            })
        
        return jsonify({
            'success': True,
            'files': formatted_files,
            'count': len(formatted_files)
        })
        
    except HttpError as e:
        return jsonify({'error': f'Error de Google Drive: {e}'}), 400
    except Exception as e:
        return jsonify({'error': f'Error: {str(e)}'}), 500

@app.route('/tasks/import-from-google-drive', methods=['POST'])
def import_tasks_from_google_drive():
    """Importar tareas desde Google Drive (CSV o Google Sheets)"""
    if 'admin_ok' not in session or not session.get('admin_ok'):
        return jsonify({'error': 'No autorizado'}), 403
    
    if not GOOGLE_DRIVE_AVAILABLE:
        flash('Google Drive no está disponible', 'error')
        return redirect('/tasks')
    
    data = request.get_json()
    file_id = data.get('file_id')
    
    if not file_id:
        return jsonify({'error': 'ID de archivo requerido'}), 400
    
    try:
        drive_service = get_google_drive_service()
        sheets_service = get_google_sheets_service()
        
        if not drive_service:
            return jsonify({'error': 'No se pudo conectar a Google Drive'}), 400
        
        # Obtener metadatos del archivo
        file_metadata = drive_service.files().get(fileId=file_id).execute()
        file_name = file_metadata['name']
        mime_type = file_metadata['mimeType']
        
        csv_content = None
        
        if mime_type == 'application/vnd.google-apps.spreadsheet':
            # Es una hoja de cálculo de Google
            if not sheets_service:
                return jsonify({'error': 'No se pudo conectar a Google Sheets'}), 400
            
            # Exportar como CSV
            request_export = drive_service.files().export_media(
                fileId=file_id,
                mimeType='text/csv'
            )
            csv_content = request_export.execute().decode('utf-8')
            
        elif mime_type == 'text/csv':
            # Es un archivo CSV regular
            request_download = drive_service.files().get_media(fileId=file_id)
            csv_content = request_download.execute().decode('utf-8')
        else:
            return jsonify({'error': 'Tipo de archivo no soportado'}), 400
        
        # Procesar el contenido CSV
        if not csv_content:
            return jsonify({'error': 'No se pudo obtener el contenido del archivo'}), 400
        
        # Usar la misma lógica de importación que el CSV upload
        csv_reader = csv.DictReader(io.StringIO(csv_content))
        
        imported_count = 0
        updated_count = 0
        errors = []
        
        for row_num, row in enumerate(csv_reader, start=2):  # Empezar en 2 porque la fila 1 son headers
            try:
                tarea_name = row.get('Tarea', '').strip()
                
                if not tarea_name:
                    continue
                
                # Buscar tarea existente
                existing = Task.query.filter_by(tarea=tarea_name).first()
                
                # Buscar estado en diferentes nombres de columna
                estado_value = (row.get('Estado', '') or 
                               row.get('Pendiente', '') or 
                               row.get('Status', '') or 
                               'Pendiente').strip()
                
                if existing:
                    # Actualizar tarea existente
                    existing.colaborador = row.get('Colaborador', '').strip()
                    existing.fecha_inicio = row.get('Fecha de inicio', '').strip()
                    existing.fecha_final = row.get('Fecha final', '').strip()
                    existing.estado = estado_value
                    existing.updated_at = datetime.now()
                    updated_count += 1
                else:
                    # Crear nueva tarea
                    new_task = Task(
                        tarea = tarea_name,
                        colaborador = row.get('Colaborador', '').strip(),
                        fecha_inicio = row.get('Fecha de inicio', '').strip(),
                        fecha_final = row.get('Fecha final', '').strip(),
                        estado = estado_value,
                        notas = ''
                    )
                    db.session.add(new_task)
                    imported_count += 1
                    
            except Exception as e:
                errors.append(f"Fila {row_num}: {str(e)}")
        
        db.session.commit()
        
        result_message = f'Importación desde Google Drive exitosa: {imported_count} tareas nuevas, {updated_count} actualizadas'
        if errors:
            result_message += f'. {len(errors)} errores encontrados.'
        
        return jsonify({
            'success': True,
            'message': result_message,
            'imported': imported_count,
            'updated': updated_count,
            'errors': errors[:5],  # Mostrar solo los primeros 5 errores
            'source': file_name
        })
        
    except HttpError as e:
        error_msg = f'Error de Google Drive: {e}'
        return jsonify({'error': error_msg}), 400
    except Exception as e:
        db.session.rollback()
        error_msg = f'Error al importar desde Google Drive: {str(e)}'
        return jsonify({'error': error_msg}), 500

print("✅ Task Manager cargado")