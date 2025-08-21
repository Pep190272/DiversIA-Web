"""
Sistema de asignación de tareas dinámico para DiversIA CRM
Permite asignar tareas a empleados usando desplegables dinámicos
"""

from flask import jsonify, request, render_template_string
from app import app
import json
from datetime import datetime

def get_active_employees():
    """Obtener lista de empleados activos para asignación"""
    try:
        from data_persistence_manager import persistence_manager
        data = persistence_manager.load_data()
        
        employees = []
        for emp in data.get('employees', []):
            if emp.get('status') == 'active' or emp.get('is_active', True):
                full_name = f"{emp.get('first_name', '')} {emp.get('last_name', '')}".strip()
                employees.append({
                    'id': emp.get('id'),
                    'name': full_name,
                    'position': emp.get('position', ''),
                    'department': emp.get('department', '')
                })
        
        return employees
    except Exception as e:
        print(f"Error obteniendo empleados: {e}")
        return [{'id': 1, 'name': 'Pep Moreno Carrillo', 'position': 'Desarrollador Principal', 'department': 'Desarrollo'}]

def update_task_assignment(task_id, assigned_to_id, assigned_to_name):
    """Actualizar asignación de tarea"""
    try:
        from data_persistence_manager import persistence_manager
        data = persistence_manager.load_data()
        
        # Buscar y actualizar la tarea
        for task in data.get('tasks', []):
            if task.get('id') == int(task_id):
                task['assigned_to'] = assigned_to_name
                task['assigned_to_id'] = int(assigned_to_id)
                task['updated_at'] = datetime.now().isoformat()
                
                # Guardar cambios
                success = persistence_manager.save_data(data)
                if success:
                    print(f"✅ Tarea {task_id} asignada a {assigned_to_name}")
                    return True
                break
        
        return False
    except Exception as e:
        print(f"❌ Error actualizando asignación: {e}")
        return False

@app.route('/api/employees', methods=['GET'])
def get_employees_api():
    """API para obtener empleados activos"""
    try:
        employees = get_active_employees()
        return jsonify({
            'success': True,
            'employees': employees,
            'total': len(employees)
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e),
            'employees': []
        }), 500

@app.route('/api/tasks/<int:task_id>/assign', methods=['POST'])
def assign_task_api(task_id):
    """API para asignar tarea a empleado"""
    try:
        data = request.get_json()
        assigned_to_id = data.get('assigned_to_id')
        assigned_to_name = data.get('assigned_to_name')
        
        if not assigned_to_id or not assigned_to_name:
            return jsonify({
                'success': False,
                'error': 'ID y nombre del empleado son requeridos'
            }), 400
        
        success = update_task_assignment(task_id, assigned_to_id, assigned_to_name)
        
        if success:
            return jsonify({
                'success': True,
                'message': f'Tarea {task_id} asignada a {assigned_to_name}'
            })
        else:
            return jsonify({
                'success': False,
                'error': 'No se pudo actualizar la asignación'
            }), 500
            
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

