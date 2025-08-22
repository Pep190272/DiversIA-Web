"""
Sistema de Gestión de Tareas para DiversIA
Gestión completa de tareas de empleados
"""

import csv
import io
from datetime import datetime
from flask import request, jsonify, render_template_string, flash, redirect, session
from app import app, db
from models import Task

@app.route('/tasks')
def tasks_dashboard():
    """Dashboard principal de gestión de tareas"""
    # Verificar autenticación admin
    if 'admin_ok' not in session or not session.get('admin_ok'):
        return redirect('/diversia-admin')
    
    # Obtener todas las tareas
    tasks = Task.query.all()
    total_tasks = len(tasks)
    
    return render_template_string(TASKS_TABLE_TEMPLATE, 
                                tasks=tasks,
                                total_tasks=total_tasks)

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
                                            <span class="editable-field" 
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
            
            // Inicializar búsqueda
            initializeSearch();

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
                if (field === 'estado') {
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

print("✅ Task Manager cargado")