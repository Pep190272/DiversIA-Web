"""
Servicio de integración de formularios para DiversIA
Maneja todos los formularios web y asegura persistencia en base de datos
"""

import json
import os
from datetime import datetime
from flask import flash
import logging

# Configurar logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def process_form_submission(form_type, data, source='web_form'):
    """Función de compatibilidad para procesar formularios"""
    try:
        from data_persistence_manager import persistence_manager
        
        # Cargar datos existentes
        crm_data = persistence_manager.load_data()
        
        # Generar ID único
        if form_type == 'contacto':
            contacts = crm_data.setdefault('contacts', [])
            max_id = max([c.get('id', 0) for c in contacts], default=0)
            contact_record = {
                'id': max_id + 1,
                'name': data.get('nombre'),
                'email': data.get('email'),
                'message': data.get('mensaje'),
                'tipo_interes': data.get('tipo_interes'),
                'source': source,
                'created_at': data.get('created_at', '2025-08-21'),
                'status': 'Nuevo'
            }
            contacts.append(contact_record)
            
        elif form_type == 'registro_persona':
            users = crm_data.setdefault('users', [])
            max_id = max([u.get('id', 0) for u in users], default=0)
            user_record = {
                'id': max_id + 1,
                'name': f"{data.get('nombre', '')} {data.get('apellidos', '')}".strip(),
                'email': data.get('email'),
                'phone': data.get('telefono'),
                'city': data.get('ciudad'),
                'tipo_neurodivergencia': data.get('tipo_neurodivergencia'),
                'source': source,
                'created_at': data.get('created_at', '2025-08-21'),
                'status': 'Activo'
            }
            users.append(user_record)
        
        # Guardar datos
        persistence_manager.save_data(crm_data)
        return max_id + 1
        
    except Exception as e:
        print(f"Error en process_form_submission: {e}")
        return None

