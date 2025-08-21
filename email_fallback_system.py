"""
Sistema de respaldo para notificaciones sin configuración de email
Guarda las notificaciones en el CRM para revisión manual
"""

import json
import os
from datetime import datetime
from typing import Dict, Any, List

class EmailFallbackSystem:
    """Sistema que funciona sin configuración de email externo"""
    
    def __init__(self):
        self.notifications_file = 'pending_notifications.json'
        self.ensure_notifications_file()
    
    def ensure_notifications_file(self):
        """Crear archivo de notificaciones si no existe"""
        if not os.path.exists(self.notifications_file):
            with open(self.notifications_file, 'w', encoding='utf-8') as f:
                json.dump({'notifications': []}, f, ensure_ascii=False, indent=2)
    
    def save_notification(self, notification_type: str, data: Dict[str, Any]) -> bool:
        """Guardar notificación para revisión manual"""
        try:
            # Leer notificaciones existentes
            with open(self.notifications_file, 'r', encoding='utf-8') as f:
                notifications_data = json.load(f)
            
            # Crear nueva notificación
            new_notification = {
                'id': len(notifications_data['notifications']) + 1,
                'type': notification_type,
                'timestamp': datetime.now().isoformat(),
                'data': data,
                'status': 'pending',
                'priority': 'normal'
            }
            
            # Determinar prioridad
            if notification_type == 'contact_form':
                new_notification['priority'] = 'high'
            elif notification_type == 'form_submission':
                new_notification['priority'] = 'medium'
            
            # Añadir notificación
            notifications_data['notifications'].append(new_notification)
            
            # Guardar archivo actualizado
            with open(self.notifications_file, 'w', encoding='utf-8') as f:
                json.dump(notifications_data, f, ensure_ascii=False, indent=2)
            
            print(f"✅ Notificación {notification_type} guardada para revisión manual")
            return True
            
        except Exception as e:
            print(f"❌ Error guardando notificación: {e}")
            return False
    
    def get_pending_notifications(self) -> List[Dict[str, Any]]:
        """Obtener notificaciones pendientes"""
        try:
            with open(self.notifications_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
                return [n for n in data['notifications'] if n['status'] == 'pending']
        except Exception:
            return []
    
    def mark_notification_read(self, notification_id: int) -> bool:
        """Marcar notificación como leída"""
        try:
            with open(self.notifications_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            for notification in data['notifications']:
                if notification['id'] == notification_id:
                    notification['status'] = 'read'
                    notification['read_at'] = datetime.now().isoformat()
                    break
            
            with open(self.notifications_file, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
            
            return True
        except Exception:
            return False
    
    def send_contact_notification(self, nombre: str, email: str, asunto: str, mensaje: str) -> bool:
        """Procesar notificación de contacto"""
        notification_data = {
            'nombre': nombre,
            'email': email,
            'asunto': asunto,
            'mensaje': mensaje,
            'source': 'web_contact_form'
        }
        
        return self.save_notification('contact_form', notification_data)
    
    def send_form_notification(self, form_type: str, form_data: Dict[str, Any]) -> bool:
        """Procesar notificación de formulario"""
        notification_data = {
            'form_type': form_type,
            'form_data': form_data,
            'source': f'web_form_{form_type}'
        }
        
        return self.save_notification('form_submission', notification_data)
    
    def get_notification_summary(self) -> Dict[str, Any]:
        """Obtener resumen de notificaciones"""
        pending = self.get_pending_notifications()
        
        summary = {
            'total_pending': len(pending),
            'high_priority': len([n for n in pending if n['priority'] == 'high']),
            'medium_priority': len([n for n in pending if n['priority'] == 'medium']),
            'recent_notifications': pending[-5:] if pending else []
        }
        
        return summary

# Instancia global
fallback_system = EmailFallbackSystem()

def send_contact_notification_fallback(nombre: str, email: str, asunto: str, mensaje: str) -> bool:
    """Función de respaldo para notificaciones de contacto"""
    return fallback_system.send_contact_notification(nombre, email, asunto, mensaje)

def send_form_notification_fallback(form_type: str, data: Dict[str, Any]) -> bool:
    """Función de respaldo para notificaciones de formulario"""
    return fallback_system.send_form_notification(form_type, data)

def get_pending_notifications_summary() -> Dict[str, Any]:
    """Obtener resumen de notificaciones pendientes"""
    return fallback_system.get_notification_summary()

print("✅ Sistema de respaldo de notificaciones inicializado")
print("📋 Las notificaciones se guardan en pending_notifications.json para revisión manual")