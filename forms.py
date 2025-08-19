from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SelectField, BooleanField, DateField, SelectMultipleField, widgets
from wtforms.validators import DataRequired, Email, Length, Optional, URL
from wtforms.widgets import CheckboxInput, ListWidget

class MultiCheckboxField(SelectMultipleField):
    widget = ListWidget(prefix_label=False)
    option_widget = CheckboxInput()

# Formulario base para registro general
class RegistroGeneralForm(FlaskForm):
    nombre = StringField('Nombre', validators=[DataRequired(message='El nombre es obligatorio')])
    apellidos = StringField('Apellidos', validators=[DataRequired(message='Los apellidos son obligatorios')])
    email = StringField('Email', validators=[DataRequired(message='El email es obligatorio'), Email(message='Introduce un email válido')])
    fecha_nacimiento = DateField('Fecha de Nacimiento', validators=[DataRequired(message='La fecha de nacimiento es obligatoria')])
    telefono = StringField('Teléfono', validators=[Optional()])
    ciudad = StringField('Ciudad', validators=[DataRequired(message='La ciudad es obligatoria')])
    diagnostico_formal = BooleanField('¿Tienes un diagnóstico formal?')
    habilidades = TextAreaField('Habilidades y fortalezas', validators=[Optional()])
    adaptaciones_necesarias = TextAreaField('Adaptaciones que necesitas en el trabajo', validators=[Optional()])
    aceptar_privacidad = BooleanField('Acepto la política de privacidad', validators=[DataRequired(message='Debes aceptar la política de privacidad')])

# Formularios específicos por neurodivergencia
class RegistroTDAHForm(RegistroGeneralForm):
    tipo_tdah = SelectField('Tipo de TDAH', choices=[
        ('', 'Selecciona una opción'),
        ('inatento', 'Predominantemente inatento'),
        ('hiperactivo', 'Predominantemente hiperactivo-impulsivo'),
        ('combinado', 'Tipo combinado')
    ], validators=[Optional()])
    
    medicacion = BooleanField('¿Tomas medicación para el TDAH?')
    
    estrategias_concentracion = MultiCheckboxField('Estrategias que te ayudan a concentrarte', choices=[
        ('musica', 'Música de fondo'),
        ('descansos', 'Descansos frecuentes'),
        ('listas', 'Listas de tareas'),
        ('recordatorios', 'Recordatorios visuales'),
        ('ambiente_tranquilo', 'Ambiente tranquilo'),
        ('fidget', 'Objetos fidget'),
        ('otras', 'Otras estrategias')
    ])
    
    desafios_trabajo = MultiCheckboxField('Principales desafíos en el trabajo', choices=[
        ('concentracion', 'Mantener la concentración'),
        ('organizacion', 'Organización de tareas'),
        ('gestion_tiempo', 'Gestión del tiempo'),
        ('multitarea', 'Realizar múltiples tareas'),
        ('reuniones_largas', 'Reuniones largas'),
        ('ruido', 'Ambientes ruidosos'),
        ('interrupciones', 'Interrupciones constantes')
    ])

class RegistroTEAForm(RegistroGeneralForm):
    nivel_apoyo = SelectField('Nivel de apoyo necesario', choices=[
        ('', 'Selecciona una opción'),
        ('minimo', 'Apoyo mínimo'),
        ('sustancial', 'Apoyo sustancial'),
        ('muy_sustancial', 'Apoyo muy sustancial')
    ], validators=[Optional()])
    
    sensibilidades = MultiCheckboxField('Sensibilidades sensoriales', choices=[
        ('auditiva', 'Sensibilidad auditiva'),
        ('visual', 'Sensibilidad visual'),
        ('tactil', 'Sensibilidad táctil'),
        ('olfativa', 'Sensibilidad olfativa'),
        ('gustativa', 'Sensibilidad gustativa'),
        ('vestibular', 'Sensibilidad vestibular'),
        ('propioceptiva', 'Sensibilidad propioceptiva')
    ])
    
    comunicacion_preferida = SelectField('Forma de comunicación preferida', choices=[
        ('', 'Selecciona una opción'),
        ('verbal', 'Comunicación verbal directa'),
        ('escrita', 'Comunicación escrita'),
        ('visual', 'Apoyos visuales'),
        ('mixta', 'Combinación de varias formas')
    ], validators=[Optional()])
    
    intereses_especiales = TextAreaField('Intereses especiales o áreas de experticia', validators=[Optional()])

