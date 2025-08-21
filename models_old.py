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

# ============ MODELOS ADICIONALES PARA CRM COMPLETO ============

class CrmContact(db.Model):
    """Contactos adicionales del CRM (no usuarios web)"""
    __tablename__ = 'crm_contacts'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    email = db.Column(db.String(120), nullable=True)
    phone = db.Column(db.String(20), nullable=True)
    company = db.Column(db.String(200), nullable=True)
    position = db.Column(db.String(100), nullable=True)
    contact_type = db.Column(db.String(50), nullable=False)  # 'partner', 'provider', 'media', 'investor'
    source = db.Column(db.String(100), nullable=True)  # Dónde se obtuvo el contacto
    notes = db.Column(db.Text, nullable=True)
    tags = db.Column(db.String(500), nullable=True)  # Etiquetas separadas por comas
    last_contact = db.Column(db.DateTime, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    created_by = db.Column(db.Integer, nullable=True)  # ID del admin que lo creó

    def __repr__(self):
        return f'<CrmContact {self.name}>'

class FormSubmission(db.Model):
    """Registro de todas las submisiones de formularios"""
    __tablename__ = 'form_submissions'
    id = db.Column(db.Integer, primary_key=True)
    form_type = db.Column(db.String(50), nullable=False)  # 'contact', 'user_registration', 'company_registration'
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=True)
    company_id = db.Column(db.Integer, db.ForeignKey('company.id'), nullable=True)
    form_data = db.Column(db.Text, nullable=False)  # JSON con todos los datos del formulario
    ip_address = db.Column(db.String(45), nullable=True)
    user_agent = db.Column(db.String(500), nullable=True)
    processed = db.Column(db.Boolean, default=False)
    processed_at = db.Column(db.DateTime, nullable=True)
    processed_by = db.Column(db.Integer, nullable=True)  # ID del admin que lo procesó
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f'<FormSubmission {self.form_type} - {self.id}>'

class Partner(db.Model):
    """Partners y colaboradores"""
    __tablename__ = 'partners'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    company = db.Column(db.String(200), nullable=True)
    partnership_type = db.Column(db.String(100), nullable=False)  # 'strategic', 'technology', 'content', 'funding'
    contact_email = db.Column(db.String(120), nullable=True)
    contact_phone = db.Column(db.String(20), nullable=True)
    website = db.Column(db.String(300), nullable=True)
    description = db.Column(db.Text, nullable=True)
    contract_start = db.Column(db.Date, nullable=True)
    contract_end = db.Column(db.Date, nullable=True)
    status = db.Column(db.String(50), default='active')  # 'active', 'inactive', 'pending', 'terminated'
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f'<Partner {self.name}>'

class SocialMediaAccount(db.Model):
    """Cuentas de redes sociales"""
    __tablename__ = 'social_media_accounts'
    id = db.Column(db.Integer, primary_key=True)
    platform = db.Column(db.String(50), nullable=False)  # 'instagram', 'linkedin', 'discord', 'telegram', 'twitter'
    username = db.Column(db.String(100), nullable=False)
    url = db.Column(db.String(300), nullable=False)
    followers_count = db.Column(db.Integer, default=0)
    engagement_rate = db.Column(db.Float, default=0.0)
    last_updated = db.Column(db.DateTime, default=datetime.utcnow)
    is_active = db.Column(db.Boolean, default=True)
    managed_by = db.Column(db.String(100), nullable=True)  # Quién gestiona la cuenta
    notes = db.Column(db.Text, nullable=True)

    def __repr__(self):
        return f'<SocialMedia {self.platform} - {self.username}>'

