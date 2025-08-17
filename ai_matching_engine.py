"""
DiversIA Matching Engine
Sistema de IA para matching perfecto entre candidatos y empresas
"""

import numpy as np
import pandas as pd
from typing import Dict, List, Tuple, Optional
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import StandardScaler
from sklearn.metrics.pairwise import cosine_similarity
from sentence_transformers import SentenceTransformer
import joblib
import logging

logger = logging.getLogger(__name__)

class NeuroMatchingEngine:
    """
    Motor de matching inteligente que considera factores específicos
    de neurodivergencia para optimizar la compatibilidad
    """
    
    def __init__(self):
        self.embedding_model = SentenceTransformer('paraphrase-multilingual-MiniLM-L12-v2')
        self.scaler = StandardScaler()
        self.matching_model = None
        self.setup_model()
        
    def setup_model(self):
        """Configurar el modelo de matching"""
        # Por ahora usamos RandomForest, luego entrenaremos con datos reales
        self.matching_model = RandomForestClassifier(
            n_estimators=100,
            max_depth=10,
            random_state=42
        )
        logger.info("✅ Matching model initialized")
    
    def encode_candidate_profile(self, candidate: Dict) -> np.ndarray:
        """
        Codificar perfil de candidato en vector numérico
        """
        features = []
        
        # 1. Tipo de neurodivergencia (one-hot encoding)
        neurodivergence_types = ['TDAH', 'TEA', 'Dislexia', 'Otro']
        nd_type = candidate.get('tipo_neurodivergencia', 'Otro')
        nd_vector = [1 if nd_type == nt else 0 for nt in neurodivergence_types]
        features.extend(nd_vector)
        
        # 2. Habilidades técnicas (embeddings semánticos)
        skills = candidate.get('habilidades', '')
        if skills:
            skill_embedding = self.embedding_model.encode([skills])[0]
            features.extend(skill_embedding[:50])  # Primeras 50 dimensiones
        else:
            features.extend([0.0] * 50)
        
        # 3. Experiencia laboral (numérico)
        experience = candidate.get('experiencia_anos', 0)
        features.append(float(experience))
        
        # 4. Nivel educativo (ordinal)
        education_levels = {
            'Secundaria': 1,
            'Técnico': 2,
            'Universitario': 3,
            'Postgrado': 4,
            'Doctorado': 5
        }
        education = candidate.get('nivel_educativo', 'Técnico')
        features.append(float(education_levels.get(education, 2)))
        
        # 5. Preferencias de trabajo
        work_prefs = candidate.get('preferencias_trabajo', {})
        features.append(float(work_prefs.get('trabajo_remoto', 0)))
        features.append(float(work_prefs.get('horario_flexible', 0)))
        features.append(float(work_prefs.get('ambiente_tranquilo', 0)))
        
        # 6. Necesidades de adaptación
        adaptations = candidate.get('adaptaciones_necesarias', [])
        adaptation_score = len(adaptations) / 10.0  # Normalizado
        features.append(adaptation_score)
        
        return np.array(features)
    
    def encode_company_profile(self, company: Dict, job_offer: Dict) -> np.ndarray:
        """
        Codificar perfil de empresa y oferta laboral
        """
        features = []
        
        # 1. Puntuación de inclusión de la empresa
        inclusion_score = company.get('puntuacion_inclusion', 5.0) / 10.0  # Normalizado
        features.append(inclusion_score)
        
        # 2. Tipo de empresa
        company_types = ['Startup', 'Corporativa', 'ONG', 'Pública', 'Otro']
        comp_type = company.get('tipo_empresa', 'Otro')
        type_vector = [1 if comp_type == ct else 0 for ct in company_types]
        features.extend(type_vector)
        
        # 3. Descripción del trabajo (embeddings)
        job_description = job_offer.get('descripcion', '')
        if job_description:
            job_embedding = self.embedding_model.encode([job_description])[0]
            features.extend(job_embedding[:50])  # Primeras 50 dimensiones
        else:
            features.extend([0.0] * 50)
        
        # 4. Modalidad de trabajo
        work_modes = job_offer.get('modalidad_trabajo', {})
        features.append(float(work_modes.get('remoto', 0)))
        features.append(float(work_modes.get('hibrido', 0)))
        features.append(float(work_modes.get('presencial', 0)))
        
        # 5. Adaptaciones disponibles
        available_adaptations = company.get('adaptaciones_disponibles', [])
        adaptation_score = len(available_adaptations) / 15.0  # Normalizado
        features.append(adaptation_score)
        
        # 6. Cultura empresarial
        culture = company.get('cultura_empresarial', {})
        features.append(float(culture.get('innovacion', 5)) / 10.0)
        features.append(float(culture.get('colaboracion', 5)) / 10.0)
        features.append(float(culture.get('inclusion', 5)) / 10.0)
        
        # 7. Beneficios específicos para neurodivergentes
        neuro_benefits = company.get('beneficios_neurodivergentes', [])
        benefits_score = len(neuro_benefits) / 10.0  # Normalizado
        features.append(benefits_score)
        
        return np.array(features)
    
    def calculate_compatibility_score(self, candidate: Dict, company: Dict, job_offer: Dict) -> float:
        """
        Calcular puntuación de compatibilidad entre candidato y empresa
        """
        try:
            # Codificar perfiles
            candidate_vector = self.encode_candidate_profile(candidate)
            company_vector = self.encode_company_profile(company, job_offer)
            
            # Asegurar misma dimensionalidad
            min_len = min(len(candidate_vector), len(company_vector))
            candidate_vector = candidate_vector[:min_len]
            company_vector = company_vector[:min_len]
            
            # Similitud coseno base
            base_similarity = cosine_similarity([candidate_vector], [company_vector])[0][0]
            
            # Factores específicos de neurodivergencia
            neurodivergence_bonus = self.calculate_neurodivergence_bonus(candidate, company, job_offer)
            
            # Compatibilidad de adaptaciones
            adaptation_bonus = self.calculate_adaptation_compatibility(candidate, company)
            
            # Puntuación final (0-100)
            final_score = (base_similarity * 60) + (neurodivergence_bonus * 25) + (adaptation_bonus * 15)
            
            return min(100, max(0, final_score))
            
        except Exception as e:
            logger.error(f"Error calculating compatibility: {e}")
            return 50.0  # Puntuación neutral en caso de error
    
    def calculate_neurodivergence_bonus(self, candidate: Dict, company: Dict, job_offer: Dict) -> float:
        """
        Calcular bonus específico por tipo de neurodivergencia
        """
        nd_type = candidate.get('tipo_neurodivergencia', '')
        company_experience = company.get('experiencia_neurodivergencia', {})
        
        # Bonus si la empresa tiene experiencia con ese tipo específico
        if nd_type in company_experience:
            experience_level = company_experience[nd_type]
            return experience_level / 10.0 * 100  # Normalizado a 0-100
        
        # Bonus general por inclusión
        general_inclusion = company.get('puntuacion_inclusion', 5)
        return general_inclusion / 10.0 * 60  # Hasta 60 puntos
    
    def calculate_adaptation_compatibility(self, candidate: Dict, company: Dict) -> float:
        """
        Calcular compatibilidad de adaptaciones necesarias vs disponibles
        """
        needed = set(candidate.get('adaptaciones_necesarias', []))
        available = set(company.get('adaptaciones_disponibles', []))
        
        if not needed:
            return 100.0  # No necesita adaptaciones específicas
        
        # Porcentaje de adaptaciones cubiertas
        covered = needed.intersection(available)
        coverage_ratio = len(covered) / len(needed)
        
        return coverage_ratio * 100
    
    def find_best_matches(self, candidate: Dict, companies_jobs: List[Tuple[Dict, Dict]], top_k: int = 5) -> List[Dict]:
        """
        Encontrar las mejores coincidencias para un candidato
        """
        matches = []
        
        for company, job_offer in companies_jobs:
            score = self.calculate_compatibility_score(candidate, company, job_offer)
            
            match = {
                'company': company,
                'job_offer': job_offer,
                'compatibility_score': score,
                'match_reasons': self.generate_match_reasons(candidate, company, job_offer, score)
            }
            matches.append(match)
        
        # Ordenar por puntuación y devolver top K
        matches.sort(key=lambda x: x['compatibility_score'], reverse=True)
        return matches[:top_k]
    
    def generate_match_reasons(self, candidate: Dict, company: Dict, job_offer: Dict, score: float) -> List[str]:
        """
        Generar razones específicas del matching
        """
        reasons = []
        
        if score >= 90:
            reasons.append("🎯 Coincidencia excepcional")
        elif score >= 80:
            reasons.append("✅ Muy buena compatibilidad")
        elif score >= 70:
            reasons.append("👍 Buena compatibilidad")
        
        # Razones específicas
        nd_type = candidate.get('tipo_neurodivergencia', '')
        company_exp = company.get('experiencia_neurodivergencia', {})
        
        if nd_type in company_exp:
            reasons.append(f"🧠 Empresa con experiencia en {nd_type}")
        
        # Adaptaciones
        needed = set(candidate.get('adaptaciones_necesarias', []))
        available = set(company.get('adaptaciones_disponibles', []))
        covered = needed.intersection(available)
        
        if len(covered) == len(needed) and needed:
            reasons.append("🔧 Todas las adaptaciones disponibles")
        elif covered:
            reasons.append(f"🔧 {len(covered)}/{len(needed)} adaptaciones cubiertas")
        
        # Modalidad de trabajo
        remote_pref = candidate.get('preferencias_trabajo', {}).get('trabajo_remoto', False)
        remote_available = job_offer.get('modalidad_trabajo', {}).get('remoto', False)
        
        if remote_pref and remote_available:
            reasons.append("🏠 Trabajo remoto disponible")
        
        return reasons
    
    def train_with_feedback(self, training_data: List[Dict]):
        """
        Entrenar el modelo con feedback de matching exitosos
        """
        if not training_data:
            logger.warning("No training data provided")
            return
        
        X = []
        y = []
        
        for record in training_data:
            candidate_vector = self.encode_candidate_profile(record['candidate'])
            company_vector = self.encode_company_profile(record['company'], record['job_offer'])
            
            # Combinar vectores
            combined_vector = np.concatenate([candidate_vector, company_vector])
            X.append(combined_vector)
            
            # Target: 1 si fue exitoso, 0 si no
            y.append(1 if record['successful'] else 0)
        
        # Entrenar modelo
        X = self.scaler.fit_transform(X)
        self.matching_model.fit(X, y)
        
        # Guardar modelo entrenado
        joblib.dump(self.matching_model, 'matching_model.pkl')
        joblib.dump(self.scaler, 'scaler.pkl')
        
        logger.info(f"✅ Model trained with {len(training_data)} samples")