class RegistroDislexiaForm(RegistroGeneralForm):
    tipo_dislexia = SelectField('Tipo de dislexia', choices=[
        ('', 'Selecciona una opción'),
        ('fonologica', 'Dislexia fonológica'),
        ('superficial', 'Dislexia superficial'),
        ('mixta', 'Dislexia mixta'),
        ('profunda', 'Dislexia profunda')
    ], validators=[Optional()])
    
    herramientas_apoyo = MultiCheckboxField('Herramientas de apoyo que utilizas', choices=[
        ('texto_voz', 'Software de texto a voz'),
        ('voz_texto', 'Software de voz a texto'),
        ('correctores', 'Correctores ortográficos'),
        ('organizadores', 'Organizadores gráficos'),
        ('fuentes_especiales', 'Fuentes especiales (dyslexic fonts)'),
        ('colores', 'Filtros de color'),
        ('audiolibros', 'Audiolibros'),
        ('grabaciones', 'Grabaciones de audio')
    ])
    
    dificultades_principales = MultiCheckboxField('Principales dificultades', choices=[
        ('lectura', 'Velocidad de lectura'),
        ('comprension', 'Comprensión lectora'),
        ('ortografia', 'Ortografía'),
        ('escritura', 'Expresión escrita'),
        ('memoria_trabajo', 'Memoria de trabajo'),
        ('secuenciacion', 'Secuenciación'),
        ('orientacion', 'Orientación espacial')
    ])

class RegistroDiscalculiaForm(RegistroGeneralForm):
    dificultades_matematicas = MultiCheckboxField('Dificultades específicas con matemáticas', choices=[
        ('numeros_basicos', 'Conceptos numéricos básicos'),
        ('calculo_mental', 'Cálculo mental'),
        ('operaciones', 'Operaciones aritméticas'),
        ('resolucion_problemas', 'Resolución de problemas'),
        ('geometria', 'Geometría y espacialidad'),
        ('tiempo', 'Conceptos de tiempo'),
        ('dinero', 'Manejo de dinero'),
        ('medidas', 'Medidas y estimaciones')
    ])
    
    herramientas_calculo = MultiCheckboxField('Herramientas de apoyo para cálculos', choices=[
        ('calculadora', 'Calculadora'),
        ('software_matematico', 'Software matemático'),
        ('tablas_multiplicar', 'Tablas de multiplicar'),
        ('apoyo_visual', 'Materiales visuales'),
        ('step_by_step', 'Guías paso a paso'),
        ('tiempo_extra', 'Tiempo adicional'),
        ('formulas_referencia', 'Fórmulas de referencia')
    ])

class RegistroTouretteForm(RegistroGeneralForm):
    tipos_tics = MultiCheckboxField('Tipos de tics que experimentas', choices=[
        ('motor_simple', 'Tics motores simples'),
        ('motor_complejo', 'Tics motores complejos'),
        ('vocal_simple', 'Tics vocales simples'),
        ('vocal_complejo', 'Tics vocales complejos'),
        ('coprolalia', 'Coprolalia'),
        ('ecolalia', 'Ecolalia')
    ])
    
    frecuencia_tics = SelectField('Frecuencia de los tics', choices=[
        ('', 'Selecciona una opción'),
        ('ocasional', 'Ocasional'),
        ('diaria', 'Diaria'),
        ('constante', 'Constante'),
        ('variable', 'Variable según el estrés')
    ], validators=[Optional()])
    
    medicacion_tics = BooleanField('¿Tomas medicación para los tics?')
    
    estrategias_control = TextAreaField('Estrategias que te ayudan a manejar los tics', validators=[Optional()])

