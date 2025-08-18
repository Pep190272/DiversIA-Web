from flask_wtf import FlaskForm
from wtforms import StringField, EmailField, TextAreaField, DateField, TelField, SelectField, BooleanField, IntegerField, SelectMultipleField
from wtforms.validators import DataRequired, Email, Length, Optional, NumberRange
from wtforms.widgets import CheckboxInput, ListWidget

class MultiCheckboxField(SelectMultipleField):
    widget = ListWidget(prefix_label=False)
    option_widget = CheckboxInput()

class RegistroGeneralForm(FlaskForm):
    nombre = StringField('Nombre', validators=[DataRequired(), Length(min=2, max=100)])
    apellidos = StringField('Apellidos', validators=[DataRequired(), Length(min=2, max=100)])
    email = EmailField('Email', validators=[DataRequired(), Email()])
    fecha_nacimiento = DateField('Fecha de nacimiento', validators=[DataRequired()])
    telefono = TelField('Teléfono', validators=[Optional(), Length(max=20)])
    ciudad = StringField('Ciudad', validators=[Optional(), Length(max=100)])
    
    tipo_neurodivergencia = SelectField('Tipo de neurodivergencia', 
                                      choices=[
                                          ('', 'Selecciona una opción'),
                                          ('tdah', 'TDAH'),
                                          ('tea', 'TEA (Trastorno del Espectro Autista)'),
                                          ('dislexia', 'Dislexia'),
                                          ('discalculia', 'Discalculia'),
                                          ('tourette', 'Síndrome de Tourette'),
                                          ('dispraxia', 'Dispraxia'),
                                          ('ansiedad', 'Trastornos de Ansiedad'),
                                          ('bipolar', 'Trastorno Bipolar'),
                                          ('altas_capacidades', 'Altas Capacidades'),
                                          ('otro', 'Otro')
                                      ], validators=[DataRequired()])
    
    diagnostico_formal = BooleanField('¿Tienes diagnóstico formal?')
    experiencia_laboral = TextAreaField('Experiencia laboral', validators=[Optional()])
    formacion_academica = TextAreaField('Formación académica', validators=[Optional()])
    habilidades = TextAreaField('Habilidades y fortalezas', validators=[Optional()])
    intereses_laborales = TextAreaField('Intereses laborales', validators=[Optional()])
    adaptaciones_necesarias = TextAreaField('Adaptaciones necesarias en el trabajo', validators=[Optional()])
    aceptar_privacidad = BooleanField('He leído y acepto la Política de Privacidad', validators=[DataRequired()])

class RegistroTDAHForm(RegistroGeneralForm):
    # Campos específicos para TDAH
    nivel_atencion = SelectField('Nivel de atención sostenida', 
                               choices=[('', 'Selecciona'), ('bajo', 'Bajo'), ('medio', 'Medio'), ('alto', 'Alto')])
    impulsividad = SelectField('Nivel de impulsividad', 
                             choices=[('', 'Selecciona'), ('bajo', 'Bajo'), ('medio', 'Medio'), ('alto', 'Alto')])
    hiperactividad = SelectField('Nivel de hiperactividad', 
                               choices=[('', 'Selecciona'), ('bajo', 'Bajo'), ('medio', 'Medio'), ('alto', 'Alto')])
    medicacion_actual = BooleanField('¿Tomas medicación actualmente?')
    estrategias_organizacion = TextAreaField('Estrategias de organización que utilizas')
    aceptar_privacidad = BooleanField('He leído y acepto la Política de Privacidad', validators=[DataRequired()])

class RegistroDislexiaForm(RegistroGeneralForm):
    # Campos específicos para Dislexia
    dificultades_lectura = MultiCheckboxField('Dificultades de lectura',
                                            choices=[('velocidad', 'Velocidad de lectura'),
                                                   ('comprension', 'Comprensión lectora'),
                                                   ('pronunciacion', 'Pronunciación'),
                                                   ('ortografia', 'Ortografía')])
    herramientas_apoyo = MultiCheckboxField('Herramientas de apoyo que utilizas',
                                          choices=[('text_to_speech', 'Texto a voz'),
                                                 ('corrector', 'Corrector ortográfico'),
                                                 ('organizadores', 'Organizadores gráficos'),
                                                 ('tiempo_extra', 'Tiempo extra para tareas')])
    aceptar_privacidad = BooleanField('He leído y acepto la Política de Privacidad', validators=[DataRequired()])

