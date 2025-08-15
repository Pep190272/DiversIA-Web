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