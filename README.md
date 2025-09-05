# DiversIA - Plataforma de Inclusión Laboral

## 📋 Descripción del Proyecto

**DiversIA** es una plataforma web integral diseñada para conectar a personas neurodivergentes con oportunidades de empleo inclusivo. El sistema actúa como puente entre candidatos neurodivergentes y empresas comprometidas con la diversidad e inclusión.

## ✨ Características Principales

### 🎯 **Sistema de Gestión de Tareas**
- **Asignación de Tareas**: Sistema completo para asignar tareas a colaboradores
- **Estados Dinámicos**: Seguimiento de estados (Pendiente, En curso, Terminada)
- **Gestión de Empleados**: Base de datos de colaboradores con estado activo/inactivo
- **Dashboard Analytics**: Análisis completo de productividad y rendimiento

### 📊 **Dashboard Analítico Avanzado**
- **Métricas Clave**: Total de tareas, completadas, en curso, sin asignar
- **Análisis de Productividad**: Eficiencia por colaborador con tendencias mensuales
- **Carga de Trabajo**: Niveles de carga por empleado (Alta/Media/Baja)
- **Tendencias Temporales**: Comparativas mensuales de tareas terminadas vs iniciadas
- **Clasificación Automática**: Tipos de tareas (Marketing, Desarrollo, Redes Sociales, Otros)
- **Gráficos Interactivos**: Visualizaciones con Chart.js

### 🧠 **Registro Especializado Neurodivergente**
- **Formulario Universal**: Registro para todos los tipos de neurodivergencia
- **Formularios Específicos**: ADHD, Autismo, Dislexia, Discalculia
- **Validación Segura**: Flask-WTF con protección CSRF
- **Perfiles Personalizados**: Gestión de perfiles con SQLAlchemy

### 🏢 **Sistema CRM Empresarial**
- **Gestión de Leads**: Administración completa de candidatos neurodivergentes
- **Registro de Empresas**: Sistema de registro y gestión de empresas inclusivas
- **Dashboard Administrativo**: Panel de control con estadísticas en tiempo real
- **Operaciones Masivas**: Exportación CSV y operaciones bulk
- **Búsqueda y Filtros**: Sistema avanzado de búsqueda

### 📧 **Marketing por Email**
- **Notificaciones Automáticas**: Sistema de emails con Gmail SMTP
- **Campañas de Marketing**: Gestión de campañas dirigidas
- **Analytics de Email**: Seguimiento de métricas de email marketing

## 🛠️ **Arquitectura Técnica**

### **Backend - Flask Production System**
- **Framework**: Flask con Python 3
- **Base de Datos**: PostgreSQL con SQLAlchemy ORM
- **Autenticación**: Sistema basado en sesiones Flask
- **APIs REST**: Endpoints para todas las funcionalidades

### **Frontend - HTML Templates with Modern CSS**
- **Templates**: Jinja2 con Flask
- **Estilos**: Bootstrap CSS con diseño responsive
- **Formularios**: Flask-WTF con validación del lado servidor
- **JavaScript**: Chart.js para visualizaciones interactivas

### **Base de Datos - SQLAlchemy ORM**
- **Modelos**: GeneralLead, NeurodivergentProfile, Company, Employee, Task, EmailMarketing, Admin
- **Validación**: Flask-WTF con protección CSRF
- **Exportación**: Funcionalidad de exportación CSV

## 🚀 **Instalación y Configuración**

### **Requisitos del Sistema**
- Python 3.8+
- PostgreSQL
- Dependencias en `requirements.txt`

### **Variables de Entorno Requeridas**
```env
DATABASE_URL=postgresql://...
SESSION_SECRET=tu_clave_secreta
GMAIL_USER=tu_email@gmail.com
GMAIL_APP_PASSWORD=tu_password_de_app
```

### **Instalación**
```bash
# Instalar dependencias
pip install -r requirements.txt

# Configurar base de datos
python -c "from app import db; db.create_all()"

# Ejecutar aplicación
gunicorn --bind 0.0.0.0:5000 --reuse-port --reload main:app
```

## 📁 **Estructura del Proyecto**

```
diversia-flask/
├── templates/              # Plantillas Jinja2 HTML
├── static/                # Assets CSS, JS e imágenes
├── models.py              # Modelos de base de datos SQLAlchemy
├── forms.py               # Definiciones de formularios Flask-WTF
├── routes_simple.py       # Rutas principales de la aplicación
├── crm_minimal.py         # Funcionalidad del dashboard CRM
├── tareas_manager.py      # Sistema de gestión de tareas
├── dashboard_tareas.py    # Dashboard analítico con gráficos
├── email_notifications.py # Sistema de automatización de emails
├── colaboradores_manager.py # Gestión de empleados
├── email_marketing_manager.py # Gestión de campañas de email
└── main.py               # Punto de entrada de la aplicación
```

## 🔑 **Acceso al Sistema**

### **Panel Administrativo**
- **URL**: `/admin-dashboard`
- **Login**: `/diversia-admin`
- **Credenciales**: Usuario admin configurado automáticamente

### **Funcionalidades Principales**
- **Gestión de Tareas**: `/tareas`
- **Dashboard Analytics**: `/dashboard-tareas`
- **CRM Leads**: `/admin-dashboard`
- **Registro Neurodivergente**: `/registro-neurodivergente`

## 📈 **Dashboard Analytics**

### **Métricas Disponibles**
- Total de tareas y porcentaje de completado
- Tareas completadas, en curso y sin asignar
- Promedio de tareas por empleado
- Análisis de carga de trabajo por colaborador

### **Gráficos Interactivos**
- **Distribución de Estados**: Gráfico circular de estados de tareas
- **Tareas por Colaborador**: Gráfico de barras de asignaciones
- **Tendencias Temporales**: Líneas de tiempo de productividad mensual
- **Tipos de Tareas**: Clasificación automática por categorías
- **Carga de Trabajo**: Análisis visual de sobrecarga de empleados

## 🛡️ **Seguridad**

- **Protección CSRF**: Flask-WTF en todos los formularios
- **Validación del Servidor**: Validación robusta con WTForms
- **Gestión de Sesiones**: Autenticación segura basada en sesiones
- **Pool de Conexiones**: Configuración avanzada de base de datos
- **Reconexión Automática**: Sistema de recuperación ante fallos

## 🎯 **Estado del Proyecto**

### **✅ Funcionalidades Completadas**
- Sistema completo de gestión de tareas con PostgreSQL
- Dashboard analítico con gráficos interactivos
- CRM funcional con operaciones CRUD
- Sistema de registro neurodivergente
- Email marketing y notificaciones
- Autenticación y seguridad
- Diseño responsive y moderno

### **🚀 Listo para Producción**
- Base de datos estabilizada con pool de conexiones
- Código depurado sin errores críticos
- Sistema de auto-recuperación ante fallos
- Funcionalidades completas e integradas

## 👥 **Equipo y Colaboradores**

El sistema gestiona actualmente los siguientes colaboradores:
- **Pep**: Desarrollador principal
- **Olga**: Especialista en marketing
- **Ana**: Coordinadora de proyectos

## 📊 **Métricas de Rendimiento**

El dashboard proporciona análisis detallados de:
- Productividad individual y grupal
- Tendencias mensuales de completado de tareas
- Distribución de carga de trabajo
- Clasificación automática de tipos de proyecto
- Comparativas de rendimiento entre empleados

---

**DiversIA** - *Conectando talento neurodivergente con oportunidades inclusivas*

*Desarrollado con Flask, PostgreSQL y tecnologías web modernas*