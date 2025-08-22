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
    """Dashboard principal de email marketing"""
    if not request.args.get('admin') == 'true':
        return redirect('/diversia-admin')
    
    # Estadísticas generales
    total_asociaciones = EmailMarketing.query.count()
    enviados_recientes = EmailMarketing.query.filter(
        EmailMarketing.fecha_enviado.like('%07/2025')
    ).count()
    
    pendientes_seguimiento = EmailMarketing.query.filter(
        EmailMarketing.seguimiento_programado.isnot(None),
        EmailMarketing.seguimiento_programado <= datetime.now()
    ).count()
    
    # Asociaciones por comunidad
    stats_comunidad = db.session.query(
        EmailMarketing.comunidad_autonoma,
        db.func.count(EmailMarketing.id).label('total')
    ).group_by(EmailMarketing.comunidad_autonoma).all()
    
    return render_template_string(EMAIL_MARKETING_TEMPLATE, 
                                total_asociaciones=total_asociaciones,
                                enviados_recientes=enviados_recientes,
                                pendientes_seguimiento=pendientes_seguimiento,
                                stats_comunidad=stats_comunidad)

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

# Template HTML para el dashboard
EMAIL_MARKETING_TEMPLATE = '''
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