class FormIntegrationService:
    """Servicio para integrar formularios con base de datos y sistemas de respaldo"""
    
    def __init__(self):
        self.backup_file = 'form_submissions_backup.json'
    
    def save_company_form(self, form_data):
        """Guardar formulario de empresa con múltiples respaldos"""
        try:
            # 1. Intentar SQLite primero
            success_sqlite = self._save_to_sqlite_company(form_data)
            
            if success_postgres:
                logger.info(f"✅ Empresa guardada en PostgreSQL: {form_data.get('nombre')}")
            else:
                # 2. Sistema de respaldo CRM
                success_crm = self._save_to_crm_company(form_data)
                
                if success_crm:
                    logger.info(f"✅ Empresa guardada en CRM: {form_data.get('nombre')}")
                else:
                    # 3. Respaldo manual en archivo
                    self._save_to_backup_file('company', form_data)
                    logger.info(f"✅ Empresa guardada en archivo respaldo: {form_data.get('nombre')}")
            
            # Enviar notificación
            self._send_notification('company', form_data)
            
            return True
            
        except Exception as e:
            logger.error(f"❌ Error guardando empresa: {e}")
            # Guardar en respaldo de emergencia
            self._save_to_backup_file('company_emergency', form_data)
            return False
    
    def save_job_offer_form(self, form_data):
        """Guardar formulario de oferta de trabajo"""
        try:
            # 1. Intentar PostgreSQL
            success_postgres = self._save_to_postgres_job_offer(form_data)
            
            if success_postgres:
                logger.info(f"✅ Oferta guardada en PostgreSQL: {form_data.get('titulo')}")
            else:
                # 2. Sistema CRM
                success_crm = self._save_to_crm_job_offer(form_data)
                
                if success_crm:
                    logger.info(f"✅ Oferta guardada en CRM: {form_data.get('titulo')}")
                else:
                    # 3. Archivo respaldo
                    self._save_to_backup_file('job_offer', form_data)
                    logger.info(f"✅ Oferta guardada en respaldo: {form_data.get('titulo')}")
            
            # Notificación
            self._send_notification('job_offer', form_data)
            
            return True
            
        except Exception as e:
            logger.error(f"❌ Error guardando oferta: {e}")
            self._save_to_backup_file('job_offer_emergency', form_data)
            return False
    
    def save_user_registration(self, form_data, neurodivergence_type):
        """Guardar registro de usuario neurodivergente"""
        try:
            # 1. PostgreSQL
            success_postgres = self._save_to_postgres_user(form_data, neurodivergence_type)
            
            if success_postgres:
                logger.info(f"✅ Usuario guardado en PostgreSQL: {form_data.get('nombre')}")
            else:
                # 2. CRM
                success_crm = self._save_to_crm_user(form_data, neurodivergence_type)
                
                if success_crm:
                    logger.info(f"✅ Usuario guardado en CRM: {form_data.get('nombre')}")
                else:
                    # 3. Respaldo
                    self._save_to_backup_file('user_registration', {
                        **form_data,
                        'neurodivergence_type': neurodivergence_type
                    })
                    logger.info(f"✅ Usuario guardado en respaldo: {form_data.get('nombre')}")
            
            # Notificación
            self._send_notification('user_registration', {
                **form_data,
                'neurodivergence_type': neurodivergence_type
            })
            
            return True
            
        except Exception as e:
            logger.error(f"❌ Error guardando usuario: {e}")
            self._save_to_backup_file('user_emergency', form_data)
            return False
    
    def save_contact_form(self, form_data):
        """Guardar formulario de contacto"""
        try:
            # Múltiples sistemas de respaldo
            self._save_to_crm_contact(form_data)
            self._save_to_backup_file('contact', form_data)
            self._send_notification('contact', form_data)
            
            logger.info(f"✅ Contacto guardado: {form_data.get('nombre')}")
            return True
            
        except Exception as e:
            logger.error(f"❌ Error guardando contacto: {e}")
            return False
    
    # === MÉTODOS PRIVADOS ===
    
    def _save_to_postgres_company(self, data):
        """Guardar empresa en PostgreSQL"""
        try:
            from models import Company
            from app import db
            
            # Verificar el modelo Company primero
            from models import Company
            import inspect
            
            # Obtener parámetros válidos del constructor
            sig = inspect.signature(Company.__init__)
            valid_params = list(sig.parameters.keys())[1:]  # Excluir 'self'
            
            company_data = {}
            # Mapear datos a nombres de columnas correctos
            field_mapping = {
                'nombre': 'name',
                'email': 'email', 
                'telefono': 'phone',
                'sector': 'sector',
                'tamaño': 'size',
                'ciudad': 'city',
                'web': 'website',
                'descripcion': 'description'
            }
            
            for field, value in data.items():
                if field in field_mapping and field_mapping[field] in valid_params:
                    company_data[field_mapping[field]] = value
                elif field in valid_params:
                    company_data[field] = value
            
            company = Company(**company_data)
            
            db.session.add(company)
            db.session.commit()
            return True
            
        except Exception as e:
            logger.warning(f"PostgreSQL empresa falló: {e}")
            return False
    
    def _save_to_postgres_job_offer(self, data):
        """Guardar oferta en PostgreSQL"""
        try:
            from models import JobOffer
            from app import db
            
            offer = JobOffer(
                title=data.get('titulo'),
                company_name=data.get('empresa'),
                location=data.get('ubicacion'),
                salary=data.get('salario'),
                description=data.get('descripcion'),
                requirements=data.get('requisitos'),
                benefits=data.get('beneficios')
            )
            
            db.session.add(offer)
            db.session.commit()
            return True
            
        except Exception as e:
            logger.warning(f"PostgreSQL oferta falló: {e}")
            return False
    
    def _save_to_postgres_user(self, data, neurodivergence_type):
        """Guardar usuario en PostgreSQL"""
        try:
            from models import User
            from app import db
            
            user = User(
                username=data.get('email'),
                email=data.get('email'),
                first_name=data.get('nombre'),
                last_name=data.get('apellidos'),
                neurodivergence_type=neurodivergence_type
            )
            
            db.session.add(user)
            db.session.commit()
            return True
            
        except Exception as e:
            logger.warning(f"PostgreSQL usuario falló: {e}")
            return False
    
    def _save_to_crm_company(self, data):
        """Guardar empresa en sistema CRM"""
        try:
            from data_persistence_manager import persistence_manager
            crm_data = persistence_manager.load_data()
            
            # Generar ID único
            max_id = max([c.get('id', 0) for c in crm_data.get('companies', [])], default=0)
            
            company_record = {
                'id': max_id + 1,
                'name': data.get('nombre'),
                'email': data.get('email'),
                'phone': data.get('telefono'),
                'sector': data.get('sector'),
                'size': data.get('tamaño'),
                'city': data.get('ciudad'),
                'website': data.get('web'),
                'description': data.get('descripcion'),
                'created_at': datetime.now().isoformat(),
                'source': 'web_form'
            }
            
            crm_data.setdefault('companies', []).append(company_record)
            return persistence_manager.save_data(crm_data)
            
        except Exception as e:
            logger.warning(f"CRM empresa falló: {e}")
            return False
    
    def _save_to_crm_job_offer(self, data):
        """Guardar oferta en sistema CRM"""
        try:
            from data_persistence_manager import persistence_manager
            crm_data = persistence_manager.load_data()
            
            max_id = max([o.get('id', 0) for o in crm_data.get('job_offers', [])], default=0)
            
            offer_record = {
                'id': max_id + 1,
                'title': data.get('titulo'),
                'company_name': data.get('empresa'),
                'location': data.get('ubicacion'),
                'salary': data.get('salario'),
                'description': data.get('descripcion'),
                'requirements': data.get('requisitos'),
                'benefits': data.get('beneficios'),
                'active': True,
                'created_at': datetime.now().isoformat(),
                'source': 'web_form'
            }
            
            crm_data.setdefault('job_offers', []).append(offer_record)
            return persistence_manager.save_data(crm_data)
            
        except Exception as e:
            logger.warning(f"CRM oferta falló: {e}")
            return False
    
    def _save_to_crm_user(self, data, neurodivergence_type):
        """Guardar usuario en sistema CRM"""
        try:
            from data_persistence_manager import persistence_manager
            crm_data = persistence_manager.load_data()
            
            max_id = max([c.get('id', 0) for c in crm_data.get('contacts', [])], default=0)
            
            user_record = {
                'id': max_id + 1,
                'name': f"{data.get('nombre', '')} {data.get('apellidos', '')}".strip(),
                'email': data.get('email'),
                'phone': data.get('telefono'),
                'city': data.get('ciudad'),
                'neurodivergence': neurodivergence_type,
                'age': data.get('edad'),
                'created_at': datetime.now().isoformat(),
                'source': 'web_registration',
                'type': 'Usuario ND'
            }
            
            crm_data.setdefault('contacts', []).append(user_record)
            return persistence_manager.save_data(crm_data)
            
        except Exception as e:
            logger.warning(f"CRM usuario falló: {e}")
            return False
    
    def _save_to_crm_contact(self, data):
        """Guardar contacto en sistema CRM"""
        try:
            from data_persistence_manager import persistence_manager
            crm_data = persistence_manager.load_data()
            
            max_id = max([c.get('id', 0) for c in crm_data.get('contacts', [])], default=0)
            
            contact_record = {
                'id': max_id + 1,
                'name': data.get('nombre'),
                'email': data.get('email'),
                'subject': data.get('asunto'),
                'message': data.get('mensaje'),
                'created_at': datetime.now().isoformat(),
                'source': 'contact_form',
                'type': 'Consulta'
            }
            
            crm_data.setdefault('contacts', []).append(contact_record)
            return persistence_manager.save_data(crm_data)
            
        except Exception as e:
            logger.warning(f"CRM contacto falló: {e}")
            return False
    
    def _save_to_backup_file(self, form_type, data):
        """Guardar en archivo de respaldo"""
        try:
            backup_data = {
                'timestamp': datetime.now().isoformat(),
                'form_type': form_type,
                'data': data
            }
            
            # Cargar respaldos existentes
            backups = []
            if os.path.exists(self.backup_file):
                with open(self.backup_file, 'r', encoding='utf-8') as f:
                    backups = json.load(f)
            
            backups.append(backup_data)
            
            # Guardar
            with open(self.backup_file, 'w', encoding='utf-8') as f:
                json.dump(backups, f, ensure_ascii=False, indent=2)
            
            return True
            
        except Exception as e:
            logger.error(f"Error guardando en archivo respaldo: {e}")
            return False
    
    def _send_notification(self, notification_type, data):
        """Enviar notificación por email"""
        try:
            from email_system_reliable import send_contact_notification
            
            if notification_type == 'company':
                subject = f"Nueva empresa registrada: {data.get('nombre')}"
                message = f"""
                Nueva empresa registrada en DiversIA:
                
                Nombre: {data.get('nombre')}
                Email: {data.get('email')}
                Sector: {data.get('sector')}
                Ciudad: {data.get('ciudad')}
                """
                
            elif notification_type == 'job_offer':
                subject = f"Nueva oferta publicada: {data.get('titulo')}"
                message = f"""
                Nueva oferta de trabajo:
                
                Título: {data.get('titulo')}
                Empresa: {data.get('empresa')}
                Ubicación: {data.get('ubicacion')}
                Salario: {data.get('salario')}
                """
                
            elif notification_type == 'user_registration':
                subject = f"Nuevo registro usuario: {data.get('nombre')}"
                message = f"""
                Nuevo usuario neurodivergente registrado:
                
                Nombre: {data.get('nombre')} {data.get('apellidos', '')}
                Email: {data.get('email')}
                Tipo: {data.get('neurodivergence_type')}
                """
                
            elif notification_type == 'contact':
                subject = f"Nuevo contacto: {data.get('asunto')}"
                message = f"""
                Nuevo mensaje de contacto:
                
                Nombre: {data.get('nombre')}
                Email: {data.get('email')}
                Asunto: {data.get('asunto')}
                Mensaje: {data.get('mensaje')}
                """
            
            else:
                return False
            
            send_contact_notification(
                data.get('nombre', 'Usuario'),
                data.get('email', 'noemail@diversia.com'),
                subject,
                message
            )
            
            return True
            
        except Exception as e:
            logger.warning(f"Error enviando notificación: {e}")
            return False

# Instancia global
form_service = FormIntegrationService()

print("✅ Servicio de integración de formularios inicializado")
print("🔧 Respaldo triple: PostgreSQL → CRM → Archivo")
print("📧 Notificaciones automáticas por email")