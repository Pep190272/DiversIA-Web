# DiversIA - Plataforma de Inclusión Laboral

## Overview

DiversIA is a comprehensive web platform designed to connect neurodivergent individuals with inclusive employment opportunities. The system serves as a bridge between neurodivergent job seekers and companies committed to diversity and inclusion. The platform features specialized registration forms for different types of neurodivergence (ADHD, Autism, Dyslexia, etc.), a comprehensive CRM system for managing leads and companies, and administrative tools for content management.

## User Preferences

Preferred communication style: Simple, everyday language.

## System Architecture

### Backend Architecture
- **Framework**: Flask web application with SQLAlchemy ORM
- **Database**: PostgreSQL as the primary and only database (no SQLite fallback)
- **Authentication**: Session-based admin authentication system with hardcoded credentials
- **File Structure**: Modular approach with separate files for different functionalities (CRM, task management, email marketing, etc.)

### Frontend Architecture
- **Template Engine**: Jinja2 templates with Bootstrap 5 for responsive design
- **Styling**: Custom CSS with accessibility features including font size controls and high contrast options
- **JavaScript**: Vanilla JavaScript for interactive features and form handling
- **Responsive Design**: Mobile-first approach with Bootstrap grid system

### Data Management
- **Models**: Separate models for different user types (GeneralLead, NeurodivergentProfile, Company, Employee, Task, EmailMarketing, AdminUser)
- **Form Handling**: WTForms for form validation and rendering
- **Data Export**: CSV export functionality for administrative data management
- **File Storage**: JSON-based backup system alongside PostgreSQL

### Authentication and Security
- **Admin System**: Simple username/password authentication stored in PostgreSQL
- **Session Management**: Flask sessions with secure cookie configuration
- **Security Headers**: CSRF protection, XSS protection, and content security policies
- **Data Protection**: Form validation and sanitization for user inputs

### CRM and Lead Management
- **Multi-tier System**: Separate handling for general leads (from tests) and detailed neurodivergent profiles
- **Company Management**: Comprehensive company registration and management system
- **Task Assignment**: Employee task management with status tracking
- **Email Marketing**: Integration with email marketing campaigns and tracking

### Specialized Registration System
- **Universal Registration**: General form for all neurodivergence types
- **Specialized Forms**: Dedicated registration forms for ADHD, Autism, Dyslexia, Dyscalculia, and other conditions
- **Gamified Testing**: Interactive assessment system for skill evaluation
- **Profile Conversion**: System to convert general leads to detailed profiles

## External Dependencies

### Required Services
- **PostgreSQL Database**: Primary data storage (DATABASE_URL environment variable required)
- **SendGrid**: Email notification system (SENDGRID_API_KEY for automated notifications)

### Frontend Libraries
- **Bootstrap 5.3.0**: UI framework and responsive design
- **Font Awesome 6.4.0**: Icon library for visual elements
- **Lucide Icons**: Additional icon system as fallback
- **CDN Dependencies**: All frontend libraries loaded via CDN for performance

### Development Tools
- **Vercel**: Deployment configuration for production hosting
- **Metricool**: Analytics integration for website traffic monitoring
- **Route Validation**: Custom validation system to prevent 500 errors

### Optional Integrations
- **Telegram**: Support chat integration for user assistance
- **CSV Import/Export**: File handling for bulk data operations
- **Google Verification**: Site verification for search engine optimization