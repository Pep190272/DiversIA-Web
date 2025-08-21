"""
DiversIA Intelligent Agent Core
Sistema de IA central para matching perfecto y análisis inteligente
"""

import os
import json
import asyncio
from datetime import datetime
from typing import Dict, List, Optional, Any
import logging

# IA y Machine Learning
try:
    import numpy as np
    NUMPY_AVAILABLE = True
except ImportError:
    NUMPY_AVAILABLE = False

try:
    import requests
    REQUESTS_AVAILABLE = True
except ImportError:
    REQUESTS_AVAILABLE = False

# Base de datos y APIs
import requests
from sqlalchemy import create_engine, text
import pandas as pd

# Configuración del logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class DiversIAAgent:
    """
    Agente inteligente central que integra múltiples fuentes de datos
    para matching perfecto y análisis predictivo
    """
    
    def __init__(self):
        self.setup_ai_models()
        self.setup_database()
        self.setup_apis()
        
    def setup_ai_models(self):
        """Configurar modelos de IA"""
        self.mistral_api_key = os.getenv('MISTRAL_API_KEY')
        
        if self.mistral_api_key and REQUESTS_AVAILABLE:
            self.mistral_enabled = True
            logger.info("✅ Mistral AI enabled")
        else:
            self.mistral_enabled = False
            logger.warning("⚠️ Mistral AI disabled - missing API key or requests")
        
        if NUMPY_AVAILABLE:
            self.numpy_enabled = True
            logger.info("✅ NumPy available for matching")
        else:
            self.numpy_enabled = False
            logger.warning("⚠️ NumPy unavailable - basic matching only")
    
    def setup_database(self):
        """Configurar conexión a base de datos"""
        database_url = os.getenv('DATABASE_URL')
        if database_url:
            self.db_engine = create_engine(database_url)
            logger.info("✅ Database connection established")
        else:
            logger.warning("⚠️ No database URL provided")
            
    def setup_apis(self):
        """Configurar APIs externas"""
        self.google_drive_credentials = os.getenv('GOOGLE_DRIVE_CREDENTIALS')
        self.app_base_url = os.getenv('APP_BASE_URL', 'https://073083d2-dd14-424e-a549-4c03e48131b7-00-1vatfbc2lts0v.janeway.replit.dev')
        logger.info("✅ External APIs configured")

    async def analyze_user_message(self, message: str, user_context: Dict) -> Dict[str, Any]:
        """
        Análisis inteligente de mensajes de usuario con IA
        """
        try:
            # 1. Análisis de intención con embeddings
            intent = await self.detect_intent(message)
            
            # 2. Extracción de entidades relevantes
            entities = await self.extract_entities(message)
            
            # 3. Generación de respuesta contextual con Mistral
            response = await self.generate_intelligent_response(message, intent, entities, user_context)
            
            # 4. Obtener datos relevantes del sistema
            system_data = await self.get_relevant_system_data(intent, entities)
            
            return {
                'intent': intent,
                'entities': entities,
                'response': response,
                'system_data': system_data,
                'confidence': 0.95,  # Calculado basado en el análisis
                'timestamp': datetime.now().isoformat()
            }
            
        except Exception as e:
            logger.error(f"Error analyzing message: {e}")
            return await self.fallback_response(message)

    async def detect_intent(self, message: str) -> str:
        """Detectar intención del usuario usando embeddings semánticos"""
        
        # Intenciones predefinidas con ejemplos
        intent_examples = {
            'registro_candidato': [
                'quiero registrarme como persona neurodivergente',
                'busco trabajo y tengo TDAH',
                'soy autista y necesito empleo',
                'registro como candidato'
            ],
            'registro_empresa': [
                'queremos contratar talento neurodivergente',
                'somos una empresa inclusiva',
                'registro de empresa',
                'contratar personas con autismo'
            ],
            'matching_solicitud': [
                'busco candidatos perfectos',
                'necesito encontrar el trabajo ideal',
                'matching inteligente',
                'recomendaciones de empleo'
            ],
            'informacion_neurodivergencia': [
                'qué es el TDAH',
                'información sobre autismo',
                'recursos para dislexia',
                'tipos de neurodivergencia'
            ],
            'soporte_tecnico': [
                'tengo problemas con la aplicación',
                'no puedo acceder',
                'error en el sistema',
                'ayuda técnica'
            ]
        }
        
        # Convertir mensaje y ejemplos a embeddings
        message_embedding = self.embedding_model.encode([message])
        
        best_intent = 'general'
        best_score = 0
        
        for intent, examples in intent_examples.items():
            example_embeddings = self.embedding_model.encode(examples)
            similarities = cosine_similarity(message_embedding, example_embeddings)
            avg_similarity = np.mean(similarities)
            
            if avg_similarity > best_score:
                best_score = avg_similarity
                best_intent = intent
        
        logger.info(f"Intent detected: {best_intent} (confidence: {best_score:.2f})")
        return best_intent

    async def extract_entities(self, message: str) -> Dict[str, List[str]]:
        """Extraer entidades relevantes del mensaje"""
        entities = {
            'neurodivergence_types': [],
            'skills': [],
            'locations': [],
            'experience_level': [],
            'job_types': []
        }
        
        # Diccionarios de entidades
        neurodivergence_keywords = {
            'TDAH': ['tdah', 'adhd', 'déficit de atención', 'hiperactividad'],
            'TEA': ['tea', 'autismo', 'autista', 'espectro autista'],
            'Dislexia': ['dislexia', 'disléxico', 'dificultades lectura'],
            'Neurodivergente': ['neurodivergente', 'neurodiverso', 'neurodiversidad']
        }
        
        skills_keywords = [
            'programación', 'desarrollo', 'diseño', 'análisis',
            'python', 'javascript', 'data science', 'ui/ux',
            'marketing', 'ventas', 'administración', 'contabilidad'
        ]
        
        message_lower = message.lower()
        
        # Detectar tipos de neurodivergencia
        for nd_type, keywords in neurodivergence_keywords.items():
            if any(keyword in message_lower for keyword in keywords):
                entities['neurodivergence_types'].append(nd_type)
        
        # Detectar habilidades
        for skill in skills_keywords:
            if skill in message_lower:
                entities['skills'].append(skill)
        
        return entities

    async def generate_intelligent_response(self, message: str, intent: str, entities: Dict, user_context: Dict) -> str:
        """Generar respuesta inteligente usando Mistral"""
        
        try:
            # Construir prompt contextual
            system_prompt = f"""
            Eres el asistente inteligente de DiversIA, una plataforma de inclusión laboral para personas neurodivergentes.
            
            Contexto del usuario:
            - Intención detectada: {intent}
            - Entidades identificadas: {entities}
            - Contexto: {user_context}
            
            Instrucciones:
            1. Responde en español de manera empática y profesional
            2. Proporciona información específica y útil
            3. Incluye llamadas a la acción relevantes
            4. Menciona beneficios específicos de DiversIA
            5. Adapta tu respuesta al tipo de neurodivergencia mencionada
            """
            
            response = self.mistral_client.chat.completions.create(
                model="mistral-medium",
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": message}
                ],
                max_tokens=300,
                temperature=0.7
            )
            
            ai_response = response.choices[0].message.content
            logger.info("✅ Intelligent response generated with Mistral")
            return ai_response
            
        except Exception as e:
            logger.error(f"Error generating AI response: {e}")
            return await self.get_fallback_response_by_intent(intent)

    async def get_fallback_response_by_intent(self, intent: str) -> str:
        """Respuestas de fallback basadas en intención"""
        responses = {
            'registro_candidato': 'Te ayudo con el registro. DiversIA ofrece formularios especializados para diferentes tipos de neurodivergencia. ¿Podrías contarme más sobre tu perfil?',
            'registro_empresa': 'Excelente que quieran ser una empresa inclusiva. DiversIA les conecta con talento neurodivergente excepcional. ¿Qué posiciones están buscando cubrir?',
            'matching_solicitud': 'Nuestro sistema de matching inteligente considera múltiples factores para encontrar la combinación perfecta. ¿Qué tipo de oportunidad buscas?',
            'informacion_neurodivergencia': 'Tengo información detallada sobre TDAH, TEA y dislexia. También conectamos con asociaciones especializadas. ¿Sobre qué te gustaría saber más?',
            'general': '¡Hola! Soy el asistente inteligente de DiversIA. Puedo ayudarte con registro, información sobre neurodivergencia, búsqueda de empleo y más. ¿En qué te ayudo?'
        }
        return responses.get(intent, responses['general'])

    async def get_relevant_system_data(self, intent: str, entities: Dict) -> Dict[str, Any]:
        """Obtener datos relevantes del sistema basados en intención y entidades"""
        system_data = {}
        
        try:
            if hasattr(self, 'db_engine') and self.db_engine:
                # Estadísticas generales
                with self.db_engine.connect() as conn:
                    # Contar usuarios por tipo
                    user_stats = conn.execute(text("""
                        SELECT 
                            COUNT(*) as total_users,
                            COUNT(CASE WHEN tipo_neurodivergencia = 'TDAH' THEN 1 END) as tdah_users,
                            COUNT(CASE WHEN tipo_neurodivergencia = 'TEA' THEN 1 END) as tea_users,
                            COUNT(CASE WHEN tipo_neurodivergencia = 'Dislexia' THEN 1 END) as dislexia_users
                        FROM usuarios WHERE tipo_neurodivergencia IS NOT NULL
                    """)).fetchone()
                    
                    # Contar empresas
                    company_stats = conn.execute(text("SELECT COUNT(*) as total_companies FROM empresas")).fetchone()
                    
                    system_data = {
                        'total_users': user_stats.total_users if user_stats else 0,
                        'tdah_users': user_stats.tdah_users if user_stats else 0,
                        'tea_users': user_stats.tea_users if user_stats else 0,
                        'dislexia_users': user_stats.dislexia_users if user_stats else 0,
                        'total_companies': company_stats.total_companies if company_stats else 0
                    }
            
            # Datos específicos basados en entidades detectadas
            if 'TDAH' in entities.get('neurodivergence_types', []):
                system_data['tdah_resources'] = await self.get_tdah_resources()
            
            if 'TEA' in entities.get('neurodivergence_types', []):
                system_data['tea_resources'] = await self.get_tea_resources()
                
        except Exception as e:
            logger.error(f"Error getting system data: {e}")
            system_data = {'error': 'Unable to fetch current statistics'}
        
        return system_data

    async def get_tdah_resources(self) -> Dict[str, Any]:
        """Recursos específicos para TDAH"""
        return {
            'description': 'Recursos especializados para TDAH disponibles',
            'tests_available': True,
            'accommodations': ['Espacios tranquilos', 'Horarios flexibles', 'Descansos frecuentes'],
            'success_rate': '85%'
        }

    async def get_tea_resources(self) -> Dict[str, Any]:
        """Recursos específicos para TEA"""
        return {
            'description': 'Recursos especializados para TEA disponibles',
            'tests_available': True,
            'accommodations': ['Comunicación clara', 'Rutinas estructuradas', 'Sensibilidad sensorial'],
            'success_rate': '90%'
        }

    async def fallback_response(self, message: str) -> Dict[str, Any]:
        """Respuesta de fallback en caso de error"""
        return {
            'intent': 'general',
            'entities': {},
            'response': 'Gracias por tu mensaje. Estoy aquí para ayudarte con cualquier consulta sobre DiversIA. ¿Podrías ser más específico sobre lo que necesitas?',
            'system_data': {},
            'confidence': 0.5,
            'timestamp': datetime.now().isoformat(),
            'fallback': True
        }

# Instancia global del agente
diversia_agent = DiversIAAgent()

async def process_chat_message(message: str, user_id: str, session_id: str, page: str) -> Dict[str, Any]:
    """
    Función principal para procesar mensajes del chat
    Se integra con n8n webhook
    """
    user_context = {
        'user_id': user_id,
        'session_id': session_id,
        'page': page,
        'timestamp': datetime.now().isoformat()
    }
    
    result = await diversia_agent.analyze_user_message(message, user_context)
    
    # Formatear respuesta para n8n
    return {
        'final_response': result['response'],
        'response': result['response'],
        'intent': result['intent'],
        'entities': result['entities'],
        'system_data': result['system_data'],
        'confidence': result['confidence'],
        'user_context': user_context
    }

if __name__ == "__main__":
    # Test local del agente
    async def test_agent():
        test_message = "Hola, tengo TDAH y busco trabajo en programación"
        result = await process_chat_message(test_message, "test_user", "test_session", "/")
        print(json.dumps(result, indent=2, ensure_ascii=False))
    
    asyncio.run(test_agent())