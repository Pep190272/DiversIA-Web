# Sistema de persistencia para CRM
import json
import os
from datetime import datetime

CRM_DATA_FILE = 'crm_persistent_data.json'

def load_persistent_crm_data():
    """Carga datos persistentes del CRM"""
    if os.path.exists(CRM_DATA_FILE):
        try:
            with open(CRM_DATA_FILE, 'r', encoding='utf-8') as f:
                data = json.load(f)
                print(f"✅ Datos CRM cargados desde {CRM_DATA_FILE}")
                return data
        except Exception as e:
            print(f"⚠️ Error cargando datos CRM: {e}")
    
    # Datos iniciales si no existe el archivo
    initial_data = {
        'contacts': [
            {'id': 1, 'name': 'Ana García', 'email': 'ana@example.com', 'phone': '+34 600 123 456', 'city': 'Madrid', 'neurodivergence': 'TDAH', 'formal_diagnosis': True, 'created_at': '2024-01-15', 'source': 'manual'},
            {'id': 2, 'name': 'Carlos López', 'email': 'carlos@example.com', 'phone': '+34 655 987 654', 'city': 'Barcelona', 'neurodivergence': 'TEA', 'formal_diagnosis': True, 'created_at': '2024-02-20', 'source': 'manual'}
        ],
        'companies': [
            {'id': 1, 'name': 'TechInclusiva S.L.', 'sector': 'Tecnología', 'email': 'rrhh@techinclusiva.com', 'phone': '+34 900 555 123', 'city': 'Madrid', 'size': '50-100', 'website': 'https://techinclusiva.com', 'created_at': '2024-01-10', 'source': 'manual'},
            {'id': 2, 'name': 'ConsultoríaND', 'sector': 'Consultoría', 'email': 'contacto@consultoriaND.es', 'phone': '+34 910 444 789', 'city': 'Valencia', 'size': '10-50', 'website': 'https://consultoriand.es', 'created_at': '2024-03-05', 'source': 'manual'}
        ],
        'employees': [
            {'id': 1, 'first_name': 'Alex', 'last_name': 'Martínez', 'email': 'alex@diversia.com', 'position': 'Desarrolladora', 'department': 'Desarrollo', 'role': 'empleado', 'hire_date': '2024-01-15', 'status': 'active', 'created_at': '2024-01-15'}
        ],
        'job_offers': [
            {'id': 1, 'company_id': 1, 'title': 'Desarrollador Frontend Junior', 'description': 'Posición para desarrollador frontend con conocimientos de React', 'requirements': 'React, JavaScript, HTML, CSS', 'location': 'Madrid', 'type': 'Tiempo completo', 'salary_range': '25000-35000', 'remote_work': True, 'accommodations': 'Horarios flexibles, workspace silencioso', 'status': 'active', 'created_at': '2024-03-15'},
            {'id': 2, 'company_id': 2, 'title': 'Analista de Datos', 'description': 'Análisis de datos para proyectos de inclusión', 'requirements': 'Python, SQL, Excel avanzado', 'location': 'Valencia', 'type': 'Tiempo completo', 'salary_range': '30000-40000', 'remote_work': True, 'accommodations': 'Pausas regulares, comunicación escrita', 'status': 'active', 'created_at': '2024-04-01'}
        ],
        'associations': [
            {'id': 1, 'name': 'Fundación TDAH Madrid', 'acronym': 'FTM', 'country': 'España', 'city': 'Madrid', 'document_type': 'CIF', 'document_number': 'G12345678', 'focus_area': 'TDAH', 'type': 'Fundación', 'email': 'info@tdahmadrid.org', 'phone': '+34 915 555 123', 'website': 'https://tdahmadrid.org', 'created_at': '2024-02-01', 'source': 'manual'},
            {'id': 2, 'name': 'Asociación TEA Andalucía', 'acronym': 'ATEA', 'country': 'España', 'city': 'Sevilla', 'document_type': 'CIF', 'document_number': 'G87654321', 'focus_area': 'TEA', 'type': 'Asociación', 'email': 'contacto@tea-andalucia.org', 'phone': '+34 954 777 888', 'website': 'https://tea-andalucia.org', 'created_at': '2024-03-10', 'source': 'manual'}
        ],
        'tasks': [
            {'id': 1, 'title': 'Revisar candidatos TDAH', 'assigned_to': 'Ana García', 'priority': 'Alta', 'status': 'En progreso', 'category': 'Recruitment', 'estimated_time': '2h', 'actual_time': '1.5h', 'due_date': '2024-12-30', 'created_at': '2024-12-15'},
            {'id': 2, 'title': 'Contactar empresa TechInclusiva', 'assigned_to': 'Carlos López', 'priority': 'Media', 'status': 'Pendiente', 'category': 'Sales', 'estimated_time': '1h', 'actual_time': '0h', 'due_date': '2024-12-25', 'created_at': '2024-12-20'}
        ],
        'metadata': {
            'last_updated': datetime.now().isoformat(),
            'version': '1.0',
            'total_interactions': 0
        }
    }
    
    save_persistent_crm_data(initial_data)
    return initial_data

