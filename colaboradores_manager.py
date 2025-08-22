"""
Sistema de Gestión de Colaboradores para DiversIA
Gestión completa de colaboradores con fichas individuales
"""

import csv
import io
from datetime import datetime
from flask import request, jsonify, render_template_string, flash, redirect, session
from app import app, db
from models import Employee

@app.route('/colaboradores')
def colaboradores_dashboard():
    """Dashboard principal de gestión de colaboradores"""
    # Verificar autenticación admin
    if 'admin_ok' not in session or not session.get('admin_ok'):
        return redirect('/diversia-admin')
    
    # Obtener todos los colaboradores
    colaboradores = Employee.query.filter_by(active=True).all()
    total_colaboradores = len(colaboradores)
    
    return render_template_string(COLABORADORES_TABLE_TEMPLATE, 
                                colaboradores=colaboradores,
                                total_colaboradores=total_colaboradores)

@app.route('/colaboradores/add', methods=['POST'])
def add_colaborador():
    """Añadir nuevo colaborador"""
    if 'admin_ok' not in session or not session.get('admin_ok'):
        return jsonify({'error': 'No autorizado'}), 403
    
    data = request.get_json()
    try:
        new_colaborador = Employee(
            name=data.get('name', '').strip(),
            email=data.get('email', '').strip(),
            rol=data.get('rol', '').strip(),
            department=data.get('department', '').strip(),
            telefono=data.get('telefono', '').strip(),
            fecha_ingreso=data.get('fecha_ingreso', '').strip(),
            especialidades=data.get('especialidades', '').strip(),
            notas=data.get('notas', '').strip()
        )
        db.session.add(new_colaborador)
        db.session.commit()
        
        return jsonify({'success': True, 'message': 'Colaborador añadido correctamente'})
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/colaboradores/update/<int:colaborador_id>', methods=['POST'])
def update_colaborador(colaborador_id):
    """Actualizar datos de colaborador"""
    if 'admin_ok' not in session or not session.get('admin_ok'):
        return jsonify({'error': 'No autorizado'}), 403
    
    data = request.get_json()
    try:
        colaborador = Employee.query.get_or_404(colaborador_id)
        
        # Actualizar campos
        if 'field' in data and 'value' in data:
            field = data['field']
            value = data['value'].strip()
            
            if hasattr(colaborador, field):
                setattr(colaborador, field, value)
                colaborador.updated_at = datetime.now()
                db.session.commit()
                return jsonify({'success': True, 'message': 'Campo actualizado'})
            else:
                return jsonify({'success': False, 'error': 'Campo no válido'}), 400
        else:
            return jsonify({'success': False, 'error': 'Datos incompletos'}), 400
            
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/colaboradores/delete/<int:colaborador_id>', methods=['DELETE'])
def delete_colaborador(colaborador_id):
    """Eliminar colaborador (soft delete)"""
    if 'admin_ok' not in session or not session.get('admin_ok'):
        return jsonify({'error': 'No autorizado'}), 403
    
    try:
        colaborador = Employee.query.get_or_404(colaborador_id)
        colaborador.active = False
        colaborador.updated_at = datetime.now()
        db.session.commit()
        return jsonify({'success': True, 'message': 'Colaborador eliminado'})
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/colaboradores/export')
def export_colaboradores_csv():
    """Exportar colaboradores a CSV"""
    if 'admin_ok' not in session or not session.get('admin_ok'):
        return redirect('/diversia-admin')
    
    colaboradores = Employee.query.filter_by(active=True).all()
    
    output = io.StringIO()
    writer = csv.writer(output)
    
    # Headers
    writer.writerow(['ID', 'Nombre', 'Email', 'Rol', 'Departamento', 'Teléfono', 
                     'Fecha Ingreso', 'Especialidades', 'Notas', 'Fecha Creación'])
    
    # Data
    for col in colaboradores:
        writer.writerow([
            col.id,
            col.name,
            col.email,
            col.rol,
            col.department,
            col.telefono or '',
            col.fecha_ingreso or '',
            col.especialidades or '',
            col.notas or '',
            col.created_at.strftime('%Y-%m-%d %H:%M:%S') if col.created_at else ''
        ])
    
    output.seek(0)
    return output.getvalue(), 200, {
        'Content-Type': 'text/csv',
        'Content-Disposition': 'attachment; filename=colaboradores_diversia.csv'
    }

