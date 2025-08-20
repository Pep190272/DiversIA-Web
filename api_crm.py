from flask import request, jsonify
from app import app, db
from models import User, Company, JobOffer, Asociacion
from datetime import datetime
import json

# CORS headers for API requests - solo aplicar a rutas API
def add_cors_headers(response):
    response.headers.add('Access-Control-Allow-Origin', '*')
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
    response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE,OPTIONS')
    return response

# ============ CONTACTOS (USUARIOS) ============
@app.route('/api/contacts', methods=['GET', 'POST'])
def handle_contacts():
    """Gestión de contactos (usuarios neurodivergentes)"""
    try:
        if request.method == 'GET':
        try:
            users = User.query.all()
            contacts = []
            for user in users:
                contacts.append({
                    'id': user.id,
                    'name': f"{user.nombre} {user.apellidos}",
                    'email': user.email,
                    'phone': user.telefono,
                    'city': user.ciudad,
                    'source': 'Registro Web',
                    'type': 'Usuario ND',
                    'neurodivergence': user.tipo_neurodivergencia,
                    'created_at': user.created_at.isoformat() if user.created_at else None,
                    'exported_to_crm': getattr(user, 'exported_to_crm', False)
                })
            return add_cors_headers(jsonify(contacts))
        except Exception as e:
            # Fallback si la base de datos no está disponible
            return add_cors_headers(jsonify([]))
        
    elif request.method == 'POST':
        data = request.json
        new_user = User(
            nombre=data.get('name', ''),
            apellidos=data.get('last_name', ''),
            email=data.get('email', ''),
            telefono=data.get('phone', ''),
            ciudad=data.get('city', ''),
            tipo_neurodivergencia=data.get('neurodivergence', 'General'),
            diagnostico_formal=data.get('formal_diagnosis', False)
        )
        try:
            db.session.add(new_user)
            db.session.commit()
            return add_cors_headers(jsonify({'message': 'Contact added successfully', 'id': new_user.id})), 201
        except Exception as e:
            return add_cors_headers(jsonify({'error': 'Database not available'})), 503
    
    elif request.method == 'POST':
        data = request.json
        # Crear nuevo usuario desde CRM
        new_user = User(
            nombre=data.get('name', '').split()[0],
            apellidos=' '.join(data.get('name', '').split()[1:]) if len(data.get('name', '').split()) > 1 else '',
            email=data.get('email', ''),
            telefono=data.get('phone', ''),
            ciudad=data.get('city', ''),
            tipo_neurodivergencia=data.get('neurodivergence', 'General'),
            diagnostico_formal=data.get('formal_diagnosis', False)
        )
            try:
                db.session.add(new_user)
                db.session.commit()
                return add_cors_headers(jsonify({'message': 'Contact added successfully', 'id': new_user.id})), 201
            except Exception as e:
                return add_cors_headers(jsonify({'error': 'Database not available'})), 503
    except Exception as e:
        return add_cors_headers(jsonify({'error': 'Internal server error'})), 500

@app.route('/api/contacts/<int:contact_id>', methods=['DELETE', 'PUT'])
def manage_contact(contact_id):
    """Eliminar o actualizar contacto específico"""
    user = User.query.get_or_404(contact_id)
    
    if request.method == 'DELETE':
        db.session.delete(user)
        db.session.commit()
        return jsonify({'message': 'Contact deleted successfully'})
    
    elif request.method == 'PUT':
        data = request.json
        user.nombre = data.get('name', '').split()[0]
        user.apellidos = ' '.join(data.get('name', '').split()[1:]) if len(data.get('name', '').split()) > 1 else ''
        user.email = data.get('email', user.email)
        user.telefono = data.get('phone', user.telefono)
        user.ciudad = data.get('city', user.ciudad)
        user.tipo_neurodivergencia = data.get('neurodivergence', user.tipo_neurodivergencia)
        db.session.commit()
        return jsonify({'message': 'Contact updated successfully'})

# ============ EMPRESAS ============
@app.route('/api/companies', methods=['GET', 'POST'])
def handle_companies():
    """Gestión de empresas"""
    if request.method == 'GET':
        companies = Company.query.all()
        result = []
        for company in companies:
            result.append({
                'id': company.id,
                'name': company.nombre,
                'email': company.email,
                'phone': company.telefono,
                'sector': company.sector,
                'size': company.tamano_empresa,
                'city': company.ciudad,
                'description': company.descripcion,
                'created_at': company.created_at.isoformat() if company.created_at else None,
                'job_offers_count': len(company.job_offers),
                'exported_to_crm': company.exported_to_crm
            })
        return jsonify(result)
    
    elif request.method == 'POST':
        data = request.json
        new_company = Company(
            nombre=data.get('name', ''),
            email=data.get('email', ''),
            telefono=data.get('phone', ''),
            sector=data.get('sector', ''),
            tamano_empresa=data.get('size', ''),
            ciudad=data.get('city', ''),
            descripcion=data.get('description', '')
        )
        db.session.add(new_company)
        db.session.commit()
        return jsonify({'message': 'Company added successfully', 'id': new_company.id}), 201

@app.route('/api/companies/<int:company_id>', methods=['DELETE', 'PUT'])
def manage_company(company_id):
    """Eliminar o actualizar empresa específica"""
    company = Company.query.get_or_404(company_id)
    
    if request.method == 'DELETE':
        # Eliminar también las ofertas de trabajo asociadas
        JobOffer.query.filter_by(company_id=company_id).delete()
        db.session.delete(company)
        db.session.commit()
        return jsonify({'message': 'Company and related job offers deleted successfully'})
    
    elif request.method == 'PUT':
        data = request.json
        company.nombre = data.get('name', company.nombre)
        company.email = data.get('email', company.email)
        company.telefono = data.get('phone', company.telefono)
        company.sector = data.get('sector', company.sector)
        company.tamano_empresa = data.get('size', company.tamano_empresa)
        company.ciudad = data.get('city', company.ciudad)
        company.descripcion = data.get('description', company.descripcion)
        db.session.commit()
        return jsonify({'message': 'Company updated successfully'})

