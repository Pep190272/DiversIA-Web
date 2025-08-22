"""
Sistema de Email Marketing para DiversIA
Gestión completa de campañas de email a asociaciones
"""

import csv
import io
from datetime import datetime
from flask import request, jsonify, render_template_string, flash, redirect, session
from app import app, db
from models import EmailMarketing

@app.route('/email-marketing/add', methods=['POST'])
def add_email_marketing_manual():
    """Añadir registro de email marketing manualmente"""
    if not request.args.get('admin') == 'true':
        return jsonify({'error': 'No autorizado'}), 403
    
    data = request.get_json()
    try:
        new_record = EmailMarketing(
            comunidad_autonoma=data.get('comunidad_autonoma', '').strip(),
            asociacion=data.get('asociacion', '').strip(),
            email=data.get('email', '').strip(),
            telefono=data.get('telefono', '').strip(),
            direccion=data.get('direccion', '').strip(),
            servicios=data.get('servicios', '').strip(),
            fecha_enviado=data.get('fecha_enviado', '').strip(),
            respuesta=data.get('respuesta', '').strip(),
            notas_especiales=data.get('notas_especiales', '').strip(),
            notas_personalizadas=data.get('notas_personalizadas', '').strip()
        )
        db.session.add(new_record)
        db.session.commit()
        
        return jsonify({'success': True, 'message': 'Registro añadido correctamente'})
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@app.route('/email-marketing/get/<int:record_id>', methods=['GET'])
def get_email_marketing_record(record_id):
    """Obtener registro específico para edición"""
    if not request.args.get('admin') == 'true':
        return jsonify({'error': 'No autorizado'}), 403
    
    try:
        record = EmailMarketing.query.get_or_404(record_id)
        return jsonify({
            'success': True,
            'data': {
                'id': record.id,
                'comunidad_autonoma': record.comunidad_autonoma,
                'asociacion': record.asociacion,
                'email': record.email,
                'telefono': record.telefono,
                'direccion': record.direccion,
                'servicios': record.servicios,
                'fecha_enviado': record.fecha_enviado,
                'respuesta': record.respuesta,
                'notas_especiales': record.notas_especiales,
                'notas_personalizadas': record.notas_personalizadas
            }
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/email-marketing/update/<int:record_id>', methods=['POST'])
def update_email_marketing_record(record_id):
    """Actualizar registro completo"""
    if not request.args.get('admin') == 'true':
        return jsonify({'error': 'No autorizado'}), 403
    
    data = request.get_json()
    
    try:
        record = EmailMarketing.query.get_or_404(record_id)
        
        # Actualizar todos los campos
        record.comunidad_autonoma = data.get('comunidad_autonoma', '').strip()
        record.asociacion = data.get('asociacion', '').strip()
        record.email = data.get('email', '').strip()
        record.telefono = data.get('telefono', '').strip()
        record.direccion = data.get('direccion', '').strip()
        record.servicios = data.get('servicios', '').strip()
        record.fecha_enviado = data.get('fecha_enviado', '').strip()
        record.respuesta = data.get('respuesta', '').strip()
        record.notas_especiales = data.get('notas_especiales', '').strip()
        record.notas_personalizadas = data.get('notas_personalizadas', '').strip()
        
        record.updated_at = datetime.now()
        db.session.commit()
        
        return jsonify({'success': True, 'message': 'Registro actualizado correctamente'})
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@app.route('/email-marketing/edit/<int:record_id>', methods=['POST'])
def edit_email_marketing_inline(record_id):
    """Editar registro de email marketing inline"""
    if not request.args.get('admin') == 'true':
        return jsonify({'error': 'No autorizado'}), 403
    
    data = request.get_json()
    
    try:
        record = EmailMarketing.query.get_or_404(record_id)
        
        field = data.get('field')
        value = data.get('value', '').strip()
        
        if field == 'comunidad_autonoma':
            record.comunidad_autonoma = value
        elif field == 'asociacion':
            record.asociacion = value
        elif field == 'email':
            record.email = value
        elif field == 'telefono':
            record.telefono = value
        elif field == 'direccion':
            record.direccion = value
        elif field == 'servicios':
            record.servicios = value
        elif field == 'fecha_enviado':
            record.fecha_enviado = value
        elif field == 'respuesta':
            record.respuesta = value
        elif field == 'notas_especiales':
            record.notas_especiales = value
        elif field == 'notas_personalizadas':
            record.notas_personalizadas = value
        else:
            return jsonify({'error': 'Campo no válido'}), 400
        
        record.updated_at = datetime.now()
        db.session.commit()
        
        return jsonify({'success': True, 'value': value})
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@app.route('/email-marketing')
def email_marketing_dashboard():
    """Dashboard principal de email marketing - Tabla simple"""
    # Verificar autenticación admin
    if 'admin_ok' not in session or not session.get('admin_ok'):
        return redirect('/diversia-admin')
    
    # Obtener todas las asociaciones
    asociaciones = EmailMarketing.query.all()
    total_asociaciones = len(asociaciones)
    
    return render_template_string(EMAIL_MARKETING_TABLE_TEMPLATE, 
                                asociaciones=asociaciones,
                                total_asociaciones=total_asociaciones)

@app.route('/email-marketing-funnel')
def email_marketing_funnel():
    """Dashboard en formato embudo con métricas reales"""
    # Verificar autenticación admin
    if 'admin_ok' not in session or not session.get('admin_ok'):
        return redirect('/diversia-admin')
    
    # Estadísticas reales basadas en datos
    total = EmailMarketing.query.count()
    enviados = EmailMarketing.query.filter(EmailMarketing.fecha_enviado != '').filter(EmailMarketing.fecha_enviado.isnot(None)).count()
    con_respuesta = EmailMarketing.query.filter(EmailMarketing.respuesta != '').filter(EmailMarketing.respuesta.isnot(None)).count()
    
    # Calcular tipos de respuesta por palabras clave
    vacaciones = EmailMarketing.query.filter(EmailMarketing.respuesta.contains('VACACIONES')).count()
    reuniones = EmailMarketing.query.filter(EmailMarketing.respuesta.contains('reunion')).count()
    contacto_nuevo = EmailMarketing.query.filter(EmailMarketing.respuesta.contains('CORREO NUEVO')).count()
    
    # Stats por comunidad autónoma (sintaxis SQLAlchemy corregida)
    stats_comunidad = db.session.query(
        EmailMarketing.comunidad_autonoma,
        db.func.count(EmailMarketing.id).label('total'),
        db.func.sum(db.case((EmailMarketing.respuesta != '', 1), else_=0)).label('con_respuesta')
    ).group_by(EmailMarketing.comunidad_autonoma).order_by(db.func.count(EmailMarketing.id).desc()).limit(10).all()
    
    # Top 5 respuestas más comunes
    respuestas_comunes = db.session.query(
        EmailMarketing.respuesta,
        db.func.count(EmailMarketing.id).label('count')
    ).filter(EmailMarketing.respuesta != '').filter(EmailMarketing.respuesta.isnot(None)).group_by(EmailMarketing.respuesta).order_by(db.func.count(EmailMarketing.id).desc()).limit(5).all()
    
    return render_template_string(EMAIL_MARKETING_DASHBOARD_INTERACTIVE,
                                total=total, enviados=enviados, con_respuesta=con_respuesta,
                                vacaciones=vacaciones, reuniones=reuniones, contacto_nuevo=contacto_nuevo,
                                stats_comunidad=stats_comunidad, respuestas_comunes=respuestas_comunes)

@app.route('/email-marketing/import', methods=['POST'])
def import_email_marketing_csv():
    """Importar CSV de email marketing"""
    if 'file' not in request.files:
        flash('No se seleccionó archivo', 'error')
        return redirect('/email-marketing?admin=true')
    
    file = request.files['file']
    if file.filename == '':
        flash('No se seleccionó archivo', 'error')
        return redirect('/email-marketing?admin=true')
    
    try:
        # Leer CSV
        stream = io.StringIO(file.stream.read().decode("UTF-8"), newline=None)
        csv_reader = csv.DictReader(stream)
        
        imported_count = 0
        updated_count = 0
        
        for row in csv_reader:
            # Validar datos esenciales
            asociacion = row.get('Asociación', '').strip()
            email = row.get('Email', '').strip()
            
            # Saltar filas vacías o sin datos válidos
            if not asociacion or len(asociacion) < 3:
                continue
                
            # Limpiar email
            if email.startswith('mailto:'):
                email = email[7:]
            
            # Validar email
            if not email or '@' not in email:
                continue
            
            # Buscar si ya existe
            existing = EmailMarketing.query.filter_by(email=email).first()
            
            if existing:
                # Actualizar
                existing.comunidad_autonoma = row.get('Comunidad Autónoma', '').strip()
                existing.asociacion = asociacion
                existing.telefono = row.get('Teléfono', '').strip()
                existing.direccion = row.get('Dirección', '').strip()
                existing.servicios = row.get('Servicios', '').strip()
                existing.fecha_enviado = row.get('Envios', '').strip()
                existing.respuesta = row.get('Respuestas', '').strip()
                existing.notas_especiales = ''
                existing.updated_at = datetime.now()
                updated_count += 1
            else:
                # Crear nuevo
                new_contact = EmailMarketing(
                    comunidad_autonoma = row.get('Comunidad Autónoma', '').strip(),
                    asociacion = asociacion,
                    email = email,
                    telefono = row.get('Teléfono', '').strip(),
                    direccion = row.get('Dirección', '').strip(),
                    servicios = row.get('Servicios', '').strip(),
                    fecha_enviado = row.get('Envios', '').strip(),
                    respuesta = row.get('Respuestas', '').strip(),
                    notas_especiales = ''
                )
                db.session.add(new_contact)
                imported_count += 1
        
        db.session.commit()
        flash(f'✅ Email Marketing actualizado: {imported_count} nuevos, {updated_count} actualizados', 'success')
        
    except Exception as e:
        db.session.rollback()
        flash(f'Error al importar: {str(e)}', 'error')
    
    return redirect('/email-marketing?admin=true')

@app.route('/email-marketing/delete/<int:contact_id>', methods=['DELETE'])
def delete_email_marketing_contact(contact_id):
    """Eliminar contacto de email marketing"""
    try:
        contact = EmailMarketing.query.get_or_404(contact_id)
        db.session.delete(contact)
        db.session.commit()
        return jsonify({'success': True, 'message': 'Contacto eliminado correctamente'})
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/email-marketing/funnel-ventas')
def email_marketing_funnel_ventas():
    """Dashboard de funnel de ventas estilo DiversIA"""
    try:
        # Obtener todos los registros
        asociaciones = EmailMarketing.query.all()
        
        # Análisis inteligente de respuestas
        contactos_iniciales = len(asociaciones)
        respuestas_totales = len([a for a in asociaciones if a.respuesta])
        
        # Análisis de reuniones (buscar palabras clave en respuestas y notas)
        reuniones_keywords = ['reunión', 'reunion', 'meeting', 'llamada', 'videollamada', 'zoom', 'teams', 'cita', 'entrevista', 'contacto', 'hablar', 'conversar']
        reuniones = []
        for a in asociaciones:
            texto_completo = ""
            if a.respuesta:
                texto_completo += a.respuesta.lower() + " "
            if a.notas_personalizadas:
                texto_completo += a.notas_personalizadas.lower() + " "
            if a.notas_especiales:
                texto_completo += a.notas_especiales.lower() + " "
            
            if texto_completo and any(keyword in texto_completo for keyword in reuniones_keywords):
                reuniones.append(a)
        
        # Análisis de NDA y contratos (palabras clave avanzadas y más específicas)
        nda_keywords = ['nda', 'confidencialidad', 'acuerdo', 'contrato', 'firma', 'legal', 'términos', 'clausula', 'firmado', 'firmar', 'pendiente', 'documento', 'protocolo']
        nda_proceso = []
        for a in asociaciones:
            texto_completo = ""
            if a.respuesta:
                texto_completo += a.respuesta.lower() + " "
            if a.notas_personalizadas:
                texto_completo += a.notas_personalizadas.lower() + " "
            if a.notas_especiales:
                texto_completo += a.notas_especiales.lower() + " "
            
            if texto_completo and any(keyword in texto_completo for keyword in nda_keywords):
                nda_proceso.append(a)
        
        # Análisis de interés positivo (más amplio)
        interes_keywords = ['interesa', 'interesante', 'colaborar', 'colaboración', 'partnership', 'alianza', 'trabajar juntos', 'sí', 'si', 'perfecto', 'genial', 'positivo', 'bien', 'adelante', 'encantados', 'dispuesto']
        interesados = []
        for a in asociaciones:
            texto_completo = ""
            if a.respuesta:
                texto_completo += a.respuesta.lower() + " "
            if a.notas_personalizadas:
                texto_completo += a.notas_personalizadas.lower() + " "
            
            if texto_completo and any(keyword in texto_completo for keyword in interes_keywords):
                interesados.append(a)
        
        # Calcular porcentajes
        tasa_respuesta = (respuestas_totales / contactos_iniciales * 100) if contactos_iniciales > 0 else 0
        tasa_reuniones = (len(reuniones) / respuestas_totales * 100) if respuestas_totales > 0 else 0
        tasa_nda = (len(nda_proceso) / len(reuniones) * 100) if len(reuniones) > 0 else 0
        
        # Estadísticas por comunidad para análisis geográfico
        stats_comunidad = {}
        for a in asociaciones:
            comunidad = a.comunidad_autonoma
            if comunidad not in stats_comunidad:
                stats_comunidad[comunidad] = {
                    'total': 0, 'respuestas': 0, 'reuniones': 0, 'nda': 0
                }
            stats_comunidad[comunidad]['total'] += 1
            if a.respuesta:
                stats_comunidad[comunidad]['respuestas'] += 1
                if a in reuniones:
                    stats_comunidad[comunidad]['reuniones'] += 1
                if a in nda_proceso:
                    stats_comunidad[comunidad]['nda'] += 1
        
        # Mejores comunidades por conversión
        mejores_comunidades = sorted(
            [(k, v) for k, v in stats_comunidad.items() if v['total'] >= 3],
            key=lambda x: (x[1]['nda'] / x[1]['total']) if x[1]['total'] > 0 else 0,
            reverse=True
        )[:5]
        
        datos_funnel = {
            'contactos_iniciales': contactos_iniciales,
            'respuestas_totales': respuestas_totales,
            'reuniones_count': len(reuniones),
            'nda_count': len(nda_proceso),
            'interesados_count': len(interesados),
            'tasa_respuesta': round(tasa_respuesta, 1),
            'tasa_reuniones': round(tasa_reuniones, 1),
            'tasa_nda': round(tasa_nda, 1),
            'mejores_comunidades': mejores_comunidades,
            'reuniones_detalle': reuniones,        # Todas las reuniones
            'nda_detalle': nda_proceso,            # Todos los NDAs
            'stats_comunidad': stats_comunidad
        }
        
        return render_template_string(EMAIL_MARKETING_FUNNEL_VENTAS_TEMPLATE, **datos_funnel)
        
    except Exception as e:
        return f"Error: {str(e)}", 500

@app.route('/email-marketing/delete-all', methods=['DELETE'])
def delete_all_email_marketing():
    """Eliminar TODOS los contactos de email marketing"""
    try:
        count = EmailMarketing.query.count()
        EmailMarketing.query.delete()
        db.session.commit()
        return jsonify({'success': True, 'message': f'{count} contactos eliminados correctamente'})
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/email-marketing/edit/<int:contact_id>', methods=['POST'])
def edit_email_marketing_contact(contact_id):
    """Editar un contacto específico inline"""
    if 'admin_ok' not in session or not session.get('admin_ok'):
        return jsonify({'error': 'No autorizado'}), 403
    data = request.get_json()
    
    try:
        contact = EmailMarketing.query.get_or_404(contact_id)
        
        # Actualizar campos editables
        field = data.get('field')
        value = data.get('value', '').strip()
        
        if field == 'comunidad_autonoma':
            contact.comunidad_autonoma = value
        elif field == 'asociacion':
            contact.asociacion = value
        elif field == 'email':
            contact.email = value
        elif field == 'telefono':
            contact.telefono = value
        elif field == 'direccion':
            contact.direccion = value
        elif field == 'servicios':
            contact.servicios = value
        elif field == 'fecha_enviado':
            contact.fecha_enviado = value
        elif field == 'respuesta':
            contact.respuesta = value
        elif field == 'notas_especiales':
            contact.notas_especiales = value
        elif field == 'notas_personalizadas':
            contact.notas_personalizadas = value
        else:
            return jsonify({'error': 'Campo no válido'}), 400
        
        contact.updated_at = datetime.now()
        db.session.commit()
        
        return jsonify({'success': True, 'value': value})
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@app.route('/email-marketing/export')
def export_email_marketing_csv():
    """Exportar datos de email marketing"""
    contacts = EmailMarketing.query.all()
    
    output = io.StringIO()
    writer = csv.writer(output)
    
    # Headers
    writer.writerow([
        'Comunidad Autónoma', 'Asociación', 'Email', 'Teléfono', 
        'Dirección', 'Servicios', 'ENVIADOS', 'RESPUESTA'
    ])
    
    # Data
    for contact in contacts:
        writer.writerow([
            contact.comunidad_autonoma,
            contact.asociacion,
            contact.email,
            contact.telefono or '',
            contact.direccion or '',
            contact.servicios or '',
            contact.fecha_enviado or '',
            contact.respuesta or ''
        ])
    
    output.seek(0)
    return output.getvalue(), 200, {
        'Content-Type': 'text/csv',
        'Content-Disposition': 'attachment; filename=email_marketing_diversia.csv'
    }

# Template para tabla de asociaciones
EMAIL_MARKETING_TABLE_TEMPLATE = '''
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Email Marketing - Tabla - DiversIA</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
    <style>
        .table-responsive { max-height: 70vh; overflow-y: auto; }
        .btn-sm { font-size: 0.8rem; }
        .editable-field {
            cursor: pointer;
            padding: 3px 6px;
            border-radius: 3px;
            transition: background-color 0.2s;
            display: inline-block;
            min-width: 60px;
            min-height: 20px;
        }
        .editable-field:hover {
            background-color: #e3f2fd;
            border: 1px solid #2196f3;
        }
        .editing {
            background-color: #fff3cd !important;
            border: 2px solid #ffc107 !important;
        }
        .edit-input {
            border: 2px solid #007bff;
            font-size: 0.9rem;
            padding: 2px 6px;
            width: 100%;
            min-width: 80px;
        }
        .edit-textarea {
            border: 2px solid #007bff;
            font-size: 0.9rem;
            padding: 5px;
            width: 100%;
            min-height: 60px;
            resize: vertical;
        }
        .save-cancel-buttons {
            margin-top: 5px;
        }
    </style>
</head>
<body class="bg-light">
    <div class="container-fluid">
        <div class="row">
            <div class="col-12">
                <div class="d-flex justify-content-between align-items-center mb-4">
                    <h2>📧 Email Marketing - Asociaciones ({{ total_asociaciones }})</h2>
                    <div>
                        <a href="/email-marketing-funnel?admin=true" class="btn btn-info me-2">Dashboard Embudo</a>
                        <a href="/email-marketing/funnel-ventas" class="btn btn-warning me-2">💼 Funnel Ventas</a>
                        <a href="/crm-minimal" class="btn btn-outline-secondary me-2">← CRM</a>
                        <a href="/diversia-admin-logout" class="btn btn-outline-danger">Salir</a>
                    </div>
                </div>
                
                <!-- Acciones rápidas -->
                <div class="row mb-3">
                    <div class="col-md-4">
                        <form action="/email-marketing/import" method="post" enctype="multipart/form-data" class="d-flex">
                            <input type="file" name="file" class="form-control me-2" accept=".csv" required>
                            <button type="submit" class="btn btn-success">Importar CSV</button>
                        </form>
                    </div>
                    <div class="col-md-4">
                        <div class="input-group">
                            <input type="text" id="searchInput" class="form-control" placeholder="Buscar por asociación o comunidad...">
                            <button class="btn btn-outline-secondary" type="button" onclick="clearSearch()">
                                <span id="clearIcon">🔍</span>
                            </button>
                        </div>
                    </div>
                    <div class="col-md-4 text-end">
                        <button class="btn btn-success me-2" onclick="showAddEmailMarketingForm()">➕ Añadir Registro</button>
                        <a href="/email-marketing/export" class="btn btn-warning me-2">Exportar CSV</a>
                        <button onclick="deleteAllAssociations()" class="btn btn-danger">🗑️ Eliminar Todo</button>
                    </div>
                </div>
                
                <!-- Contador de resultados -->
                <div class="row mb-2">
                    <div class="col-12">
                        <small class="text-muted">
                            Mostrando <span id="visibleCount">{{ total_asociaciones }}</span> de {{ total_asociaciones }} asociaciones
                        </small>
                    </div>
                </div>
                
                <!-- Formulario añadir registro -->
                <div id="addEmailMarketingForm" class="card mb-4" style="display: none;">
                    <div class="card-header">
                        <h5>Añadir Nuevo Registro de Email Marketing</h5>
                    </div>
                    <div class="card-body">
                        <form id="emailMarketingForm">
                            <div class="row">
                                <div class="col-md-6">
                                    <div class="mb-3">
                                        <label class="form-label">Comunidad Autónoma *</label>
                                        <input type="text" class="form-control" id="emComunidad" required 
                                               placeholder="Ej: Andalucía, Madrid, Cataluña...">
                                    </div>
                                </div>
                                <div class="col-md-6">
                                    <div class="mb-3">
                                        <label class="form-label">Nombre de la Asociación *</label>
                                        <input type="text" class="form-control" id="emAsociacion" required 
                                               placeholder="Nombre completo de la asociación">
                                    </div>
                                </div>
                                <div class="col-md-6">
                                    <div class="mb-3">
                                        <label class="form-label">Email *</label>
                                        <input type="email" class="form-control" id="emEmail" required 
                                               placeholder="contacto@asociacion.org">
                                    </div>
                                </div>
                                <div class="col-md-6">
                                    <div class="mb-3">
                                        <label class="form-label">Teléfono</label>
                                        <input type="text" class="form-control" id="emTelefono" 
                                               placeholder="600 123 456">
                                    </div>
                                </div>
                                <div class="col-md-12">
                                    <div class="mb-3">
                                        <label class="form-label">Dirección</label>
                                        <input type="text" class="form-control" id="emDireccion" 
                                               placeholder="Dirección completa">
                                    </div>
                                </div>
                                <div class="col-md-6">
                                    <div class="mb-3">
                                        <label class="form-label">Servicios</label>
                                        <textarea class="form-control" id="emServicios" rows="2" 
                                                placeholder="Descripción de servicios ofrecidos"></textarea>
                                    </div>
                                </div>
                                <div class="col-md-6">
                                    <div class="mb-3">
                                        <label class="form-label">Fecha Enviado</label>
                                        <input type="date" class="form-control" id="emFechaEnviado">
                                    </div>
                                </div>
                                <div class="col-md-6">
                                    <div class="mb-3">
                                        <label class="form-label">Respuesta</label>
                                        <textarea class="form-control" id="emRespuesta" rows="2" 
                                                placeholder="Respuesta recibida"></textarea>
                                    </div>
                                </div>
                                <div class="col-md-6">
                                    <div class="mb-3">
                                        <label class="form-label">Notas Personalizadas</label>
                                        <textarea class="form-control" id="emNotasPersonalizadas" rows="2" 
                                                placeholder="Notas adicionales y seguimiento"></textarea>
                                    </div>
                                </div>
                            </div>
                            <div class="d-flex gap-2">
                                <button type="submit" class="btn btn-success">Crear Registro</button>
                                <button type="button" class="btn btn-secondary" onclick="hideAddEmailMarketingForm()">Cancelar</button>
                            </div>
                        </form>
                    </div>
                </div>
                
                <!-- Tabla de Asociaciones con Fichas de Edición -->
                <div class="card">
                    <div class="card-body p-0">
                        <div class="table-responsive">
                            <table class="table table-striped table-hover mb-0">
                                <thead class="table-dark">
                                    <tr>
                                        <th>ID</th>
                                        <th>Comunidad</th>
                                        <th>Asociación</th>
                                        <th>Email</th>
                                        <th>Estado Email</th>
                                        <th>Respuesta</th>
                                        <th>Acciones</th>
                                    </tr>
                                </thead>
                                <tbody>
                                    {% for asociacion in asociaciones %}
                                    <tr data-id="{{ asociacion.id }}">
                                        <td><span class="badge bg-primary">#{{ asociacion.id }}</span></td>
                                        <td><small class="text-muted">{{ asociacion.comunidad_autonoma }}</small></td>
                                        <td><strong>{{ asociacion.asociacion }}</strong></td>
                                        <td>
                                            <a href="mailto:{{ asociacion.email }}" class="text-decoration-none">{{ asociacion.email }}</a>
                                        </td>
                                        <td>
                                            {% if asociacion.fecha_enviado %}
                                                <span class="badge bg-success">{{ asociacion.fecha_enviado }}</span>
                                            {% else %}
                                                <span class="badge bg-secondary">No enviado</span>
                                            {% endif %}
                                        </td>
                                        <td>
                                            {% if asociacion.respuesta %}
                                                <span class="badge bg-info">Respondido</span>
                                            {% else %}
                                                <span class="badge bg-warning text-dark">Sin respuesta</span>
                                            {% endif %}
                                        </td>
                                        <td>
                                            <div class="btn-group" role="group">
                                                <button class="btn btn-sm btn-outline-primary" onclick="openEditModal({{ asociacion.id }})">
                                                    ✏️ Editar
                                                </button>
                                                <button class="btn btn-sm btn-outline-danger" onclick="deleteAssociation({{ asociacion.id }})">
                                                    🗑️
                                                </button>
                                            </div>
                                        </td>
                                    </tr>
                                    {% endfor %}
                                </tbody>
                            </table>
                        </div>
                    </div>
                </div>

                <!-- Modal de Edición -->
                <div class="modal fade" id="editModal" tabindex="-1">
                    <div class="modal-dialog modal-lg">
                        <div class="modal-content">
                            <div class="modal-header">
                                <h5 class="modal-title">✏️ Editar Asociación</h5>
                                <button type="button" class="btn-close" data-bs-dismiss="modal"></button>
                            </div>
                            <div class="modal-body">
                                <form id="editForm">
                                    <input type="hidden" id="editId">
                                    <div class="row">
                                        <div class="col-md-6">
                                            <div class="mb-3">
                                                <label class="form-label">Comunidad Autónoma *</label>
                                                <input type="text" class="form-control" id="editComunidad" required>
                                            </div>
                                        </div>
                                        <div class="col-md-6">
                                            <div class="mb-3">
                                                <label class="form-label">Asociación *</label>
                                                <input type="text" class="form-control" id="editAsociacion" required>
                                            </div>
                                        </div>
                                        <div class="col-md-6">
                                            <div class="mb-3">
                                                <label class="form-label">Email *</label>
                                                <input type="email" class="form-control" id="editEmail" required>
                                            </div>
                                        </div>
                                        <div class="col-md-6">
                                            <div class="mb-3">
                                                <label class="form-label">Teléfono</label>
                                                <input type="text" class="form-control" id="editTelefono">
                                            </div>
                                        </div>
                                        <div class="col-md-12">
                                            <div class="mb-3">
                                                <label class="form-label">Dirección</label>
                                                <input type="text" class="form-control" id="editDireccion">
                                            </div>
                                        </div>
                                        <div class="col-md-6">
                                            <div class="mb-3">
                                                <label class="form-label">Servicios</label>
                                                <textarea class="form-control" id="editServicios" rows="3"></textarea>
                                            </div>
                                        </div>
                                        <div class="col-md-6">
                                            <div class="mb-3">
                                                <label class="form-label">Fecha Enviado</label>
                                                <input type="date" class="form-control" id="editFechaEnviado">
                                            </div>
                                        </div>
                                        <div class="col-md-6">
                                            <div class="mb-3">
                                                <label class="form-label">Respuesta</label>
                                                <textarea class="form-control" id="editRespuesta" rows="3"></textarea>
                                            </div>
                                        </div>
                                        <div class="col-md-6">
                                            <div class="mb-3">
                                                <label class="form-label">Notas Personalizadas</label>
                                                <textarea class="form-control" id="editNotasPersonalizadas" rows="3"></textarea>
                                            </div>
                                        </div>
                                    </div>
                                </form>
                            </div>
                            <div class="modal-footer">
                                <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Cancelar</button>
                                <button type="button" class="btn btn-primary" onclick="saveChanges()">💾 Guardar Cambios</button>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </div>
    
    <script>
        function deleteAssociation(id) {
            if (confirm('¿Estás seguro de que quieres eliminar esta asociación?')) {
                fetch(`/email-marketing/delete/${id}`, {
                    method: 'DELETE'
                })
                .then(response => response.json())
                .then(data => {
                    if (data.success) {
                        location.reload();
                    } else {
                        alert('Error al eliminar: ' + data.error);
                    }
                })
                .catch(error => {
                    alert('Error de conexión: ' + error);
                });
            }
        }
        
        function showAddEmailMarketingForm() {
            document.getElementById('addEmailMarketingForm').style.display = 'block';
            document.getElementById('emComunidad').focus();
        }
        
        function hideAddEmailMarketingForm() {
            document.getElementById('addEmailMarketingForm').style.display = 'none';
            document.getElementById('emailMarketingForm').reset();
        }
        
        // Gestión de registros manuales
        document.getElementById('emailMarketingForm').addEventListener('submit', function(e) {
            e.preventDefault();
            
            const formData = {
                comunidad_autonoma: document.getElementById('emComunidad').value.trim(),
                asociacion: document.getElementById('emAsociacion').value.trim(),
                email: document.getElementById('emEmail').value.trim(),
                telefono: document.getElementById('emTelefono').value.trim(),
                direccion: document.getElementById('emDireccion').value.trim(),
                servicios: document.getElementById('emServicios').value.trim(),
                fecha_enviado: document.getElementById('emFechaEnviado').value.trim(),
                respuesta: document.getElementById('emRespuesta').value.trim(),
                notas_personalizadas: document.getElementById('emNotasPersonalizadas').value.trim()
            };
            
            if (!formData.comunidad_autonoma || !formData.asociacion || !formData.email) {
                alert('Por favor, completa los campos obligatorios (Comunidad, Asociación, Email)');
                return;
            }
            
            fetch('/email-marketing/add?admin=true', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(formData)
            })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    alert('✅ Registro añadido correctamente');
                    hideAddEmailMarketingForm();
                    location.reload(); // Actualizar la tabla
                } else {
                    alert('❌ Error: ' + data.error);
                }
            })
            .catch(error => {
                alert('❌ Error de conexión: ' + error);
            });
        });
        
        // Modal de edición
        function openEditModal(id) {
            fetch(`/email-marketing/get/${id}?admin=true`)
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    const asociacion = data.data;
                    document.getElementById('editId').value = asociacion.id;
                    document.getElementById('editComunidad').value = asociacion.comunidad_autonoma || '';
                    document.getElementById('editAsociacion').value = asociacion.asociacion || '';
                    document.getElementById('editEmail').value = asociacion.email || '';
                    document.getElementById('editTelefono').value = asociacion.telefono || '';
                    document.getElementById('editDireccion').value = asociacion.direccion || '';
                    document.getElementById('editServicios').value = asociacion.servicios || '';
                    document.getElementById('editFechaEnviado').value = asociacion.fecha_enviado || '';
                    document.getElementById('editRespuesta').value = asociacion.respuesta || '';
                    document.getElementById('editNotasPersonalizadas').value = asociacion.notas_personalizadas || '';
                    
                    var editModal = new bootstrap.Modal(document.getElementById('editModal'));
                    editModal.show();
                } else {
                    alert('Error cargando datos: ' + data.error);
                }
            })
            .catch(error => {
                alert('Error de conexión: ' + error);
            });
        }
        
        function saveChanges() {
            const id = document.getElementById('editId').value;
            const formData = {
                comunidad_autonoma: document.getElementById('editComunidad').value.trim(),
                asociacion: document.getElementById('editAsociacion').value.trim(),
                email: document.getElementById('editEmail').value.trim(),
                telefono: document.getElementById('editTelefono').value.trim(),
                direccion: document.getElementById('editDireccion').value.trim(),
                servicios: document.getElementById('editServicios').value.trim(),
                fecha_enviado: document.getElementById('editFechaEnviado').value.trim(),
                respuesta: document.getElementById('editRespuesta').value.trim(),
                notas_personalizadas: document.getElementById('editNotasPersonalizadas').value.trim()
            };
            
            if (!formData.comunidad_autonoma || !formData.asociacion || !formData.email) {
                alert('Por favor, completa los campos obligatorios');
                return;
            }
            
            fetch(`/email-marketing/update/${id}?admin=true`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(formData)
            })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    alert('✅ Cambios guardados correctamente');
                    var editModal = bootstrap.Modal.getInstance(document.getElementById('editModal'));
                    editModal.hide();
                    location.reload();
                } else {
                    alert('❌ Error: ' + data.error);
                }
            })
            .catch(error => {
                alert('❌ Error de conexión: ' + error);
            });
        }
        
        function deleteAllAssociations() {
            if (confirm('⚠️ ATENCIÓN: ¿Estás COMPLETAMENTE SEGURO de eliminar TODAS las asociaciones?')) {
                if (confirm('🛑 ÚLTIMA CONFIRMACIÓN: Esto eliminará TODOS los contactos de Email Marketing. ¿Confirmas?')) {
                    fetch('/email-marketing/delete-all', {
                        method: 'DELETE'
                    })
                    .then(response => response.json())
                    .then(data => {
                        if (data.success) {
                            alert('✅ ' + data.message);
                            location.reload();
                        } else {
                            alert('❌ Error al eliminar todo: ' + data.error);
                        }
                    })
                    .catch(error => {
                        alert('❌ Error de conexión: ' + error);
                    });
                }
            }
        }

        // Sistema de búsqueda
        let allRows = [];
        
        function initializeSearch() {
            allRows = Array.from(document.querySelectorAll('tbody tr'));
            const searchInput = document.getElementById('searchInput');
            
            searchInput.addEventListener('input', function() {
                performSearch(this.value);
            });
            
            searchInput.addEventListener('keydown', function(e) {
                if (e.key === 'Escape') {
                    clearSearch();
                }
            });
        }
        
        function performSearch(searchTerm) {
            const term = searchTerm.toLowerCase().trim();
            let visibleCount = 0;
            
            allRows.forEach(row => {
                const comunidad = row.cells[1].textContent.toLowerCase();
                const asociacion = row.cells[2].textContent.toLowerCase();
                const email = row.cells[3].textContent.toLowerCase();
                
                const matches = comunidad.includes(term) || 
                              asociacion.includes(term) || 
                              email.includes(term);
                
                if (matches || term === '') {
                    row.style.display = '';
                    visibleCount++;
                } else {
                    row.style.display = 'none';
                }
            });
            
            document.getElementById('visibleCount').textContent = visibleCount;
            document.getElementById('clearIcon').textContent = term ? '✗' : '🔍';
        }
        
        function clearSearch() {
            document.getElementById('searchInput').value = '';
            performSearch('');
            document.getElementById('searchInput').focus();
        }

        // Sistema de edición inline
        document.addEventListener('DOMContentLoaded', function() {
            let currentlyEditing = null;
            
            // Inicializar búsqueda
            initializeSearch();

            // Hacer todos los campos editables
            document.querySelectorAll('.editable-field').forEach(field => {
                field.addEventListener('click', function() {
                    if (currentlyEditing && currentlyEditing !== this) {
                        cancelEdit(currentlyEditing);
                    }
                    startEdit(this);
                });
            });

            function startEdit(element) {
                if (currentlyEditing === element) return;

                currentlyEditing = element;
                const originalValue = element.textContent.trim();
                const field = element.getAttribute('data-field');
                const contactId = element.getAttribute('data-id');
                
                element.classList.add('editing');
                
                // Crear input apropiado según el campo
                let inputElement;
                if (field === 'servicios' || field === 'respuesta') {
                    inputElement = document.createElement('textarea');
                    inputElement.className = 'edit-textarea';
                    inputElement.rows = 3;
                } else {
                    inputElement = document.createElement('input');
                    inputElement.className = 'edit-input';
                    inputElement.type = field === 'email' ? 'email' : 'text';
                }
                
                inputElement.value = originalValue === '-' || originalValue === 'Sin respuesta' || originalValue === 'Pendiente' ? '' : originalValue;
                
                // Crear botones de acción
                const buttonContainer = document.createElement('div');
                buttonContainer.className = 'save-cancel-buttons';
                
                const saveBtn = document.createElement('button');
                saveBtn.className = 'btn btn-sm btn-success me-1';
                saveBtn.textContent = '✓';
                saveBtn.onclick = () => saveEdit(element, inputElement, contactId, field, originalValue);
                
                const cancelBtn = document.createElement('button');
                cancelBtn.className = 'btn btn-sm btn-secondary';
                cancelBtn.textContent = '✗';
                cancelBtn.onclick = () => cancelEdit(element, originalValue);
                
                buttonContainer.appendChild(saveBtn);
                buttonContainer.appendChild(cancelBtn);
                
                // Reemplazar contenido
                element.innerHTML = '';
                element.appendChild(inputElement);
                element.appendChild(buttonContainer);
                
                inputElement.focus();
                inputElement.select();
                
                // Guardar con Enter, cancelar con Escape
                inputElement.addEventListener('keydown', function(e) {
                    if (e.key === 'Enter' && !e.shiftKey) {
                        e.preventDefault();
                        saveEdit(element, inputElement, contactId, field, originalValue);
                    } else if (e.key === 'Escape') {
                        e.preventDefault();
                        cancelEdit(element, originalValue);
                    }
                });
            }

            function saveEdit(element, inputElement, contactId, field, originalValue) {
                const newValue = inputElement.value.trim();
                
                // Mostrar loading
                element.innerHTML = '<div class="spinner-border spinner-border-sm" role="status"></div>';
                
                fetch(`/email-marketing/edit/${contactId}`, {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify({
                        field: field,
                        value: newValue
                    })
                })
                .then(response => response.json())
                .then(data => {
                    if (data.success) {
                        // Mostrar valor actualizado
                        const displayValue = newValue || (field === 'telefono' ? '-' : field === 'respuesta' ? 'Sin respuesta' : field === 'fecha_enviado' ? 'Pendiente' : '');
                        element.textContent = displayValue;
                        element.classList.remove('editing');
                        currentlyEditing = null;
                        
                        // Efecto visual de éxito
                        element.style.backgroundColor = '#d4edda';
                        setTimeout(() => {
                            element.style.backgroundColor = '';
                        }, 1000);
                    } else {
                        alert('Error al guardar: ' + data.error);
                        cancelEdit(element, originalValue);
                    }
                })
                .catch(error => {
                    alert('Error de conexión: ' + error);
                    cancelEdit(element, originalValue);
                });
            }

            function cancelEdit(element, originalValue = null) {
                if (originalValue !== null) {
                    element.textContent = originalValue;
                }
                element.classList.remove('editing');
                currentlyEditing = null;
            }
        });
    </script>

    <!-- Bootstrap JS - Carga crítica para modals -->
    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/js/bootstrap.bundle.min.js"></script>
    <script>
        // Verificar y corregir Bootstrap
        document.addEventListener('DOMContentLoaded', function() {
            // Esperar un momento para que Bootstrap se cargue completamente
            setTimeout(function() {
                if (typeof bootstrap === 'undefined') {
                    console.error('⚠️ Bootstrap no disponible - usando solución alternativa');
                    // Redefinir openEditModal para trabajar sin Bootstrap
                    window.openEditModal = function(id) {
                        // Usar modal nativo HTML/CSS
                        const modal = document.getElementById('editModal');
                        if (modal) {
                            modal.style.display = 'block';
                            modal.classList.add('show');
                            modal.style.backgroundColor = 'rgba(0,0,0,0.5)';
                            document.body.style.overflow = 'hidden';
                            
                            // Cargar datos del registro
                            fetch(`/email-marketing/get/${id}?admin=true`)
                            .then(response => response.json())
                            .then(data => {
                                if (data.success) {
                                    const asociacion = data.data;
                                    document.getElementById('editId').value = asociacion.id;
                                    document.getElementById('editComunidad').value = asociacion.comunidad_autonoma || '';
                                    document.getElementById('editAsociacion').value = asociacion.asociacion || '';
                                    document.getElementById('editEmail').value = asociacion.email || '';
                                    document.getElementById('editTelefono').value = asociacion.telefono || '';
                                    document.getElementById('editDireccion').value = asociacion.direccion || '';
                                    document.getElementById('editServicios').value = asociacion.servicios || '';
                                    document.getElementById('editFechaEnviado').value = asociacion.fecha_enviado || '';
                                    document.getElementById('editRespuesta').value = asociacion.respuesta || '';
                                    document.getElementById('editNotasPersonalizadas').value = asociacion.notas_personalizadas || '';
                                } else {
                                    alert('Error cargando datos: ' + data.error);
                                }
                            })
                            .catch(error => {
                                alert('Error de conexión: ' + error);
                            });
                        }
                    };
                    
                    // Agregar cierre del modal
                    document.querySelectorAll('[data-bs-dismiss="modal"]').forEach(btn => {
                        btn.onclick = function() {
                            const modal = document.getElementById('editModal');
                            modal.style.display = 'none';
                            modal.classList.remove('show');
                            document.body.style.overflow = 'auto';
                        };
                    });
                } else {
                    console.log('✅ Bootstrap cargado correctamente');
                }
            }, 100);
        });
    </script>
</body>
</html>
'''

# Template para dashboard embudo
EMAIL_MARKETING_FUNNEL_TEMPLATE = '''
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Dashboard Embudo - Email Marketing</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
    <style>
        .funnel-step {
            background: linear-gradient(135deg, #007bff, #0056b3);
            color: white;
            margin: 10px 0;
            padding: 20px;
            border-radius: 10px;
            position: relative;
        }
        .funnel-step:nth-child(2) { background: linear-gradient(135deg, #28a745, #1e7e34); }
        .funnel-step:nth-child(3) { background: linear-gradient(135deg, #ffc107, #e0a800); }
        .funnel-step:nth-child(4) { background: linear-gradient(135deg, #dc3545, #c82333); }
        .funnel-number { font-size: 2rem; font-weight: bold; }
        .funnel-label { font-size: 1.1rem; }
        .stats-card { border-left: 4px solid #007bff; }
    </style>
</head>
<body class="bg-light">
    <div class="container-fluid">
        <div class="row">
            <div class="col-12">
                <div class="d-flex justify-content-between align-items-center mb-4">
                    <h2>📊 Dashboard Embudo - Email Marketing</h2>
                    <div>
                        <a href="/email-marketing?admin=true" class="btn btn-primary me-2">Ver Tabla</a>
                        <a href="/crm-minimal" class="btn btn-outline-secondary me-2">← CRM</a>
                        <a href="/diversia-admin-logout" class="btn btn-outline-danger">Salir</a>
                    </div>
                </div>
                
                <!-- Embudo de conversión -->
                <div class="row">
                    <div class="col-lg-6">
                        <h4>Embudo de Email Marketing</h4>
                        
                        <div class="funnel-step">
                            <div class="d-flex justify-content-between align-items-center">
                                <div>
                                    <div class="funnel-number">{{ total }}</div>
                                    <div class="funnel-label">Total Asociaciones</div>
                                </div>
                                <div>100%</div>
                            </div>
                        </div>
                        
                        <div class="funnel-step">
                            <div class="d-flex justify-content-between align-items-center">
                                <div>
                                    <div class="funnel-number">{{ enviados }}</div>
                                    <div class="funnel-label">Emails Enviados</div>
                                </div>
                                <div>{{ "%.1f"|format((enviados/total)*100 if total > 0 else 0) }}%</div>
                            </div>
                        </div>
                        
                        <div class="funnel-step">
                            <div class="d-flex justify-content-between align-items-center">
                                <div>
                                    <div class="funnel-number">{{ respondidos }}</div>
                                    <div class="funnel-label">Respuestas Recibidas</div>
                                </div>
                                <div>{{ "%.1f"|format((respondidos/enviados)*100 if enviados > 0 else 0) }}%</div>
                            </div>
                        </div>
                        
                        <div class="funnel-step">
                            <div class="d-flex justify-content-between align-items-center">
                                <div>
                                    <div class="funnel-number">{{ interesados }}</div>
                                    <div class="funnel-label">Interesados</div>
                                </div>
                                <div>{{ "%.1f"|format((interesados/respondidos)*100 if respondidos > 0 else 0) }}%</div>
                            </div>
                        </div>
                    </div>
                    
                    <!-- Distribución por comunidad -->
                    <div class="col-lg-6">
                        <h4>Top Comunidades Autónomas</h4>
                        <div class="card">
                            <div class="card-body">
                                {% for comunidad, total_com in stats_comunidad[:10] %}
                                <div class="d-flex justify-content-between align-items-center mb-2">
                                    <span><strong>{{ comunidad }}</strong></span>
                                    <span>
                                        <span class="badge bg-primary">{{ total_com }}</span>
                                        <small class="text-muted">({{ "%.1f"|format((total_com/total)*100) }}%)</small>
                                    </span>
                                </div>
                                <div class="progress mb-3" style="height: 8px;">
                                    <div class="progress-bar" style="width: {{ (total_com/total)*100 }}%"></div>
                                </div>
                                {% endfor %}
                            </div>
                        </div>
                        
                        <!-- Métricas clave -->
                        <div class="row mt-4">
                            <div class="col-6">
                                <div class="card stats-card">
                                    <div class="card-body text-center">
                                        <h3 class="text-primary">{{ "%.1f"|format((respondidos/enviados)*100 if enviados > 0 else 0) }}%</h3>
                                        <p class="mb-0">Tasa de Respuesta</p>
                                    </div>
                                </div>
                            </div>
                            <div class="col-6">
                                <div class="card stats-card">
                                    <div class="card-body text-center">
                                        <h3 class="text-success">{{ "%.1f"|format((interesados/total)*100 if total > 0 else 0) }}%</h3>
                                        <p class="mb-0">Conversión Total</p>
                                    </div>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </div>
</body>
</html>
'''

# Template de Funnel de Ventas estilo DiversIA
EMAIL_MARKETING_FUNNEL_VENTAS_TEMPLATE = '''
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Funnel de Ventas - DiversIA (Agosto 2025)</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
    <style>
        body {
            background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
        }
        
        .funnel-container {
            max-width: 800px;
            margin: 50px auto;
            padding: 40px;
            background: white;
            border-radius: 20px;
            box-shadow: 0 15px 35px rgba(0,0,0,0.1);
        }
        
        .funnel-title {
            text-align: center;
            font-size: 24px;
            font-weight: bold;
            color: #2c3e50;
            margin-bottom: 40px;
            border-bottom: 3px solid #3498db;
            padding-bottom: 15px;
        }
        
        .funnel-step {
            margin: 20px auto;
            max-width: 400px;
            position: relative;
        }
        
        .funnel-box {
            background: linear-gradient(135deg, #3498db, #2980b9);
            color: white;
            padding: 20px;
            border-radius: 15px;
            text-align: center;
            box-shadow: 0 8px 16px rgba(52, 152, 219, 0.3);
            position: relative;
            overflow: hidden;
        }
        
        .funnel-box:nth-child(2) .funnel-box { background: linear-gradient(135deg, #2ecc71, #27ae60); }
        .funnel-box:nth-child(3) .funnel-box { background: linear-gradient(135deg, #f39c12, #e67e22); }
        .funnel-box:nth-child(4) .funnel-box { background: linear-gradient(135deg, #e74c3c, #c0392b); }
        
        .funnel-number {
            font-size: 36px;
            font-weight: bold;
            margin-bottom: 5px;
        }
        
        .funnel-label {
            font-size: 16px;
            margin-bottom: 10px;
        }
        
        .funnel-percentage {
            font-size: 14px;
            opacity: 0.9;
        }
        
        .funnel-arrow {
            text-align: center;
            font-size: 30px;
            color: #3498db;
            margin: 10px 0;
        }
        
        .stats-panel {
            background: #f8f9fa;
            border-radius: 15px;
            padding: 25px;
            margin-top: 40px;
        }
        
        .metric-card {
            background: white;
            border-radius: 10px;
            padding: 20px;
            text-align: center;
            box-shadow: 0 4px 8px rgba(0,0,0,0.1);
            margin-bottom: 20px;
        }
        
        .metric-number {
            font-size: 28px;
            font-weight: bold;
            color: #2c3e50;
        }
        
        .metric-label {
            color: #7f8c8d;
            font-size: 14px;
        }
        
        .navigation-bar {
            position: fixed;
            top: 20px;
            right: 20px;
            z-index: 1000;
        }
        
        .detail-list {
            max-height: 200px;
            overflow-y: auto;
            background: white;
            border-radius: 8px;
            padding: 15px;
            margin-top: 15px;
        }
        
        .step-respuestas { background: linear-gradient(135deg, #2ecc71, #27ae60) !important; }
        .step-reuniones { background: linear-gradient(135deg, #f39c12, #e67e22) !important; }
        .step-nda { background: linear-gradient(135deg, #e74c3c, #c0392b) !important; }
    </style>
</head>
<body>
    <div class="navigation-bar">
        <a href="/email-marketing?admin=true" class="btn btn-primary me-2">📊 Ver Tabla</a>
        <a href="/crm-minimal" class="btn btn-outline-secondary me-2">← CRM</a>
        <a href="/diversia-admin-logout" class="btn btn-outline-danger">Salir</a>
    </div>

    <div class="funnel-container">
        <div class="funnel-title">
            Funnel de Ventas - DiversIA (Agosto 2025)
        </div>
        
        <!-- Paso 1: Contactos iniciales -->
        <div class="funnel-step">
            <div class="funnel-box">
                <div class="funnel-number">{{ contactos_iniciales }}</div>
                <div class="funnel-label">Contactos iniciales</div>
            </div>
        </div>
        
        <div class="funnel-arrow">▼</div>
        
        <!-- Paso 2: Respuestas -->
        <div class="funnel-step">
            <div class="funnel-box step-respuestas">
                <div class="funnel-number">{{ respuestas_totales }}</div>
                <div class="funnel-label">Respuestas</div>
                <div class="funnel-percentage">({{ tasa_respuesta }}%)</div>
            </div>
        </div>
        
        <div class="funnel-arrow">▼</div>
        
        <!-- Paso 3: Reuniones -->
        <div class="funnel-step">
            <div class="funnel-box step-reuniones">
                <div class="funnel-number">{{ reuniones_count }}</div>
                <div class="funnel-label">Reuniones</div>
                <div class="funnel-percentage">({{ tasa_reuniones }}% de respuestas)</div>
            </div>
        </div>
        
        <div class="funnel-arrow">▼</div>
        
        <!-- Paso 4: NDA en proceso -->
        <div class="funnel-step">
            <div class="funnel-box step-nda">
                <div class="funnel-number">{{ nda_count }}</div>
                <div class="funnel-label">NDA en proceso</div>
                <div class="funnel-percentage">({{ tasa_nda }}% de reuniones)</div>
            </div>
        </div>
        
        <!-- Panel de estadísticas adicionales -->
        <div class="stats-panel">
            <h5 class="text-center mb-4">📈 Métricas Detalladas</h5>
            
            <div class="row">
                <div class="col-md-4">
                    <div class="metric-card">
                        <div class="metric-number">{{ tasa_respuesta }}%</div>
                        <div class="metric-label">Tasa de Respuesta</div>
                    </div>
                </div>
                <div class="col-md-4">
                    <div class="metric-card">
                        <div class="metric-number">{{ interesados_count }}</div>
                        <div class="metric-label">Interesados</div>
                    </div>
                </div>
                <div class="col-md-4">
                    <div class="metric-card">
                        <div class="metric-number">{{ mejores_comunidades|length }}</div>
                        <div class="metric-label">Top Comunidades</div>
                    </div>
                </div>
            </div>
            
            {% if reuniones_detalle %}
            <div class="mt-4">
                <h6>🤝 Reuniones Programadas/Realizadas</h6>
                <div class="detail-list">
                    {% for reunion in reuniones_detalle %}
                    <div class="mb-3 border-bottom pb-2">
                        <strong>{{ reunion.asociacion }}</strong> 
                        <span class="badge bg-info">{{ reunion.comunidad_autonoma }}</span><br>
                        {% if reunion.respuesta %}
                        <small class="text-primary"><strong>Respuesta:</strong> {{ reunion.respuesta[:150] }}{% if reunion.respuesta|length > 150 %}...{% endif %}</small><br>
                        {% endif %}
                        {% if reunion.notas_personalizadas %}
                        <small class="text-success"><strong>Notas:</strong> {{ reunion.notas_personalizadas[:100] }}{% if reunion.notas_personalizadas|length > 100 %}...{% endif %}</small>
                        {% endif %}
                    </div>
                    {% endfor %}
                </div>
            </div>
            {% endif %}
            
            {% if nda_detalle %}
            <div class="mt-4">
                <h6>📋 NDAs y Contratos en Proceso</h6>
                <div class="detail-list">
                    {% for nda in nda_detalle %}
                    <div class="mb-3 border-bottom pb-2">
                        <strong>{{ nda.asociacion }}</strong> 
                        <span class="badge bg-danger">{{ nda.comunidad_autonoma }}</span><br>
                        {% if nda.respuesta %}
                        <small class="text-primary"><strong>Respuesta:</strong> {{ nda.respuesta[:150] }}{% if nda.respuesta|length > 150 %}...{% endif %}</small><br>
                        {% endif %}
                        {% if nda.notas_personalizadas %}
                        <small class="text-warning"><strong>Notas:</strong> {{ nda.notas_personalizadas[:100] }}{% if nda.notas_personalizadas|length > 100 %}...{% endif %}</small><br>
                        {% endif %}
                        {% if nda.notas_especiales %}
                        <small class="text-info"><strong>Especiales:</strong> {{ nda.notas_especiales[:100] }}{% if nda.notas_especiales|length > 100 %}...{% endif %}</small>
                        {% endif %}
                    </div>
                    {% endfor %}
                </div>
            </div>
            {% endif %}
            
            {% if mejores_comunidades %}
            <div class="mt-4">
                <h6>🗺️ Top Comunidades por Conversión</h6>
                <div class="detail-list">
                    {% for comunidad, stats in mejores_comunidades %}
                    <div class="d-flex justify-content-between mb-2">
                        <span><strong>{{ comunidad }}</strong></span>
                        <span>
                            <span class="badge bg-primary">{{ stats.nda }}/{{ stats.total }}</span>
                            <small class="text-muted">({{ "%.1f"|format((stats.nda/stats.total)*100) }}%)</small>
                        </span>
                    </div>
                    {% endfor %}
                </div>
            </div>
            {% endif %}
        </div>
    </div>
    
    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/js/bootstrap.bundle.min.js"></script>
</body>
</html>
'''

# Template original simplificado
EMAIL_MARKETING_SIMPLE_TEMPLATE = '''
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Email Marketing - DiversIA</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
    <script src="https://unpkg.com/lucide@latest/dist/umd/lucide.js"></script>
    <style>
        .stats-card { border-left: 4px solid #007bff; }
        .table-responsive { max-height: 60vh; overflow-y: auto; }
    </style>
</head>
<body class="bg-light">
    <div class="container-fluid">
        <div class="row">
            <div class="col-12">
                <div class="d-flex justify-content-between align-items-center mb-4">
                    <h2><i data-lucide="mail" class="me-2"></i>Email Marketing DiversIA</h2>
                    <div>
                        <a href="/crm-minimal" class="btn btn-outline-secondary me-2">← CRM</a>
                        <a href="/diversia-admin-logout" class="btn btn-outline-danger">Salir</a>
                    </div>
                </div>
                
                <!-- Estadísticas -->
                <div class="row mb-4">
                    <div class="col-md-3">
                        <div class="card stats-card">
                            <div class="card-body">
                                <h5 class="card-title">Total Asociaciones</h5>
                                <h3 class="text-primary">{{ total_asociaciones }}</h3>
                            </div>
                        </div>
                    </div>
                    <div class="col-md-3">
                        <div class="card stats-card">
                            <div class="card-body">
                                <h5 class="card-title">Enviados Julio 2025</h5>
                                <h3 class="text-success">{{ enviados_recientes }}</h3>
                            </div>
                        </div>
                    </div>
                    <div class="col-md-3">
                        <div class="card stats-card">
                            <div class="card-body">
                                <h5 class="card-title">Seguimiento Pendiente</h5>
                                <h3 class="text-warning">{{ pendientes_seguimiento }}</h3>
                            </div>
                        </div>
                    </div>
                    <div class="col-md-3">
                        <div class="card stats-card">
                            <div class="card-body">
                                <h5 class="card-title">Comunidades</h5>
                                <h3 class="text-info">{{ stats_comunidad|length }}</h3>
                            </div>
                        </div>
                    </div>
                </div>
                
                <!-- Acciones principales -->
                <div class="row mb-4">
                    <div class="col-md-6">
                        <div class="card">
                            <div class="card-header">
                                <h5><i data-lucide="upload" class="me-2"></i>Importar CSV</h5>
                            </div>
                            <div class="card-body">
                                <form action="/email-marketing/import" method="post" enctype="multipart/form-data">
                                    <div class="mb-3">
                                        <label class="form-label">Archivo CSV de Email Marketing:</label>
                                        <input type="file" name="file" class="form-control" accept=".csv" required>
                                        <small class="text-muted">Formato: Comunidad Autónoma, Asociación, Email, Teléfono, Dirección, Servicios, ENVIADOS</small>
                                    </div>
                                    <button type="submit" class="btn btn-primary">
                                        <i data-lucide="upload" class="me-1"></i>Importar
                                    </button>
                                </form>
                            </div>
                        </div>
                    </div>
                    
                    <div class="col-md-6">
                        <div class="card">
                            <div class="card-header">
                                <h5><i data-lucide="download" class="me-2"></i>Exportar Datos</h5>
                            </div>
                            <div class="card-body">
                                <p>Descargar todos los datos de email marketing</p>
                                <a href="/email-marketing/export" class="btn btn-success">
                                    <i data-lucide="download" class="me-1"></i>Exportar CSV
                                </a>
                            </div>
                        </div>
                    </div>
                </div>
                
                <!-- Distribución por Comunidad -->
                <div class="card">
                    <div class="card-header">
                        <h5><i data-lucide="map" class="me-2"></i>Distribución por Comunidad Autónoma</h5>
                    </div>
                    <div class="card-body">
                        <div class="table-responsive">
                            <table class="table table-striped">
                                <thead>
                                    <tr>
                                        <th>Comunidad Autónoma</th>
                                        <th>Total Asociaciones</th>
                                        <th>% del Total</th>
                                    </tr>
                                </thead>
                                <tbody>
                                    {% for comunidad, total in stats_comunidad %}
                                    <tr>
                                        <td>{{ comunidad }}</td>
                                        <td><span class="badge bg-primary">{{ total }}</span></td>
                                        <td>{{ "%.1f"|format((total/total_asociaciones)*100) }}%</td>
                                    </tr>
                                    {% endfor %}
                                </tbody>
                            </table>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </div>
    
    <script>
        lucide.createIcons();
        
        // Flash messages auto-hide
        setTimeout(function() {
            const alerts = document.querySelectorAll('.alert');
            alerts.forEach(alert => {
                if (alert.classList.contains('alert-success')) {
                    alert.style.transition = 'opacity 0.5s';
                    alert.style.opacity = '0';
                    setTimeout(() => alert.remove(), 500);
                }
            });
        }, 3000);
    </script>
</body>
</html>
'''

# Template de Dashboard Interactivo
EMAIL_MARKETING_DASHBOARD_INTERACTIVE = """
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Email Marketing - Dashboard Interactivo - DiversIA</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
    <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
    <style>
        .metric-card { 
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            border: none;
            border-radius: 15px;
        }
        .chart-container { height: 300px; }
        .progress-custom { height: 25px; }
    </style>
</head>
<body>
    <div class="container-fluid py-4">
        <div class="d-flex justify-content-between align-items-center mb-4">
            <h1>📊 Dashboard Email Marketing - DiversIA</h1>
            <a href="/email-marketing" class="btn btn-outline-primary">← Ver Tabla</a>
        </div>
        
        <!-- Métricas principales -->
        <div class="row mb-4">
            <div class="col-md-3">
                <div class="card metric-card">
                    <div class="card-body text-center">
                        <h3>{{ total }}</h3>
                        <p class="mb-0">Total Asociaciones</p>
                    </div>
                </div>
            </div>
            <div class="col-md-3">
                <div class="card metric-card">
                    <div class="card-body text-center">
                        <h3>{{ enviados }}</h3>
                        <p class="mb-0">Emails Enviados</p>
                        <small>{% if total > 0 %}{{ (enviados / total * 100)|round(1) }}%{% else %}0%{% endif %}</small>
                    </div>
                </div>
            </div>
            <div class="col-md-3">
                <div class="card metric-card">
                    <div class="card-body text-center">
                        <h3>{{ con_respuesta }}</h3>
                        <p class="mb-0">Con Respuesta</p>
                        <small>{% if enviados > 0 %}{{ (con_respuesta / enviados * 100)|round(1) }}%{% else %}0%{% endif %}</small>
                    </div>
                </div>
            </div>
            <div class="col-md-3">
                <div class="card metric-card">
                    <div class="card-body text-center">
                        <h3>{{ reuniones }}</h3>
                        <p class="mb-0">Solicitan Reunión</p>
                        <small>{% if con_respuesta > 0 %}{{ (reuniones / con_respuesta * 100)|round(1) }}%{% else %}0%{% endif %}</small>
                    </div>
                </div>
            </div>
        </div>
        
        <!-- Gráficos -->
        <div class="row">
            <div class="col-md-6">
                <div class="card">
                    <div class="card-header">
                        <h5>📈 Distribución por Comunidad Autónoma</h5>
                    </div>
                    <div class="card-body">
                        <div class="chart-container">
                            <canvas id="comunidadChart"></canvas>
                        </div>
                    </div>
                </div>
            </div>
            
            <div class="col-md-6">
                <div class="card">
                    <div class="card-header">
                        <h5>🎯 Estado de Respuestas</h5>
                    </div>
                    <div class="card-body">
                        <div class="chart-container">
                            <canvas id="respuestasChart"></canvas>
                        </div>
                    </div>
                </div>
            </div>
        </div>
        
        <!-- Tabla de respuestas comunes -->
        <div class="row mt-4">
            <div class="col-md-8">
                <div class="card">
                    <div class="card-header">
                        <h5>💬 Respuestas Más Comunes</h5>
                    </div>
                    <div class="card-body">
                        <div class="table-responsive">
                            <table class="table table-striped">
                                <thead>
                                    <tr>
                                        <th>Respuesta</th>
                                        <th>Frecuencia</th>
                                        <th>%</th>
                                    </tr>
                                </thead>
                                <tbody>
                                    {% for respuesta, count in respuestas_comunes %}
                                    <tr>
                                        <td>{{ respuesta[:50] }}{% if respuesta|length > 50 %}...{% endif %}</td>
                                        <td><span class="badge bg-primary">{{ count }}</span></td>
                                        <td>{% if con_respuesta > 0 %}{{ (count / con_respuesta * 100)|round(1) }}%{% else %}0%{% endif %}</td>
                                    </tr>
                                    {% endfor %}
                                </tbody>
                            </table>
                        </div>
                    </div>
                </div>
            </div>
            
            <div class="col-md-4">
                <div class="card">
                    <div class="card-header">
                        <h5>📊 Resumen de Categorías</h5>
                    </div>
                    <div class="card-body">
                        <div class="mb-3">
                            <div class="d-flex justify-content-between">
                                <span>🏖️ De Vacaciones</span>
                                <span class="badge bg-warning">{{ vacaciones }}</span>
                            </div>
                        </div>
                        <div class="mb-3">
                            <div class="d-flex justify-content-between">
                                <span>🤝 Solicitan Reunión</span>
                                <span class="badge bg-success">{{ reuniones }}</span>
                            </div>
                        </div>
                        <div class="mb-3">
                            <div class="d-flex justify-content-between">
                                <span>✉️ Nuevo Contacto</span>
                                <span class="badge bg-info">{{ contacto_nuevo }}</span>
                            </div>
                        </div>
                        <div class="mb-3">
                            <div class="d-flex justify-content-between">
                                <span>📧 Sin Respuesta</span>
                                <span class="badge bg-secondary">{{ enviados - con_respuesta }}</span>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </div>

    <script>
        // Gráfico de Comunidades
        const comunidadCtx = document.getElementById('comunidadChart').getContext('2d');
        const comunidadChart = new Chart(comunidadCtx, {
            type: 'doughnut',
            data: {
                labels: [{% for comunidad, total, con_resp in stats_comunidad %}'{{ comunidad }}'{% if not loop.last %},{% endif %}{% endfor %}],
                datasets: [{
                    data: [{% for comunidad, total, con_resp in stats_comunidad %}{{ total }}{% if not loop.last %},{% endif %}{% endfor %}],
                    backgroundColor: [
                        '#FF6384', '#36A2EB', '#FFCE56', '#4BC0C0', '#9966FF',
                        '#FF9F40', '#FF6384', '#C9CBCF', '#4BC0C0', '#FF6384'
                    ]
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                    legend: {
                        position: 'right'
                    }
                }
            }
        });

        // Gráfico de Estado de Respuestas
        const respuestasCtx = document.getElementById('respuestasChart').getContext('2d');
        const respuestasChart = new Chart(respuestasCtx, {
            type: 'bar',
            data: {
                labels: ['Enviados', 'Con Respuesta', 'Vacaciones', 'Reuniones'],
                datasets: [{
                    label: 'Cantidad',
                    data: [{{ enviados }}, {{ con_respuesta }}, {{ vacaciones }}, {{ reuniones }}],
                    backgroundColor: ['#36A2EB', '#4BC0C0', '#FFCE56', '#FF6384']
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                scales: {
                    y: {
                        beginAtZero: true
                    }
                }
            }
        });
    </script>
</body>
</html>
"""

print("✅ Email Marketing Manager cargado")