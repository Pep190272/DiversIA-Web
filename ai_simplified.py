"""
DiversIA AI Agent - Versión Simplificada
Agente inteligente funcional con Mistral sin dependencias complejas
"""

import os
import json
import asyncio
import logging
from datetime import datetime
from typing import Dict, List, Optional, Any

import requests
from openai import OpenAI

logger = logging.getLogger(__name__)

class DiversIASimpleAgent:
    """
    Agente inteligente simplificado para DiversIA
    """
    
    def __init__(self):
        self.setup_mistral()
        
    def setup_mistral(self):
        """Configurar cliente de Mistral"""
        api_key = os.getenv('MISTRAL_API_KEY')
        if not api_key:
            logger.warning("MISTRAL_API_KEY not found")
            self.mistral_client = None
            return
            
        self.mistral_client = OpenAI(
            api_key=api_key,
            base_url="https://api.mistral.ai/v1"
        )
        logger.info("✅ Mistral AI client initialized")
    
    async def process_message(self, message: str, user_context: Dict) -> Dict[str, Any]:
        """
        Procesar mensaje con IA
        """
        try:
            # 1. Detectar intención
            intent = self.detect_intent(message)
            
            # 2. Obtener datos del sistema
            system_data = await self.get_system_data()
            
            # 3. Generar respuesta con Mistral
            if self.mistral_client:
                ai_response = await self.generate_mistral_response(message, intent, system_data)
            else:
                ai_response = self.get_fallback_response(message, intent)
            
            # 4. Enriquecer respuesta con datos
            enhanced_response = self.enhance_response(ai_response, intent, system_data)
            
            return {
                'final_response': enhanced_response,
                'response': enhanced_response,
                'intent': intent,
                'system_data': system_data,
                'confidence': 0.95 if self.mistral_client else 0.75,
                'powered_by': 'Mistral AI' if self.mistral_client else 'DiversIA Local AI'
            }
            
        except Exception as e:
            logger.error(f"Error processing message: {e}")
            return {
                'final_response': self.get_error_response(),
                'response': self.get_error_response(),
                'intent': 'error',
                'confidence': 0.5,
                'error': str(e)
            }
    
    def detect_intent(self, message: str) -> str:
        """Detectar intención del usuario"""
        message_lower = message.lower()
        
        if any(word in message_lower for word in ['registro', 'registrar', 'registrarme']):
            return 'registration'
        elif any(word in message_lower for word in ['trabajo', 'empleo', 'busco', 'oportunidad']):
            return 'job_search'
        elif any(word in message_lower for word in ['tdah', 'adhd', 'tea', 'autismo', 'dislexia']):
            return 'neurodivergence_info'
        elif any(word in message_lower for word in ['empresa', 'contratar', 'corporativo']):
            return 'company_registration'
        elif any(word in message_lower for word in ['ayuda', 'soporte', 'problema']):
            return 'support'
        else:
            return 'general'
    
    async def get_system_data(self) -> Dict[str, Any]:
        """Obtener datos del sistema"""
        try:
            # Intentar obtener estadísticas de la base de datos
            app_url = os.getenv('APP_BASE_URL', 'https://073083d2-dd14-424e-a549-4c03e48131b7-00-1vatfbc2lts0v.janeway.replit.dev')
            
            response = requests.get(f"{app_url}/api/v1/user-insights", timeout=5)
            if response.status_code == 200:
                return response.json()
            else:
                return {'total_users': 0, 'total_companies': 0}
                
        except Exception as e:
            logger.error(f"Error getting system data: {e}")
            return {'total_users': 0, 'total_companies': 0}
    
    async def generate_mistral_response(self, message: str, intent: str, system_data: Dict) -> str:
        """Generar respuesta con Mistral"""
        try:
            # Construir prompt contextual
            system_prompt = self.build_system_prompt(intent, system_data)
            
            response = self.mistral_client.chat.completions.create(
                model="mistral-medium",
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": message}
                ],
                max_tokens=250,
                temperature=0.7
            )
            
            return response.choices[0].message.content
            
        except Exception as e:
            logger.error(f"Error with Mistral: {e}")
            return self.get_fallback_response(message, intent)
    
    def build_system_prompt(self, intent: str, system_data: Dict) -> str:
        """Construir prompt del sistema"""
        base_prompt = """Eres el asistente inteligente de DiversIA, una plataforma de inclusión laboral para personas neurodivergentes (TDAH, TEA, Dislexia).

Características de tu personalidad:
- Empático y profesional
- Especializado en neurodivergencia e inclusión laboral
- Respuestas concisas pero completas
- Siempre en español
- Orientado a la acción

Datos actuales del sistema:"""
        
        if system_data.get('total_users', 0) > 0:
            base_prompt += f"\n- {system_data['total_users']} profesionales registrados"
        if system_data.get('total_companies', 0) > 0:
            base_prompt += f"\n- {system_data['total_companies']} empresas inclusivas"
        
        intent_prompts = {
            'registration': "\n\nEl usuario quiere registrarse. Pregunta si es candidato neurodivergente o empresa. Explica brevemente los beneficios.",
            'job_search': "\n\nEl usuario busca empleo. Pregunta sobre su experiencia y tipo de neurodivergencia para ofrecer matching personalizado.",
            'neurodivergence_info': "\n\nEl usuario pregunta sobre neurodivergencia. Proporciona información útil y conecta con recursos de DiversIA.",
            'company_registration': "\n\nUna empresa quiere contratar talento neurodivergente. Explica nuestro proceso de matching y beneficios.",
            'support': "\n\nEl usuario necesita ayuda técnica. Ofrece soluciones prácticas y escalamiento si es necesario."
        }
        
        return base_prompt + intent_prompts.get(intent, "\n\nResponde de manera útil y dirigida hacia los servicios de DiversIA.")
    
    def get_fallback_response(self, message: str, intent: str) -> str:
        """Respuestas de fallback sin IA"""
        responses = {
            'registration': 'Te ayudo con el registro en DiversIA. ¿Eres una persona neurodivergente buscando empleo o una empresa que quiere contratar talento diverso?',
            'job_search': 'Nuestro sistema de matching conecta candidatos neurodivergentes con empresas inclusivas. ¿Cuál es tu área de experiencia y tipo de neurodivergencia?',
            'neurodivergence_info': 'DiversIA apoya TDAH, TEA y Dislexia con formularios especializados y conexión con empresas inclusivas. ¿Sobre qué neurodivergencia necesitas información?',
            'company_registration': 'Ayudamos a empresas a encontrar talento neurodivergente excepcional. Nuestro proceso incluye matching inteligente y orientación sobre inclusión.',
            'support': 'Estoy aquí para ayudarte con cualquier consulta sobre DiversIA. ¿Podrías explicarme específicamente qué necesitas?',
            'general': 'Soy el asistente de DiversIA, especializado en inclusión laboral para personas neurodivergentes. Puedo ayudarte con registro, búsqueda de empleo, información sobre TDAH/TEA/Dislexia, o registro de empresas.'
        }
        return responses.get(intent, responses['general'])
    
    def enhance_response(self, base_response: str, intent: str, system_data: Dict) -> str:
        """Enriquecer respuesta con datos específicos"""
        enhanced = base_response
        
        # Agregar estadísticas si están disponibles
        if system_data.get('total_users', 0) > 0:
            enhanced += f"\n\n📊 Actualmente tenemos {system_data['total_users']} profesionales registrados"
            if system_data.get('total_companies', 0) > 0:
                enhanced += f" y {system_data['total_companies']} empresas inclusivas"
        
        # Agregar CTAs específicos
        cta_map = {
            'registration': '\n\n🔗 ¿Te gustaría que te ayude con el proceso de registro paso a paso?',
            'job_search': '\n\n💼 Puedo ayudarte a encontrar oportunidades específicas para tu perfil.',
            'neurodivergence_info': '\n\n🧠 ¿Necesitas información sobre recursos específicos o evaluaciones?',
            'company_registration': '\n\n🏢 ¿Te gustaría conocer cómo funciona nuestro sistema de matching?',
            'support': '\n\n💬 Si necesitas ayuda adicional, puedo escalarlo al equipo técnico.'
        }
        
        if intent in cta_map:
            enhanced += cta_map[intent]
        
        return enhanced
    
    def get_error_response(self) -> str:
        """Respuesta de error"""
        return "Disculpa, estoy teniendo dificultades técnicas en este momento. Puedo ayudarte con información general sobre DiversIA mientras se resuelve. ¿En qué puedo asistirte?"

# Instancia global
simple_agent = DiversIASimpleAgent()

async def process_chat_message_simple(message: str, user_id: str, session_id: str, page: str) -> Dict[str, Any]:
    """
    Función principal para procesar mensajes - versión simplificada
    """
    user_context = {
        'user_id': user_id,
        'session_id': session_id,
        'page': page,
        'timestamp': datetime.now().isoformat()
    }
    
    return await simple_agent.process_message(message, user_context)

# Función de test
if __name__ == "__main__":
    async def test():
        result = await process_chat_message_simple(
            "Hola, tengo TDAH y busco trabajo en programación",
            "test_user", "test_session", "/"
        )
        print(json.dumps(result, indent=2, ensure_ascii=False))
    
    asyncio.run(test())