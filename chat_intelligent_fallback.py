"""
Intelligent Fallback Chat System for DiversIA
Sistema de chat inteligente que funciona sin dependencias externas
"""

import json
import re
from datetime import datetime
from typing import Dict, Any

class DiversIAIntelligentFallback:
    """Chat inteligente con información específica de DiversIA"""
    
    def __init__(self):
        self.company_info = {
            'name': 'DiversIA',
            'ceo': 'Olga Cruz Hernández',
            'address': 'Avda Espoia, 762, 08789 Barcelona, Spain',
            'phone': '695 260 546',
            'email': 'diversiaeternals@gmail.com',
            'description': 'Plataforma de inclusión laboral especializada en conectar talento neurodivergente con empresas inclusivas'
        }
        
        self.services = {
            'tests_gamificados': 'Evaluaciones neurocognitivas diseñadas como juegos para identificar fortalezas únicas',
            'empleo_inclusivo': 'Conectamos perfiles con empresas que buscan específicamente talento neurodivergente',
            'comunidad': 'Red de apoyo para crecimiento profesional y experiencias compartidas',
            'matching': 'Sistema inteligente que conecta candidatos con oportunidades compatibles'
        }
        
        self.neurodivergence_info = {
            'TDAH': {
                'description': 'Trastorno por Déficit de Atención e Hiperactividad',
                'strengths': ['creatividad', 'innovación', 'energía', 'multitarea'],
                'adaptations': ['ambiente tranquilo', 'horarios flexibles', 'descansos frecuentes']
            },
            'TEA': {
                'description': 'Trastorno del Espectro Autista',
                'strengths': ['atención al detalle', 'pensamiento sistemático', 'honestidad', 'especialización'],
                'adaptations': ['comunicación clara', 'rutinas estructuradas', 'consideración sensorial']
            },
            'Dislexia': {
                'description': 'Dificultades específicas en el procesamiento del lenguaje escrito',
                'strengths': ['pensamiento visual', 'creatividad', 'resolución de problemas', 'pensamiento global'],
                'adaptations': ['formatos alternativos', 'tiempo adicional', 'tecnología asistiva']
            }
        }
    
    def process_message(self, message: str, user_context: Dict = None) -> Dict[str, Any]:
        """Procesar mensaje y generar respuesta inteligente"""
        if not user_context:
            user_context = {}
            
        # Normalizar mensaje
        message_lower = message.lower().strip()
        
        # Detectar intención y generar respuesta
        intent = self.detect_intent(message_lower)
        response = self.generate_response(message_lower, intent)
        
        return {
            'final_response': response,
            'response': response,
            'intent': intent,
            'confidence': 0.9,
            'powered_by': 'DiversIA Intelligent System',
            'timestamp': datetime.now().isoformat()
        }
    
    def detect_intent(self, message: str) -> str:
        """Detectar intención del mensaje"""
        # Patrones específicos para detectar intenciones
        patterns = {
            'company_info': [
                r'qu[eé] es diversia', r'sobre diversia', r'qu[eé] hace diversia',
                r'informaci[oó]n.*diversia', r'c[oó]mo funciona', r'explicame.*diversia'
            ],
            'ceo_info': [
                r'qui[eé]n.*ceo', r'director.*diversia', r'olga cruz', r'responsable',
                r'qui[eé]n dirige', r'equipo.*diversia'
            ],
            'contact_info': [
                r'contacto', r'tel[eé]fono', r'direcci[oó]n', r'email', r'ubicaci[oó]n',
                r'd[oó]nde est[aá]', r'c[oó]mo contactar'
            ],
            'tests_info': [
                r'tests?', r'evaluaci[oó]n', r'gamificado', r'juegos', r'assessment',
                r'c[oó]mo.*test', r'qu[eé].*evaluaci[oó]n'
            ],
            'registration': [
                r'registr', r'inscrib', r'apunt', r'unir', r'empezar',
                r'c[oó]mo.*registro', r'quiero.*registrar'
            ],
            'job_search': [
                r'trabajo', r'empleo', r'oportunidad', r'busco.*trabajo', r'encontrar.*empleo',
                r'ofertas?', r'vacantes?'
            ],
            'neurodivergence_tdah': [
                r'tdah', r'adhd', r'd[eé]ficit.*atenci[oó]n', r'hiperactividad'
            ],
            'neurodivergence_tea': [
                r'tea', r'autismo', r'autista', r'espectro.*autista', r'asperger'
            ],
            'neurodivergence_dislexia': [
                r'dislexia', r'disl[eé]xic', r'dificultad.*lectura', r'problema.*lectura'
            ],
            'company_registration': [
                r'empresa', r'contratar', r'corporativ', r'reclutamiento', r'talento',
                r'busco.*candidatos', r'queremos.*contratar'
            ]
        }
        
        # Buscar patrones
        for intent, pattern_list in patterns.items():
            for pattern in pattern_list:
                if re.search(pattern, message):
                    return intent
        
        return 'general'
    
    def generate_response(self, message: str, intent: str) -> str:
        """Generar respuesta basada en la intención"""
        
        if intent == 'company_info':
            return f"""**DiversIA** es una plataforma de inclusión laboral especializada en conectar talento neurodivergente con empresas inclusivas.

🎯 **Cómo funciona:**
• **Tests gamificados:** Evaluaciones neurocognitivas diseñadas como juegos para identificar fortalezas únicas
• **Empleo inclusivo:** Conectamos perfiles con empresas que buscan específicamente talento neurodivergente
• **Comunidad:** Red de apoyo para crecimiento profesional y experiencias compartidas

Nuestra misión es crear un mundo laboral donde las diferencias cognitivas sean valoradas como fortalezas.

¿Te gustaría saber más sobre algún aspecto específico?"""

        elif intent == 'ceo_info':
            return f"""El **CEO de DiversIA** es **{self.company_info['ceo']}**.

📍 **Contacto directo:**
• Email: {self.company_info['email']}
• Teléfono: {self.company_info['phone']}
• Ubicación: {self.company_info['address']}

Nuestro equipo está comprometido con crear oportunidades laborales inclusivas para personas neurodivergentes.

¿Necesitas contactar directamente con el equipo?"""

        elif intent == 'contact_info':
            return f"""📞 **Información de contacto DiversIA:**

• **Email:** {self.company_info['email']}
• **Teléfono:** {self.company_info['phone']}
• **Dirección:** {self.company_info['address']}

• **CEO:** {self.company_info['ceo']}

Estamos disponibles para cualquier consulta sobre inclusión laboral y neurodivergencia.

¿En qué podemos ayudarte específicamente?"""

        elif intent == 'tests_info':
            return """🎮 **Tests Gamificados de DiversIA:**

Nuestras evaluaciones neurocognitivas están diseñadas como juegos interactivos que:

✨ **Características:**
• Son divertidos y atractivos, no intimidantes
• Identifican fortalezas únicas de cada persona
• Adaptan a diferentes tipos de neurodivergencia
• Proporcionan insights valiosos para empleadores

🎯 **Objetivo:** Revelar tu verdadero potencial profesional de manera natural y sin estrés.

¿Te gustaría comenzar tu evaluación personalizada?"""

        elif intent == 'registration':
            return """📝 **Registro en DiversIA:**

Tenemos formularios especializados según tu perfil:

👤 **Para candidatos neurodivergentes:**
• Formulario adaptado según tu tipo de neurodivergencia (TDAH, TEA, Dislexia)
• Tests gamificados personalizados
• Perfil completo de fortalezas y preferencias

🏢 **Para empresas inclusivas:**
• Registro como empleador comprometido con la diversidad
• Acceso a nuestro pool de talento neurodivergente
• Orientación sobre mejores prácticas inclusivas

¿Eres candidato o empresa?"""

        elif intent == 'job_search':
            return """💼 **Búsqueda de Empleo en DiversIA:**

Nuestro sistema de **matching inteligente** conecta candidatos neurodivergentes con oportunidades perfectas:

🎯 **Proceso:**
1. **Evaluación personalizada** - Tests gamificados adaptativos
2. **Perfil de fortalezas** - Identificamos tus superpoderes únicos
3. **Matching inteligente** - Conectamos con empresas compatibles
4. **Apoyo continuo** - Acompañamiento durante todo el proceso

🌟 **Ventajas:** Las empresas en nuestra red buscan específicamente talento neurodivergente.

¿Cuál es tu área de experiencia?"""

        elif intent.startswith('neurodivergence_'):
            nd_type = intent.split('_')[1].upper()
            if nd_type in self.neurodivergence_info:
                info = self.neurodivergence_info[nd_type]
                return f"""🧠 **Información sobre {nd_type}:**

**Definición:** {info['description']}

💪 **Fortalezas típicas:**
{self._format_list(info['strengths'])}

🔧 **Adaptaciones que ofrecemos:**
{self._format_list(info['adaptations'])}

En DiversIA, estas características son vistas como **superpoderes profesionales**. Conectamos con empresas que comprenden y valoran específicamente el talento con {nd_type}.

¿Te gustaría conocer más sobre oportunidades específicas para {nd_type}?"""

        elif intent == 'company_registration':
            return """🏢 **Registro de Empresas en DiversIA:**

Ayudamos a empresas a encontrar y retener talento neurodivergente excepcional.

📋 **Nuestro proceso incluye:**
• **Matching inteligente** - Candidatos pre-evaluados y compatibles
• **Orientación inclusiva** - Mejores prácticas para integración
• **Seguimiento continuo** - Apoyo post-contratación
• **Acceso exclusivo** - Pool de talento especializado

🎯 **Beneficios:**
• Mayor innovación y creatividad en equipos
• Perspectivas únicas para resolución de problemas
• Compromiso y lealtad excepcionales
• Cumplimiento de objetivos de diversidad

¿Qué tipo de posiciones están buscando cubrir?"""

        else:  # general
            return """¡Hola! Soy el asistente inteligente de **DiversIA**, tu plataforma de inclusión laboral para talento neurodivergente.

🌟 **Puedo ayudarte con:**
• Información sobre DiversIA y nuestro equipo
• Tests gamificados y evaluaciones neurocognitivas
• Registro como candidato neurodivergente o empresa inclusiva
• Información sobre TDAH, TEA y Dislexia
• Proceso de matching y búsqueda de empleo
• Contacto y ubicación

💡 **CEO:** Olga Cruz Hernández | 📞 695 260 546 | 📧 diversiaeternals@gmail.com

¿Qué te gustaría saber específicamente?"""

    def _format_list(self, items: list) -> str:
        """Formatear lista como bullets"""
        return '\n'.join([f"• {item.capitalize()}" for item in items])

# Instancia global
intelligent_fallback = DiversIAIntelligentFallback()

def get_intelligent_response(message: str, user_context: Dict = None) -> Dict[str, Any]:
    """Función principal para obtener respuesta inteligente"""
    return intelligent_fallback.process_message(message, user_context)

if __name__ == "__main__":
    # Tests
    test_messages = [
        "Hola me puedes hablar de Diversia?",
        "Quien es el CEO de Diversia?",
        "Que es Diversia?",
        "Tengo TDAH y busco trabajo"
    ]
    
    for msg in test_messages:
        print(f"\n> {msg}")
        response = get_intelligent_response(msg)
        print(f"< {response['final_response'][:200]}...")