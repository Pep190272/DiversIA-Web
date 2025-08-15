from flask import Blueprint, request, jsonify
from app import db
from models import User, Company, JobOffer
from datetime import datetime
import json

# API Blueprint for n8n integration
api = Blueprint('api', __name__, url_prefix='/api/v1')

@api.route('/users', methods=['GET'])
def get_users():
    """Get all neurodivergent users for the agent"""
    try:
        users = User.query.all()
        users_data = []
        for user in users:
            users_data.append({
                'id': user.id,
                'nombre': user.nombre,
                'email': user.email,
                'telefono': user.telefono,
                'neurodivergencia': user.tipo_neurodivergencia,
                'ciudad': user.ciudad,
                'experiencia': user.experiencia_laboral,
                'fecha_registro': user.created_at.isoformat() if user.created_at else None,
                'disponible': True  # Default availability
            })
        return jsonify({
            'success': True,
            'data': users_data,
            'count': len(users_data)
        })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@api.route('/companies', methods=['GET'])
def get_companies():
    """Get all companies for the agent"""
    try:
        companies = Company.query.all()
        companies_data = []
        for company in companies:
            companies_data.append({
                'id': company.id,
                'nombre': company.nombre,
                'email': company.email,
                'telefono': company.telefono,
                'sector': company.sector,
                'ciudad': company.ciudad,
                'descripcion': company.descripcion,
                'fecha_registro': company.fecha_registro.isoformat() if company.fecha_registro else None
            })
        return jsonify({
            'success': True,
            'data': companies_data,
            'count': len(companies_data)
        })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@api.route('/job-offers', methods=['GET'])
def get_job_offers():
    """Get all job offers for matching"""
    try:
        offers = JobOffer.query.all()
        offers_data = []
        for offer in offers:
            offers_data.append({
                'id': offer.id,
                'company_id': offer.company_id,
                'titulo': offer.titulo,
                'descripcion': offer.descripcion,
                'ubicacion': offer.ubicacion,
                'salario': offer.salario,
                'neurodivergencias_aceptadas': offer.neurodivergencias_aceptadas.split(',') if offer.neurodivergencias_aceptadas else [],
                'fecha_creacion': offer.fecha_creacion.isoformat() if offer.fecha_creacion else None
            })
        return jsonify({
            'success': True,
            'data': offers_data,
            'count': len(offers_data)
        })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@api.route('/match-candidates', methods=['POST'])
