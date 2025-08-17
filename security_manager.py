"""
Security Manager for DiversIA
Gestión de seguridad de máximo nivel para datos sensibles
"""

import os
import jwt
import bcrypt
import secrets
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
import base64
import logging
import hashlib

logger = logging.getLogger(__name__)

class SecurityManager:
    """
    Gestor de seguridad centralizado para DiversIA
    """
    
    def __init__(self):
        self.setup_encryption()
        self.setup_jwt()
        self.audit_log = []
        
    def setup_encryption(self):
        """Configurar sistema de cifrado"""
        try:
            # Obtener o generar clave maestra
            master_key = os.getenv('MASTER_ENCRYPTION_KEY')
            if not master_key:
                # Generar nueva clave para desarrollo
                master_key = Fernet.generate_key().decode()
                logger.warning("Generated new master key - set MASTER_ENCRYPTION_KEY in production")
            
            # Configurar Fernet para cifrado simétrico
            if isinstance(master_key, str):
                master_key = master_key.encode()
            
            self.cipher_suite = Fernet(master_key)
            logger.info("✅ Encryption system initialized")
            
        except Exception as e:
            logger.error(f"Error setting up encryption: {e}")
            self.cipher_suite = None
    
    def setup_jwt(self):
        """Configurar JWT para autenticación"""
        self.jwt_secret = os.getenv('JWT_SECRET_KEY', secrets.token_urlsafe(32))
        self.jwt_algorithm = 'HS256'
        self.jwt_expiration_hours = 24
        logger.info("✅ JWT system initialized")
    
    def encrypt_sensitive_data(self, data: str) -> str:
        """Cifrar datos sensibles"""
        try:
            if not self.cipher_suite:
                logger.error("Encryption not available")
                return data
            
            if isinstance(data, str):
                data = data.encode('utf-8')
            
            encrypted_data = self.cipher_suite.encrypt(data)
            return base64.b64encode(encrypted_data).decode('utf-8')
            
        except Exception as e:
            logger.error(f"Error encrypting data: {e}")
            return data
    
    def decrypt_sensitive_data(self, encrypted_data: str) -> str:
        """Descifrar datos sensibles"""
        try:
            if not self.cipher_suite:
                logger.error("Encryption not available")
                return encrypted_data
            
            encrypted_bytes = base64.b64decode(encrypted_data.encode('utf-8'))
            decrypted_data = self.cipher_suite.decrypt(encrypted_bytes)
            return decrypted_data.decode('utf-8')
            
        except Exception as e:
            logger.error(f"Error decrypting data: {e}")
            return encrypted_data
    
    def hash_password(self, password: str) -> str:
        """Hash seguro de contraseñas"""
        try:
            salt = bcrypt.gensalt(rounds=12)
            hashed = bcrypt.hashpw(password.encode('utf-8'), salt)
            return hashed.decode('utf-8')
        except Exception as e:
            logger.error(f"Error hashing password: {e}")
            return password
    
    def verify_password(self, password: str, hashed: str) -> bool:
        """Verificar contraseña"""
        try:
            return bcrypt.checkpw(password.encode('utf-8'), hashed.encode('utf-8'))
        except Exception as e:
            logger.error(f"Error verifying password: {e}")
            return False
    
    def generate_jwt_token(self, user_data: Dict) -> str:
        """Generar token JWT"""
        try:
            payload = {
                'user_id': user_data.get('user_id'),
                'email': user_data.get('email'),
                'role': user_data.get('role', 'user'),
                'permissions': user_data.get('permissions', []),
                'iat': datetime.utcnow(),
                'exp': datetime.utcnow() + timedelta(hours=self.jwt_expiration_hours)
            }
            
            token = jwt.encode(payload, self.jwt_secret, algorithm=self.jwt_algorithm)
            
            # Log de auditoría
            self.log_security_event('token_generated', {
                'user_id': user_data.get('user_id'),
                'timestamp': datetime.utcnow().isoformat()
            })
            
            return token
            
        except Exception as e:
            logger.error(f"Error generating JWT: {e}")
            return None
    
    def verify_jwt_token(self, token: str) -> Optional[Dict]:
        """Verificar token JWT"""
        try:
            payload = jwt.decode(token, self.jwt_secret, algorithms=[self.jwt_algorithm])
            
            # Log de auditoría
            self.log_security_event('token_verified', {
                'user_id': payload.get('user_id'),
                'timestamp': datetime.utcnow().isoformat()
            })
            
            return payload
            
        except jwt.ExpiredSignatureError:
            logger.warning("JWT token expired")
            return None
        except jwt.InvalidTokenError:
            logger.warning("Invalid JWT token")
            return None
        except Exception as e:
            logger.error(f"Error verifying JWT: {e}")
            return None
    
    def sanitize_input(self, input_data: str) -> str:
        """Sanitizar entrada de usuario"""
        try:
            # Remover caracteres peligrosos
            dangerous_chars = ['<', '>', '"', "'", '&', 'script', 'javascript:', 'data:']
            sanitized = input_data
            
            for char in dangerous_chars:
                sanitized = sanitized.replace(char, '')
            
            # Limitar longitud
            if len(sanitized) > 1000:
                sanitized = sanitized[:1000]
            
            return sanitized.strip()
            
        except Exception as e:
            logger.error(f"Error sanitizing input: {e}")
            return ""
    
    def generate_api_key(self, user_id: str, scope: List[str]) -> str:
        """Generar clave API"""
        try:
            # Crear payload de la clave
            key_data = {
                'user_id': user_id,
                'scope': scope,
                'created_at': datetime.utcnow().isoformat(),
                'random': secrets.token_urlsafe(16)
            }
            
            # Cifrar los datos
            encrypted_data = self.encrypt_sensitive_data(str(key_data))
            
            # Crear hash para identificación rápida
            key_hash = hashlib.sha256(encrypted_data.encode()).hexdigest()[:16]
            
            api_key = f"diversia_{key_hash}_{encrypted_data}"
            
            # Log de auditoría
            self.log_security_event('api_key_generated', {
                'user_id': user_id,
                'scope': scope,
                'timestamp': datetime.utcnow().isoformat()
            })
            
            return api_key
            
        except Exception as e:
            logger.error(f"Error generating API key: {e}")
            return None
    
    def verify_api_key(self, api_key: str) -> Optional[Dict]:
        """Verificar clave API"""
        try:
            if not api_key.startswith('diversia_'):
                return None
            
            # Extraer datos cifrados
            parts = api_key.split('_', 2)
            if len(parts) != 3:
                return None
            
            encrypted_data = parts[2]
            
            # Descifrar y evaluar
            decrypted_str = self.decrypt_sensitive_data(encrypted_data)
            key_data = eval(decrypted_str)  # En producción usar json.loads
            
            # Verificar vigencia (30 días)
            created_at = datetime.fromisoformat(key_data['created_at'])
            if datetime.utcnow() - created_at > timedelta(days=30):
                logger.warning("API key expired")
                return None
            
            return key_data
            
        except Exception as e:
            logger.error(f"Error verifying API key: {e}")
            return None
    
    def log_security_event(self, event_type: str, details: Dict):
        """Registrar evento de seguridad"""
        try:
            event = {
                'event_type': event_type,
                'timestamp': datetime.utcnow().isoformat(),
                'details': details,
                'ip_hash': self.hash_ip_address(details.get('ip_address', ''))
            }
            
            self.audit_log.append(event)
            
            # Mantener solo los últimos 1000 eventos en memoria
            if len(self.audit_log) > 1000:
                self.audit_log = self.audit_log[-1000:]
            
            logger.info(f"Security event logged: {event_type}")
            
        except Exception as e:
            logger.error(f"Error logging security event: {e}")
    
    def hash_ip_address(self, ip_address: str) -> str:
        """Hash de dirección IP para auditoría"""
        try:
            if not ip_address:
                return ""
            
            # Hash con salt fijo para consistencia en auditorías
            salt = "diversia_ip_salt_2025"
            hash_input = f"{ip_address}{salt}"
            return hashlib.sha256(hash_input.encode()).hexdigest()[:16]
            
        except Exception as e:
            logger.error(f"Error hashing IP: {e}")
            return ""
    
    def check_rate_limit(self, identifier: str, limit: int = 100, window_minutes: int = 60) -> bool:
        """Verificar límite de velocidad"""
        try:
            current_time = datetime.utcnow()
            window_start = current_time - timedelta(minutes=window_minutes)
            
            # Contar eventos recientes para este identificador
            recent_events = [
                event for event in self.audit_log
                if event.get('details', {}).get('identifier') == identifier
                and datetime.fromisoformat(event['timestamp']) > window_start
            ]
            
            if len(recent_events) >= limit:
                self.log_security_event('rate_limit_exceeded', {
                    'identifier': identifier,
                    'limit': limit,
                    'window_minutes': window_minutes
                })
                return False
            
            return True
            
        except Exception as e:
            logger.error(f"Error checking rate limit: {e}")
            return True  # En caso de error, permitir acceso
    
    def anonymize_personal_data(self, data: Dict) -> Dict:
        """Anonimizar datos personales para ML"""
        try:
            anonymized = data.copy()
            
            # Campos a anonimizar
            sensitive_fields = [
                'nombre', 'apellidos', 'email', 'telefono', 
                'direccion', 'dni', 'fecha_nacimiento'
            ]
            
            for field in sensitive_fields:
                if field in anonymized:
                    # Reemplazar con hash único pero consistente
                    original_value = str(anonymized[field])
                    hash_value = hashlib.sha256(original_value.encode()).hexdigest()[:8]
                    anonymized[field] = f"anon_{hash_value}"
            
            # Mantener campos relevantes para ML
            ml_relevant_fields = [
                'tipo_neurodivergencia', 'experiencia_anos', 'nivel_educativo',
                'habilidades', 'preferencias_trabajo', 'adaptaciones_necesarias'
            ]
            
            anonymized['_anonymized'] = True
            anonymized['_anonymization_date'] = datetime.utcnow().isoformat()
            
            return anonymized
            
        except Exception as e:
            logger.error(f"Error anonymizing data: {e}")
            return data
    
    def validate_gdpr_compliance(self, operation: str, data: Dict) -> bool:
        """Validar cumplimiento GDPR"""
        try:
            # Verificar consentimiento
            if not data.get('gdpr_consent', False):
                logger.warning(f"GDPR consent missing for operation: {operation}")
                return False
            
            # Verificar minimización de datos
            required_fields = {
                'user_registration': ['email', 'gdpr_consent'],
                'data_processing': ['user_id', 'gdpr_consent'],
                'data_export': ['user_id', 'export_consent']
            }
            
            if operation in required_fields:
                for field in required_fields[operation]:
                    if field not in data:
                        logger.warning(f"Required GDPR field missing: {field}")
                        return False
            
            # Log de cumplimiento
            self.log_security_event('gdpr_validation', {
                'operation': operation,
                'compliant': True,
                'timestamp': datetime.utcnow().isoformat()
            })
            
            return True
            
        except Exception as e:
            logger.error(f"Error validating GDPR compliance: {e}")
            return False
    
    def get_security_report(self) -> Dict[str, Any]:
        """Generar reporte de seguridad"""
        try:
            current_time = datetime.utcnow()
            last_24h = current_time - timedelta(hours=24)
            
            # Filtrar eventos de las últimas 24h
            recent_events = [
                event for event in self.audit_log
                if datetime.fromisoformat(event['timestamp']) > last_24h
            ]
            
            # Contadores por tipo de evento
            event_counts = {}
            for event in recent_events:
                event_type = event['event_type']
                event_counts[event_type] = event_counts.get(event_type, 0) + 1
            
            # Identificar anomalías
            anomalies = []
            if event_counts.get('rate_limit_exceeded', 0) > 10:
                anomalies.append("High rate limit violations detected")
            
            if event_counts.get('token_verification_failed', 0) > 50:
                anomalies.append("High authentication failure rate")
            
            report = {
                'report_period': '24 hours',
                'total_events': len(recent_events),
                'event_breakdown': event_counts,
                'anomalies': anomalies,
                'security_status': 'GREEN' if not anomalies else 'YELLOW',
                'generated_at': current_time.isoformat()
            }
            
            return report
            
        except Exception as e:
            logger.error(f"Error generating security report: {e}")
            return {'error': str(e)}