# Instancia global del motor de matching
matching_engine = NeuroMatchingEngine()

def get_candidate_recommendations(candidate_id: str, max_results: int = 5) -> List[Dict]:
    """
    Obtener recomendaciones para un candidato específico
    """
    # Esta función se integrará con la base de datos real
    # Por ahora, devolvemos estructura de ejemplo
    
    example_matches = [
        {
            'company_name': 'TechInclusiva S.L.',
            'job_title': 'Desarrollador Python Junior',
            'compatibility_score': 92.5,
            'match_reasons': [
                '🎯 Coincidencia excepcional',
                '🧠 Empresa con experiencia en TDAH', 
                '🔧 Todas las adaptaciones disponibles',
                '🏠 Trabajo remoto disponible'
            ],
            'next_steps': 'Enviar candidatura personalizada'
        }
    ]
    
    return example_matches

if __name__ == "__main__":
    # Test del motor de matching
    candidate_test = {
        'tipo_neurodivergencia': 'TDAH',
        'habilidades': 'Python, Machine Learning, análisis de datos',
        'experiencia_anos': 2,
        'nivel_educativo': 'Universitario',
        'preferencias_trabajo': {
            'trabajo_remoto': True,
            'horario_flexible': True,
            'ambiente_tranquilo': True
        },
        'adaptaciones_necesarias': ['ambiente_tranquilo', 'descansos_frecuentes']
    }
    
    company_test = {
        'puntuacion_inclusion': 9,
        'tipo_empresa': 'Startup',
        'experiencia_neurodivergencia': {'TDAH': 8, 'TEA': 6},
        'adaptaciones_disponibles': ['ambiente_tranquilo', 'descansos_frecuentes', 'horario_flexible'],
        'cultura_empresarial': {
            'innovacion': 9,
            'colaboracion': 8,
            'inclusion': 10
        },
        'beneficios_neurodivergentes': ['coaching', 'mentoría', 'seguimiento']
    }
    
    job_test = {
        'descripcion': 'Desarrollador Python para proyectos de IA y machine learning',
        'modalidad_trabajo': {
            'remoto': True,
            'hibrido': True,
            'presencial': False
        }
    }
    
    score = matching_engine.calculate_compatibility_score(candidate_test, company_test, job_test)
    print(f"Compatibility Score: {score:.2f}")
    
    matches = matching_engine.find_best_matches(candidate_test, [(company_test, job_test)])
    print(f"Match reasons: {matches[0]['match_reasons']}")