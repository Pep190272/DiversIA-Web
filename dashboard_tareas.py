from flask import Blueprint, render_template_string, jsonify, session, redirect
from app import app, db
import logging
from datetime import datetime, timedelta

# Configure logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

# Crear blueprint para el dashboard
dashboard_bp = Blueprint('dashboard_tareas', __name__)

@dashboard_bp.route('/dashboard-tareas')
def mostrar_dashboard():
    """Dashboard principal con gráficos interactivos"""
    if 'admin_ok' not in session or not session.get('admin_ok'):
        return redirect('/diversia-admin')
    
    return render_template_string(DASHBOARD_TEMPLATE)

@dashboard_bp.route('/api/dashboard/estados')
def api_estados():
    """API para obtener distribución de estados de tareas"""
    try:
        with db.engine.connect() as conn:
            result = conn.execute(db.text("""
                SELECT estado, COUNT(*) as cantidad 
                FROM tareas_empresa 
                GROUP BY estado
            """))
            
            datos = [{'estado': row[0] or 'Sin estado', 'cantidad': row[1]} for row in result.fetchall()]
        
        return jsonify(datos)
    except Exception as e:
        logger.error(f"Error en api_estados: {e}")
        return jsonify([])

@dashboard_bp.route('/api/dashboard/colaboradores')
def api_colaboradores():
    """API para obtener tareas por colaborador"""
    try:
        with db.engine.connect() as conn:
            result = conn.execute(db.text("""
                SELECT colaborador, COUNT(*) as cantidad 
                FROM tareas_empresa 
                GROUP BY colaborador
            """))
            
            datos = [{'colaborador': row[0] or 'Sin asignar', 'cantidad': row[1]} for row in result.fetchall()]
        
        return jsonify(datos)
    except Exception as e:
        logger.error(f"Error en api_colaboradores: {e}")
        return jsonify([])

@dashboard_bp.route('/api/dashboard/productividad')
def api_productividad():
    """API para métricas de productividad avanzadas"""
    try:
        with db.engine.connect() as conn:
            # Análisis completo por colaborador
            result = conn.execute(db.text("""
                SELECT 
                    colaborador,
                    SUM(CASE WHEN estado = 'Terminada' THEN 1 ELSE 0 END) as completadas,
                    SUM(CASE WHEN estado = 'En curso' THEN 1 ELSE 0 END) as en_curso,
                    SUM(CASE WHEN estado = 'Pendiente' OR estado IS NULL THEN 1 ELSE 0 END) as pendientes,
                    COUNT(*) as total,
                    SUM(CASE WHEN estado = 'Terminada' AND fecha_final LIKE '%07/2025%' THEN 1 ELSE 0 END) as julio_terminadas,
                    SUM(CASE WHEN estado = 'Terminada' AND fecha_final LIKE '%08/2025%' THEN 1 ELSE 0 END) as agosto_terminadas
                FROM tareas_empresa 
                WHERE colaborador IS NOT NULL
                GROUP BY colaborador
            """))
            
            datos = []
            for row in result.fetchall():
                colaborador = row[0]
                completadas = row[1]
                en_curso = row[2] 
                pendientes = row[3]
                total = row[4]
                julio_terminadas = row[5]
                agosto_terminadas = row[6]
                
                porcentaje = (completadas / total * 100) if total > 0 else 0
                
                # Calcular velocidad (tareas por mes)
                velocidad_julio = julio_terminadas
                velocidad_agosto = agosto_terminadas
                tendencia = "📈" if agosto_terminadas > julio_terminadas else "📉" if agosto_terminadas < julio_terminadas else "➡️"
                
                # Calcular eficiencia (completadas vs total asignadas)
                eficiencia = "Alta" if porcentaje >= 80 else "Media" if porcentaje >= 60 else "Baja"
                
                datos.append({
                    'colaborador': colaborador,
                    'completadas': completadas,
                    'en_curso': en_curso,
                    'pendientes': pendientes,
                    'total': total,
                    'porcentaje_completado': round(porcentaje, 1),
                    'julio_terminadas': julio_terminadas,
                    'agosto_terminadas': agosto_terminadas,
                    'tendencia': tendencia,
                    'eficiencia': eficiencia,
                    'velocidad_promedio': round((julio_terminadas + agosto_terminadas) / 2, 1)
                })
        
        return jsonify(datos)
    except Exception as e:
        logger.error(f"Error en api_productividad: {e}")
        return jsonify([])