# Template para gestión de colaboradores
COLABORADORES_TABLE_TEMPLATE = '''
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Gestión de Colaboradores - DiversIA</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
    <style>
        .colaborador-card {
            transition: transform 0.2s;
        }
        .colaborador-card:hover {
            transform: translateY(-5px);
            box-shadow: 0 4px 15px rgba(0,0,0,0.1);
        }
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
        .role-badge {
            font-size: 0.8rem;
        }
    </style>
</head>
<body class="bg-light">
    <div class="container-fluid">
        <div class="row">
            <div class="col-12">
                <div class="d-flex justify-content-between align-items-center mb-4">
                    <h2>👥 Gestión de Colaboradores - DiversIA ({{ total_colaboradores }})</h2>
                    <div>
                        <a href="/tasks" class="btn btn-info me-2">📋 Tareas</a>
                        <a href="/crm-minimal" class="btn btn-outline-secondary me-2">← CRM</a>
                        <a href="/diversia-admin-logout" class="btn btn-outline-danger">Salir</a>
                    </div>
                </div>
                
                <!-- Acciones rápidas -->
                <div class="row mb-3">
                    <div class="col-md-6">
                        <div class="input-group">
                            <input type="text" id="searchInput" class="form-control" placeholder="Buscar por nombre, rol o departamento...">
                            <button class="btn btn-outline-secondary" type="button" onclick="clearSearch()">
                                <span id="clearIcon">🔍</span>
                            </button>
                        </div>
                    </div>
                    <div class="col-md-6 text-end">
                        <button class="btn btn-success me-2" onclick="showAddColaboradorForm()">➕ Añadir Colaborador</button>
                        <a href="/colaboradores/export" class="btn btn-warning me-2">📤 Exportar CSV</a>
                        <button onclick="deleteAllColaboradores()" class="btn btn-danger">🗑️ Eliminar Todo</button>
                    </div>
                </div>
                
                <!-- Contador de resultados -->
                <div class="row mb-3">
                    <div class="col-12">
                        <small class="text-muted">
                            Mostrando <span id="visibleCount">{{ total_colaboradores }}</span> de {{ total_colaboradores }} colaboradores
                        </small>
                    </div>
                </div>
                
                <!-- Formulario añadir colaborador -->
                <div id="addColaboradorForm" class="card mb-4" style="display: none;">
                    <div class="card-header">
                        <h5>➕ Añadir Nuevo Colaborador</h5>
                    </div>
                    <div class="card-body">
                        <form id="colaboradorForm">
                            <div class="row">
                                <div class="col-md-6">
                                    <div class="mb-3">
                                        <label class="form-label">Nombre Completo *</label>
                                        <input type="text" class="form-control" id="colName" required>
                                    </div>
                                </div>
                                <div class="col-md-6">
                                    <div class="mb-3">
                                        <label class="form-label">Email *</label>
                                        <input type="email" class="form-control" id="colEmail" required>
                                    </div>
                                </div>
                                <div class="col-md-6">
                                    <div class="mb-3">
                                        <label class="form-label">Rol *</label>
                                        <select class="form-control" id="colRol" required>
                                            <option value="">Seleccionar rol...</option>
                                            <option value="Developer">Developer</option>
                                            <option value="Designer">Designer</option>
                                            <option value="Marketing">Marketing</option>
                                            <option value="Manager">Manager</option>
                                            <option value="Analyst">Analyst</option>
                                            <option value="Support">Support</option>
                                            <option value="HR">Recursos Humanos</option>
                                            <option value="Sales">Ventas</option>
                                        </select>
                                    </div>
                                </div>
                                <div class="col-md-6">
                                    <div class="mb-3">
                                        <label class="form-label">Departamento</label>
                                        <input type="text" class="form-control" id="colDepartment" placeholder="Ej: Tecnología, Marketing...">
                                    </div>
                                </div>
                                <div class="col-md-6">
                                    <div class="mb-3">
                                        <label class="form-label">Teléfono</label>
                                        <input type="tel" class="form-control" id="colTelefono" placeholder="+34 600 000 000">
                                    </div>
                                </div>
                                <div class="col-md-6">
                                    <div class="mb-3">
                                        <label class="form-label">Fecha de Ingreso</label>
                                        <input type="date" class="form-control" id="colFechaIngreso">
                                    </div>
                                </div>
                                <div class="col-md-12">
                                    <div class="mb-3">
                                        <label class="form-label">Especialidades</label>
                                        <input type="text" class="form-control" id="colEspecialidades" placeholder="Ej: React, Python, SEO, Diseño UX...">
                                    </div>
                                </div>
                                <div class="col-md-12">
                                    <div class="mb-3">
                                        <label class="form-label">Notas Adicionales</label>
                                        <textarea class="form-control" id="colNotas" rows="2" 
                                                placeholder="Información adicional sobre el colaborador..."></textarea>
                                    </div>
                                </div>
                            </div>
                            <div class="d-flex gap-2">
                                <button type="submit" class="btn btn-success">✅ Crear Colaborador</button>
                                <button type="button" class="btn btn-secondary" onclick="hideAddColaboradorForm()">❌ Cancelar</button>
                            </div>
                        </form>
                    </div>
                </div>
                
                <!-- Grid de tarjetas de colaboradores -->
                <div class="row" id="colaboradoresGrid">
                    {% for col in colaboradores %}
                    <div class="col-md-6 col-lg-4 mb-4 colaborador-item">
                        <div class="card colaborador-card h-100">
                            <div class="card-header d-flex justify-content-between align-items-center">
                                <h6 class="mb-0">
                                    <span class="editable-field fw-bold" 
                                          data-field="name" 
                                          data-id="{{ col.id }}"
                                          title="Click para editar">{{ col.name }}</span>
                                </h6>
                                <span class="badge bg-primary role-badge">{{ col.rol }}</span>
                            </div>
                            <div class="card-body">
                                <div class="mb-2">
                                    <small class="text-muted">📧 Email:</small><br>
                                    <span class="editable-field" 
                                          data-field="email" 
                                          data-id="{{ col.id }}"
                                          title="Click para editar">{{ col.email }}</span>
                                </div>
                                
                                <div class="mb-2">
                                    <small class="text-muted">🏢 Departamento:</small><br>
                                    <span class="editable-field" 
                                          data-field="department" 
                                          data-id="{{ col.id }}"
                                          title="Click para editar">{{ col.department or '-' }}</span>
                                </div>
                                
                                {% if col.telefono %}
                                <div class="mb-2">
                                    <small class="text-muted">📞 Teléfono:</small><br>
                                    <span class="editable-field" 
                                          data-field="telefono" 
                                          data-id="{{ col.id }}"
                                          title="Click para editar">{{ col.telefono }}</span>
                                </div>
                                {% endif %}
                                
                                {% if col.fecha_ingreso %}
                                <div class="mb-2">
                                    <small class="text-muted">📅 Ingreso:</small><br>
                                    <span class="editable-field" 
                                          data-field="fecha_ingreso" 
                                          data-id="{{ col.id }}"
                                          title="Click para editar">{{ col.fecha_ingreso }}</span>
                                </div>
                                {% endif %}
                                
                                {% if col.especialidades %}
                                <div class="mb-2">
                                    <small class="text-muted">💡 Especialidades:</small><br>
                                    <span class="editable-field" 
                                          data-field="especialidades" 
                                          data-id="{{ col.id }}"
                                          title="Click para editar">{{ col.especialidades }}</span>
                                </div>
                                {% endif %}
                                
                                {% if col.notas %}
                                <div class="mb-2">
                                    <small class="text-muted">📝 Notas:</small><br>
                                    <span class="editable-field" 
                                          data-field="notas" 
                                          data-id="{{ col.id }}"
                                          title="Click para editar">{{ col.notas }}</span>
                                </div>
                                {% endif %}
                            </div>
                            <div class="card-footer d-flex justify-content-between">
                                <small class="text-muted">ID: {{ col.id }}</small>
                                <button class="btn btn-sm btn-danger" onclick="deleteColaborador({{ col.id }})">🗑️ Eliminar</button>
                            </div>
                        </div>
                    </div>
                    {% endfor %}
                </div>
                
                {% if not colaboradores %}
                <div class="text-center py-5">
                    <h4 class="text-muted">No hay colaboradores registrados</h4>
                    <p class="text-muted">Haz clic en "Añadir Colaborador" para empezar</p>
                </div>
                {% endif %}
            </div>
        </div>
    </div>
    
    <script>
        function deleteColaborador(id) {
            if (confirm('¿Estás seguro de que quieres eliminar este colaborador?')) {
                fetch(`/colaboradores/delete/${id}`, {
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
        
        function showAddColaboradorForm() {
            document.getElementById('addColaboradorForm').style.display = 'block';
            document.getElementById('colName').focus();
        }
        
        function hideAddColaboradorForm() {
            document.getElementById('addColaboradorForm').style.display = 'none';
            document.getElementById('colaboradorForm').reset();
        }
        
        function deleteAllColaboradores() {
            if (confirm('⚠️ ATENCIÓN: ¿Estás COMPLETAMENTE SEGURO de eliminar TODOS los colaboradores?')) {
                if (confirm('🛑 ÚLTIMA CONFIRMACIÓN: Esto eliminará TODOS los colaboradores. ¿Confirmas?')) {
                    // Implementar función para eliminar todos si es necesario
                    alert('Función de eliminar todo pendiente de implementar');
                }
            }
        }
        
        // Gestión de colaboradores
        document.getElementById('colaboradorForm').addEventListener('submit', function(e) {
            e.preventDefault();
            
            const formData = {
                name: document.getElementById('colName').value.trim(),
                email: document.getElementById('colEmail').value.trim(),
                rol: document.getElementById('colRol').value.trim(),
                department: document.getElementById('colDepartment').value.trim(),
                telefono: document.getElementById('colTelefono').value.trim(),
                fecha_ingreso: document.getElementById('colFechaIngreso').value.trim(),
                especialidades: document.getElementById('colEspecialidades').value.trim(),
                notas: document.getElementById('colNotas').value.trim()
            };
            
            if (!formData.name || !formData.email || !formData.rol) {
                alert('Por favor, completa todos los campos obligatorios');
                return;
            }
            
            fetch('/colaboradores/add', {
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
                    hideAddColaboradorForm();
                    location.reload();
                } else {
                    alert('❌ Error: ' + data.error);
                }
            })
            .catch(error => {
                alert('❌ Error de conexión: ' + error);
            });
        });

        // Sistema de búsqueda
        let allItems = [];
        
        function initializeSearch() {
            allItems = Array.from(document.querySelectorAll('.colaborador-item'));
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
            
            allItems.forEach(item => {
                const text = item.textContent.toLowerCase();
                const matches = text.includes(term);
                
                if (matches || term === '') {
                    item.style.display = '';
                    visibleCount++;
                } else {
                    item.style.display = 'none';
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
            initializeSearch();
            
            // Edición inline de campos
            document.querySelectorAll('.editable-field').forEach(field => {
                field.addEventListener('click', function() {
                    if (this.classList.contains('editing')) return;
                    
                    const fieldName = this.dataset.field;
                    const collaboratorId = this.dataset.id;
                    const currentValue = this.textContent.trim();
                    
                    // Crear input de edición
                    const input = document.createElement('input');
                    input.type = 'text';
                    input.className = 'edit-input';
                    input.value = currentValue === '-' ? '' : currentValue;
                    
                    // Reemplazar contenido
                    this.classList.add('editing');
                    const originalContent = this.innerHTML;
                    this.innerHTML = '';
                    this.appendChild(input);
                    
                    // Focus y seleccionar
                    input.focus();
                    input.select();
                    
                    // Función para guardar
                    const saveEdit = () => {
                        const newValue = input.value.trim();
                        
                        fetch(`/colaboradores/update/${collaboratorId}`, {
                            method: 'POST',
                            headers: {
                                'Content-Type': 'application/json',
                            },
                            body: JSON.stringify({
                                field: fieldName,
                                value: newValue
                            })
                        })
                        .then(response => response.json())
                        .then(data => {
                            if (data.success) {
                                this.classList.remove('editing');
                                this.textContent = newValue || '-';
                            } else {
                                alert('Error al actualizar: ' + data.error);
                                this.classList.remove('editing');
                                this.innerHTML = originalContent;
                            }
                        })
                        .catch(error => {
                            alert('Error de conexión: ' + error);
                            this.classList.remove('editing');
                            this.innerHTML = originalContent;
                        });
                    };
                    
                    // Función para cancelar
                    const cancelEdit = () => {
                        this.classList.remove('editing');
                        this.innerHTML = originalContent;
                    };
                    
                    // Event listeners
                    input.addEventListener('blur', saveEdit);
                    input.addEventListener('keydown', function(e) {
                        if (e.key === 'Enter') {
                            e.preventDefault();
                            saveEdit();
                        } else if (e.key === 'Escape') {
                            e.preventDefault();
                            cancelEdit();
                        }
                    });
                });
            });
        });
    </script>
</body>
</html>
'''