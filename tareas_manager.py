from flask import Blueprint, render_template_string, request, jsonify, session, redirect
from app import app, db
import logging

# Configure logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

# Crear blueprint para tareas
tareas_bp = Blueprint('tareas', __name__)

@tareas_bp.route('/tareas')
def mostrar_tareas():
    """Mostrar tabla de tareas con edición inline"""
    if 'admin_ok' not in session or not session.get('admin_ok'):
        return redirect('/admin/login-new')
    
    try:
        # Obtener tareas directamente de la tabla SQL
        with db.engine.connect() as conn:
            result = conn.execute(db.text("SELECT * FROM tareas_empresa ORDER BY id"))
            tareas = result.fetchall()
        
        # Obtener empleados
        with db.engine.connect() as conn:
            result = conn.execute(db.text("SELECT name, rol FROM empleados WHERE active = true"))
            empleados = result.fetchall()
        
        return render_template_string(TAREAS_TEMPLATE, tareas=tareas, empleados=empleados)
    except Exception as e:
        logger.error(f"Error en mostrar_tareas: {e}")
        return f"Error: {e}", 500

@tareas_bp.route('/tareas/editar/<int:tarea_id>', methods=['POST'])
def editar_tarea(tarea_id):
    """Editar una tarea específica"""
    if 'admin_ok' not in session or not session.get('admin_ok'):
        return jsonify({'error': 'No autorizado'}), 403
    
    try:
        data = request.get_json()
        campo = data.get('campo')
        valor = data.get('valor')
        
        # Actualizar en la base de datos
        if campo == 'estado':
            with db.engine.connect() as conn:
                conn.execute(db.text("UPDATE tareas_empresa SET estado = :valor WHERE id = :id"), 
                           {'valor': valor, 'id': tarea_id})
                conn.commit()
        elif campo == 'colaborador':
            with db.engine.connect() as conn:
                conn.execute(db.text("UPDATE tareas_empresa SET colaborador = :valor WHERE id = :id"), 
                           {'valor': valor if valor else None, 'id': tarea_id})
                conn.commit()
        
        return jsonify({'success': True})
    except Exception as e:
        logger.error(f"Error editando tarea: {e}")
        return jsonify({'error': str(e)}), 500

@tareas_bp.route('/tareas/eliminar/<int:tarea_id>', methods=['DELETE'])
def eliminar_tarea(tarea_id):
    """Eliminar una tarea"""
    if 'admin_ok' not in session or not session.get('admin_ok'):
        return jsonify({'error': 'No autorizado'}), 403
    
    try:
        with db.engine.connect() as conn:
            conn.execute(db.text("DELETE FROM tareas_empresa WHERE id = :id"), {'id': tarea_id})
            conn.commit()
        
        return jsonify({'success': True})
    except Exception as e:
        logger.error(f"Error eliminando tarea: {e}")
        return jsonify({'error': str(e)}), 500

@tareas_bp.route('/tareas/empleados')
def obtener_empleados():
    """Obtener lista de empleados para dropdowns"""
    try:
        with db.engine.connect() as conn:
            result = conn.execute(db.text("SELECT name, rol FROM empleados WHERE active = true"))
            empleados = [{'name': row[0], 'rol': row[1]} for row in result.fetchall()]
        
        return jsonify(empleados)
    except Exception as e:
        logger.error(f"Error obteniendo empleados: {e}")
        return jsonify([])