@dashboard_bp.route('/api/dashboard/resumen')
def api_resumen():
    """API para métricas generales del resumen"""
    try:
        with db.engine.connect() as conn:
            # Total de tareas
            result = conn.execute(db.text("SELECT COUNT(*) FROM tareas_empresa"))
            total_tareas = result.scalar()
            
            # Tareas completadas
            result = conn.execute(db.text("SELECT COUNT(*) FROM tareas_empresa WHERE estado = 'Terminada'"))
            tareas_completadas = result.scalar()
            
            # Tareas en curso
            result = conn.execute(db.text("SELECT COUNT(*) FROM tareas_empresa WHERE estado = 'En curso'"))
            tareas_en_curso = result.scalar()
            
            # Tareas pendientes
            result = conn.execute(db.text("SELECT COUNT(*) FROM tareas_empresa WHERE estado = 'Pendiente' OR estado IS NULL"))
            tareas_pendientes = result.scalar()
            
            # Total empleados activos
            result = conn.execute(db.text("SELECT COUNT(*) FROM empleados WHERE active = true"))
            total_empleados = result.scalar()
            
            # Colaboradores con tareas asignadas
            result = conn.execute(db.text("SELECT COUNT(DISTINCT colaborador) FROM tareas_empresa WHERE colaborador IS NOT NULL"))
            colaboradores_activos = result.scalar()
            
            # Porcentaje de completado
            porcentaje_completado = (tareas_completadas / total_tareas * 100) if total_tareas > 0 else 0
            
            # Tareas sin asignar
            result = conn.execute(db.text("SELECT COUNT(*) FROM tareas_empresa WHERE colaborador IS NULL"))
            tareas_sin_asignar = result.scalar()
            
            # Eficiencia por mes (tareas terminadas este mes vs total)
            result = conn.execute(db.text("""
                SELECT COUNT(*) FROM tareas_empresa 
                WHERE estado = 'Terminada' AND fecha_final LIKE '%07/2025%'
            """))
            terminadas_julio = result.scalar()
            
            result = conn.execute(db.text("""
                SELECT COUNT(*) FROM tareas_empresa 
                WHERE estado = 'Terminada' AND fecha_final LIKE '%08/2025%'
            """))
            terminadas_agosto = result.scalar()
            
            datos = {
                'total_tareas': total_tareas,
                'tareas_completadas': tareas_completadas,
                'tareas_en_curso': tareas_en_curso,
                'tareas_pendientes': tareas_pendientes,
                'tareas_sin_asignar': tareas_sin_asignar,
                'total_empleados': total_empleados,
                'colaboradores_activos': colaboradores_activos,
                'porcentaje_completado': round(porcentaje_completado, 1),
                'terminadas_julio': terminadas_julio,
                'terminadas_agosto': terminadas_agosto,
                'promedio_tareas_por_empleado': round(total_tareas / total_empleados, 1) if total_empleados > 0 else 0
            }
        
        return jsonify(datos)
    except Exception as e:
        logger.error(f"Error en api_resumen: {e}")
        return jsonify({})

@dashboard_bp.route('/api/dashboard/tendencias')
def api_tendencias():
    """API para análisis de tendencias temporales"""
    try:
        with db.engine.connect() as conn:
            # Tareas por mes
            result = conn.execute(db.text("""
                SELECT 
                    'Julio 2025' as mes,
                    SUM(CASE WHEN estado = 'Terminada' AND fecha_final LIKE '%07/2025%' THEN 1 ELSE 0 END) as terminadas,
                    SUM(CASE WHEN fecha_inicio LIKE '%07/2025%' THEN 1 ELSE 0 END) as iniciadas
                FROM tareas_empresa
                UNION ALL
                SELECT 
                    'Agosto 2025' as mes,
                    SUM(CASE WHEN estado = 'Terminada' AND fecha_final LIKE '%08/2025%' THEN 1 ELSE 0 END) as terminadas,
                    SUM(CASE WHEN fecha_inicio LIKE '%08/2025%' THEN 1 ELSE 0 END) as iniciadas
                FROM tareas_empresa
                UNION ALL
                SELECT 
                    'Septiembre 2025' as mes,
                    SUM(CASE WHEN estado = 'Terminada' AND fecha_final LIKE '%09/2025%' THEN 1 ELSE 0 END) as terminadas,
                    SUM(CASE WHEN fecha_inicio LIKE '%09/2025%' THEN 1 ELSE 0 END) as iniciadas
                FROM tareas_empresa
            """))
            
            datos = [{'mes': row[0], 'terminadas': row[1], 'iniciadas': row[2]} for row in result.fetchall()]
            
        return jsonify(datos)
    except Exception as e:
        logger.error(f"Error en api_tendencias: {e}")
        return jsonify([])