class Task(db.Model):
    """Sistema de tareas y seguimiento"""
    __tablename__ = 'tasks'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text, nullable=True)
    priority = db.Column(db.String(20), default='medium')  # 'low', 'medium', 'high', 'urgent'
    status = db.Column(db.String(20), default='pending')  # 'pending', 'in_progress', 'completed', 'cancelled'
    category = db.Column(db.String(50), nullable=True)  # 'development', 'marketing', 'content', 'admin'
    assigned_to = db.Column(db.String(100), nullable=True)
    due_date = db.Column(db.DateTime, nullable=True)
    completed_at = db.Column(db.DateTime, nullable=True)
    created_by = db.Column(db.Integer, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f'<Task {self.title}>'

class Metric(db.Model):
    """Métricas y KPIs del negocio"""
    __tablename__ = 'metrics'
    id = db.Column(db.Integer, primary_key=True)
    metric_name = db.Column(db.String(100), nullable=False)
    metric_value = db.Column(db.Float, nullable=False)
    metric_type = db.Column(db.String(50), nullable=False)  # 'users', 'revenue', 'engagement', 'conversion'
    date_recorded = db.Column(db.Date, nullable=False)
    source = db.Column(db.String(100), nullable=True)  # Fuente de la métrica
    notes = db.Column(db.Text, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f'<Metric {self.metric_name}: {self.metric_value}>'

# ============ SISTEMA DE EMPLEADOS Y GESTIÓN AVANZADA ============

class Employee(db.Model):
    """Empleados de DiversIA"""
    __tablename__ = 'employees'
    id = db.Column(db.Integer, primary_key=True)
    admin_id = db.Column(db.Integer, db.ForeignKey('admin.id'), nullable=True)  # Relación con sistema admin
    first_name = db.Column(db.String(100), nullable=False)
    last_name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    phone = db.Column(db.String(20), nullable=True)
    position = db.Column(db.String(100), nullable=False)
    department = db.Column(db.String(100), nullable=True)
    hire_date = db.Column(db.Date, nullable=False)
    salary = db.Column(db.Float, nullable=True)
    is_active = db.Column(db.Boolean, default=True)
    role = db.Column(db.String(50), default='empleado')  # 'admin', 'colaborador', 'empleado'
    skills = db.Column(db.Text, nullable=True)  # JSON con habilidades
    notes = db.Column(db.Text, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relaciones
    tasks = db.relationship('EmployeeTask', back_populates='assigned_employee', lazy=True)

    def __repr__(self):
        return f'<Employee {self.first_name} {self.last_name}>'

    def get_full_name(self):
        return f"{self.first_name} {self.last_name}"

class EmployeeTask(db.Model):
    """Tareas asignadas a empleados"""
    __tablename__ = 'employee_tasks'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text, nullable=True)
    priority = db.Column(db.String(20), default='medium')  # 'low', 'medium', 'high', 'urgent'
    status = db.Column(db.String(20), default='pending')  # 'pending', 'in_progress', 'completed', 'cancelled'
    category = db.Column(db.String(50), nullable=True)  # 'development', 'marketing', 'content', 'admin', 'research'
    
    # Asignación
    assigned_to_id = db.Column(db.Integer, db.ForeignKey('employees.id'), nullable=False)
    assigned_by_id = db.Column(db.Integer, db.ForeignKey('admin.id'), nullable=True)
    
    # Tiempo
    estimated_hours = db.Column(db.Float, nullable=True)
    actual_hours = db.Column(db.Float, nullable=True)
    due_date = db.Column(db.DateTime, nullable=True)
    started_at = db.Column(db.DateTime, nullable=True)
    completed_at = db.Column(db.DateTime, nullable=True)
    
    # Metadata
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relaciones
    assigned_employee = db.relationship('Employee', back_populates='tasks')

    def __repr__(self):
        return f'<EmployeeTask {self.title}>'

    def get_progress_percentage(self):
        if self.status == 'completed':
            return 100
        elif self.status == 'in_progress':
            return 50
        else:
            return 0

class UserInvitation(db.Model):
    """Invitaciones de usuarios al sistema"""
    __tablename__ = 'user_invitations'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), nullable=False)
    invited_by_id = db.Column(db.Integer, db.ForeignKey('admin.id'), nullable=False)
    role = db.Column(db.String(50), nullable=False)  # 'colaborador', 'empleado'
    invitation_token = db.Column(db.String(255), unique=True, nullable=False)
    expires_at = db.Column(db.DateTime, nullable=False)
    is_used = db.Column(db.Boolean, default=False)
    used_at = db.Column(db.DateTime, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Datos adicionales para el empleado
    first_name = db.Column(db.String(100), nullable=True)
    last_name = db.Column(db.String(100), nullable=True)
    position = db.Column(db.String(100), nullable=True)
    department = db.Column(db.String(100), nullable=True)

    def __repr__(self):
        return f'<UserInvitation {self.email} - {self.role}>'

    def is_expired(self):
        return datetime.utcnow() > self.expires_at

class TimeTracking(db.Model):
    """Seguimiento de tiempo trabajado"""
    __tablename__ = 'time_tracking'
    id = db.Column(db.Integer, primary_key=True)
    employee_id = db.Column(db.Integer, db.ForeignKey('employees.id'), nullable=False)
    task_id = db.Column(db.Integer, db.ForeignKey('employee_tasks.id'), nullable=True)
    start_time = db.Column(db.DateTime, nullable=False)
    end_time = db.Column(db.DateTime, nullable=True)
    duration_minutes = db.Column(db.Integer, nullable=True)
    description = db.Column(db.Text, nullable=True)
    date_worked = db.Column(db.Date, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f'<TimeTracking {self.employee_id} - {self.date_worked}>'