# Template JavaScript para gestión dinámica de asignaciones
TASK_ASSIGNMENT_JS = """
<script>
class TaskAssignmentManager {
    constructor() {
        this.employees = [];
        this.loadEmployees();
        this.initializeAssignmentDropdowns();
    }
    
    async loadEmployees() {
        try {
            const response = await fetch('/api/employees');
            const data = await response.json();
            
            if (data.success) {
                this.employees = data.employees;
                this.updateAllDropdowns();
                console.log(`✅ ${this.employees.length} empleados cargados`);
            } else {
                console.error('Error cargando empleados:', data.error);
            }
        } catch (error) {
            console.error('Error en la API de empleados:', error);
        }
    }
    
    initializeAssignmentDropdowns() {
        // Convertir elementos de asignación en dropdowns
        document.querySelectorAll('.task-assignment').forEach(element => {
            this.createAssignmentDropdown(element);
        });
    }
    
    createAssignmentDropdown(element) {
        const taskId = element.dataset.taskId;
        const currentAssignment = element.textContent.trim();
        
        const select = document.createElement('select');
        select.className = 'form-select form-select-sm';
        select.dataset.taskId = taskId;
        
        // Agregar opción por defecto
        const defaultOption = document.createElement('option');
        defaultOption.value = '';
        defaultOption.textContent = 'Seleccionar empleado...';
        select.appendChild(defaultOption);
        
        // Event listener para cambios
        select.addEventListener('change', (e) => {
            this.handleAssignmentChange(e.target);
        });
        
        // Reemplazar elemento original
        element.parentNode.replaceChild(select, element);
        
        // Actualizar con empleados actuales
        this.updateDropdown(select, currentAssignment);
    }
    
    updateAllDropdowns() {
        document.querySelectorAll('select[data-task-id]').forEach(select => {
            const currentValue = select.value;
            this.updateDropdown(select, currentValue);
        });
    }
    
    updateDropdown(selectElement, currentAssignment = '') {
        // Limpiar opciones existentes (excepto la primera)
        while (selectElement.children.length > 1) {
            selectElement.removeChild(selectElement.lastChild);
        }
        
        // Agregar empleados
        this.employees.forEach(employee => {
            const option = document.createElement('option');
            option.value = JSON.stringify({
                id: employee.id,
                name: employee.name
            });
            option.textContent = `${employee.name} (${employee.position})`;
            
            // Marcar como seleccionado si coincide con asignación actual
            if (employee.name === currentAssignment) {
                option.selected = true;
            }
            
            selectElement.appendChild(option);
        });
    }
    
    async handleAssignmentChange(selectElement) {
        const taskId = selectElement.dataset.taskId;
        const selectedValue = selectElement.value;
        
        if (!selectedValue) return;
        
        try {
            const assignmentData = JSON.parse(selectedValue);
            
            const response = await fetch(`/api/tasks/${taskId}/assign`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    assigned_to_id: assignmentData.id,
                    assigned_to_name: assignmentData.name
                })
            });
            
            const result = await response.json();
            
            if (result.success) {
                this.showNotification(`✅ Tarea asignada a ${assignmentData.name}`, 'success');
                // Actualizar visualmente
                selectElement.style.backgroundColor = '#d4edda';
                setTimeout(() => {
                    selectElement.style.backgroundColor = '';
                }, 2000);
            } else {
                this.showNotification(`❌ Error: ${result.error}`, 'error');
            }
            
        } catch (error) {
            console.error('Error asignando tarea:', error);
            this.showNotification('❌ Error de conexión', 'error');
        }
    }
    
    showNotification(message, type = 'info') {
        // Crear notificación toast
        const toast = document.createElement('div');
        toast.className = `alert alert-${type === 'success' ? 'success' : 'danger'} alert-dismissible fade show position-fixed`;
        toast.style.cssText = 'top: 20px; right: 20px; z-index: 9999; min-width: 300px;';
        toast.innerHTML = `
            ${message}
            <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
        `;
        
        document.body.appendChild(toast);
        
        // Auto-eliminar después de 3 segundos
        setTimeout(() => {
            if (toast.parentNode) {
                toast.parentNode.removeChild(toast);
            }
        }, 3000);
    }
    
    // Método para refrescar empleados (útil cuando se crea un nuevo empleado)
    refresh() {
        this.loadEmployees();
    }
}

// Inicializar cuando la página esté lista
document.addEventListener('DOMContentLoaded', function() {
    window.taskAssignmentManager = new TaskAssignmentManager();
});

// Función global para refrescar desde otros scripts
function refreshTaskAssignments() {
    if (window.taskAssignmentManager) {
        window.taskAssignmentManager.refresh();
    }
}
</script>
"""

def get_task_assignment_js():
    """Obtener JavaScript para gestión de asignaciones"""
    return TASK_ASSIGNMENT_JS

print("✅ Sistema de asignación de tareas dinámico inicializado")
print("🔧 APIs disponibles: /api/employees, /api/tasks/<id>/assign")