# Template HTML simple y funcional
TAREAS_TEMPLATE = '''
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Gestión de Tareas - DiversIA</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
    <style>
        .editable-cell {
            cursor: pointer;
            padding: 8px;
            border-radius: 4px;
            transition: all 0.2s;
            min-width: 100px;
        }
        .editable-cell:hover {
            background-color: #e3f2fd;
            border: 1px solid #2196f3;
        }
        .estado-pendiente { background-color: #fff3cd; color: #856404; }
        .estado-en-curso { background-color: #d1ecf1; color: #0c5460; }
        .estado-terminada { background-color: #d4edda; color: #155724; }
        .dropdown-overlay {
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            background: rgba(0,0,0,0.01);
            z-index: 1000;
            display: none;
        }
        .dropdown-content {
            position: absolute;
            background: white;
            border: 1px solid #ccc;
            border-radius: 4px;
            box-shadow: 0 4px 6px rgba(0,0,0,0.1);
            min-width: 150px;
            z-index: 1001;
        }
        .dropdown-item {
            padding: 8px 12px;
            cursor: pointer;
            border-bottom: 1px solid #eee;
        }
        .dropdown-item:hover {
            background-color: #f8f9fa;
        }
        .dropdown-item:last-child {
            border-bottom: none;
        }
    </style>
</head>
<body>
    <div class="container-fluid mt-4">
        <div class="row">
            <div class="col-12">
                <div class="d-flex justify-content-between align-items-center mb-3">
                    <div>
                        <h2>📋 Gestión de Tareas</h2>
                    </div>
                    <div>
                        <a href="/dashboard-tareas" class="btn btn-outline-primary me-2">📈 Analytics</a>
                        <a href="/crm-minimal" class="btn btn-secondary">← Volver al CRM</a>
                    </div>
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
                                    {% for tarea in tareas %}
                                    <tr>
                                        <td>{{ tarea[0] }}</td>
                                        <td>{{ tarea[1] }}</td>
                                        <td class="editable-cell" data-field="colaborador" data-id="{{ tarea[0] }}">
                                            {{ tarea[2] or 'Sin asignar' }}
                                        </td>
                                        <td>{{ tarea[3] or '-' }}</td>
                                        <td>{{ tarea[4] or '-' }}</td>
                                        <td class="editable-cell estado-{{ (tarea[5] or 'pendiente').lower().replace(' ', '-') }}" 
                                            data-field="estado" data-id="{{ tarea[0] }}">
                                            {{ tarea[5] or 'Pendiente' }}
                                        </td>
                                        <td>
                                            <button class="btn btn-sm btn-danger" onclick="eliminarTarea({{ tarea[0] }})">
                                                🗑️ Eliminar
                                            </button>
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
        let empleados = [];
        let dropdownActivo = null;
        
        // Cargar empleados al inicio
        fetch('/tareas/empleados')
        .then(response => response.json())
        .then(data => {
            empleados = data;
            console.log('Empleados cargados:', empleados.length);
        })
        .catch(error => console.error('Error cargando empleados:', error));
        
        // Event listeners para celdas editables
        document.addEventListener('DOMContentLoaded', function() {
            const celdas = document.querySelectorAll('.editable-cell');
            celdas.forEach(celda => {
                celda.addEventListener('click', function() {
                    if (dropdownActivo) return; // Prevenir múltiples dropdowns
                    
                    const campo = this.dataset.field;
                    const id = this.dataset.id;
                    const valorActual = this.textContent.trim();
                    
                    if (campo === 'estado') {
                        mostrarDropdownEstado(this, id, valorActual);
                    } else if (campo === 'colaborador') {
                        mostrarDropdownColaborador(this, id, valorActual);
                    }
                });
            });
        });
        
        function mostrarDropdownEstado(celda, id, valorActual) {
            const opciones = ['Pendiente', 'En curso', 'Terminada'];
            mostrarDropdown(celda, id, 'estado', opciones, valorActual);
        }
        
        function mostrarDropdownColaborador(celda, id, valorActual) {
            const opciones = ['Sin asignar', ...empleados.map(emp => emp.name)];
            mostrarDropdown(celda, id, 'colaborador', opciones, valorActual);
        }
        
        function mostrarDropdown(celda, id, campo, opciones, valorActual) {
            // Crear overlay
            const overlay = document.createElement('div');
            overlay.className = 'dropdown-overlay';
            
            // Crear contenido del dropdown
            const dropdown = document.createElement('div');
            dropdown.className = 'dropdown-content';
            
            const rect = celda.getBoundingClientRect();
            dropdown.style.top = rect.bottom + window.scrollY + 'px';
            dropdown.style.left = rect.left + window.scrollX + 'px';
            
            // Crear opciones
            opciones.forEach(opcion => {
                const item = document.createElement('div');
                item.className = 'dropdown-item';
                item.textContent = opcion;
                
                if (opcion === valorActual) {
                    item.style.backgroundColor = '#007bff';
                    item.style.color = 'white';
                }
                
                item.addEventListener('click', function() {
                    const nuevoValor = opcion === 'Sin asignar' && campo === 'colaborador' ? '' : opcion;
                    guardarCambio(id, campo, nuevoValor, celda);
                    cerrarDropdown();
                });
                
                dropdown.appendChild(item);
            });
            
            // Agregar al DOM
            overlay.appendChild(dropdown);
            overlay.style.display = 'block';
            document.body.appendChild(overlay);
            
            // Event listener para cerrar
            overlay.addEventListener('click', function(e) {
                if (e.target === overlay) {
                    cerrarDropdown();
                }
            });
            
            // Auto-cerrar después de 10 segundos por seguridad
            setTimeout(function() {
                if (dropdownActivo === overlay) {
                    cerrarDropdown();
                }
            }, 10000);
            
            dropdownActivo = overlay;
        }
        
        function cerrarDropdown() {
            if (dropdownActivo) {
                dropdownActivo.style.display = 'none';
                try {
                    document.body.removeChild(dropdownActivo);
                } catch(e) {
                    console.log('Error removiendo overlay:', e);
                }
                dropdownActivo = null;
            }
        }
        
        function guardarCambio(id, campo, valor, celda) {
            fetch(`/tareas/editar/${id}`, {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify({campo: campo, valor: valor})
            })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    // Actualizar la celda
                    if (campo === 'colaborador') {
                        celda.textContent = valor || 'Sin asignar';
                    } else {
                        celda.textContent = valor;
                        // Actualizar clase de estado
                        celda.className = celda.className.replace(/estado-[\\w-]+/g, '');
                        celda.classList.add('estado-' + valor.toLowerCase().replace(' ', '-'));
                    }
                } else {
                    alert('Error: ' + data.error);
                    location.reload();
                }
            })
            .catch(error => {
                alert('Error de conexión: ' + error);
                location.reload();
            });
        }
        
        function eliminarTarea(id) {
            if (confirm('¿Estás seguro de eliminar esta tarea?')) {
                fetch(`/tareas/eliminar/${id}`, {method: 'DELETE'})
                .then(response => response.json())
                .then(data => {
                    if (data.success) {
                        location.reload();
                    } else {
                        alert('Error: ' + data.error);
                    }
                })
                .catch(error => {
                    alert('Error: ' + error);
                });
            }
        }
        
        // Cerrar dropdown con Escape
        document.addEventListener('keydown', function(e) {
            if (e.key === 'Escape' && dropdownActivo) {
                cerrarDropdown();
            }
        });
    </script>
</body>
</html>
'''

# Registrar blueprint
app.register_blueprint(tareas_bp)
print("✅ Sistema de Tareas completamente nuevo cargado")