class RegistroTEAForm(RegistroGeneralForm):
    # Campos específicos para TEA
    nivel_comunicacion = SelectField('Nivel de comunicación social',
                                   choices=[('', 'Selecciona'), ('bajo', 'Necesita apoyo'),
                                          ('medio', 'Comunicación funcional'), ('alto', 'Comunicación fluida')])
    sensibilidades_sensoriales = MultiCheckboxField('Sensibilidades sensoriales',
                                                   choices=[('auditiva', 'Auditiva'), ('visual', 'Visual'),
                                                          ('tactil', 'Táctil'), ('olfativa', 'Olfativa')])
    rutinas_importantes = BooleanField('¿Son importantes las rutinas para ti?')
    intereses_especiales = TextAreaField('Intereses especiales o áreas de expertise')
    aceptar_privacidad = BooleanField('He leído y acepto la Política de Privacidad', validators=[DataRequired()])

class RegistroDiscalculiaForm(RegistroGeneralForm):
    # Campos específicos para Discalculia
    dificultades_matematicas = MultiCheckboxField('Dificultades matemáticas',
                                                choices=[('calculo_basico', 'Cálculo básico'),
                                                       ('numeros_grandes', 'Números grandes'),
                                                       ('tiempo_dinero', 'Tiempo y dinero'),
                                                       ('geometria', 'Geometría')])
    herramientas_calculo = MultiCheckboxField('Herramientas de apoyo',
                                            choices=[('calculadora', 'Calculadora'),
                                                   ('apps_matematicas', 'Apps matemáticas'),
                                                   ('tiempo_extra', 'Tiempo extra'),
                                                   ('explicaciones_visuales', 'Explicaciones visuales')])
    aceptar_privacidad = BooleanField('He leído y acepto la Política de Privacidad', validators=[DataRequired()])

class RegistroTouretteForm(RegistroGeneralForm):
    # Campos específicos para Síndrome de Tourette
    tipos_tics = MultiCheckboxField('Tipos de tics',
                                  choices=[('motores', 'Tics motores'),
                                         ('vocales', 'Tics vocales'),
                                         ('complejos', 'Tics complejos')])
    frecuencia_tics = SelectField('Frecuencia de tics',
                                choices=[('', 'Selecciona'), ('baja', 'Ocasionales'),
                                       ('media', 'Moderados'), ('alta', 'Frecuentes')])
    medicacion_tics = BooleanField('¿Tomas medicación para los tics?')
    estrategias_control = TextAreaField('Estrategias para controlar los tics')
    aceptar_privacidad = BooleanField('He leído y acepto la Política de Privacidad', validators=[DataRequired()])

class RegistroDispraxiaForm(RegistroGeneralForm):
    # Campos específicos para Dispraxia
    dificultades_coordinacion = MultiCheckboxField('Dificultades de coordinación',
                                                 choices=[('motora_gruesa', 'Motora gruesa'),
                                                        ('motora_fina', 'Motora fina'),
                                                        ('planificacion_movimiento', 'Planificación del movimiento'),
                                                        ('equilibrio', 'Equilibrio')])
    herramientas_organizacion = MultiCheckboxField('Herramientas de organización',
                                                 choices=[('agenda_visual', 'Agenda visual'),
                                                        ('recordatorios', 'Recordatorios'),
                                                        ('rutinas_estructuradas', 'Rutinas estructuradas')])
    aceptar_privacidad = BooleanField('He leído y acepto la Política de Privacidad', validators=[DataRequired()])

class RegistroAnsiedadForm(RegistroGeneralForm):
    # Campos específicos para Trastornos de Ansiedad
    tipo_ansiedad = MultiCheckboxField('Tipo de ansiedad',
                                     choices=[('generalizada', 'Ansiedad generalizada'),
                                            ('social', 'Ansiedad social'),
                                            ('panico', 'Trastorno de pánico'),
                                            ('especifica', 'Fobia específica')])
    tecnicas_manejo = MultiCheckboxField('Técnicas de manejo',
                                       choices=[('respiracion', 'Técnicas de respiración'),
                                              ('mindfulness', 'Mindfulness'),
                                              ('terapia', 'Terapia psicológica'),
                                              ('medicacion', 'Medicación')])
    desencadenantes_laborales = TextAreaField('Desencadenantes en el ambiente laboral')
    aceptar_privacidad = BooleanField('He leído y acepto la Política de Privacidad', validators=[DataRequired()])

