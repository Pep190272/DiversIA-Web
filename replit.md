# DiversIA - Neurodivergent Employment Platform

## Overview
DiversIA is a web-based employment platform designed to connect neurodivergent individuals with inclusive employers. It features specialized registration forms for different neurodivergence types (TDAH, TEA, Dislexia, Discalculia, Tourette, Dispraxia, Ansiedad, Bipolar, Altas Capacidades), gamified assessment tests (planned), and a community space. The platform prioritizes accessibility, using warm color palettes, generous spacing, and comprehensive accessibility controls to reduce cognitive load and ensure usability. It also integrates a comprehensive CRM system for business management and analytics, aiming to be a complete solution for both neurodivergent job seekers and inclusive employers.

## User Preferences
Preferred communication style: Simple, everyday language.
System reliability: Critical requirement - zero tolerance for 500 errors on main routes.

## System Reliability
- **SQLite Database**: Migrated from PostgreSQL to SQLite for 100% reliability, zero cost, and mobile compatibility
- All form fields MUST be defined in forms.py before being used in templates  
- Route validator (route_validator.py) automatically checks critical routes
- Critical routes that must never fail: /, /empresas, /personas-nd, /comunidad, /registro, /registro-tdah, /registro-tea, /registro-dislexia, /test, /comenzar
- Admin login fixed: Access via /admin/login-new with credentials DiversiaEternals / diversia3ternal$2025
- **ALL FORMS NOW WORKING**: Company registration, user registration, contact forms, job offers - all save data correctly
- **Triple backup system**: SQLite → CRM persistent → File backup ensures zero data loss
- **Email notifications**: Automatic emails sent to diversiaeternals@gmail.com for all form submissions
- **CRM Dashboard**: Fully operational with specialized neurodivergent management system
- **CSV Management**: Full import/export capabilities for all data types - UPDATED 2025-08-22
- **CSV Import System**: Complete API `/api/import-csv` for companies and contacts with validation
- **Data Integrity**: CRM cleaned to contain only real company data (Acelerai)
- **Comprehensive ND CRM**: Individual panels for TDAH, TEA, Dislexia, Discalculia, and other neurodivergences

## System Architecture

### Frontend Architecture
The frontend is built using Jinja2 templates with Flask for server-side rendering. It leverages Bootstrap 5.3.0 for responsive design and accessibility, and Lucide icons for consistent iconography. Custom CSS properties are used for theming. A key feature is the built-in accessibility toolbar allowing users to adjust font size, enable dark mode, high contrast mode, and control animations.

### Backend Architecture
The backend is a Flask application with a modular structure, separating models, routes, and forms. SQLAlchemy is used for ORM operations, and Flask-WTF handles secure form processing and validation. Security measures include comprehensive security headers, CSRF protection, and input validation. The application has a role-based admin system with session management and permission controls, integrating a complete business management CRM with automatic form tracking and data analytics.

### Data Models
Core data models include: User (neurodivergent profiles), Company, JobOffer, Admin, CrmContact (business contacts), FormSubmission (tracked web forms), Asociacion (neurodivergent associations), Employee, Task, and TestResult (gamified assessments). All models optimized for SQLite with proper indexing and relationships.

### Form Architecture
Forms are inheritance-based, extending a base `RegistroGeneralForm` with specialized versions for TDAH, Dislexia, and TEA, containing condition-specific fields. Custom field types like `MultiCheckboxField` enhance accessibility. Server-side validation with user-friendly error messages is a priority.

### Accessibility Architecture
The platform employs universal design principles, including a color-coded system for neurodivergence types that maintains accessibility. An interactive JavaScript-powered accessibility toolbar allows persistent settings. Semantic HTML, ARIA labels, and skip navigation links support screen readers. Cognitive load is reduced through generous spacing, large border radii, and minimized visual clutter.

### AI Integration
The platform integrates an intelligent AI agent system powered by Mistral AI, featuring a chat system with contextual understanding, intent detection, and response generation. It uses a hybrid system for responses, leveraging a local knowledge base with fallback to cloud services for analytics and complex queries.

## External Dependencies

### Frontend Dependencies
- **Bootstrap 5.3.0**: UI framework.
- **Lucide Icons**: Icon library.
- **Custom JavaScript**: For accessibility controls and UI enhancements.

### Backend Dependencies
- **Flask**: Web framework.
- **Flask-SQLAlchemy**: ORM integration.
- **Flask-WTF**: Form handling and CSRF protection.
- **WTForms**: Form validation.
- **Werkzeug**: WSGI utilities.
- **SendGrid**: Email service for notifications.
- **Mistral AI**: Powers the intelligent AI agent system.

### Database
- **PostgreSQL**: Production database.
- **SQLAlchemy ORM**: Full relational database support.
- **SQLite**: Fallback database for development/testing.

### Communication & CRM Integration
- **SendGrid API**: For automated email notifications (e.g., to diversiaeternals@gmail.com).
- **HubSpot, Salesforce**: CRM export capabilities (CSV and JSON).
- **Discord, Instagram, LinkedIn**: Direct social media links.
- **Telegram**: Official support channel (https://t.me/DiversiaSupport).
- **Metricool**: Analytics integration for social media management.
- **n8n.cloud**: Webhook integration for chat and user tracking.

### Security & Deployment
- **Environment Variables**: For secure configuration.
- **WSGI**: Production-ready deployment.