@dashboard_bp.route('/api/dashboard/carga-trabajo')
def api_carga_trabajo():
    """API para análisis de carga de trabajo"""
    try:
        with db.engine.connect() as conn:
            # Distribución de carga por empleado
            result = conn.execute(db.text("""
                SELECT 
                    colaborador,
                    COUNT(*) as total_asignadas,
                    SUM(CASE WHEN estado = 'En curso' THEN 1 ELSE 0 END) as activas,
                    SUM(CASE WHEN estado = 'Pendiente' OR estado IS NULL THEN 1 ELSE 0 END) as pendientes_asignadas
                FROM tareas_empresa 
                WHERE colaborador IS NOT NULL
                GROUP BY colaborador
            """))
            
            datos = []
            for row in result.fetchall():
                colaborador = row[0]
                total = row[1]
                activas = row[2]
                pendientes = row[3]
                carga_actual = activas + pendientes
                
                # Clasificar nivel de carga
                if carga_actual >= 3:
                    nivel_carga = "Alta"
                    color_carga = "#dc3545"
                elif carga_actual == 2:
                    nivel_carga = "Media" 
                    color_carga = "#ffc107"
                else:
                    nivel_carga = "Baja"
                    color_carga = "#28a745"
                
                datos.append({
                    'colaborador': colaborador,
                    'total_asignadas': total,
                    'carga_actual': carga_actual,
                    'activas': activas,
                    'pendientes_asignadas': pendientes,
                    'nivel_carga': nivel_carga,
                    'color_carga': color_carga
                })
                
        return jsonify(datos)
    except Exception as e:
        logger.error(f"Error en api_carga_trabajo: {e}")
        return jsonify([])

@dashboard_bp.route('/api/dashboard/tipos-tareas')
def api_tipos_tareas():
    """API para análisis de tipos de tareas"""
    try:
        with db.engine.connect() as conn:
            # Categorización automática por palabras clave en el nombre
            result = conn.execute(db.text("""
                SELECT 
                    nombre,
                    estado,
                    colaborador,
                    CASE 
                        WHEN LOWER(nombre) LIKE '%marketing%' OR LOWER(nombre) LIKE '%email%' OR LOWER(nombre) LIKE '%campaña%' THEN 'Marketing'
                        WHEN LOWER(nombre) LIKE '%web%' OR LOWER(nombre) LIKE '%app%' OR LOWER(nombre) LIKE '%aplicaci%' THEN 'Desarrollo'
                        WHEN LOWER(nombre) LIKE '%linkedin%' OR LOWER(nombre) LIKE '%instagram%' OR LOWER(nombre) LIKE '%telegram%' OR LOWER(nombre) LIKE '%discord%' THEN 'Redes Sociales'
                        ELSE 'Otros'
                    END as categoria
                FROM tareas_empresa
            """))
            
            # Agrupar por categoría
            categorias = {}
            for row in result.fetchall():
                categoria = row[3]
                if categoria not in categorias:
                    categorias[categoria] = {
                        'categoria': categoria,
                        'total': 0,
                        'completadas': 0,
                        'en_curso': 0,
                        'pendientes': 0
                    }
                
                categorias[categoria]['total'] += 1
                if row[1] == 'Terminada':
                    categorias[categoria]['completadas'] += 1
                elif row[1] == 'En curso':
                    categorias[categoria]['en_curso'] += 1
                else:
                    categorias[categoria]['pendientes'] += 1
            
            datos = list(categorias.values())
            
        return jsonify(datos)
    except Exception as e:
        logger.error(f"Error en api_tipos_tareas: {e}")
        return jsonify([])