class RegistroBipolarForm(RegistroGeneralForm):
    # Campos específicos para Trastorno Bipolar
    tipo_bipolar = SelectField('Tipo de trastorno bipolar',
                             choices=[('', 'Selecciona'), ('tipo1', 'Tipo I'),
                                    ('tipo2', 'Tipo II'), ('ciclotimia', 'Ciclotimia')])
    estabilidad_actual = SelectField('Estabilidad actual',
                                   choices=[('', 'Selecciona'), ('estable', 'Estable'),
                                          ('episodio_leve', 'Episodio leve'),
                                          ('en_tratamiento', 'En tratamiento activo')])
    medicacion_estabilizador = BooleanField('¿Tomas estabilizadores del ánimo?')
    apoyo_terapeutico = BooleanField('¿Tienes apoyo terapéutico regular?')
    aceptar_privacidad = BooleanField('He leído y acepto la Política de Privacidad', validators=[DataRequired()])

class RegistroAltasCapacidadesForm(RegistroGeneralForm):
    # Campos específicos para Altas Capacidades
    area_talento = MultiCheckboxField('Áreas de talento',
                                    choices=[('matematicas', 'Matemáticas'),
                                           ('linguisticas', 'Lingüísticas'),
                                           ('artisticas', 'Artísticas'),
                                           ('cientificas', 'Científicas'),
                                           ('tecnologicas', 'Tecnológicas')])
    nivel_ci = SelectField('Nivel de CI (si conoces)',
                         choices=[('', 'No lo conozco'), ('130-145', '130-145'),
                                ('145-160', '145-160'), ('160+', '160+')])
    desafios_sociales = BooleanField('¿Has experimentado desafíos sociales por tus altas capacidades?')
    necesidades_estimulo = TextAreaField('Necesidades de estímulo intelectual')
    aceptar_privacidad = BooleanField('He leído y acepto la Política de Privacidad', validators=[DataRequired()])

class EmpresaRegistroForm(FlaskForm):
    nombre_empresa = StringField('Nombre de la empresa', validators=[DataRequired(), Length(min=2, max=200)])
    email_contacto = EmailField('Email de contacto', validators=[DataRequired(), Email()])
    telefono = TelField('Teléfono', validators=[Optional(), Length(max=20)])
    sector = StringField('Sector', validators=[Optional(), Length(max=100)])
    tamano_empresa = SelectField('Tamaño de la empresa',
                               choices=[('', 'Selecciona'),
                                      ('startup', 'Startup (1-10 empleados)'),
                                      ('pequena', 'Pequeña (11-50 empleados)'),
                                      ('mediana', 'Mediana (51-250 empleados)'),
                                      ('grande', 'Grande (250+ empleados)')])
    ciudad = StringField('Ciudad', validators=[Optional(), Length(max=100)])
    aceptar_privacidad = BooleanField('He leído y acepto la Política de Privacidad', validators=[DataRequired()])

class OfertaEmpleoForm(FlaskForm):
    titulo_puesto = StringField('Título del puesto', validators=[DataRequired(), Length(min=2, max=200)])
    descripcion = TextAreaField('Descripción del puesto', validators=[DataRequired()])
    tipo_contrato = SelectField('Tipo de contrato',
                              choices=[('', 'Selecciona'),
                                     ('indefinido', 'Indefinido'),
                                     ('temporal', 'Temporal'),
                                     ('practicas', 'Prácticas'),
                                     ('freelance', 'Freelance')])
    modalidad_trabajo = SelectField('Modalidad de trabajo',
                                  choices=[('', 'Selecciona'),
                                         ('presencial', 'Presencial'),
                                         ('remoto', 'Remoto'),
                                         ('hibrido', 'Híbrido')])
    salario_min = IntegerField('Salario mínimo (€)', validators=[Optional(), NumberRange(min=0)])
    salario_max = IntegerField('Salario máximo (€)', validators=[Optional(), NumberRange(min=0)])
    requisitos = TextAreaField('Requisitos del puesto')
    adaptaciones_disponibles = TextAreaField('Adaptaciones disponibles')
    neurodivergencias_target = MultiCheckboxField('Neurodivergencias objetivo',
                                                choices=[('tdah', 'TDAH'),
                                                       ('tea', 'TEA'),
                                                       ('dislexia', 'Dislexia'),
                                                       ('discalculia', 'Discalculia'),
                                                       ('tourette', 'Síndrome de Tourette'),
                                                       ('dispraxia', 'Dispraxia'),
                                                       ('ansiedad', 'Trastornos de Ansiedad'),
                                                       ('bipolar', 'Trastorno Bipolar'),
                                                       ('altas_capacidades', 'Altas Capacidades'),
                                                       ('todas', 'Todas')])
    aceptar_privacidad = BooleanField('He leído y acepto la Política de Privacidad', validators=[DataRequired()])