# ============ OFERTAS DE TRABAJO ============
@app.route('/api/job-offers', methods=['GET', 'POST'])
def handle_job_offers():
    """Gestión de ofertas de trabajo"""
    if request.method == 'GET':
        offers = JobOffer.query.all()
        result = []
        for offer in offers:
            result.append({
                'id': offer.id,
                'title': offer.titulo,
                'description': offer.descripcion,
                'location': offer.ubicacion,
                'salary': offer.salario,
                'company_name': offer.company.nombre if offer.company else 'Sin empresa',
                'company_id': offer.company_id,
                'accepted_neurodivergences': offer.neurodivergencias_aceptadas,
                'active': offer.activa,
                'created_at': offer.created_at.isoformat() if offer.created_at else None,
                'exported_to_crm': offer.exported_to_crm
            })
        return jsonify(result)
    
    elif request.method == 'POST':
        data = request.json
        new_offer = JobOffer(
            company_id=data.get('company_id'),
            titulo=data.get('title', ''),
            descripcion=data.get('description', ''),
            ubicacion=data.get('location', ''),
            salario=data.get('salary', ''),
            neurodivergencias_aceptadas=data.get('accepted_neurodivergences', ''),
            activa=data.get('active', True)
        )
        db.session.add(new_offer)
        db.session.commit()
        return jsonify({'message': 'Job offer added successfully', 'id': new_offer.id}), 201

@app.route('/api/job-offers/<int:offer_id>', methods=['DELETE', 'PUT'])
def manage_job_offer(offer_id):
    """Eliminar o actualizar oferta específica"""
    offer = JobOffer.query.get_or_404(offer_id)
    
    if request.method == 'DELETE':
        db.session.delete(offer)
        db.session.commit()
        return jsonify({'message': 'Job offer deleted successfully'})
    
    elif request.method == 'PUT':
        data = request.json
        offer.titulo = data.get('title', offer.titulo)
        offer.descripcion = data.get('description', offer.descripcion)
        offer.ubicacion = data.get('location', offer.ubicacion)
        offer.salario = data.get('salary', offer.salario)
        offer.neurodivergencias_aceptadas = data.get('accepted_neurodivergences', offer.neurodivergencias_aceptadas)
        offer.activa = data.get('active', offer.activa)
        db.session.commit()
        return jsonify({'message': 'Job offer updated successfully'})

# ============ ASOCIACIONES ============
@app.route('/api/associations', methods=['GET'])
def handle_associations():
    """Gestión de asociaciones"""
    associations = Asociacion.query.all()
    result = []
    for assoc in associations:
        result.append({
            'id': assoc.id,
            'name': assoc.nombre_asociacion,
            'acronym': assoc.acronimo,
            'country': assoc.pais,
            'document_type': assoc.tipo_documento,
            'document_number': assoc.numero_documento,
            'created_at': assoc.created_at.isoformat() if hasattr(assoc, 'created_at') and assoc.created_at else None
        })
    return jsonify(result)

# ============ ESTADÍSTICAS ============
@app.route('/api/stats', methods=['GET'])
def get_stats():
    """Estadísticas generales del CRM"""
    stats = {
        'total_users': User.query.count(),
        'total_companies': Company.query.count(),
        'total_job_offers': JobOffer.query.count(),
        'active_job_offers': JobOffer.query.filter_by(activa=True).count(),
        'total_associations': Asociacion.query.count(),
        'users_by_neurodivergence': {},
        'companies_by_sector': {},
        'recent_registrations': User.query.filter(User.created_at >= datetime.now().replace(day=1)).count()
    }
    
    # Usuarios por tipo de neurodivergencia
    neurodivergence_counts = db.session.query(User.tipo_neurodivergencia, db.func.count(User.id)).group_by(User.tipo_neurodivergencia).all()
    stats['users_by_neurodivergence'] = {nd: count for nd, count in neurodivergence_counts}
    
    # Empresas por sector
    sector_counts = db.session.query(Company.sector, db.func.count(Company.id)).group_by(Company.sector).all()
    stats['companies_by_sector'] = {sector: count for sector, count in sector_counts if sector}
    
    return jsonify(stats)

# ============ EXPORTACIÓN CRM ============
@app.route('/api/export/<entity_type>', methods=['POST'])
def mark_exported(entity_type):
    """Marcar entidades como exportadas al CRM externo"""
    data = request.json
    entity_ids = data.get('ids', [])
    
    if entity_type == 'users':
        User.query.filter(User.id.in_(entity_ids)).update({
            'exported_to_crm': True,
            'crm_export_date': datetime.utcnow()
        }, synchronize_session=False)
    elif entity_type == 'companies':
        Company.query.filter(Company.id.in_(entity_ids)).update({
            'exported_to_crm': True,
            'crm_export_date': datetime.utcnow()
        }, synchronize_session=False)
    elif entity_type == 'job_offers':
        JobOffer.query.filter(JobOffer.id.in_(entity_ids)).update({
            'exported_to_crm': True,
            'crm_export_date': datetime.utcnow()
        }, synchronize_session=False)
    
    db.session.commit()
    return jsonify({'message': f'{len(entity_ids)} {entity_type} marked as exported'})