class RegistroDispraxiaForm(RegistroGeneralForm):
    dificultades_coordinacion = MultiCheckboxField('Dificultades de coordinación', choices=[
        ('motora_gruesa', 'Motricidad gruesa'),
        ('motora_fina', 'Motricidad fina'),
        ('coordinacion_ojo_mano', 'Coordinación ojo-mano'),
        ('equilibrio', 'Equilibrio'),
        ('planificacion_motora', 'Planificación motora'),
        ('secuenciacion', 'Secuenciación de movimientos')
    ])
    
    herramientas_organizacion = MultiCheckboxField('Herramientas de organización', choices=[
        ('agendas_visuales', 'Agendas visuales'),
        ('recordatorios', 'Recordatorios'),
        ('listas_pasos', 'Listas de pasos'),
        ('tecnologia_asistiva', 'Tecnología asistiva'),
        ('ergonomia', 'Adaptaciones ergonómicas')
    ])

class RegistroAnsiedadForm(RegistroGeneralForm):
    tipo_ansiedad = MultiCheckboxField('Tipo de trastorno de ansiedad', choices=[
        ('generalizada', 'Trastorno de ansiedad generalizada'),
        ('social', 'Ansiedad social'),
        ('panico', 'Trastorno de pánico'),
        ('fobias', 'Fobias específicas'),
        ('obsesivo_compulsivo', 'Trastorno obsesivo-compulsivo'),
        ('estres_postraumatico', 'Trastorno de estrés postraumático')
    ])
    
    tecnicas_manejo = MultiCheckboxField('Técnicas de manejo de ansiedad', choices=[
        ('respiracion', 'Técnicas de respiración'),
        ('meditacion', 'Meditación/mindfulness'),
        ('ejercicio', 'Ejercicio físico'),
        ('terapia_cognitiva', 'Terapia cognitiva'),
        ('medicacion', 'Medicación'),
        ('apoyo_social', 'Apoyo social'),
        ('rutinas', 'Rutinas estructuradas')
    ])
    
    desencadenantes_laborales = TextAreaField('Principales desencadenantes de ansiedad en el trabajo', validators=[Optional()])

class RegistroBipolarForm(RegistroGeneralForm):
    tipo_bipolar = SelectField('Tipo de trastorno bipolar', choices=[
        ('', 'Selecciona una opción'),
        ('bipolar_i', 'Trastorno bipolar I'),
        ('bipolar_ii', 'Trastorno bipolar II'),
        ('ciclotimico', 'Trastorno ciclotímico'),
        ('mixto', 'Episodios mixtos')
    ], validators=[Optional()])
    
    estabilidad_actual = SelectField('Estado de estabilidad actual', choices=[
        ('', 'Selecciona una opción'),
        ('estable', 'Estable'),
        ('episodio_maniaco', 'En episodio maníaco'),
        ('episodio_depresivo', 'En episodio depresivo'),
        ('episodio_mixto', 'En episodio mixto'),
        ('recuperacion', 'En recuperación')
    ], validators=[Optional()])
    
    medicacion_estabilizador = BooleanField('¿Tomas estabilizadores del ánimo?')
    apoyo_terapeutico = BooleanField('¿Recibes apoyo terapéutico regular?')

class RegistroAltasCapacidadesForm(RegistroGeneralForm):
    area_talento = MultiCheckboxField('Áreas de talento destacado', choices=[
        ('intelectual', 'Capacidad intelectual general'),
        ('academica', 'Aptitud académica específica'),
        ('creativa', 'Pensamiento creativo'),
        ('liderazgo', 'Capacidad de liderazgo'),
        ('artistica', 'Artes visuales y escénicas'),
        ('psicomotriz', 'Capacidad psicomotriz')
    ])
    
    nivel_ci = SelectField('Nivel de CI (si lo conoces)', choices=[
        ('', 'Prefiero no especificar'),
        ('superior', 'Superior (120-129)'),
        ('muy_superior', 'Muy superior (130-144)'),
        ('excepcional', 'Excepcional (145+)'),
        ('no_evaluado', 'No he sido evaluado')
    ], validators=[Optional()])
    
    desafios_sociales = BooleanField('¿Experimentas desafíos sociales relacionados con tus altas capacidades?')
    
    necesidades_estimulo = TextAreaField('Necesidades específicas de estimulación intelectual en el trabajo', validators=[Optional()])

