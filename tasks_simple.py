from flask import Blueprint, render_template_string, request, jsonify, session, redirect, url_for
from models import db, Task, Employee
from datetime import datetime
import csv
import io

tasks_bp = Blueprint('tasks_simple', __name__)

@tasks_bp.route('/tasks-simple')
def tasks_simple():
    """Tabla de tareas simple y funcional"""
    if 'admin_ok' not in session or not session.get('admin_ok'):
        return redirect('/diversia-admin')
    
    # Obtener todas las tareas
    tasks = Task.query.all()
    
    # Obtener empleados para dropdowns
    employees = Employee.query.filter_by(active=True).all()
    
    return render_template_string(SIMPLE_TASKS_TEMPLATE, tasks=tasks, employees=employees)

@tasks_bp.route('/tasks-simple/edit/<int:task_id>', methods=['POST'])
def edit_task_simple(task_id):
    """Editar tarea"""
    if 'admin_ok' not in session or not session.get('admin_ok'):
        return jsonify({'error': 'No autorizado'}), 403
    
    try:
        task = Task.query.get_or_404(task_id)
        data = request.get_json()
        
        field = data.get('field')
        value = data.get('value')
        
        if field == 'estado':
            task.estado = value
        elif field == 'colaborador':
            task.colaborador = value if value else None
        elif field == 'tarea':
            task.tarea = value
        
        db.session.commit()
        return jsonify({'success': True})
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@tasks_bp.route('/tasks-simple/delete/<int:task_id>', methods=['DELETE'])
def delete_task_simple(task_id):
    """Eliminar tarea"""
    if 'admin_ok' not in session or not session.get('admin_ok'):
        return jsonify({'error': 'No autorizado'}), 403
    
    try:
        task = Task.query.get_or_404(task_id)
        db.session.delete(task)
        db.session.commit()
        return jsonify({'success': True})
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@tasks_bp.route('/tasks-simple/employees')
def get_employees_simple():
    """Obtener empleados para dropdowns"""
    employees = Employee.query.filter_by(active=True).all()
    return jsonify([{
        'name': emp.name,
        'rol': emp.rol
    } for emp in employees])

