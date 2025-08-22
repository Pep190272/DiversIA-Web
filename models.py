from datetime import datetime
from app import db
from werkzeug.security import generate_password_hash, check_password_hash

# Modelos principales para DiversIA
class User(db.Model):
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    apellidos = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False, index=True)
    telefono = db.Column(db.String(20), nullable=True)
    ciudad = db.Column(db.String(100), nullable=False)
    fecha_nacimiento = db.Column(db.Date, nullable=False)
    
    # Información de neurodivergencia
    tipo_neurodivergencia = db.Column(db.String(50), nullable=False)
    diagnostico_formal = db.Column(db.Boolean, default=False)
    
    # Información laboral
    habilidades = db.Column(db.Text, nullable=True)
    experiencia_laboral = db.Column(db.Text, nullable=True)
    formacion_academica = db.Column(db.Text, nullable=True)
    intereses_laborales = db.Column(db.Text, nullable=True)
    adaptaciones_necesarias = db.Column(db.Text, nullable=True)
    motivaciones = db.Column(db.Text, nullable=True)
    
    # Campos específicos TDAH
    tipo_tdah = db.Column(db.String(20), nullable=True)
    nivel_atencion = db.Column(db.String(10), nullable=True)
    impulsividad = db.Column(db.String(10), nullable=True)
    hiperactividad = db.Column(db.String(10), nullable=True)
    medicacion = db.Column(db.Boolean, default=False)
    
    # Campos específicos TEA
    nivel_comunicacion = db.Column(db.String(10), nullable=True)
    sensibilidades = db.Column(db.Text, nullable=True)
    rutinas_importantes = db.Column(db.Text, nullable=True)
    
    # Campos específicos Dislexia
    areas_dificultad = db.Column(db.String(100), nullable=True)
    herramientas_apoyo = db.Column(db.Text, nullable=True)
    
    # Timestamps
    created_at = db.Column(db.DateTime, default=datetime.utcnow, index=True)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def __repr__(self):
        return f'<User {self.nombre} {self.apellidos}>'

class Company(db.Model):
    __tablename__ = 'companies'
    
    id = db.Column(db.Integer, primary_key=True)
    nombre_empresa = db.Column(db.String(200), nullable=False)
    email_contacto = db.Column(db.String(120), nullable=False, index=True)
    telefono = db.Column(db.String(20), nullable=True)
    sector = db.Column(db.String(100), nullable=False)
    tamano_empresa = db.Column(db.String(50), nullable=False)
    ciudad = db.Column(db.String(100), nullable=False)
    sitio_web = db.Column(db.String(200), nullable=True)
    descripcion_empresa = db.Column(db.Text, nullable=True)
    
    # Información de inclusión
    experiencia_neurodivergentes = db.Column(db.Boolean, default=False)
    politicas_inclusion = db.Column(db.Text, nullable=True)
    adaptaciones_disponibles = db.Column(db.Text, nullable=True)
    
    # Timestamps
    created_at = db.Column(db.DateTime, default=datetime.utcnow, index=True)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relaciones
    job_offers = db.relationship('JobOffer', backref='company', lazy=True, cascade='all, delete-orphan')
    
    def __repr__(self):
        return f'<Company {self.nombre_empresa}>'

class JobOffer(db.Model):
    __tablename__ = 'job_offers'
    
    id = db.Column(db.Integer, primary_key=True)
    company_id = db.Column(db.Integer, db.ForeignKey('companies.id'), nullable=False)
    
    titulo_puesto = db.Column(db.String(200), nullable=False)
    descripcion = db.Column(db.Text, nullable=False)
    tipo_contrato = db.Column(db.String(50), nullable=False)
    modalidad_trabajo = db.Column(db.String(50), nullable=False)
    
    salario_min = db.Column(db.Integer, nullable=True)
    salario_max = db.Column(db.Integer, nullable=True)
    
    requisitos = db.Column(db.Text, nullable=True)
    adaptaciones_disponibles = db.Column(db.Text, nullable=True)
    neurodivergencias_target = db.Column(db.String(200), nullable=True)
    
    activa = db.Column(db.Boolean, default=True)
    
    # Timestamps
    created_at = db.Column(db.DateTime, default=datetime.utcnow, index=True)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def __repr__(self):
        return f'<JobOffer {self.titulo_puesto}>'

class TestResult(db.Model):
    __tablename__ = 'test_results'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    
    tipo_test = db.Column(db.String(50), nullable=False)  # 'neurocognitivo', 'matching', etc.
    puntuacion_total = db.Column(db.Integer, nullable=False)
    resultados_detalle = db.Column(db.Text, nullable=True)  # JSON string
    
    recomendaciones = db.Column(db.Text, nullable=True)
    
    # Timestamps
    created_at = db.Column(db.DateTime, default=datetime.utcnow, index=True)
    
    # Relaciones
    user = db.relationship('User', backref='test_results', lazy=True)
    
    def __repr__(self):
        return f'<TestResult {self.tipo_test} - User {self.user_id}>'

# Modelos para CRM Administrativo
class Admin(db.Model):
    __tablename__ = 'admins'
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(256), nullable=False)
    
    # Información adicional
    full_name = db.Column(db.String(150), nullable=True)
    active = db.Column(db.Boolean, default=True)
    
    # Timestamps
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    last_login = db.Column(db.DateTime, nullable=True)
    
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
    
    def __repr__(self):
        return f'<Admin {self.username}>'

