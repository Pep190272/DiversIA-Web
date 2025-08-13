from app import db
from datetime import datetime

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    nombre = db.Column(db.String(100), nullable=False)
    apellidos = db.Column(db.String(100), nullable=False)
    fecha_nacimiento = db.Column(db.Date)
    telefono = db.Column(db.String(20))
    ciudad = db.Column(db.String(100))
    tipo_neurodivergencia = db.Column(db.String(50))
    diagnostico_formal = db.Column(db.Boolean, default=False)
    experiencia_laboral = db.Column(db.Text)
    formacion_academica = db.Column(db.Text)
    habilidades = db.Column(db.Text)
    intereses_laborales = db.Column(db.Text)
    adaptaciones_necesarias = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
class Company(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre_empresa = db.Column(db.String(200), nullable=False)
    email_contacto = db.Column(db.String(120), nullable=False)
    telefono = db.Column(db.String(20))
    sector = db.Column(db.String(100))
    tamano_empresa = db.Column(db.String(50))
    ciudad = db.Column(db.String(100))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class JobOffer(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    company_id = db.Column(db.Integer, db.ForeignKey('company.id'), nullable=False)
    titulo_puesto = db.Column(db.String(200), nullable=False)
    descripcion = db.Column(db.Text, nullable=False)
    tipo_contrato = db.Column(db.String(50))
    modalidad_trabajo = db.Column(db.String(50))
    salario_min = db.Column(db.Integer)
    salario_max = db.Column(db.Integer)
    requisitos = db.Column(db.Text)
    adaptaciones_disponibles = db.Column(db.Text)
    neurodivergencias_target = db.Column(db.String(200))
    activa = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    company = db.relationship('Company', backref=db.backref('job_offers', lazy=True))

class TestResult(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    tipo_test = db.Column(db.String(50), nullable=False)
    resultados = db.Column(db.Text)
    puntuacion = db.Column(db.Integer)
    recomendaciones = db.Column(db.Text)
    completed_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    user = db.relationship('User', backref=db.backref('test_results', lazy=True))