# Instancia global del gestor de seguridad
security_manager = SecurityManager()

def encrypt_user_data(data: str) -> str:
    """Función de conveniencia para cifrar datos de usuario"""
    return security_manager.encrypt_sensitive_data(data)

def decrypt_user_data(encrypted_data: str) -> str:
    """Función de conveniencia para descifrar datos de usuario"""
    return security_manager.decrypt_sensitive_data(encrypted_data)

def create_secure_session(user_data: Dict) -> str:
    """Crear sesión segura para usuario"""
    return security_manager.generate_jwt_token(user_data)

def verify_secure_session(token: str) -> Optional[Dict]:
    """Verificar sesión segura"""
    return security_manager.verify_jwt_token(token)

if __name__ == "__main__":
    # Test del sistema de seguridad
    test_data = "Información sensible de prueba"
    encrypted = security_manager.encrypt_sensitive_data(test_data)
    decrypted = security_manager.decrypt_sensitive_data(encrypted)
    
    print(f"Original: {test_data}")
    print(f"Encrypted: {encrypted[:50]}...")
    print(f"Decrypted: {decrypted}")
    print(f"Match: {test_data == decrypted}")
    
    # Test JWT
    user_data = {'user_id': 'test123', 'email': 'test@example.com', 'role': 'user'}
    token = security_manager.generate_jwt_token(user_data)
    verified = security_manager.verify_jwt_token(token)
    
    print(f"JWT Token generated: {bool(token)}")
    print(f"JWT Token verified: {bool(verified)}")
    
    # Reporte de seguridad
    report = security_manager.get_security_report()
    print("Security Report:", report)