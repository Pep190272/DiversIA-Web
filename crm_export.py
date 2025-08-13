"""
CRM Export utilities for DiversIA platform
This module provides functions to export data to various CRM systems
"""

import csv
import json
import os
from datetime import datetime
from app import db
from models import User, Company, JobOffer, CRMExportLog

def export_to_csv(record_type='all', output_dir='exports'):
    """
    Export database records to CSV files for CRM import
    
    Args:
        record_type (str): Type of records to export ('users', 'companies', 'job_offers', 'all')
        output_dir (str): Directory to save CSV files
    
    Returns:
        dict: Export results with file paths and record counts
    """
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    results = {}
    
    # Export Users
    if record_type in ['users', 'all']:
        users = User.query.filter_by(exported_to_crm=False).all()
        if users:
            filename = f'users_export_{timestamp}.csv'
            filepath = os.path.join(output_dir, filename)
            
            with open(filepath, 'w', newline='', encoding='utf-8') as csvfile:
                fieldnames = [
                    'id', 'nombre', 'apellidos', 'email', 'fecha_nacimiento',
                    'telefono', 'ciudad', 'tipo_neurodivergencia', 'diagnostico_formal',
                    'experiencia_laboral', 'formacion_academica', 'habilidades',
                    'intereses_laborales', 'adaptaciones_necesarias', 'created_at'
                ]
                writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                writer.writeheader()
                
                for user in users:
                    writer.writerow({
                        'id': user.id,
                        'nombre': user.nombre,
                        'apellidos': user.apellidos,
                        'email': user.email,
                        'fecha_nacimiento': user.fecha_nacimiento.strftime('%Y-%m-%d') if user.fecha_nacimiento else '',
                        'telefono': user.telefono or '',
                        'ciudad': user.ciudad or '',
                        'tipo_neurodivergencia': user.tipo_neurodivergencia,
                        'diagnostico_formal': user.diagnostico_formal,
                        'experiencia_laboral': user.experiencia_laboral or '',
                        'formacion_academica': user.formacion_academica or '',
                        'habilidades': user.habilidades or '',
                        'intereses_laborales': user.intereses_laborales or '',
                        'adaptaciones_necesarias': user.adaptaciones_necesarias or '',
                        'created_at': user.created_at.strftime('%Y-%m-%d %H:%M:%S')
                    })
                    
                    # Mark as exported
                    user.exported_to_crm = True
                    user.crm_export_date = datetime.utcnow()
                    
                    # Log export
                    log = CRMExportLog(
                        record_type='user',
                        record_id=user.id,
                        export_status='success',
                        export_method='csv',
                        exported_by='system'
                    )
                    db.session.add(log)
                
                db.session.commit()
            
            results['users'] = {
                'file': filepath,
                'count': len(users),
                'status': 'success'
            }
    
    # Export Companies
    if record_type in ['companies', 'all']:
        companies = Company.query.filter_by(exported_to_crm=False).all()
        if companies:
            filename = f'companies_export_{timestamp}.csv'
            filepath = os.path.join(output_dir, filename)
            
            with open(filepath, 'w', newline='', encoding='utf-8') as csvfile:
                fieldnames = [
                    'id', 'nombre_empresa', 'email_contacto', 'telefono',
                    'sector', 'tamano_empresa', 'ciudad', 'created_at'
                ]
                writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                writer.writeheader()
                
                for company in companies:
                    writer.writerow({
                        'id': company.id,
                        'nombre_empresa': company.nombre_empresa,
                        'email_contacto': company.email_contacto,
                        'telefono': company.telefono or '',
                        'sector': company.sector or '',
                        'tamano_empresa': company.tamano_empresa or '',
                        'ciudad': company.ciudad or '',
                        'created_at': company.created_at.strftime('%Y-%m-%d %H:%M:%S')
                    })
                    
                    # Mark as exported
                    company.exported_to_crm = True
                    company.crm_export_date = datetime.utcnow()
                    
                    # Log export
                    log = CRMExportLog(
                        record_type='company',
                        record_id=company.id,
                        export_status='success',
                        export_method='csv',
                        exported_by='system'
                    )
                    db.session.add(log)
                
                db.session.commit()
            
            results['companies'] = {
                'file': filepath,
                'count': len(companies),
                'status': 'success'
            }
    
    # Export Job Offers
    if record_type in ['job_offers', 'all']:
        job_offers = JobOffer.query.filter_by(exported_to_crm=False).all()
        if job_offers:
            filename = f'job_offers_export_{timestamp}.csv'
            filepath = os.path.join(output_dir, filename)
            
            with open(filepath, 'w', newline='', encoding='utf-8') as csvfile:
                fieldnames = [
                    'id', 'company_id', 'company_name', 'titulo_puesto', 'descripcion',
                    'tipo_contrato', 'modalidad_trabajo', 'salario_min', 'salario_max',
                    'requisitos', 'adaptaciones_disponibles', 'neurodivergencias_target',
                    'activa', 'created_at'
                ]
                writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                writer.writeheader()
                
                for offer in job_offers:
                    writer.writerow({
                        'id': offer.id,
                        'company_id': offer.company_id,
                        'company_name': offer.company.nombre_empresa,
                        'titulo_puesto': offer.titulo_puesto,
                        'descripcion': offer.descripcion,
                        'tipo_contrato': offer.tipo_contrato,
                        'modalidad_trabajo': offer.modalidad_trabajo,
                        'salario_min': offer.salario_min or '',
                        'salario_max': offer.salario_max or '',
                        'requisitos': offer.requisitos or '',
                        'adaptaciones_disponibles': offer.adaptaciones_disponibles or '',
                        'neurodivergencias_target': offer.neurodivergencias_target or '',
                        'activa': offer.activa,
                        'created_at': offer.created_at.strftime('%Y-%m-%d %H:%M:%S')
                    })
                    
                    # Mark as exported
                    offer.exported_to_crm = True
                    offer.crm_export_date = datetime.utcnow()
                    
                    # Log export
                    log = CRMExportLog(
                        record_type='job_offer',
                        record_id=offer.id,
                        export_status='success',
                        export_method='csv',
                        exported_by='system'
                    )
                    db.session.add(log)
                
                db.session.commit()
            
            results['job_offers'] = {
                'file': filepath,
                'count': len(job_offers),
                'status': 'success'
            }
    
    return results

