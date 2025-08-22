"""
Sistema de Email Marketing para DiversIA
Gestión completa de campañas de email a asociaciones
"""

import csv
import io
from datetime import datetime
from flask import request, jsonify, render_template_string, flash, redirect
from app import app, db
from models import EmailMarketing

@app.route('/email-marketing')
def email_marketing_dashboard():
    """Dashboard principal de email marketing - Tabla simple"""
    if not request.args.get('admin') == 'true':
        return redirect('/diversia-admin')
    
    # Obtener todas las asociaciones
    asociaciones = EmailMarketing.query.all()
    total_asociaciones = len(asociaciones)
    
    return render_template_string(EMAIL_MARKETING_TABLE_TEMPLATE, 
                                asociaciones=asociaciones,
                                total_asociaciones=total_asociaciones)

@app.route('/email-marketing-funnel')
def email_marketing_funnel():
    """Dashboard en formato embudo"""
    if not request.args.get('admin') == 'true':
        return redirect('/diversia-admin')
    
    # Estadísticas para embudo
    total = EmailMarketing.query.count()
    enviados = EmailMarketing.query.filter(EmailMarketing.fecha_enviado.isnot(None)).count()
    respondidos = EmailMarketing.query.filter(EmailMarketing.tipo_respuesta.isnot(None)).count()
    interesados = EmailMarketing.query.filter(EmailMarketing.tipo_respuesta == 'interesado').count()
    
    # Stats por comunidad
    stats_comunidad = db.session.query(
        EmailMarketing.comunidad_autonoma,
        db.func.count(EmailMarketing.id).label('total')
    ).group_by(EmailMarketing.comunidad_autonoma).order_by(db.func.count(EmailMarketing.id).desc()).all()
    
    return render_template_string(EMAIL_MARKETING_FUNNEL_TEMPLATE,
                                total=total, enviados=enviados, respondidos=respondidos,
                                interesados=interesados, stats_comunidad=stats_comunidad)

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
            # Buscar si ya existe
            existing = EmailMarketing.query.filter_by(
                email=row.get('Email', '').strip()
            ).first()
            
            # Separar notas especiales si existen
            notas_especiales = ''
            servicios = row.get('Servicios', '')
            if ',' in row:
                # Buscar texto después de ENVIADOS (columna extra)
                row_values = list(row.values())
                if len(row_values) > 7:  # Si hay columna extra
                    notas_especiales = row_values[-1].strip()
            
            if existing:
                # Actualizar
                existing.comunidad_autonoma = row.get('Comunidad Autónoma', '')
                existing.asociacion = row.get('Asociación', '')
                existing.telefono = row.get('Teléfono', '')
                existing.direccion = row.get('Dirección', '')
                existing.servicios = servicios
                existing.fecha_enviado = row.get('ENVIADOS', '')
                existing.notas_especiales = notas_especiales
                existing.updated_at = datetime.now()
                updated_count += 1
            else:
                # Crear nuevo
                new_contact = EmailMarketing(
                    comunidad_autonoma = row.get('Comunidad Autónoma', ''),
                    asociacion = row.get('Asociación', ''),
                    email = row.get('Email', '').strip(),
                    telefono = row.get('Teléfono', ''),
                    direccion = row.get('Dirección', ''),
                    servicios = servicios,
                    fecha_enviado = row.get('ENVIADOS', ''),
                    notas_especiales = notas_especiales
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

@app.route('/email-marketing/export')
def export_email_marketing_csv():
    """Exportar datos de email marketing"""
    contacts = EmailMarketing.query.all()
    
    output = io.StringIO()
    writer = csv.writer(output)
    
    # Headers
    writer.writerow([
        'ID', 'Comunidad Autónoma', 'Asociación', 'Email', 'Teléfono', 
        'Dirección', 'Servicios', 'Fecha Enviado', 'Estado Email', 
        'Tipo Respuesta', 'Notas Especiales'
    ])
    
    # Data
    for contact in contacts:
        writer.writerow([
            contact.id,
            contact.comunidad_autonoma,
            contact.asociacion,
            contact.email,
            contact.telefono or '',
            contact.direccion or '',
            contact.servicios or '',
            contact.fecha_enviado or '',
            contact.estado_email or '',
            contact.tipo_respuesta or '',
            contact.notas_especiales or ''
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
                    <div class="col-md-8">
                        <form action="/email-marketing/import" method="post" enctype="multipart/form-data" class="d-flex">
                            <input type="file" name="file" class="form-control me-2" accept=".csv" required>
                            <button type="submit" class="btn btn-success">Importar CSV</button>
                        </form>
                    </div>
                    <div class="col-md-4 text-end">
                        <a href="/email-marketing/export" class="btn btn-warning me-2">Exportar CSV</a>
                        <button onclick="deleteAllAssociations()" class="btn btn-danger">🗑️ Eliminar Todo</button>
                    </div>
                </div>
                
                <!-- Tabla de asociaciones -->
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
                                        <th>Teléfono</th>
                                        <th>Servicios</th>
                                        <th>Enviado</th>
                                        <th>Estado</th>
                                        <th>Notas</th>
                                        <th>Acciones</th>
                                    </tr>
                                </thead>
                                <tbody>
                                    {% for asociacion in asociaciones %}
                                    <tr>
                                        <td>{{ asociacion.id }}</td>
                                        <td><span class="badge bg-secondary">{{ asociacion.comunidad_autonoma }}</span></td>
                                        <td><strong>{{ asociacion.asociacion }}</strong></td>
                                        <td><a href="mailto:{{ asociacion.email }}">{{ asociacion.email }}</a></td>
                                        <td>{{ asociacion.telefono or '-' }}</td>
                                        <td>{{ (asociacion.servicios or '')[:50] }}{% if asociacion.servicios and asociacion.servicios|length > 50 %}...{% endif %}</td>
                                        <td>
                                            {% if asociacion.fecha_enviado %}
                                                <span class="badge bg-success">{{ asociacion.fecha_enviado }}</span>
                                            {% else %}
                                                <span class="badge bg-warning">Pendiente</span>
                                            {% endif %}
                                        </td>
                                        <td>
                                            {% if asociacion.tipo_respuesta == 'interesado' %}
                                                <span class="badge bg-success">Interesado</span>
                                            {% elif asociacion.tipo_respuesta == 'no_interesado' %}
                                                <span class="badge bg-danger">No interesado</span>
                                            {% elif asociacion.estado_email == 'respondido' %}
                                                <span class="badge bg-info">Respondido</span>
                                            {% else %}
                                                <span class="badge bg-primary">{{ asociacion.estado_email or 'Enviado' }}</span>
                                            {% endif %}
                                        </td>
                                        <td>
                                            {% if asociacion.notas_especiales %}
                                                <span class="text-warning" title="{{ asociacion.notas_especiales }}">⚠️</span>
                                            {% endif %}
                                        </td>
                                        <td>
                                            <button class="btn btn-sm btn-danger" onclick="deleteAssociation({{ asociacion.id }})">Eliminar</button>
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

print("✅ Email Marketing Manager cargado")