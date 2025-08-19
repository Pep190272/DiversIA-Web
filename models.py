from app import db
from datetime import datetime

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    apellidos = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    fecha_nacimiento = db.Column(db.Date, nullable=True)
    telefono = db.Column(db.String(20), nullable=True)
    ciudad = db.Column(db.String(100), nullable=True)
    tipo_neurodivergencia = db.Column(db.String(50), nullable=False)
    diagnostico_formal = db.Column(db.Boolean, default=False)
    experiencia_laboral = db.Column(db.Text, nullable=True)
    formacion_academica = db.Column(db.Text, nullable=True)
    habilidades = db.Column(db.Text, nullable=True)
    intereses_laborales = db.Column(db.Text, nullable=True)
    adaptaciones_necesarias = db.Column(db.Text, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    # CRM export status
    exported_to_crm = db.Column(db.Boolean, default=False)
    crm_export_date = db.Column(db.DateTime, nullable=True)

    def __repr__(self):
        return f'<User {self.nombre} {self.apellidos}>'

class Company(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(200), nullable=False)
    email = db.Column(db.String(120), nullable=False)
    telefono = db.Column(db.String(20), nullable=True)
    sector = db.Column(db.String(100), nullable=True)
    tamano_empresa = db.Column(db.String(50), nullable=True)
    ciudad = db.Column(db.String(100), nullable=True)
    descripcion = db.Column(db.Text, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    # CRM export status
    exported_to_crm = db.Column(db.Boolean, default=False)
    crm_export_date = db.Column(db.DateTime, nullable=True)
    
    # Relationships
    job_offers = db.relationship('JobOffer', backref='company', lazy=True)

    def __repr__(self):
        return f'<Company {self.nombre}>'

class JobOffer(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    company_id = db.Column(db.Integer, db.ForeignKey('company.id'), nullable=False)
    titulo = db.Column(db.String(200), nullable=False)
    descripcion = db.Column(db.Text, nullable=False)
    ubicacion = db.Column(db.String(100), nullable=True)
    salario = db.Column(db.String(50), nullable=True)
    neurodivergencias_aceptadas = db.Column(db.String(200), nullable=True)
    activa = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    fecha_creacion = db.Column(db.DateTime, default=datetime.utcnow)
    # CRM export status
    exported_to_crm = db.Column(db.Boolean, default=False)
    crm_export_date = db.Column(db.DateTime, nullable=True)

    def __repr__(self):
        return f'<JobOffer {self.titulo}>'

class Asociacion(db.Model):
    """Modelo para asociaciones de neurodiversidad"""
    id = db.Column(db.Integer, primary_key=True)
    nombre_asociacion = db.Column(db.String(200), nullable=False)
    acronimo = db.Column(db.String(20), nullable=True)
    pais = db.Column(db.String(10), nullable=False)
    otro_pais = db.Column(db.String(100), nullable=True)
    
    # Información legal
    tipo_documento = db.Column(db.String(100), nullable=False)
    numero_documento = db.Column(db.String(50), nullable=False)
    descripcion_otro_documento = db.Column(db.String(200), nullable=True)
    
    # Información de la asociación
    neurodivergencias_atendidas = db.Column(db.Text, nullable=False)  # JSON string
    servicios = db.Column(db.Text, nullable=False)  # JSON string
    ciudad = db.Column(db.String(100), nullable=False)
    direccion = db.Column(db.String(200), nullable=True)
    telefono = db.Column(db.String(20), nullable=False)
    email = db.Column(db.String(100), nullable=False)
    sitio_web = db.Column(db.String(200), nullable=True)
    descripcion = db.Column(db.Text, nullable=False)
    
    # Información operativa
    años_funcionamiento = db.Column(db.String(20), nullable=False)
    numero_socios = db.Column(db.String(20), nullable=False)
    certificaciones = db.Column(db.Text, nullable=True)  # JSON string
    
    # Contacto
    contacto_nombre = db.Column(db.String(100), nullable=False)
    contacto_cargo = db.Column(db.String(100), nullable=False)
    
    # Estado y verificación
    estado = db.Column(db.String(20), default='pendiente')  # pendiente, verificada, rechazada
    fecha_solicitud = db.Column(db.DateTime, default=db.func.current_timestamp())
    fecha_verificacion = db.Column(db.DateTime, nullable=True)
    notas_verificacion = db.Column(db.Text, nullable=True)
    
    # Campos de auditoría
    ip_solicitud = db.Column(db.String(45), nullable=True)
    user_agent = db.Column(db.String(500), nullable=True)
    
    def __repr__(self):
        return f'<Asociacion {self.nombre_asociacion}>'
    
    def to_dict(self):
        """Convierte el objeto a diccionario para JSON"""
        import json
        return {
            'id': self.id,
            'nombre_asociacion': self.nombre_asociacion,
            'acronimo': self.acronimo,
            'pais': self.pais,
            'ciudad': self.ciudad,
            'neurodivergencias_atendidas': json.loads(self.neurodivergencias_atendidas) if self.neurodivergencias_atendidas else [],
            'servicios': json.loads(self.servicios) if self.servicios else [],
            'telefono': self.telefono,
            'email': self.email,
            'sitio_web': self.sitio_web,
            'descripcion': self.descripcion,
            'estado': self.estado,
            'fecha_solicitud': self.fecha_solicitud.isoformat() if self.fecha_solicitud else None
        }

class TestResult(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    test_type = db.Column(db.String(50), nullable=False)
    score = db.Column(db.Integer, nullable=True)
    results_data = db.Column(db.JSON, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f'<TestResult {self.test_type} for User {self.user_id}>'
    completed_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationships
    user = db.relationship('User', backref=db.backref('test_results', lazy=True))

    def __repr__(self):
        return f'<TestResult {self.test_type} for User {self.user_id}>'

class CRMExportLog(db.Model):
    """Log table to track all CRM exports for audit purposes"""
    id = db.Column(db.Integer, primary_key=True)
    record_type = db.Column(db.String(50), nullable=False)  # 'user', 'company', 'job_offer'
    record_id = db.Column(db.Integer, nullable=False)
    export_status = db.Column(db.String(20), nullable=False)  # 'success', 'failed', 'pending'
    export_method = db.Column(db.String(50), nullable=False)  # 'api', 'csv', 'json'
    error_message = db.Column(db.Text, nullable=True)
    exported_at = db.Column(db.DateTime, default=datetime.utcnow)
    exported_by = db.Column(db.String(100), nullable=True)  # system user or admin

    def __repr__(self):
        return f'<CRMExport {self.record_type}:{self.record_id} - {self.export_status}>'

class Association(db.Model):
    """Table for neurodivergent-related associations directory"""
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(200), nullable=False)
    tipo_neurodivergencia = db.Column(db.String(50), nullable=False)  # tdah, tea, dislexia, general
    ubicacion = db.Column(db.String(100), nullable=False)
    descripcion = db.Column(db.Text, nullable=True)
    servicios = db.Column(db.String(500), nullable=True)  # comma-separated services
    sitio_web = db.Column(db.String(200), nullable=True)
    email_contacto = db.Column(db.String(120), nullable=True)
    telefono = db.Column(db.String(20), nullable=True)
    activa = db.Column(db.Boolean, default=True)
    verified = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def __repr__(self):
        return f'<Association {self.nombre}>'