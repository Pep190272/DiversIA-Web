"""
Gestor de persistencia de datos para DiversIA
Asegura que los datos se mantengan entre reinicios
"""

import json
import os
import shutil
from datetime import datetime
from typing import Dict, Any, List
import threading
import time

class DataPersistenceManager:
    """Gestiona la persistencia de datos del CRM"""
    
    def __init__(self):
        self.data_file = 'crm_persistent_data.json'
        self.backup_dir = 'data_backups'
        self.lock = threading.Lock()
        self.ensure_backup_dir()
    
    def ensure_backup_dir(self):
        """Crear directorio de respaldos si no existe"""
        if not os.path.exists(self.backup_dir):
            os.makedirs(self.backup_dir)
    
    def create_backup(self) -> str:
        """Crear respaldo con timestamp"""
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        backup_file = f"{self.backup_dir}/crm_backup_{timestamp}.json"
        
        if os.path.exists(self.data_file):
            shutil.copy2(self.data_file, backup_file)
            print(f"✅ Backup creado: {backup_file}")
            return backup_file
        return ""
    
    def load_data(self) -> Dict[str, Any]:
        """Cargar datos del archivo JSON"""
        try:
            with self.lock:
                if os.path.exists(self.data_file):
                    with open(self.data_file, 'r', encoding='utf-8') as f:
                        data = json.load(f)
                    print(f"✅ Datos cargados: {len(data.get('tasks', []))} tareas, {len(data.get('employees', []))} empleados")
                    return data
                else:
                    print("⚠️ Archivo de datos no existe, creando estructura inicial")
                    return self.create_initial_structure()
        except Exception as e:
            print(f"❌ Error cargando datos: {e}")
            return self.create_initial_structure()
    
    def save_data(self, data: Dict[str, Any]) -> bool:
        """Guardar datos al archivo JSON"""
        try:
            with self.lock:
                # Crear backup antes de sobrescribir
                if os.path.exists(self.data_file):
                    self.create_backup()
                
                # Actualizar metadata
                data['metadata'] = {
                    'last_updated': datetime.now().isoformat(),
                    'version': '1.0',
                    'total_interactions': data.get('metadata', {}).get('total_interactions', 0) + 1
                }
                
                # Guardar datos
                with open(self.data_file, 'w', encoding='utf-8') as f:
                    json.dump(data, f, ensure_ascii=False, indent=2)
                
                print(f"✅ Datos guardados: {len(data.get('tasks', []))} tareas, {len(data.get('employees', []))} empleados")
                return True
                
        except Exception as e:
            print(f"❌ Error guardando datos: {e}")
            return False
    
    def create_initial_structure(self) -> Dict[str, Any]:
        """Crear estructura inicial de datos"""
        initial_data = {
            "contacts": [],
            "companies": [
                {
                    "id": 1,
                    "name": "TechInclusiva S.L.",
                    "sector": "Tecnología",
                    "email": "rrhh@techinclusiva.com",
                    "phone": "+34 900 555 123",
                    "city": "Madrid",
                    "size": "50-100",
                    "website": "https://techinclusiva.com",
                    "created_at": "2024-01-10",
                    "source": "manual"
                }
            ],
            "employees": [
                {
                    "id": 1,
                    "first_name": "Pep",
                    "last_name": "Moreno Carrillo",
                    "email": "jose190272@gmail.com",
                    "position": "Desarrollador Principal",
                    "department": "Desarrollo",
                    "role": "empleado",
                    "hire_date": "2025-08-20",
                    "status": "active",
                    "is_active": True,
                    "salary": 54000,
                    "created_at": "2025-08-20T00:00:00"
                }
            ],
            "job_offers": [],
            "associations": [],
            "tasks": [
                {
                    "id": 1,
                    "title": "Email Marketing - Configuración inicial",
                    "assigned_to": "Pep Moreno",
                    "priority": "Alta",
                    "status": "Completada",
                    "category": "Marketing",
                    "estimated_time": "8h",
                    "actual_time": "8h",
                    "due_date": "2024-08-01",
                    "created_at": "2024-08-01",
                    "completed_at": "2024-08-01"
                },
                {
                    "id": 2,
                    "title": "LinkedIn - Optimización de perfil corporativo",
                    "assigned_to": "Pep Moreno",
                    "priority": "Alta",
                    "status": "Completada",
                    "category": "RRSS",
                    "estimated_time": "6h",
                    "actual_time": "6h",
                    "due_date": "2024-08-01",
                    "created_at": "2024-08-01",
                    "completed_at": "2024-08-01"
                },
                {
                    "id": 3,
                    "title": "Discord - Bot y configuración de comunidad",
                    "assigned_to": "Pep Moreno",
                    "priority": "Alta",
                    "status": "Completada",
                    "category": "Comunidad",
                    "estimated_time": "12h",
                    "actual_time": "12h",
                    "due_date": "2024-08-01",
                    "created_at": "2024-08-01",
                    "completed_at": "2024-08-01"
                },
                {
                    "id": 4,
                    "title": "Instagram - Estrategia de contenido visual",
                    "assigned_to": "Pep Moreno",
                    "priority": "Media",
                    "status": "Completada",
                    "category": "RRSS",
                    "estimated_time": "4h",
                    "actual_time": "4h",
                    "due_date": "2024-08-01",
                    "created_at": "2024-08-01",
                    "completed_at": "2024-08-01"
                },
                {
                    "id": 5,
                    "title": "Telegram - Canal de soporte oficial",
                    "assigned_to": "Pep Moreno",
                    "priority": "Media",
                    "status": "Completada",
                    "category": "Soporte",
                    "estimated_time": "3h",
                    "actual_time": "3h",
                    "due_date": "2024-08-01",
                    "created_at": "2024-08-01",
                    "completed_at": "2024-08-01"
                },
                {
                    "id": 6,
                    "title": "Web - Formularios con integración directa CRM",
                    "assigned_to": "Pep Moreno",
                    "priority": "Crítica",
                    "status": "Completada",
                    "category": "Desarrollo",
                    "estimated_time": "16h",
                    "actual_time": "16h",
                    "due_date": "2024-08-01",
                    "created_at": "2024-08-01",
                    "completed_at": "2024-08-01"
                },
                {
                    "id": 7,
                    "title": "Agente IA - Integración con Mistral API",
                    "assigned_to": "Pep Moreno",
                    "priority": "Alta",
                    "status": "En progreso",
                    "category": "IA",
                    "estimated_time": "20h",
                    "actual_time": "15h",
                    "due_date": "2024-08-15",
                    "created_at": "2024-08-01",
                    "notes": "Conectado con API gratuita Mistral. Funciona via N8N con 4 nodos, sin memoria ni BD. Necesita escalado."
                }
            ],
            "metadata": {
                "last_updated": datetime.now().isoformat(),
                "version": "1.0",
                "total_interactions": 1
            }
        }
        
        self.save_data(initial_data)
        return initial_data
    
    def add_task(self, task_data: Dict[str, Any]) -> bool:
        """Añadir nueva tarea"""
        data = self.load_data()
        
        # Obtener nuevo ID
        max_id = max([task.get('id', 0) for task in data.get('tasks', [])], default=0)
        task_data['id'] = max_id + 1
        
        # Añadir timestamp si no existe
        if 'created_at' not in task_data:
            task_data['created_at'] = datetime.now().isoformat()
        
        data.setdefault('tasks', []).append(task_data)
        return self.save_data(data)
    
    def add_employee(self, employee_data: Dict[str, Any]) -> bool:
        """Añadir nuevo empleado"""
        data = self.load_data()
        
        # Obtener nuevo ID
        max_id = max([emp.get('id', 0) for emp in data.get('employees', [])], default=0)
        employee_data['id'] = max_id + 1
        
        # Añadir timestamp si no existe
        if 'created_at' not in employee_data:
            employee_data['created_at'] = datetime.now().isoformat()
        
        data.setdefault('employees', []).append(employee_data)
        return self.save_data(data)
    
    def get_summary(self) -> Dict[str, Any]:
        """Obtener resumen de datos"""
        data = self.load_data()
        
        tasks = data.get('tasks', [])
        employees = data.get('employees', [])
        
        return {
            'total_tasks': len(tasks),
            'completed_tasks': len([t for t in tasks if t.get('status') == 'Completada']),
            'in_progress_tasks': len([t for t in tasks if t.get('status') == 'En progreso']),
            'total_employees': len(employees),
            'active_employees': len([e for e in employees if e.get('status') == 'active']),
            'last_updated': data.get('metadata', {}).get('last_updated', 'Unknown')
        }

# Instancia global
persistence_manager = DataPersistenceManager()

def ensure_data_persistence():
    """Función para asegurar que los datos se mantengan"""
    return persistence_manager.load_data()

def save_persistent_data(data):
    """Función para guardar datos persistentes"""
    return persistence_manager.save_data(data)

print("✅ Gestor de persistencia de datos inicializado")
print("📂 Datos se guardan en crm_persistent_data.json con backups automáticos")