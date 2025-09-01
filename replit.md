# DiversIA - Plataforma de Inclusión Laboral

## Overview

DiversIA is a comprehensive web platform designed to connect neurodivergent individuals with inclusive employment opportunities. The system serves as a bridge between neurodivergent job seekers and companies committed to diversity and inclusion. The platform features specialized registration forms for different types of neurodivergence (ADHD, Autism, Dyslexia, etc.), a comprehensive CRM system for managing leads and companies, and administrative tools for content management.

## User Preferences

Preferred communication style: Simple, everyday language.

## System Architecture

### Backend Architecture - FLASK PRODUCTION SYSTEM
- **Framework**: Flask with Python 3
- **Database**: PostgreSQL with SQLAlchemy ORM
- **API Routes**: Flask routes for all backend functionality
- **Authentication**: Custom Flask session-based authentication
- **File Structure**: Traditional Flask app structure with clear separation of concerns

### Frontend Architecture - HTML TEMPLATES WITH MODERN CSS
- **Framework**: Jinja2 templates with Flask
- **Styling**: Bootstrap CSS with custom responsive design
- **Components**: Reusable HTML templates with Flask forms
- **Forms**: Flask-WTF with WTForms validation and CSRF protection
- **State Management**: Server-side state with Flask sessions
- **Responsive Design**: Bootstrap responsive framework

### Data Management - SQLALCHEMY ORM
- **Models**: SQLAlchemy models (GeneralLead, NeurodivergentProfile, Company, Employee, Task, EmailMarketing, Admin)
- **Form Handling**: Flask-WTF with server-side validation and CSRF protection
- **Data Export**: CSV export functionality implemented with bulk operations
- **Database Operations**: SQLAlchemy ORM with PostgreSQL backend

### Authentication and Security - FLASK SECURITY
- **Admin System**: Flask session-based authentication with secure login
- **API Security**: Flask-WTF CSRF protection and server-side validation  
- **Data Protection**: SQLAlchemy ORM with parameterized queries
- **Security Headers**: Custom security headers and session management

### CRM and Lead Management - FLASK DASHBOARD
- **CRM Dashboard**: HTML-based CRM dashboard with real-time statistics
- **API Integration**: Flask API endpoints for all CRM operations
- **Company Management**: Full company registration and management with Flask forms
- **Statistics Display**: Server-rendered data visualization with Bootstrap UI
- **Responsive CRM**: Mobile-friendly administration interface with bulk operations

### Specialized Registration System - FLASK FORMS
- **Universal Registration**: Flask-WTF form for all neurodivergence types
- **Specialized Forms**: Flask-powered forms for ADHD, Autism, Dyslexia, Dyscalculia, and other conditions
- **Form Validation**: Server-side validation with error handling and user feedback
- **Profile Management**: SQLAlchemy-based profile creation and management system
- **User Experience**: Clean UX with Flash messages, success notifications, and error handling

## External Dependencies

### Required Services
- **PostgreSQL Database**: Primary data storage (DATABASE_URL environment variable required)
- **SQLAlchemy**: Python ORM for database operations
- **Gmail SMTP**: Email notification system (GMAIL_USER and GMAIL_APP_PASSWORD for automated notifications)

### Frontend Libraries - PRODUCTION STACK
- **Bootstrap CSS**: Responsive UI framework
- **jQuery**: JavaScript functionality for interactive components
- **Flask-WTF**: Secure form handling with CSRF protection
- **Jinja2**: Template engine for dynamic HTML generation

### Development Tools - FLASK STACK
- **Flask Debug Mode**: Built-in development server with hot reload
- **SQLAlchemy Models**: Database schema management and queries
- **Python Logging**: Comprehensive error tracking and debugging

### Current System Status
- **✅ Database Schema**: PostgreSQL with SQLAlchemy models
- **✅ API Routes**: All Flask routes fully functional
- **✅ Frontend Templates**: HTML templates with Bootstrap CSS
- **✅ Forms**: Flask-WTF forms with server-side validation
- **✅ CRM System**: Complete admin dashboard with bulk operations
- **✅ Authentication**: Flask session-based secure login system
- **✅ Responsive Design**: Bootstrap responsive framework

### Project Structure
```
diversia-flask/
├── templates/              # Jinja2 HTML templates
├── static/                # CSS, JS, and image assets
├── models.py              # SQLAlchemy database models
├── forms.py               # Flask-WTF form definitions
├── routes_simple.py       # Main application routes
├── crm_minimal.py         # CRM dashboard functionality
├── email_notifications.py # Email automation system
└── main.py               # Application entry point
```