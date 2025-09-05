from app import app, db
from models import Task, Employee
from datetime import datetime

def load_tasks_from_csv():
    """Cargar tareas del CSV proporcionado"""
    
    with app.app_context():
        # Limpiar tareas existentes
        Task.query.delete()
        
        # Asegurar que existen empleados
        if not Employee.query.filter_by(name='Pep').first():
            pep = Employee(name='Pep', email='pep@diversia.com', rol='Desarrollador', department='Tecnología', active=True)
            db.session.add(pep)
        
        if not Employee.query.filter_by(name='Olga').first():
            olga = Employee(name='Olga', email='olga@diversia.com', rol='Marketing', department='Marketing', active=True)
            db.session.add(olga)
        
        # Datos del CSV
        tareas_csv = [
            {
                'tarea': 'Marketing por correo electrónico',
                'colaborador': 'Olga',
                'fecha_inicio': '29/07/2025',
                'fecha_final': '29/07/2025',
                'estado': 'Terminada'
            },
            {
                'tarea': 'LinkedIn',
                'colaborador': 'Pep',
                'fecha_inicio': '29/07/2025',
                'fecha_final': '29/07/2025',
                'estado': 'Terminada'
            },
            {
                'tarea': 'Discord con bot',
                'colaborador': 'Olga',
                'fecha_inicio': '30/07/2025',
                'fecha_final': '30/07/2025',
                'estado': 'Terminada'
            },
            {
                'tarea': 'Instagram',
                'colaborador': 'Pep',
                'fecha_inicio': '03/08/2025',
                'fecha_final': '03/08/2025',
                'estado': 'Terminada'
            },
            {
                'tarea': 'Telegram',
                'colaborador': 'Pep',
                'fecha_inicio': '04/08/2025',
                'fecha_final': '04/08/2025',
                'estado': 'Terminada'
            },
            {
                'tarea': 'Web con formularios y agente de IA',
                'colaborador': 'Pep',
                'fecha_inicio': '29/07/2025',
                'fecha_final': None,
                'estado': 'En curso'
            },
            {
                'tarea': 'Aplicación (App)',
                'colaborador': None,
                'fecha_inicio': '06/09/2025',
                'fecha_final': None,
                'estado': 'Pendiente'
            },
            {
                'tarea': 'Campañas publicitarias en redes sociales',
                'colaborador': 'Olga',
                'fecha_inicio': '25/08/2025',
                'fecha_final': None,
                'estado': 'En curso'
            }
        ]
        
        # Crear tareas
        for tarea_data in tareas_csv:
            tarea = Task(
                tarea=tarea_data['tarea'],
                colaborador=tarea_data['colaborador'],
                fecha_inicio=tarea_data['fecha_inicio'],
                fecha_final=tarea_data['fecha_final'],
                estado=tarea_data['estado'],
                notas=None
            )
            db.session.add(tarea)
        
        db.session.commit()
        print(f"✅ Cargadas {len(tareas_csv)} tareas desde CSV")

if __name__ == "__main__":
    load_tasks_from_csv()