def export_to_json(record_type='all', output_dir='exports'):
    """
    Export database records to JSON files for API-based CRM integration
    
    Args:
        record_type (str): Type of records to export
        output_dir (str): Directory to save JSON files
    
    Returns:
        dict: Export results with file paths and record counts
    """
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    results = {}
    
    # Export Users to JSON
    if record_type in ['users', 'all']:
        users = User.query.filter_by(exported_to_crm=False).all()
        if users:
            filename = f'users_export_{timestamp}.json'
            filepath = os.path.join(output_dir, filename)
            
            users_data = []
            for user in users:
                user_dict = {
                    'id': user.id,
                    'nombre': user.nombre,
                    'apellidos': user.apellidos,
                    'email': user.email,
                    'fecha_nacimiento': user.fecha_nacimiento.isoformat() if user.fecha_nacimiento else None,
                    'telefono': user.telefono,
                    'ciudad': user.ciudad,
                    'tipo_neurodivergencia': user.tipo_neurodivergencia,
                    'diagnostico_formal': user.diagnostico_formal,
                    'experiencia_laboral': user.experiencia_laboral,
                    'formacion_academica': user.formacion_academica,
                    'habilidades': user.habilidades,
                    'intereses_laborales': user.intereses_laborales,
                    'adaptaciones_necesarias': user.adaptaciones_necesarias,
                    'created_at': user.created_at.isoformat()
                }
                users_data.append(user_dict)
            
            with open(filepath, 'w', encoding='utf-8') as jsonfile:
                json.dump(users_data, jsonfile, ensure_ascii=False, indent=2)
            
            results['users'] = {
                'file': filepath,
                'count': len(users),
                'status': 'success'
            }
    
    return results

def get_export_statistics():
    """
    Get statistics about CRM exports
    
    Returns:
        dict: Statistics about exported and pending records
    """
    stats = {
        'users': {
            'total': User.query.count(),
            'exported': User.query.filter_by(exported_to_crm=True).count(),
            'pending': User.query.filter_by(exported_to_crm=False).count()
        },
        'companies': {
            'total': Company.query.count(),
            'exported': Company.query.filter_by(exported_to_crm=True).count(),
            'pending': Company.query.filter_by(exported_to_crm=False).count()
        },
        'job_offers': {
            'total': JobOffer.query.count(),
            'exported': JobOffer.query.filter_by(exported_to_crm=True).count(),
            'pending': JobOffer.query.filter_by(exported_to_crm=False).count()
        }
    }
    
    # Get recent export logs
    recent_exports = CRMExportLog.query.order_by(CRMExportLog.exported_at.desc()).limit(10).all()
    stats['recent_exports'] = [
        {
            'record_type': log.record_type,
            'record_id': log.record_id,
            'status': log.export_status,
            'method': log.export_method,
            'exported_at': log.exported_at.isoformat()
        }
        for log in recent_exports
    ]
    
    return stats

# CRM Integration helpers for popular platforms
def prepare_hubspot_format(users_data):
    """
    Convert user data to HubSpot format
    """
    hubspot_contacts = []
    for user in users_data:
        contact = {
            'properties': {
                'email': user['email'],
                'firstname': user['nombre'],
                'lastname': user['apellidos'],
                'phone': user['telefono'],
                'city': user['ciudad'],
                'custom_neurodivergence_type': user['tipo_neurodivergencia'],
                'custom_has_formal_diagnosis': user['diagnostico_formal'],
                'custom_work_experience': user['experiencia_laboral'],
                'custom_education': user['formacion_academica'],
                'custom_skills': user['habilidades'],
                'custom_job_interests': user['intereses_laborales'],
                'custom_accommodations_needed': user['adaptaciones_necesarias']
            }
        }
        hubspot_contacts.append(contact)
    return hubspot_contacts

def prepare_salesforce_format(users_data):
    """
    Convert user data to Salesforce format
    """
    salesforce_leads = []
    for user in users_data:
        lead = {
            'FirstName': user['nombre'],
            'LastName': user['apellidos'],
            'Email': user['email'],
            'Phone': user['telefono'],
            'City': user['ciudad'],
            'Company': 'DiversIA Candidate',
            'Status': 'New',
            'LeadSource': 'Website Registration',
            'Neurodivergence_Type__c': user['tipo_neurodivergencia'],
            'Has_Formal_Diagnosis__c': user['diagnostico_formal'],
            'Work_Experience__c': user['experiencia_laboral'],
            'Education__c': user['formacion_academica'],
            'Skills__c': user['habilidades'],
            'Job_Interests__c': user['intereses_laborales'],
            'Accommodations_Needed__c': user['adaptaciones_necesarias']
        }
        salesforce_leads.append(lead)
    return salesforce_leads