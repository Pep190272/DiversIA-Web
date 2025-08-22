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

@app.route('/email-marketing/update/<int:record_id>', methods=['POST'])
def update_email_marketing_complete(record_id):
    """Actualizar registro completo de email marketing"""
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
        record.notas_personalizadas = data.get('notas_personalizadas', '').strip()
        record.updated_at = datetime.now()
        
        db.session.commit()
        
        return jsonify({'success': True, 'message': 'Asociación actualizada correctamente'})
        
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
                
                <!-- Contador de resultados y leyenda -->
                <div class="row mb-2">
                    <div class="col-md-8">
                        <small class="text-muted">
                            Mostrando <span id="visibleCount">{{ total_asociaciones }}</span> de {{ total_asociaciones }} asociaciones
                        </small>
                    </div>
                    <div class="col-md-4 text-end">
                        <small class="text-muted">
                            <span class="badge bg-warning text-dark">Amarillo: Con notas (prioridad)</span>
                            <span class="badge bg-success">Verde: Con respuesta</span>
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
                
                <!-- Tabla de Asociaciones con Fichas Editables -->
                <div class="card">
                    <div class="card-body p-0">
                        <div class="table-responsive">
                            <table class="table table-striped mb-0">
                                <thead class="table-dark">
                                    <tr>
                                        <th>ID</th>
                                        <th>Comunidad</th>
                                        <th>Asociación</th>
                                        <th>Email</th>
                                        <th>Fecha Envío</th>
                                        <th>Acciones</th>
                                    </tr>
                                </thead>
                                <tbody>
                                    {% for asociacion in asociaciones %}
                                    <tr class="association-row {% if asociacion.notas_personalizadas %}table-warning{% elif asociacion.respuesta %}table-success{% endif %}" data-id="{{ asociacion.id }}">
                                        <td>{{ asociacion.id }}</td>
                                        <td>{{ asociacion.comunidad_autonoma }}</td>
                                        <td><strong>{{ asociacion.asociacion }}</strong></td>
                                        <td>{{ asociacion.email }}</td>
                                        <td>
                                            {% if asociacion.fecha_enviado %}
                                                <span class="badge bg-success">{{ asociacion.fecha_enviado }}</span>
                                            {% else %}
                                                <span class="badge bg-secondary">Pendiente</span>
                                            {% endif %}
                                        </td>
                                        <td>
                                            <button class="btn btn-sm btn-primary me-1" onclick="toggleEditCard({{ asociacion.id }})">
                                                <i class="bi bi-pencil"></i> Editar
                                            </button>
                                            <button class="btn btn-sm btn-danger" onclick="deleteAssociation({{ asociacion.id }})">
                                                <i class="bi bi-trash"></i>
                                            </button>
                                        </td>
                                    </tr>
                                    
                                    <!-- Ficha de edición expandible -->
                                    <tr id="editCard-{{ asociacion.id }}" class="edit-card-row d-none">
                                        <td colspan="6">
                                            <div class="card {% if asociacion.notas_personalizadas %}border-warning{% elif asociacion.respuesta %}border-success{% else %}border-primary{% endif %}">
                                                <div class="card-header {% if asociacion.notas_personalizadas %}bg-warning{% elif asociacion.respuesta %}bg-success{% else %}bg-primary{% endif %} text-white d-flex justify-content-between align-items-center">
                                                    <div>
                                                        <strong>Editar Asociación #{{ asociacion.id }}</strong>
                                                        {% if asociacion.fecha_enviado %}
                                                            <small class="ms-2">📅 Enviado: {{ asociacion.fecha_enviado }}</small>
                                                        {% endif %}
                                                    </div>
                                                    <div class="d-flex gap-2">
                                                        {% if asociacion.respuesta %}
                                                            <span class="badge bg-light text-dark">✅ Con Respuesta</span>
                                                        {% endif %}
                                                        {% if asociacion.notas_personalizadas %}
                                                            <span class="badge bg-light text-dark">📝 Con Notas</span>
                                                        {% endif %}
                                                    </div>
                                                </div>
                                                <div class="card-body">
                                                    <form id="editForm-{{ asociacion.id }}">
                                                        <div class="row">
                                                            <div class="col-md-6">
                                                                <div class="mb-3">
                                                                    <label class="form-label">Comunidad Autónoma</label>
                                                                    <input type="text" class="form-control" name="comunidad_autonoma" value="{{ asociacion.comunidad_autonoma }}">
                                                                </div>
                                                            </div>
                                                            <div class="col-md-6">
                                                                <div class="mb-3">
                                                                    <label class="form-label">Nombre de la Asociación</label>
                                                                    <input type="text" class="form-control" name="asociacion" value="{{ asociacion.asociacion }}">
                                                                </div>
                                                            </div>
                                                            <div class="col-md-6">
                                                                <div class="mb-3">
                                                                    <label class="form-label">Email</label>
                                                                    <input type="email" class="form-control" name="email" value="{{ asociacion.email }}">
                                                                </div>
                                                            </div>
                                                            <div class="col-md-6">
                                                                <div class="mb-3">
                                                                    <label class="form-label">Teléfono</label>
                                                                    <input type="text" class="form-control" name="telefono" value="{{ asociacion.telefono or '' }}">
                                                                </div>
                                                            </div>
                                                            <div class="col-md-12">
                                                                <div class="mb-3">
                                                                    <label class="form-label">Dirección</label>
                                                                    <input type="text" class="form-control" name="direccion" value="{{ asociacion.direccion or '' }}">
                                                                </div>
                                                            </div>
                                                            <div class="col-md-6">
                                                                <div class="mb-3">
                                                                    <label class="form-label">Servicios</label>
                                                                    <textarea class="form-control" name="servicios" rows="3">{{ asociacion.servicios or '' }}</textarea>
                                                                </div>
                                                            </div>
                                                            <div class="col-md-6">
                                                                <div class="mb-3">
                                                                    <label class="form-label">Fecha Enviado</label>
                                                                    <input type="date" class="form-control" name="fecha_enviado" value="{{ asociacion.fecha_enviado or '' }}">
                                                                </div>
                                                                <div class="mb-3">
                                                                    <label class="form-label">Respuesta</label>
                                                                    <textarea class="form-control" name="respuesta" rows="2">{{ asociacion.respuesta or '' }}</textarea>
                                                                </div>
                                                            </div>
                                                            <div class="col-md-12">
                                                                <div class="mb-3">
                                                                    <label class="form-label">Notas Personalizadas</label>
                                                                    <textarea class="form-control" name="notas_personalizadas" rows="2" placeholder="Añadir notas de seguimiento...">{{ asociacion.notas_personalizadas or '' }}</textarea>
                                                                </div>
                                                            </div>
                                                        </div>
                                                        <div class="d-flex gap-2">
                                                            <button type="button" class="btn btn-success" onclick="saveAssociation({{ asociacion.id }})">
                                                                Guardar Cambios
                                                            </button>
                                                            <button type="button" class="btn btn-secondary" onclick="cancelEdit({{ asociacion.id }})">
                                                                Cancelar
                                                            </button>
                                                        </div>
                                                    </form>
                                                </div>
                                            </div>
                                        </td>
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
        
        // Sistema de fichas editables
        function toggleEditCard(id) {
            const editCard = document.getElementById(`editCard-${id}`);
            if (editCard.classList.contains('d-none')) {
                // Cerrar otras fichas abiertas
                document.querySelectorAll('.edit-card-row').forEach(row => {
                    row.classList.add('d-none');
                });
                // Abrir la ficha seleccionada
                editCard.classList.remove('d-none');
            } else {
                editCard.classList.add('d-none');
            }
        }
        
        function cancelEdit(id) {
            document.getElementById(`editCard-${id}`).classList.add('d-none');
        }
        
        function saveAssociation(id) {
            const form = document.getElementById(`editForm-${id}`);
            const formData = new FormData(form);
            const data = Object.fromEntries(formData);
            
            fetch(`/email-marketing/update/${id}?admin=true`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(data)
            })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    alert('✅ Asociación actualizada correctamente');
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

        // Sistema de búsqueda mejorado para fichas editables
        function initializeSearch() {
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
            const rows = document.querySelectorAll('.association-row');
            let visibleCount = 0;
            
            rows.forEach(row => {
                try {
                    const cells = row.querySelectorAll('td');
                    if (cells.length >= 4) {
                        const comunidad = cells[1].textContent.toLowerCase();
                        const asociacion = cells[2].textContent.toLowerCase();
                        const email = cells[3].textContent.toLowerCase();
                        
                        const matches = comunidad.includes(term) || 
                                      asociacion.includes(term) || 
                                      email.includes(term) ||
                                      term === '';
                        
                        if (matches) {
                            row.style.display = '';
                            // Mantener la ficha de edición disponible pero cerrada
                            const editRow = document.getElementById(`editCard-${row.dataset.id}`);
                            if (editRow) {
                                editRow.style.display = '';
                                if (!editRow.classList.contains('d-none')) {
                                    // Si estaba abierta, mantenerla abierta
                                } else {
                                    editRow.classList.add('d-none');
                                }
                            }
                            visibleCount++;
                        } else {
                            row.style.display = 'none';
                            // Ocultar y cerrar la ficha de edición
                            const editRow = document.getElementById(`editCard-${row.dataset.id}`);
                            if (editRow) {
                                editRow.style.display = 'none';
                                editRow.classList.add('d-none');
                            }
                        }
                    }
                } catch (error) {
                    console.warn('Error processing row during search:', error);
                }
            });
            
            const visibleCountElement = document.getElementById('visibleCount');
            if (visibleCountElement) {
                visibleCountElement.textContent = visibleCount;
            }
            
            const clearIcon = document.getElementById('clearIcon');
            if (clearIcon) {
                clearIcon.textContent = term ? '❌' : '🔍';
            }
        }
        
        function clearSearch() {
            const searchInput = document.getElementById('searchInput');
            if (searchInput) {
                searchInput.value = '';
                performSearch('');
                searchInput.focus();
            }
        }

        // Sistema de fichas editables
        function toggleEditCard(id) {
            const editCard = document.getElementById(`editCard-${id}`);
            if (editCard.classList.contains('d-none')) {
                // Cerrar otras fichas abiertas
                document.querySelectorAll('.edit-card-row').forEach(row => {
                    row.classList.add('d-none');
                });
                // Abrir la ficha seleccionada
                editCard.classList.remove('d-none');
            } else {
                editCard.classList.add('d-none');
            }
        }
        
        function cancelEdit(id) {
            document.getElementById(`editCard-${id}`).classList.add('d-none');
        }
        
        function saveAssociation(id) {
            const form = document.getElementById(`editForm-${id}`);
            const formData = new FormData(form);
            const data = Object.fromEntries(formData);
            
            fetch(`/email-marketing/update/${id}?admin=true`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(data)
            })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    alert('✅ Asociación actualizada correctamente');
                    location.reload();
                } else {
                    alert('❌ Error: ' + data.error);
                }
            })
            .catch(error => {
                alert('❌ Error de conexión: ' + error);
            });
        }

        // Inicialización al cargar la página
        document.addEventListener('DOMContentLoaded', function() {
            // Inicializar búsqueda
            initializeSearch();
        });
    </script>
    
    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/js/bootstrap.bundle.min.js"></script>
</body>
</html>
'''

print("✅ Email Marketing Manager cargado")