def save_persistent_crm_data(data):
    """Guarda datos del CRM de forma persistente"""
    try:
        # Actualizar metadatos
        if 'metadata' not in data:
            data['metadata'] = {}
        
        data['metadata']['last_updated'] = datetime.now().isoformat()
        data['metadata']['total_interactions'] = data['metadata'].get('total_interactions', 0) + 1
        
        with open(CRM_DATA_FILE, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        
        print(f"✅ Datos CRM guardados persistentemente en {CRM_DATA_FILE}")
        return True
    except Exception as e:
        print(f"⚠️ Error guardando datos CRM: {e}")
        return False

def add_employee_persistent(employee_data):
    """Añade empleado y guarda persistentemente"""
    try:
        # Cargar datos actuales
        crm_data = load_persistent_crm_data()
        
        # Generar nuevo ID
        max_id = max([e.get('id', 0) for e in crm_data.get('employees', [])], default=0)
        new_id = max_id + 1
        
        # Crear empleado
        new_employee = {
            'id': new_id,
            'first_name': employee_data.get('first_name', ''),
            'last_name': employee_data.get('last_name', ''),
            'email': employee_data.get('email', ''),
            'position': employee_data.get('position', ''),
            'department': employee_data.get('department', ''),
            'role': employee_data.get('role', 'empleado'),
            'hire_date': employee_data.get('hire_date', datetime.now().strftime('%Y-%m-%d')),
            'status': 'active',
            'is_active': True,
            'salary': employee_data.get('salary', 0),
            'created_at': datetime.now().isoformat()
        }
        
        # Añadir a la lista
        crm_data['employees'].append(new_employee)
        
        # Guardar persistentemente
        if save_persistent_crm_data(crm_data):
            print(f"✅ Empleado {new_employee['first_name']} {new_employee['last_name']} guardado persistentemente con ID {new_id}")
            return new_employee
        else:
            print("⚠️ Error guardando empleado")
            return None
            
    except Exception as e:
        print(f"⚠️ Error añadiendo empleado persistente: {e}")
        return None

def fix_sendgrid_email_system():
    """
    Configura el sistema de emails para funcionar correctamente
    """
    try:
        # Verificar API key
        import os
        api_key = os.environ.get('SENDGRID_API_KEY')
        
        if not api_key:
            print("⚠️ SENDGRID_API_KEY no configurado")
            return False
        
        if api_key.startswith('eX9u'):  # API key de demo inválido
            print("⚠️ SENDGRID_API_KEY parece ser un ejemplo/demo - necesita configurar uno real")
            return False
        
        print(f"✅ SENDGRID_API_KEY configurado (termina en: ...{api_key[-4:]})")
        return True
        
    except Exception as e:
        print(f"⚠️ Error verificando SendGrid: {e}")
        return False

def send_test_email():
    """Envía email de prueba para verificar configuración"""
    try:
        from employee_email_service import send_employee_welcome_email
        
        test_employee = {
            'id': 999,
            'first_name': 'Test',
            'last_name': 'Developer',
            'email': 'diversiaeternals@gmail.com',  # Email real
            'position': 'Desarrollador de Prueba',
            'department': 'Testing',
            'role': 'empleado',
            'hire_date': datetime.now().strftime('%Y-%m-%d')
        }
        
        result = send_employee_welcome_email(test_employee)
        if result:
            print("✅ Email de prueba enviado correctamente")
        else:
            print("⚠️ Error enviando email de prueba")
        
        return result
        
    except Exception as e:
        print(f"⚠️ Error en email de prueba: {e}")
        return False

print("✅ Sistema de persistencia CRM cargado")