# Formulario para empresas
class EmpresaForm(FlaskForm):
    nombre_empresa = StringField('Nombre de la Empresa', validators=[DataRequired()])
    sector = StringField('Sector', validators=[DataRequired()])
    tamaño = SelectField('Tamaño de la Empresa', choices=[
        ('startup', 'Startup (1-10 empleados)'),
        ('pequeña', 'Pequeña (11-50 empleados)'),
        ('mediana', 'Mediana (51-250 empleados)'),
        ('grande', 'Grande (250+ empleados)')
    ], validators=[DataRequired()])
    contacto_nombre = StringField('Nombre del Contacto', validators=[DataRequired()])
    contacto_email = StringField('Email de Contacto', validators=[DataRequired(), Email()])
    telefono = StringField('Teléfono', validators=[Optional()])
    ciudad = StringField('Ciudad', validators=[DataRequired()])
    descripcion = TextAreaField('Descripción de la Empresa', validators=[Optional()])
    
    # Campos específicos para inclusión
    politicas_inclusion = BooleanField('¿Tienen políticas de inclusión activas?')
    experiencia_neurodivergentes = BooleanField('¿Han trabajado antes con personas neurodivergentes?')
    adaptaciones_disponibles = MultiCheckboxField('Adaptaciones que pueden ofrecer', choices=[
        ('horario_flexible', 'Horario flexible'),
        ('trabajo_remoto', 'Trabajo remoto'),
        ('ambiente_tranquilo', 'Espacios de trabajo tranquilos'),
        ('tecnologia_asistiva', 'Tecnología asistiva'),
        ('formacion_equipo', 'Formación del equipo'),
        ('mentor', 'Programa de mentoring'),
        ('pausas_extra', 'Pausas adicionales'),
        ('instrucciones_escritas', 'Instrucciones por escrito')
    ])
    
    aceptar_privacidad = BooleanField('Acepto la política de privacidad', validators=[DataRequired()])

# Formulario para ofertas de trabajo
class OfertaTrabajoForm(FlaskForm):
    titulo = StringField('Título del Puesto', validators=[DataRequired()])
    descripcion = TextAreaField('Descripción del Puesto', validators=[DataRequired()])
    requisitos = TextAreaField('Requisitos', validators=[DataRequired()])
    beneficios = TextAreaField('Beneficios y Adaptaciones', validators=[Optional()])
    salario_min = StringField('Salario Mínimo', validators=[Optional()])
    salario_max = StringField('Salario Máximo', validators=[Optional()])
    modalidad = SelectField('Modalidad de Trabajo', choices=[
        ('presencial', 'Presencial'),
        ('remoto', 'Remoto'),
        ('hibrido', 'Híbrido')
    ], validators=[DataRequired()])
    ubicacion = StringField('Ubicación', validators=[DataRequired()])
    
    neurodivergencias_buscadas = MultiCheckboxField('Tipos de neurodivergencia que buscan específicamente', choices=[
        ('tdah', 'TDAH'),
        ('tea', 'TEA (Espectro Autista)'),
        ('dislexia', 'Dislexia'),
        ('discalculia', 'Discalculia'),
        ('tourette', 'Síndrome de Tourette'),
        ('dispraxia', 'Dispraxia'),
        ('ansiedad', 'Trastornos de Ansiedad'),
        ('bipolar', 'Trastorno Bipolar'),
        ('altas_capacidades', 'Altas Capacidades'),
        ('todas', 'Abierto a todas las neurodivergencias')
    ])

