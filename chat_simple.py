"""
Sistema de Chat Inteligente Simplificado para DiversIA
Compatible con Mistral AI y funcionalidad offline
"""

import os
import json
import logging
from datetime import datetime
from typing import Dict, Optional

# Configurar logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class DiversIAChatBot:
    """Chatbot inteligente para DiversIA con respaldo local"""
    
    def __init__(self):
        self.mistral_api_key = os.getenv('MISTRAL_API_KEY')
        self.knowledge_base = self.load_knowledge_base()
        
        # Verificar si Mistral está disponible
        try:
            import requests
            self.requests_available = True
            if self.mistral_api_key:
                self.mistral_enabled = True
                logger.info("✅ Chat con Mistral AI activado")
            else:
                self.mistral_enabled = False
                logger.warning("⚠️ Mistral API key no encontrada")
        except ImportError:
            self.requests_available = False
            self.mistral_enabled = False
            logger.warning("⚠️ Requests no disponible - modo offline")
    
    def load_knowledge_base(self) -> Dict:
        """Cargar base de conocimientos local"""
        return {
            "saludo": [
                "¡Hola! Soy el asistente de DiversIA. ¿En qué puedo ayudarte hoy?",
                "¡Bienvenido a DiversIA! Estoy aquí para ayudarte con cualquier pregunta sobre neurodivergencia y empleo."
            ],
            "registro": [
                "Para registrarte, puedes hacer clic en 'Haz mi test' en la página principal o ir directamente a la sección de registro.",
                "El proceso de registro es muy sencillo. Te haremos unas preguntas para conocer mejor tu perfil y encontrar las mejores oportunidades para ti."
            ],
            "empresas": [
                "Las empresas pueden registrarse en nuestra plataforma para encontrar talento neurodivergente.",
                "Ofrecemos a las empresas acceso a candidatos únicos con habilidades especiales y perspectivas valiosas."
            ],
            "neurodivergencia": [
                "La neurodivergencia incluye condiciones como TDAH, TEA, dislexia, y muchas otras que representan formas diferentes de pensar.",
                "En DiversIA celebramos la neurodiversidad como una fortaleza que aporta valor único al mundo laboral."
            ],
            "ayuda": [
                "Puedes contactarnos a través del formulario de contacto o unirte a nuestra comunidad de Telegram: https://t.me/DiversiaSupport",
                "Si necesitas ayuda específica, también puedes escribir a diversiaeternals@gmail.com"
            ]
        }
    
    def get_intent(self, message: str) -> str:
        """Detectar la intención del mensaje"""
        message_lower = message.lower()
        
        if any(word in message_lower for word in ['hola', 'buenas', 'saludos']):
            return 'saludo'
        elif any(word in message_lower for word in ['registro', 'registrar', 'unir']):
            return 'registro'
        elif any(word in message_lower for word in ['empresa', 'empleador', 'contrat']):
            return 'empresas'
        elif any(word in message_lower for word in ['neurodiverg', 'tdah', 'tea', 'dislexia', 'autis']):
            return 'neurodivergencia'
        elif any(word in message_lower for word in ['ayuda', 'help', 'contacto', 'soporte']):
            return 'ayuda'
        else:
            return 'general'
    
    def get_local_response(self, intent: str) -> str:
        """Obtener respuesta local basada en la intención"""
        if intent in self.knowledge_base:
            import random
            return random.choice(self.knowledge_base[intent])
        else:
            return "Gracias por tu mensaje. Para ayudarte mejor, puedes explorar nuestra web o contactarnos directamente."
    
    def query_mistral(self, message: str, context: Dict) -> Optional[str]:
        """Consultar Mistral AI para respuestas avanzadas"""
        if not self.mistral_enabled or not self.requests_available:
            return None
        
        try:
            import requests
            
            headers = {
                'Content-Type': 'application/json',
                'Authorization': f'Bearer {self.mistral_api_key}'
            }
            
            prompt = f"""
            Eres el asistente de DiversIA, una plataforma de empleo para personas neurodivergentes.
            
            Contexto de DiversIA:
            - Conectamos personas neurodivergentes con empresas inclusivas
            - Ofrecemos formularios especializados para TDAH, TEA, dislexia, etc.
            - Tenemos una comunidad activa y recursos educativos
            
            Pregunta del usuario: {message}
            
            Responde de forma amigable, útil y enfocada en cómo DiversIA puede ayudar.
            Mantén la respuesta concisa (máximo 2-3 oraciones).
            """
            
            data = {
                "model": "mistral-small",
                "messages": [{"role": "user", "content": prompt}],
                "max_tokens": 150,
                "temperature": 0.7
            }
            
            response = requests.post(
                'https://api.mistral.ai/v1/chat/completions',
                headers=headers,
                json=data,
                timeout=10
            )
            
            if response.status_code == 200:
                result = response.json()
                return result['choices'][0]['message']['content'].strip()
            else:
                logger.error(f"Mistral API error: {response.status_code}")
                return None
                
        except Exception as e:
            logger.error(f"Error querying Mistral: {e}")
            return None
    
    def get_response(self, message: str, context: Optional[Dict] = None) -> Dict:
        """Obtener respuesta principal del chatbot"""
        if context is None:
            context = {}
        
        intent = self.get_intent(message)
        
        # Intentar respuesta con Mistral AI primero
        mistral_response = self.query_mistral(message, context)
        
        if mistral_response:
            return {
                'response': mistral_response,
                'intent': intent,
                'source': 'mistral',
                'confidence': 0.9,
                'timestamp': datetime.now().isoformat()
            }
        else:
            # Usar respuesta local como fallback
            local_response = self.get_local_response(intent)
            return {
                'response': local_response,
                'intent': intent,
                'source': 'local',
                'confidence': 0.7,
                'timestamp': datetime.now().isoformat()
            }

# Instancia global del chatbot
diversia_chatbot = DiversIAChatBot()

def get_chat_response(message: str, context: Optional[Dict] = None) -> Dict:
    """Función principal para obtener respuestas del chat"""
    return diversia_chatbot.get_response(message, context)