# Template simple y funcional
SIMPLE_TASKS_TEMPLATE = '''
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Tareas - DiversIA</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
    <style>
        .edit-cell {
            cursor: pointer;
            padding: 5px 8px;
            border-radius: 4px;
            transition: background-color 0.2s;
            min-width: 100px;
            display: inline-block;
        }
        .edit-cell:hover {
            background-color: #e3f2fd;
            border: 1px solid #2196f3;
        }
        .status-pendiente { background-color: #fff3cd; }
        .status-en-curso { background-color: #d1ecf1; }
        .status-terminada { background-color: #d4edda; }
    </style>
</head>
<body>
    <div class="container-fluid mt-4">
        <div class="row">
            <div class="col-12">
                <div class="d-flex justify-content-between align-items-center mb-3">
                    <h2>📋 Gestión de Tareas</h2>
                    <a href="/tasks" class="btn btn-secondary">← Volver al Dashboard</a>
                </div>
                
                <div class="card">
                    <div class="card-body p-0">
                        <div class="table-responsive">
                            <table class="table table-striped table-hover mb-0">
                                <thead class="table-dark">
                                    <tr>
                                        <th>ID</th>
                                        <th>Tarea</th>
                                        <th>Colaborador</th>
                                        <th>Fecha Inicio</th>
                                        <th>Fecha Final</th>
                                        <th>Estado</th>
                                        <th>Acciones</th>
                                    </tr>
                                </thead>
                                <tbody>
                                    {% for task in tasks %}
                                    <tr class="status-{{ (task.estado or 'pendiente').lower().replace(' ', '-') }}">
                                        <td>{{ task.id }}</td>
                                        <td>{{ task.tarea }}</td>
                                        <td>
                                            <span class="edit-cell" 
                                                  onclick="editColaborador(this, {{ task.id }})"
                                                  title="Click para editar">{{ task.colaborador or 'Sin asignar' }}</span>
                                        </td>
                                        <td>{{ task.fecha_inicio or '-' }}</td>
                                        <td>{{ task.fecha_final or '-' }}</td>
                                        <td>
                                            <span class="edit-cell" 
                                                  onclick="editEstado(this, {{ task.id }})"
                                                  title="Click para editar">{{ task.estado or 'Pendiente' }}</span>
                                        </td>
                                        <td>
                                            <button class="btn btn-sm btn-danger" onclick="eliminarTarea({{ task.id }})">Eliminar</button>
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
        // Variables globales
        var empleados = [];
        
        // Cargar empleados
        fetch('/tasks-simple/employees')
        .then(function(response) {
            return response.json();
        })
        .then(function(data) {
            empleados = data;
            console.log('Empleados cargados:', empleados.length);
        });
        
        // Editar estado
        function editEstado(celda, taskId) {
            // Prevenir múltiples ediciones
            if (celda.querySelector('select')) return;
            
            var valorActual = celda.textContent.trim();
            var select = document.createElement('select');
            select.className = 'form-select form-select-sm';
            select.style.minWidth = '120px';
            
            var opciones = [
                {value: 'Pendiente', text: 'Pendiente'},
                {value: 'En curso', text: 'En curso'},
                {value: 'Terminada', text: 'Terminada'}
            ];
            
            for (var i = 0; i < opciones.length; i++) {
                var option = document.createElement('option');
                option.value = opciones[i].value;
                option.text = opciones[i].text;
                if (valorActual === opciones[i].value) {
                    option.selected = true;
                }
                select.appendChild(option);
            }
            
            // Eventos para manejar cambios y cancelación
            select.onchange = function() {
                guardarEstado(this, taskId, celda, valorActual);
            };
            
            select.onblur = function() {
                setTimeout(function() {
                    if (select.parentNode) {
                        celda.textContent = valorActual;
                    }
                }, 200);
            };
            
            select.onkeydown = function(e) {
                if (e.key === 'Escape') {
                    celda.textContent = valorActual;
                }
            };
            
            celda.innerHTML = '';
            celda.appendChild(select);
            
            // Abrir dropdown automáticamente
            setTimeout(function() {
                select.focus();
                select.click();
            }, 50);
        }
        
        // Editar colaborador
        function editColaborador(celda, taskId) {
            // Prevenir múltiples ediciones
            if (celda.querySelector('select')) return;
            
            var valorActual = celda.textContent.trim();
            var select = document.createElement('select');
            select.className = 'form-select form-select-sm';
            select.style.minWidth = '150px';
            
            // Opción sin asignar
            var optionVacio = document.createElement('option');
            optionVacio.value = '';
            optionVacio.text = 'Sin asignar';
            if (valorActual === 'Sin asignar') {
                optionVacio.selected = true;
            }
            select.appendChild(optionVacio);
            
            // Empleados
            for (var i = 0; i < empleados.length; i++) {
                var emp = empleados[i];
                var option = document.createElement('option');
                option.value = emp.name;
                option.text = emp.name + ' (' + emp.rol + ')';
                if (valorActual === emp.name) {
                    option.selected = true;
                }
                select.appendChild(option);
            }
            
            // Eventos para manejar cambios y cancelación
            select.onchange = function() {
                guardarColaborador(this, taskId, celda, valorActual);
            };
            
            select.onblur = function() {
                setTimeout(function() {
                    if (select.parentNode) {
                        celda.textContent = valorActual;
                    }
                }, 200);
            };
            
            select.onkeydown = function(e) {
                if (e.key === 'Escape') {
                    celda.textContent = valorActual;
                }
            };
            
            celda.innerHTML = '';
            celda.appendChild(select);
            
            // Abrir dropdown automáticamente
            setTimeout(function() {
                select.focus();
                select.click();
            }, 50);
        }
        
        // Guardar estado
        function guardarEstado(select, taskId, celda, valorOriginal) {
            var nuevoValor = select.value;
            
            fetch('/tasks-simple/edit/' + taskId, {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify({field: 'estado', value: nuevoValor})
            })
            .then(function(response) {
                return response.json();
            })
            .then(function(data) {
                if (data.success) {
                    celda.textContent = nuevoValor;
                    // Actualizar clase de la fila
                    var fila = celda.closest('tr');
                    fila.className = fila.className.replace(/status-[\\w-]+/g, '');
                    fila.classList.add('status-' + nuevoValor.toLowerCase().replace(' ', '-'));
                } else {
                    alert('Error: ' + data.error);
                    location.reload();
                }
            })
            .catch(function(error) {
                alert('Error de conexión: ' + error);
                location.reload();
            });
        }
        
        // Guardar colaborador
        function guardarColaborador(select, taskId, celda, valorOriginal) {
            var nuevoValor = select.value || 'Sin asignar';
            
            fetch('/tasks-simple/edit/' + taskId, {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify({field: 'colaborador', value: select.value})
            })
            .then(function(response) {
                return response.json();
            })
            .then(function(data) {
                if (data.success) {
                    celda.textContent = nuevoValor;
                } else {
                    alert('Error: ' + data.error);
                    location.reload();
                }
            })
            .catch(function(error) {
                alert('Error de conexión: ' + error);
                location.reload();
            });
        }
        
        // Eliminar tarea
        function eliminarTarea(taskId) {
            if (confirm('¿Estás seguro de eliminar esta tarea?')) {
                fetch('/tasks-simple/delete/' + taskId, {method: 'DELETE'})
                .then(function(response) {
                    return response.json();
                })
                .then(function(data) {
                    if (data.success) {
                        location.reload();
                    } else {
                        alert('Error: ' + data.error);
                    }
                })
                .catch(function(error) {
                    alert('Error: ' + error);
                });
            }
        }
    </script>
</body>
</html>
'''

print("✅ Tasks Simple cargado")