class CrmContact(db.Model):
    __tablename__ = 'crm_contacts'
    
    id = db.Column(db.Integer, primary_key=True)
    
    # Información básica
    name = db.Column(db.String(150), nullable=False, index=True)
    email = db.Column(db.String(120), nullable=False, index=True)
    phone = db.Column(db.String(20), nullable=True)
    company = db.Column(db.String(200), nullable=True)
    
    # Información específica DiversIA
    neurodivergence = db.Column(db.String(50), nullable=True)
    contact_reason = db.Column(db.String(100), nullable=True)  # 'job_search', 'hiring', 'partnership'
    city = db.Column(db.String(100), nullable=True)
    
    # Estado del contacto
    status = db.Column(db.String(20), default='new')  # 'new', 'contacted', 'closed'
    notes = db.Column(db.Text, nullable=True)
    
    # Timestamps
    created_at = db.Column(db.DateTime, default=datetime.utcnow, index=True)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def __repr__(self):
        return f'<CrmContact {self.name}>'

# Modelo para Email Marketing de Asociaciones
class EmailMarketing(db.Model):
    __tablename__ = 'email_marketing'
    
    id = db.Column(db.Integer, primary_key=True)
    comunidad_autonoma = db.Column(db.String(100), nullable=False)
    asociacion = db.Column(db.String(200), nullable=False)
    email = db.Column(db.String(120), nullable=False)
    telefono = db.Column(db.String(20))
    direccion = db.Column(db.String(300))
    servicios = db.Column(db.Text)
    fecha_enviado = db.Column(db.String(20))  # Formato: 30/07/2025
    respuesta = db.Column(db.Text)  # Columna para respuestas del CSV
    notas_especiales = db.Column(db.Text)  # Para notas como "VACACIONES HASTA..."
    
    # Campos de seguimiento
    estado_email = db.Column(db.String(50), default='enviado')  # enviado, abierto, respondido, rebotado
    fecha_respuesta = db.Column(db.DateTime)
    tipo_respuesta = db.Column(db.String(100))  # interesado, no_interesado, info_solicitada
    seguimiento_programado = db.Column(db.DateTime)
    
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def __repr__(self):
        return f'<EmailMarketing {self.asociacion}>'

class Task(db.Model):
    __tablename__ = 'tasks'
    
    id = db.Column(db.Integer, primary_key=True)
    tarea = db.Column(db.String(300), nullable=False)
    colaborador = db.Column(db.String(100))
    fecha_inicio = db.Column(db.String(50))
    fecha_final = db.Column(db.String(50))
    estado = db.Column(db.String(50), default='Pendiente')  # Pendiente, En curso, Completado
    notas = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.now)
    updated_at = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now)
    
    def __repr__(self):
        return f'<Task {self.tarea[:50]}>'

# Modelos para formularios web
class FormSubmission(db.Model):
    __tablename__ = 'form_submissions'
    
    id = db.Column(db.Integer, primary_key=True)
    
    form_type = db.Column(db.String(50), nullable=False, index=True)  # 'contact', 'registration', 'company'
    data = db.Column(db.Text, nullable=False)  # JSON string con los datos del formulario
    
    # Información de origen
    ip_address = db.Column(db.String(45), nullable=True)
    user_agent = db.Column(db.String(200), nullable=True)
    
    # Estado
    processed = db.Column(db.Boolean, default=False)
    crm_id = db.Column(db.Integer, nullable=True)  # ID en el sistema CRM si se procesa
    
    # Timestamps
    created_at = db.Column(db.DateTime, default=datetime.utcnow, index=True)
    processed_at = db.Column(db.DateTime, nullable=True)
    
    def __repr__(self):
        return f'<FormSubmission {self.form_type} - {self.id}>'

class Employee(db.Model):
    __tablename__ = 'employees'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    rol = db.Column(db.String(100), nullable=False)  # Developer, Designer, Marketing, Manager, etc.
    department = db.Column(db.String(100), nullable=True)
    active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.now)
    updated_at = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now)
    
    def __repr__(self):
        return f'<Employee {self.name}>'
    
    def __repr__(self):
        return f'<Employee {self.name}>'

class Asociacion(db.Model):
    __tablename__ = 'asociaciones'
    
    id = db.Column(db.Integer, primary_key=True)
    
    # Información básica
    nombre_asociacion = db.Column(db.String(200), nullable=False)
    acronimo = db.Column(db.String(20), nullable=True)
    pais = db.Column(db.String(10), nullable=False)
    otro_pais = db.Column(db.String(100), nullable=True)
    
    # Información legal
    tipo_documento = db.Column(db.String(100), nullable=False)
    numero_documento = db.Column(db.String(50), nullable=False)
    descripcion_otro_documento = db.Column(db.Text, nullable=True)
    
    # Servicios y neurodivergencias (JSON strings)
    neurodivergencias_atendidas = db.Column(db.Text, nullable=True)
    servicios = db.Column(db.Text, nullable=True)
    certificaciones = db.Column(db.Text, nullable=True)
    
    # Información de contacto
    ciudad = db.Column(db.String(100), nullable=False)
    direccion = db.Column(db.Text, nullable=True)
    telefono = db.Column(db.String(20), nullable=True)
    email = db.Column(db.String(120), nullable=False)
    sitio_web = db.Column(db.String(200), nullable=True)
    descripcion = db.Column(db.Text, nullable=True)
    
    # Información operativa
    años_funcionamiento = db.Column(db.Integer, nullable=True)
    numero_socios = db.Column(db.Integer, nullable=True)
    
    # Contacto responsable
    contacto_nombre = db.Column(db.String(150), nullable=True)
    contacto_cargo = db.Column(db.String(100), nullable=True)
    
    # Información de auditoría
    ip_solicitud = db.Column(db.String(45), nullable=True)
    user_agent = db.Column(db.String(500), nullable=True)
    estado = db.Column(db.String(20), default='pendiente')
    
    # Timestamps
    created_at = db.Column(db.DateTime, default=datetime.utcnow, index=True)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def __repr__(self):
        return f'<Asociacion {self.nombre_asociacion}>'