# Template del dashboard
DASHBOARD_TEMPLATE = '''
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Dashboard de Tareas - DiversIA</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
    <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
    <style>
        .metric-card {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            border-radius: 15px;
            padding: 20px;
            margin-bottom: 20px;
            box-shadow: 0 4px 15px rgba(0,0,0,0.1);
        }
        .metric-card h3 {
            font-size: 2.5rem;
            font-weight: bold;
            margin-bottom: 5px;
        }
        .metric-card p {
            margin-bottom: 0;
            opacity: 0.9;
        }
        .chart-container {
            background: white;
            border-radius: 15px;
            padding: 20px;
            margin-bottom: 20px;
            box-shadow: 0 4px 15px rgba(0,0,0,0.1);
        }
        .chart-title {
            font-size: 1.3rem;
            font-weight: bold;
            margin-bottom: 20px;
            color: #2c3e50;
        }
        .productivity-bar {
            background: #e9ecef;
            border-radius: 10px;
            height: 25px;
            overflow: hidden;
            margin: 10px 0;
        }
        .productivity-fill {
            height: 100%;
            background: linear-gradient(90deg, #28a745, #20c997);
            border-radius: 10px;
            transition: width 0.5s ease;
        }
        .colaborador-item {
            background: #f8f9fa;
            border-radius: 10px;
            padding: 15px;
            margin-bottom: 10px;
            border-left: 4px solid #007bff;
        }
        body {
            background-color: #f5f7fa;
        }
    </style>
</head>
<body>
    <div class="container-fluid mt-4">
        <!-- Header -->
        <div class="row mb-4">
            <div class="col-12">
                <div class="d-flex justify-content-between align-items-center">
                    <div>
                        <h1 class="mb-1">📊 Dashboard de Tareas</h1>
                        <p class="text-muted">Análisis completo de productividad y rendimiento</p>
                    </div>
                    <div>
                        <a href="/tareas" class="btn btn-primary me-2">📋 Ver Tareas</a>
                        <a href="/admin-dashboard" class="btn btn-outline-secondary">← Dashboard</a>
                    </div>
                </div>
            </div>
        </div>

        <!-- Métricas principales expandidas -->
        <div class="row mb-4" id="metricas-principales">
            <div class="col-md-2">
                <div class="metric-card">
                    <h3 id="total-tareas">-</h3>
                    <p>Total de Tareas</p>
                </div>
            </div>
            <div class="col-md-2">
                <div class="metric-card" style="background: linear-gradient(135deg, #28a745 0%, #20c997 100%);">
                    <h3 id="tareas-completadas">-</h3>
                    <p>Completadas</p>
                </div>
            </div>
            <div class="col-md-2">
                <div class="metric-card" style="background: linear-gradient(135deg, #ffc107 0%, #fd7e14 100%);">
                    <h3 id="tareas-en-curso">-</h3>
                    <p>En Curso</p>
                </div>
            </div>
            <div class="col-md-2">
                <div class="metric-card" style="background: linear-gradient(135deg, #dc3545 0%, #e83e8c 100%);">
                    <h3 id="tareas-sin-asignar">-</h3>
                    <p>Sin Asignar</p>
                </div>
            </div>
            <div class="col-md-2">
                <div class="metric-card" style="background: linear-gradient(135deg, #6f42c1 0%, #e83e8c 100%);">
                    <h3 id="porcentaje-completado">-</h3>
                    <p>% Completado</p>
                </div>
            </div>
            <div class="col-md-2">
                <div class="metric-card" style="background: linear-gradient(135deg, #17a2b8 0%, #6f42c1 100%);">
                    <h3 id="promedio-tareas">-</h3>
                    <p>Promedio/Empleado</p>
                </div>
            </div>
        </div>

        <!-- Gráficos principales -->
        <div class="row mb-4">
            <div class="col-md-6">
                <div class="chart-container">
                    <div class="chart-title">📈 Distribución de Estados</div>
                    <canvas id="chartEstados" width="400" height="200"></canvas>
                </div>
            </div>
            <div class="col-md-6">
                <div class="chart-container">
                    <div class="chart-title">👥 Tareas por Colaborador</div>
                    <canvas id="chartColaboradores" width="400" height="200"></canvas>
                </div>
            </div>
        </div>

        <!-- Análisis de productividad avanzado -->
        <div class="row mb-4">
            <div class="col-md-8">
                <div class="chart-container">
                    <div class="chart-title">🎯 Análisis de Productividad Avanzado</div>
                    <div id="productividad-colaboradores">
                        <div class="text-center">
                            <div class="spinner-border text-primary" role="status">
                                <span class="visually-hidden">Cargando...</span>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
            <div class="col-md-4">
                <div class="chart-container">
                    <div class="chart-title">⚖️ Carga de Trabajo</div>
                    <div id="carga-trabajo">
                        <div class="text-center">
                            <div class="spinner-border text-primary" role="status">
                                <span class="visually-hidden">Cargando...</span>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>

        <!-- Nuevos análisis -->
        <div class="row mb-4">
            <div class="col-md-6">
                <div class="chart-container">
                    <div class="chart-title">📈 Tendencias Temporales</div>
                    <canvas id="chartTendencias" width="400" height="200"></canvas>
                </div>
            </div>
            <div class="col-md-6">
                <div class="chart-container">
                    <div class="chart-title">📂 Tipos de Tareas</div>
                    <canvas id="chartTipos" width="400" height="200"></canvas>
                </div>
            </div>
        </div>

        <!-- Gráfico de barras comparativo -->
        <div class="row mb-4">
            <div class="col-12">
                <div class="chart-container">
                    <div class="chart-title">📊 Comparativa de Rendimiento por Colaborador</div>
                    <canvas id="chartComparativo" width="400" height="200"></canvas>
                </div>
            </div>
        </div>
    </div>

    <script>
        // Variables globales para los gráficos
        let chartEstados, chartColaboradores, chartComparativo, chartTendencias, chartTipos;
        
        // Cargar datos al iniciar la página
        document.addEventListener('DOMContentLoaded', function() {
            cargarMetricasPrincipales();
            cargarGraficoEstados();
            cargarGraficoColaboradores();
            cargarProductividadColaboradores();
            cargarCargaTrabajo();
            cargarGraficoTendencias();
            cargarGraficoTipos();
            cargarGraficoComparativo();
        });
        
        function cargarMetricasPrincipales() {
            fetch('/api/dashboard/resumen')
            .then(response => response.json())
            .then(data => {
                document.getElementById('total-tareas').textContent = data.total_tareas || 0;
                document.getElementById('tareas-completadas').textContent = data.tareas_completadas || 0;
                document.getElementById('tareas-en-curso').textContent = data.tareas_en_curso || 0;
                document.getElementById('tareas-sin-asignar').textContent = data.tareas_sin_asignar || 0;
                document.getElementById('porcentaje-completado').textContent = (data.porcentaje_completado || 0) + '%';
                document.getElementById('promedio-tareas').textContent = data.promedio_tareas_por_empleado || 0;
            })
            .catch(error => console.error('Error cargando métricas:', error));
        }
        
        function cargarGraficoEstados() {
            fetch('/api/dashboard/estados')
            .then(response => response.json())
            .then(data => {
                const ctx = document.getElementById('chartEstados').getContext('2d');
                
                chartEstados = new Chart(ctx, {
                    type: 'doughnut',
                    data: {
                        labels: data.map(item => item.estado),
                        datasets: [{
                            data: data.map(item => item.cantidad),
                            backgroundColor: [
                                '#28a745',  // Verde para Terminada
                                '#ffc107',  // Amarillo para En curso
                                '#dc3545',  // Rojo para Pendiente
                                '#6c757d'   // Gris para otros
                            ],
                            borderWidth: 2,
                            borderColor: '#fff'
                        }]
                    },
                    options: {
                        responsive: true,
                        plugins: {
                            legend: {
                                position: 'bottom',
                                labels: {
                                    padding: 20,
                                    usePointStyle: true
                                }
                            },
                            tooltip: {
                                callbacks: {
                                    label: function(context) {
                                        const total = context.dataset.data.reduce((a, b) => a + b, 0);
                                        const percentage = ((context.parsed / total) * 100).toFixed(1);
                                        return context.label + ': ' + context.parsed + ' (' + percentage + '%)';
                                    }
                                }
                            }
                        }
                    }
                });
            })
            .catch(error => console.error('Error cargando gráfico de estados:', error));
        }
        
        function cargarGraficoColaboradores() {
            fetch('/api/dashboard/colaboradores')
            .then(response => response.json())
            .then(data => {
                const ctx = document.getElementById('chartColaboradores').getContext('2d');
                
                chartColaboradores = new Chart(ctx, {
                    type: 'bar',
                    data: {
                        labels: data.map(item => item.colaborador),
                        datasets: [{
                            label: 'Tareas Asignadas',
                            data: data.map(item => item.cantidad),
                            backgroundColor: [
                                '#007bff',
                                '#28a745',
                                '#ffc107',
                                '#dc3545',
                                '#17a2b8'
                            ],
                            borderColor: [
                                '#0056b3',
                                '#1e7e34',
                                '#d39e00',
                                '#bd2130',
                                '#117a8b'
                            ],
                            borderWidth: 2,
                            borderRadius: 5
                        }]
                    },
                    options: {
                        responsive: true,
                        plugins: {
                            legend: {
                                display: false
                            },
                            tooltip: {
                                callbacks: {
                                    title: function(context) {
                                        return 'Colaborador: ' + context[0].label;
                                    }
                                }
                            }
                        },
                        scales: {
                            y: {
                                beginAtZero: true,
                                ticks: {
                                    stepSize: 1
                                }
                            }
                        }
                    }
                });
            })
            .catch(error => console.error('Error cargando gráfico de colaboradores:', error));
        }
        
        function cargarProductividadColaboradores() {
            fetch('/api/dashboard/productividad')
            .then(response => response.json())
            .then(data => {
                const container = document.getElementById('productividad-colaboradores');
                
                let html = '';
                data.forEach(colaborador => {
                    html += `
                        <div class="colaborador-item">
                            <div class="d-flex justify-content-between align-items-center mb-2">
                                <h6 class="mb-0">${colaborador.colaborador}</h6>
                                <div>
                                    <span class="badge bg-primary">${colaborador.porcentaje_completado}% completado</span>
                                    <span class="badge bg-secondary ms-1">${colaborador.tendencia}</span>
                                </div>
                            </div>
                            <div class="productivity-bar">
                                <div class="productivity-fill" style="width: ${colaborador.porcentaje_completado}%"></div>
                            </div>
                            <div class="row mt-2">
                                <div class="col-6">
                                    <small class="text-muted">
                                        ✅ ${colaborador.completadas} • 🔄 ${colaborador.en_curso} • ⏳ ${colaborador.pendientes}
                                    </small>
                                </div>
                                <div class="col-6">
                                    <small class="text-muted">
                                        Eficiencia: <strong>${colaborador.eficiencia}</strong> | Velocidad: ${colaborador.velocidad_promedio}/mes
                                    </small>
                                </div>
                            </div>
                            <div class="mt-2">
                                <small class="text-success">Julio: ${colaborador.julio_terminadas}</small>
                                <small class="text-info ms-2">Agosto: ${colaborador.agosto_terminadas}</small>
                            </div>
                        </div>
                    `;
                });
                
                container.innerHTML = html;
            })
            .catch(error => console.error('Error cargando productividad:', error));
        }
        
        function cargarCargaTrabajo() {
            fetch('/api/dashboard/carga-trabajo')
            .then(response => response.json())
            .then(data => {
                const container = document.getElementById('carga-trabajo');
                
                let html = '';
                data.forEach(empleado => {
                    html += `
                        <div class="mb-3 p-3 border rounded" style="border-left: 4px solid ${empleado.color_carga} !important;">
                            <div class="d-flex justify-content-between">
                                <strong>${empleado.colaborador}</strong>
                                <span class="badge" style="background-color: ${empleado.color_carga};">${empleado.nivel_carga}</span>
                            </div>
                            <div class="mt-2">
                                <div class="small">Carga actual: <strong>${empleado.carga_actual}</strong> tareas</div>
                                <div class="small text-muted">${empleado.activas} activas + ${empleado.pendientes_asignadas} pendientes</div>
                                <div class="small text-muted">Total asignadas: ${empleado.total_asignadas}</div>
                            </div>
                        </div>
                    `;
                });
                
                container.innerHTML = html;
            })
            .catch(error => console.error('Error cargando carga de trabajo:', error));
        }
        
        function cargarGraficoTendencias() {
            fetch('/api/dashboard/tendencias')
            .then(response => response.json())
            .then(data => {
                const ctx = document.getElementById('chartTendencias').getContext('2d');
                
                chartTendencias = new Chart(ctx, {
                    type: 'line',
                    data: {
                        labels: data.map(item => item.mes),
                        datasets: [
                            {
                                label: 'Tareas Terminadas',
                                data: data.map(item => item.terminadas),
                                borderColor: '#28a745',
                                backgroundColor: 'rgba(40, 167, 69, 0.2)',
                                fill: true,
                                tension: 0.4
                            },
                            {
                                label: 'Tareas Iniciadas',
                                data: data.map(item => item.iniciadas),
                                borderColor: '#007bff',
                                backgroundColor: 'rgba(0, 123, 255, 0.2)',
                                fill: false,
                                tension: 0.4
                            }
                        ]
                    },
                    options: {
                        responsive: true,
                        plugins: {
                            legend: {
                                position: 'top',
                            },
                            tooltip: {
                                mode: 'index',
                                intersect: false,
                            }
                        },
                        scales: {
                            y: {
                                beginAtZero: true,
                                ticks: {
                                    stepSize: 1
                                }
                            }
                        },
                        interaction: {
                            mode: 'nearest',
                            axis: 'x',
                            intersect: false
                        }
                    }
                });
            })
            .catch(error => console.error('Error cargando tendencias:', error));
        }
        
        function cargarGraficoTipos() {
            fetch('/api/dashboard/tipos-tareas')
            .then(response => response.json())
            .then(data => {
                const ctx = document.getElementById('chartTipos').getContext('2d');
                
                chartTipos = new Chart(ctx, {
                    type: 'doughnut',
                    data: {
                        labels: data.map(item => item.categoria),
                        datasets: [{
                            data: data.map(item => item.total),
                            backgroundColor: [
                                '#FF6384',  // Marketing
                                '#36A2EB',  // Desarrollo
                                '#FFCE56',  // Redes Sociales
                                '#4BC0C0'   // Otros
                            ],
                            borderWidth: 2,
                            borderColor: '#fff'
                        }]
                    },
                    options: {
                        responsive: true,
                        plugins: {
                            legend: {
                                position: 'bottom',
                                labels: {
                                    padding: 15,
                                    usePointStyle: true
                                }
                            },
                            tooltip: {
                                callbacks: {
                                    label: function(context) {
                                        const item = data[context.dataIndex];
                                        return `${context.label}: ${item.total} tareas (${item.completadas} completadas, ${item.en_curso} en curso, ${item.pendientes} pendientes)`;
                                    }
                                }
                            }
                        }
                    }
                });
            })
            .catch(error => console.error('Error cargando tipos de tareas:', error));
        }
        
        function cargarGraficoComparativo() {
            fetch('/api/dashboard/productividad')
            .then(response => response.json())
            .then(data => {
                const ctx = document.getElementById('chartComparativo').getContext('2d');
                
                chartComparativo = new Chart(ctx, {
                    type: 'bar',
                    data: {
                        labels: data.map(item => item.colaborador),
                        datasets: [
                            {
                                label: 'Completadas',
                                data: data.map(item => item.completadas),
                                backgroundColor: '#28a745',
                                borderColor: '#1e7e34',
                                borderWidth: 2
                            },
                            {
                                label: 'En Curso/Pendientes',
                                data: data.map(item => item.pendientes),
                                backgroundColor: '#ffc107',
                                borderColor: '#d39e00',
                                borderWidth: 2
                            }
                        ]
                    },
                    options: {
                        responsive: true,
                        plugins: {
                            legend: {
                                position: 'top',
                                labels: {
                                    usePointStyle: true,
                                    padding: 20
                                }
                            },
                            tooltip: {
                                mode: 'index',
                                intersect: false
                            }
                        },
                        scales: {
                            x: {
                                stacked: false
                            },
                            y: {
                                beginAtZero: true,
                                ticks: {
                                    stepSize: 1
                                }
                            }
                        },
                        interaction: {
                            mode: 'nearest',
                            axis: 'x',
                            intersect: false
                        }
                    }
                });
            })
            .catch(error => console.error('Error cargando gráfico comparativo:', error));
        }
        
        // Función para actualizar datos (se puede llamar periódicamente)
        function actualizarDashboard() {
            cargarMetricasPrincipales();
            
            // Destruir gráficos existentes antes de recrear
            if (chartEstados) chartEstados.destroy();
            if (chartColaboradores) chartColaboradores.destroy();
            if (chartComparativo) chartComparativo.destroy();
            if (chartTendencias) chartTendencias.destroy();
            if (chartTipos) chartTipos.destroy();
            
            cargarGraficoEstados();
            cargarGraficoColaboradores();
            cargarProductividadColaboradores();
            cargarCargaTrabajo();
            cargarGraficoTendencias();
            cargarGraficoTipos();
            cargarGraficoComparativo();
        }
        
        // Auto-actualizar cada 5 minutos
        setInterval(actualizarDashboard, 300000);
    </script>
</body>
</html>
'''

# Registrar blueprint
app.register_blueprint(dashboard_bp)
print("✅ Dashboard de Tareas con gráficos interactivos cargado")