def match_candidates():
    """Match candidates with job offers based on neurodivergence and location"""
    try:
        data = request.get_json()
        job_offer_id = data.get('job_offer_id')
        
        if not job_offer_id:
            return jsonify({'success': False, 'error': 'job_offer_id required'}), 400
        
        offer = JobOffer.query.get(job_offer_id)
        if not offer:
            return jsonify({'success': False, 'error': 'Job offer not found'}), 404
        
        # Find matching candidates
        accepted_neurodivergences = offer.neurodivergencias_aceptadas.split(',') if offer.neurodivergencias_aceptadas else []
        
        matching_users = User.query.filter(
            User.tipo_neurodivergencia.in_(accepted_neurodivergences)
        ).all()
        
        matches = []
        for user in matching_users:
            matches.append({
                'user_id': user.id,
                'nombre': user.nombre,
                'email': user.email,
                'neurodivergencia': user.tipo_neurodivergencia,
                'experiencia': user.experiencia_laboral,
                'ciudad': user.ciudad,
                'match_score': calculate_match_score(user, offer)
            })
        
        # Sort by match score
        matches.sort(key=lambda x: x['match_score'], reverse=True)
        
        return jsonify({
            'success': True,
            'job_offer': {
                'id': offer.id,
                'titulo': offer.titulo,
                'ubicacion': offer.ubicacion
            },
            'matches': matches,
            'count': len(matches)
        })
    
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@api.route('/user-insights', methods=['GET'])
def get_user_insights():
    """Get insights about users for the sales funnel"""
    try:
        # Basic statistics
        total_users = User.query.count()
        available_users = total_users  # All users considered available by default
        
        # Neurodivergence distribution
        neurodivergences = db.session.query(User.tipo_neurodivergencia, db.func.count(User.id)).group_by(User.tipo_neurodivergencia).all()
        neurodivergence_stats = [{'type': nd[0], 'count': nd[1]} for nd in neurodivergences]
        
        # City distribution
        cities = db.session.query(User.ciudad, db.func.count(User.id)).group_by(User.ciudad).all()
        city_stats = [{'city': city[0], 'count': city[1]} for city in cities]
        
        # Recent registrations (last 30 days)
        from datetime import timedelta
        recent_date = datetime.now() - timedelta(days=30)
        recent_users = User.query.filter(User.created_at >= recent_date).count()
        
        return jsonify({
            'success': True,
            'insights': {
                'total_users': total_users,
                'available_users': available_users,
                'recent_registrations': recent_users,
                'neurodivergence_distribution': neurodivergence_stats,
                'city_distribution': city_stats
            }
        })
    
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@api.route('/company-insights', methods=['GET'])
def get_company_insights():
    """Get insights about companies for the sales funnel"""
    try:
        total_companies = Company.query.count()
        
        # Sector distribution
        sectors = db.session.query(Company.sector, db.func.count(Company.id)).group_by(Company.sector).all()
        sector_stats = [{'sector': sector[0], 'count': sector[1]} for sector in sectors]
        
        # City distribution
        cities = db.session.query(Company.ciudad, db.func.count(Company.id)).group_by(Company.ciudad).all()
        city_stats = [{'city': city[0], 'count': city[1]} for city in cities]
        
        return jsonify({
            'success': True,
            'insights': {
                'total_companies': total_companies,
                'sector_distribution': sector_stats,
                'city_distribution': city_stats
            }
        })
    
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@api.route('/lead-scoring', methods=['POST'])
def score_lead():
    """Score a potential lead (user or company) for sales prioritization"""
    try:
        data = request.get_json()
        lead_type = data.get('type')  # 'user' or 'company'
        lead_id = data.get('id')
        
        if not lead_type or not lead_id:
            return jsonify({'success': False, 'error': 'type and id required'}), 400
        
        score = 0
        factors = []
        
        if lead_type == 'user':
            user = User.query.get(lead_id)
            if not user:
                return jsonify({'success': False, 'error': 'User not found'}), 404
            
            # Scoring factors for users
            score += 30  # All users considered available
            factors.append('Available for work')
            
            if user.experiencia_laboral and 'años' in user.experiencia_laboral.lower():
                score += 20
                factors.append('Has work experience')
            
            if user.telefono:
                score += 15
                factors.append('Phone number provided')
            
            # Recent registration bonus
            if user.created_at and (datetime.now() - user.created_at).days < 7:
                score += 25
                factors.append('Recent registration')
        
        elif lead_type == 'company':
            company = Company.query.get(lead_id)
            if not company:
                return jsonify({'success': False, 'error': 'Company not found'}), 404
            
            # Scoring factors for companies
            if company.descripcion and len(company.descripcion) > 100:
                score += 25
                factors.append('Detailed company description')
            
            if company.telefono:
                score += 20
                factors.append('Phone number provided')
            
            # High-demand sectors
            high_demand_sectors = ['tecnologia', 'salud', 'educacion']
            if company.sector and any(sector in company.sector.lower() for sector in high_demand_sectors):
                score += 30
                factors.append('High-demand sector')
        
        return jsonify({
            'success': True,
            'lead_score': score,
            'priority': 'high' if score >= 60 else 'medium' if score >= 30 else 'low',
            'factors': factors
        })
    
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

def calculate_match_score(user, offer):
    """Calculate compatibility score between user and job offer"""
    score = 0
    
    # Neurodivergence match
    if user.tipo_neurodivergencia in offer.neurodivergencias_aceptadas:
        score += 40
    
    # Location match
    if user.ciudad and offer.ubicacion and user.ciudad.lower() in offer.ubicacion.lower():
        score += 30
    
    # Experience factor
    if user.experiencia_laboral and 'años' in user.experiencia_laboral.lower():
        score += 20
    
    # Availability (default true)
    score += 10
    
    return score

# Error handlers for API
@api.errorhandler(404)
def api_not_found(error):
    return jsonify({'success': False, 'error': 'Endpoint not found'}), 404

@api.errorhandler(500)
def api_internal_error(error):
    return jsonify({'success': False, 'error': 'Internal server error'}), 500