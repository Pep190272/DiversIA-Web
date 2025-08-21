"""
Motor de Emparejamiento Inteligente Simplificado para DiversIA
Conecta personas neurodivergentes con ofertas de trabajo compatibles
"""

import os
import json
import logging
from datetime import datetime
from typing import Dict, List, Optional, Tuple

# Configurar logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class DiversIAMatcher:
    """Motor de emparejamiento que conecta candidatos con ofertas laborales"""
    
    def __init__(self):
        self.compatibility_weights = {
            'neurodivergence_match': 0.3,  # Coincidencia de tipo de neurodivergencia
            'skills_match': 0.25,          # Coincidencia de habilidades
            'location_match': 0.15,        # Proximidad geográfica
            'adaptations_match': 0.2,      # Adaptaciones disponibles vs necesarias
            'experience_match': 0.1        # Nivel de experiencia
        }
        
        # Mapeo de neurodivergencias compatibles
        self.neurodivergence_compatibility = {
            'tdah': ['tdah', 'todas', 'general'],
            'tea': ['tea', 'tdah', 'todas', 'general'],  # TEA y TDAH pueden ser compatibles
            'dislexia': ['dislexia', 'todas', 'general'],
            'discalculia': ['discalculia', 'dislexia', 'todas', 'general'],
            'tourette': ['tourette', 'todas', 'general'],
            'dispraxia': ['dispraxia', 'todas', 'general'],
            'ansiedad': ['ansiedad', 'todas', 'general'],
            'bipolar': ['bipolar', 'todas', 'general'],
            'altas_capacidades': ['altas_capacidades', 'todas', 'general']
        }
    
    def calculate_neurodivergence_score(self, user_type: str, job_targets: List[str]) -> float:
        """Calcular puntuación de compatibilidad neurodivergente"""
        if not user_type or not job_targets:
            return 0.5
        
        user_type = user_type.lower()
        job_targets = [target.lower() for target in job_targets]
        
        # Verificar compatibilidades
        compatible_types = self.neurodivergence_compatibility.get(user_type, [user_type])
        
        for job_target in job_targets:
            if job_target in compatible_types:
                return 1.0
            elif job_target == 'todas':
                return 0.9
        
        return 0.3  # Puntuación baja pero no cero
    
    def calculate_skills_score(self, user_skills: str, job_requirements: str) -> float:
        """Calcular compatibilidad de habilidades"""
        if not user_skills or not job_requirements:
            return 0.5
        
        user_skills_lower = user_skills.lower()
        job_requirements_lower = job_requirements.lower()
        
        # Palabras clave técnicas comunes
        tech_keywords = [
            'python', 'javascript', 'java', 'react', 'sql', 'html', 'css',
            'programación', 'desarrollo', 'diseño', 'análisis', 'gestión',
            'comunicación', 'liderazgo', 'organización', 'creatividad'
        ]
        
        user_tech_skills = [skill for skill in tech_keywords if skill in user_skills_lower]
        job_tech_requirements = [skill for skill in tech_keywords if skill in job_requirements_lower]
        
        if not job_tech_requirements:
            return 0.7  # Si no hay requisitos específicos, puntuación neutral-alta
        
        matches = len(set(user_tech_skills) & set(job_tech_requirements))
        total_required = len(job_tech_requirements)
        
        return min(1.0, matches / total_required + 0.3)  # Base de 0.3 + coincidencias
    
    def calculate_location_score(self, user_city: str, job_location: str, job_modality: str = '') -> float:
        """Calcular compatibilidad de ubicación"""
        if not user_city or not job_location:
            return 0.6
        
        # Si es remoto, ubicación no importa
        if 'remoto' in job_modality.lower():
            return 1.0
        
        if 'híbrido' in job_modality.lower():
            return 0.8 if user_city.lower() == job_location.lower() else 0.4
        
        # Trabajo presencial
        return 1.0 if user_city.lower() == job_location.lower() else 0.2
    
    def calculate_adaptations_score(self, user_needs: str, job_adaptations: List[str]) -> float:
        """Calcular compatibilidad de adaptaciones"""
        if not user_needs:
            return 0.8  # Si no necesita adaptaciones específicas
        
        if not job_adaptations:
            return 0.4  # Si necesita adaptaciones pero el trabajo no las ofrece
        
        user_needs_lower = user_needs.lower()
        job_adaptations_lower = [adapt.lower() for adapt in job_adaptations]
        
        # Adaptaciones comunes
        adaptation_keywords = {
            'horario': 'horario_flexible',
            'remoto': 'trabajo_remoto',
            'tranquilo': 'ambiente_tranquilo',
            'tecnología': 'tecnologia_asistiva',
            'formación': 'formacion_equipo',
            'mentor': 'mentor',
            'pausas': 'pausas_extra',
            'escrito': 'instrucciones_escritas'
        }
        
        needed_adaptations = []
        for keyword, adaptation in adaptation_keywords.items():
            if keyword in user_needs_lower:
                needed_adaptations.append(adaptation)
        
        if not needed_adaptations:
            return 0.7  # Texto libre sin palabras clave específicas
        
        available_adaptations = set(job_adaptations_lower)
        provided = sum(1 for adapt in needed_adaptations if adapt in available_adaptations)
        
        return min(1.0, provided / len(needed_adaptations) + 0.4)
    
    def calculate_experience_score(self, user_experience: str, job_level: str = '') -> float:
        """Calcular compatibilidad de experiencia"""
        if not user_experience:
            return 0.6
        
        user_exp_lower = user_experience.lower()
        job_level_lower = job_level.lower() if job_level else ''
        
        # Detectar nivel de experiencia del usuario
        if any(word in user_exp_lower for word in ['sin experiencia', 'principiante', 'recién']):
            user_level = 'junior'
        elif any(word in user_exp_lower for word in ['senior', 'experto', 'años']):
            user_level = 'senior'
        else:
            user_level = 'mid'
        
        # Detectar nivel requerido del trabajo
        if any(word in job_level_lower for word in ['junior', 'principiante', 'sin experiencia']):
            job_req_level = 'junior'
        elif any(word in job_level_lower for word in ['senior', 'experto']):
            job_req_level = 'senior'
        else:
            job_req_level = 'mid'
        
        # Matriz de compatibilidad
        compatibility_matrix = {
            ('junior', 'junior'): 1.0,
            ('junior', 'mid'): 0.7,
            ('junior', 'senior'): 0.3,
            ('mid', 'junior'): 0.9,
            ('mid', 'mid'): 1.0,
            ('mid', 'senior'): 0.6,
            ('senior', 'junior'): 0.8,
            ('senior', 'mid'): 0.9,
            ('senior', 'senior'): 1.0
        }
        
        return compatibility_matrix.get((user_level, job_req_level), 0.7)
    
    def calculate_compatibility(self, user_profile: Dict, job_offer: Dict) -> Tuple[float, Dict]:
        """Calcular compatibilidad total entre usuario y oferta"""
        
        # Calcular puntuaciones individuales
        neuro_score = self.calculate_neurodivergence_score(
            user_profile.get('tipo_neurodivergencia', ''),
            job_offer.get('neurodivergencias_target', [])
        )
        
        skills_score = self.calculate_skills_score(
            user_profile.get('habilidades', ''),
            job_offer.get('requisitos', '')
        )
        
        location_score = self.calculate_location_score(
            user_profile.get('ciudad', ''),
            job_offer.get('ubicacion', ''),
            job_offer.get('modalidad_trabajo', '')
        )
        
        adaptations_score = self.calculate_adaptations_score(
            user_profile.get('adaptaciones_necesarias', ''),
            job_offer.get('adaptaciones_disponibles', [])
        )
        
        experience_score = self.calculate_experience_score(
            user_profile.get('experiencia_laboral', ''),
            job_offer.get('nivel_experiencia', '')
        )
        
        # Calcular puntuación ponderada total
        total_score = (
            neuro_score * self.compatibility_weights['neurodivergence_match'] +
            skills_score * self.compatibility_weights['skills_match'] +
            location_score * self.compatibility_weights['location_match'] +
            adaptations_score * self.compatibility_weights['adaptations_match'] +
            experience_score * self.compatibility_weights['experience_match']
        )
        
        # Detalles del cálculo
        score_breakdown = {
            'total_score': round(total_score, 3),
            'neurodivergence_match': round(neuro_score, 3),
            'skills_match': round(skills_score, 3),
            'location_match': round(location_score, 3),
            'adaptations_match': round(adaptations_score, 3),
            'experience_match': round(experience_score, 3),
            'recommendation': self.get_recommendation(total_score)
        }
        
        return total_score, score_breakdown
    
    def get_recommendation(self, score: float) -> str:
        """Obtener recomendación basada en la puntuación"""
        if score >= 0.8:
            return "Excelente compatibilidad - ¡Muy recomendado!"
        elif score >= 0.6:
            return "Buena compatibilidad - Vale la pena considerar"
        elif score >= 0.4:
            return "Compatibilidad moderada - Revisar detalles"
        else:
            return "Baja compatibilidad - Buscar otras opciones"
    
    def find_matches(self, user_profile: Dict, job_offers: List[Dict], top_n: int = 5) -> List[Dict]:
        """Encontrar las mejores coincidencias para un usuario"""
        matches = []
        
        for job in job_offers:
            score, breakdown = self.calculate_compatibility(user_profile, job)
            
            match_result = {
                'job_id': job.get('id', 'unknown'),
                'job_title': job.get('titulo', 'Sin título'),
                'company': job.get('empresa', 'Empresa no especificada'),
                'score': score,
                'breakdown': breakdown,
                'job_data': job
            }
            
            matches.append(match_result)
        
        # Ordenar por puntuación descendente y tomar los top N
        matches.sort(key=lambda x: x['score'], reverse=True)
        return matches[:top_n]

# Instancia global del motor de emparejamiento
diversia_matcher = DiversIAMatcher()

def find_job_matches(user_profile: Dict, job_offers: List[Dict], top_n: int = 5) -> List[Dict]:
    """Función principal para encontrar coincidencias de trabajo"""
    return diversia_matcher.find_matches(user_profile, job_offers, top_n)

def calculate_job_compatibility(user_profile: Dict, job_offer: Dict) -> Tuple[float, Dict]:
    """Función principal para calcular compatibilidad de un trabajo específico"""
    return diversia_matcher.calculate_compatibility(user_profile, job_offer)