# Nuevo formulario para asociaciones
class AsociacionForm(FlaskForm):
    nombre_asociacion = StringField('Nombre de la Asociación', validators=[
        DataRequired(message='El nombre de la asociación es obligatorio'),
        Length(min=5, max=200, message='El nombre debe tener entre 5 y 200 caracteres')
    ])
    
    acronimo = StringField('Acrónimo o Siglas', validators=[
        Optional(),
        Length(max=20, message='El acrónimo no puede exceder 20 caracteres')
    ])
    
    pais = SelectField('País', choices=[
        ('ES', 'España'),
        ('MX', 'México'),
        ('AR', 'Argentina'),
        ('CO', 'Colombia'),
        ('PE', 'Perú'),
        ('CL', 'Chile'),
        ('VE', 'Venezuela'),
        ('EC', 'Ecuador'),
        ('BO', 'Bolivia'),
        ('PY', 'Paraguay'),
        ('UY', 'Uruguay'),
        ('CR', 'Costa Rica'),
        ('PA', 'Panamá'),
        ('GT', 'Guatemala'),
        ('HN', 'Honduras'),
        ('SV', 'El Salvador'),
        ('NI', 'Nicaragua'),
        ('DO', 'República Dominicana'),
        ('CU', 'Cuba'),
        ('US', 'Estados Unidos'),
        ('CA', 'Canadá'),
        ('OTHER', 'Otro país')
    ], validators=[DataRequired(message='Debes seleccionar un país')])
    
    otro_pais = StringField('Especifica el país', validators=[Optional()])
    
    # Documentos de verificación según el país
    tipo_documento = SelectField('Tipo de Documento Legal', choices=[
        ('', 'Selecciona el tipo de documento'),
        ('nif_es', 'NIF - Número de Identificación Fiscal (España)'),
        ('cif_es', 'CIF - Código de Identificación Fiscal (España)'),
        ('registro_asociaciones_es', 'Registro Nacional de Asociaciones (España)'),
        ('rfc_mx', 'RFC - Registro Federal de Contribuyentes (México)'),
        ('cuit_ar', 'CUIT - Clave Única de Identificación Tributaria (Argentina)'),
        ('cnpj_br', 'CNPJ - Cadastro Nacional da Pessoa Jurídica (Brasil)'),
        ('rut_cl', 'RUT - Rol Único Tributario (Chile)'),
        ('nit_co', 'NIT - Número de Identificación Tributaria (Colombia)'),
        ('ruc_pe', 'RUC - Registro Único de Contribuyentes (Perú)'),
        ('ein_us', 'EIN - Employer Identification Number (Estados Unidos)'),
        ('bn_ca', 'Business Number (Canadá)'),
        ('registro_ong', 'Registro de ONG/Asociación'),
        ('certificado_utilidad_publica', 'Certificado de Utilidad Pública'),
        ('otro', 'Otro tipo de documento')
    ], validators=[DataRequired(message='Debes especificar el tipo de documento legal')])
    
    numero_documento = StringField('Número del Documento', validators=[
        DataRequired(message='El número de documento es obligatorio'),
        Length(min=5, max=50, message='El número debe tener entre 5 y 50 caracteres')
    ])
    
    descripcion_otro_documento = StringField('Describe el tipo de documento', validators=[Optional()])
    
    neurodivergencias_atendidas = MultiCheckboxField('Tipos de neurodivergencia que atiende', choices=[
        ('tdah', 'TDAH'),
        ('tea', 'TEA (Trastorno del Espectro Autista)'),
        ('dislexia', 'Dislexia'),
        ('discalculia', 'Discalculia'),
        ('tourette', 'Síndrome de Tourette'),
        ('dispraxia', 'Dispraxia'),
        ('ansiedad', 'Trastornos de Ansiedad'),
        ('bipolar', 'Trastorno Bipolar'),
        ('altas_capacidades', 'Altas Capacidades'),
        ('general', 'Neurodiversidad en general'),
        ('otras', 'Otras condiciones')
    ], validators=[DataRequired(message='Debes seleccionar al menos un tipo de neurodivergencia')])
    
    servicios = MultiCheckboxField('Servicios que ofrece', choices=[
        ('apoyo_familias', 'Apoyo a familias'),
        ('orientacion_laboral', 'Orientación laboral'),
        ('formacion', 'Formación y capacitación'),
        ('terapia', 'Servicios terapéuticos'),
        ('evaluacion', 'Evaluación y diagnóstico'),
        ('advocacy', 'Advocacy y derechos'),
        ('grupos_apoyo', 'Grupos de apoyo'),
        ('investigacion', 'Investigación'),
        ('sensibilizacion', 'Sensibilización social'),
        ('inclusion_educativa', 'Inclusión educativa'),
        ('inclusion_laboral', 'Inclusión laboral'),
        ('otros', 'Otros servicios')
    ], validators=[DataRequired(message='Debes seleccionar al menos un servicio')])
    
    ciudad = StringField('Ciudad', validators=[
        DataRequired(message='La ciudad es obligatoria'),
        Length(min=2, max=100, message='La ciudad debe tener entre 2 y 100 caracteres')
    ])
    
    direccion = StringField('Dirección (opcional)', validators=[
        Optional(),
        Length(max=200, message='La dirección no puede exceder 200 caracteres')
    ])
    
    telefono = StringField('Teléfono de contacto', validators=[
        DataRequired(message='El teléfono es obligatorio'),
        Length(min=7, max=20, message='El teléfono debe tener entre 7 y 20 caracteres')
    ])
    
    email = StringField('Email de contacto', validators=[
        DataRequired(message='El email es obligatorio'),
        Email(message='Introduce un email válido'),
        Length(max=100, message='El email no puede exceder 100 caracteres')
    ])
    
    sitio_web = StringField('Sitio web (opcional)', validators=[
        Optional(),
        URL(message='Introduce una URL válida'),
        Length(max=200, message='La URL no puede exceder 200 caracteres')
    ])
    
    descripcion = TextAreaField('Descripción de la asociación', validators=[
        DataRequired(message='La descripción es obligatoria'),
        Length(min=50, max=1000, message='La descripción debe tener entre 50 y 1000 caracteres')
    ])
    
    años_funcionamiento = SelectField('Años de funcionamiento', choices=[
        ('', 'Selecciona una opción'),
        ('menos_1', 'Menos de 1 año'),
        ('1_3', '1-3 años'),
        ('4_10', '4-10 años'),
        ('11_20', '11-20 años'),
        ('mas_20', 'Más de 20 años')
    ], validators=[DataRequired(message='Debes especificar los años de funcionamiento')])
    
    numero_socios = SelectField('Número aproximado de socios/miembros', choices=[
        ('', 'Selecciona una opción'),
        ('menos_50', 'Menos de 50'),
        ('50_100', '50-100'),
        ('101_500', '101-500'),
        ('501_1000', '501-1000'),
        ('mas_1000', 'Más de 1000')
    ], validators=[DataRequired(message='Debes especificar el número de socios')])
    
    certificaciones = MultiCheckboxField('Certificaciones o reconocimientos', choices=[
        ('utilidad_publica', 'Declarada de utilidad pública'),
        ('iso', 'Certificación ISO'),
        ('transparencia', 'Certificación de transparencia'),
        ('calidad', 'Certificación de calidad'),
        ('gobierno', 'Reconocimiento gubernamental'),
        ('internacional', 'Reconocimiento internacional'),
        ('ninguna', 'Sin certificaciones específicas')
    ])
    
    contacto_nombre = StringField('Nombre de la persona de contacto', validators=[
        DataRequired(message='El nombre del contacto es obligatorio'),
        Length(min=2, max=100, message='El nombre debe tener entre 2 y 100 caracteres')
    ])
    
    contacto_cargo = StringField('Cargo de la persona de contacto', validators=[
        DataRequired(message='El cargo es obligatorio'),
        Length(min=2, max=100, message='El cargo debe tener entre 2 y 100 caracteres')
    ])
    
    aceptar_verificacion = BooleanField('Acepto que DiversIA verifique la información proporcionada', validators=[
        DataRequired(message='Debes aceptar el proceso de verificación')
    ])
    
    aceptar_privacidad = BooleanField('Acepto la política de privacidad', validators=[
        DataRequired(message='Debes aceptar la política de privacidad')
    ])