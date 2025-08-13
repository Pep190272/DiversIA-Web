# DiversIA - Neurodivergent Employment Platform

## Overview

DiversIA is a web-based employment platform designed to connect neurodivergent individuals with inclusive employers. The platform features specialized registration forms tailored to different neurodivergence types (TDAH, TEA, Dislexia), gamified assessment tests, and a community space for networking and support. Built with accessibility as a core principle, the platform uses warm color palettes, generous spacing, and comprehensive accessibility controls to reduce cognitive load and ensure usability for all users.

## User Preferences

Preferred communication style: Simple, everyday language.

## System Architecture

### Frontend Architecture
- **Template Engine**: Jinja2 templates with Flask for server-side rendering
- **CSS Framework**: Bootstrap 5.3.0 for responsive design and accessibility features
- **Icon System**: Lucide icons for consistent and accessible iconography
- **Custom Styling**: CSS custom properties (variables) for consistent theming and accessibility features
- **Accessibility Features**: Built-in accessibility controls including font size adjustment, dark mode, high contrast mode, and animation controls

### Backend Architecture
- **Web Framework**: Flask with modular structure separating models, routes, and forms
- **Database ORM**: SQLAlchemy with declarative base for database operations
- **Form Handling**: Flask-WTF with WTForms for secure form processing and validation
- **Security**: Comprehensive security headers, CSRF protection, and input validation
- **Application Structure**: Modular design with separate files for models, routes, forms, and configuration

### Data Models
- **User Model**: Stores neurodivergent individual profiles with specialized fields for different conditions
- **Company Model**: Manages employer information and contact details
- **JobOffer Model**: Links companies to job postings with neurodivergence-specific requirements
- **TestResult Model**: Placeholder for gamified assessment results (incomplete implementation)

### Form Architecture
- **Inheritance-based Forms**: Base `RegistroGeneralForm` extended by condition-specific forms
- **Custom Field Types**: `MultiCheckboxField` for accessibility-friendly multi-select options
- **Validation Strategy**: Comprehensive server-side validation with user-friendly error messaging
- **Specialized Forms**: Separate forms for TDAH, Dislexia, TEA with condition-specific fields

### Accessibility Architecture
- **Universal Design**: Color-coded system for different neurodivergence types while maintaining accessibility
- **Interactive Controls**: JavaScript-powered accessibility toolbar with persistent settings
- **Screen Reader Support**: Semantic HTML, ARIA labels, and skip navigation links
- **Cognitive Load Reduction**: Generous spacing, large border radius, and reduced visual clutter

## External Dependencies

### Frontend Dependencies
- **Bootstrap 5.3.0**: UI framework for responsive design and accessibility components
- **Lucide Icons**: Modern icon library with accessibility features
- **Custom JavaScript**: Accessibility controls and carousel functionality without heavy frameworks

### Backend Dependencies
- **Flask**: Lightweight web framework for Python applications
- **Flask-SQLAlchemy**: Database ORM integration for Flask
- **Flask-WTF**: Form handling and CSRF protection
- **WTForms**: Form validation and rendering library
- **Werkzeug**: WSGI utilities including ProxyFix for deployment

### Database
- **SQLite**: Default development database (configurable via DATABASE_URL environment variable)
- **PostgreSQL Ready**: Architecture supports PostgreSQL for production deployment

### Security & Deployment
- **Environment Configuration**: Secure configuration via environment variables
- **Security Headers**: Comprehensive security header implementation
- **Session Management**: Secure session handling with configurable secret keys
- **WSGI Deployment**: Production-ready with ProxyFix middleware