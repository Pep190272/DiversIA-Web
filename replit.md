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
- **SendGrid**: Email service for automated notifications and form submissions

### Database
- **PostgreSQL**: Production database with environment variables configuration
- **SQLAlchemy ORM**: Full relational database support with migration capabilities

### Communication & CRM Integration
- **SendGrid API**: Automated email notifications to diversiaeternals@gmail.com
- **CRM Export Module**: CSV and JSON export capabilities for HubSpot, Salesforce integration
- **Social Media Integration**: Direct links to Discord, Instagram, LinkedIn, and email contact

### Security & Deployment
- **Environment Configuration**: Secure configuration via environment variables
- **Security Headers**: Comprehensive security header implementation
- **Session Management**: Secure session handling with configurable secret keys
- **WSGI Deployment**: Production-ready with ProxyFix middleware

## Recent Updates (2025-01-16)

### Translation System Enhancement
- ✓ Fixed translator to work without page reloads between language changes
- ✓ Implemented intelligent content restoration system
- ✓ Added automatic reinitialization of icons and chat widget after translation
- ✓ Original content preservation for seamless language switching

### n8n Chat Integration (COMPLETE)
- ✓ Chat widget fully functional with intelligent fallback responses
- ✓ Application URL: `https://073083d2-dd14-424e-a549-4c03e48131b7-00-1vatfbc2lts0v.janeway.replit.dev/`
- ✓ n8n.cloud webhook configured: `https://pepmorenocreador.app.n8n.cloud/webhook-test/diversia-chat`
- ✓ Webhook properly activated and path verified from user screenshot
- ✓ Full integration between DiversIA chat and n8n intelligent agent
- ✓ Real-time chat responses with user insights and statistics
- ✓ Created comprehensive setup guides for both local and cloud configurations

## Previous Updates (2025-01-14)

### Translation System (CRITICAL FIX)
- ✓ Implemented 100% functional Google Translate integration
- ✓ Robust error handling and retry mechanisms
- ✓ Support for 9 languages with visual indicators
- ✓ Automatic language preference restoration
- ✓ Professional error messaging and loading states
- ✓ Complete replacement of AVADIS broken links with working Spanish dyslexia tests

### Content Updates
- ✓ Replaced non-functional AVADIS link with working Spanish dyslexia test providers
- ✓ Added Upbility Spanish dyslexia test (validated with 86% reliability)
- ✓ Added Espacio Autismo evaluation system
- ✓ All new links tested and verified functional

### n8n Agent Integration (2025-01-15)
- ✓ Created comprehensive API endpoints for agent integration
- ✓ Built intelligent chat widget with professional UI
- ✓ Implemented webhooks for real-time chat and user tracking
- ✓ Added lead scoring system for sales funnel optimization
- ✓ Created user insights and analytics endpoints
- ✓ Integrated chat widget in all pages with session management
- ✓ Added comprehensive n8n integration guide

## Previous Updates (2025-01-13)

### Social Media & Communication
- ✓ Added direct links to DiversIA social media accounts (Discord, Instagram, LinkedIn)
- ✓ Integrated email contact (diversiaeternals@gmail.com) in footer
- ✓ All social links open in new tabs with proper security attributes

### Email Integration
- ✓ Automated email notifications for all form submissions
- ✓ SendGrid integration with HTML-formatted emails
- ✓ Separate email templates for user registrations and company registrations
- ✓ All form data automatically sent to diversiaeternals@gmail.com

### Associations Section
- ✓ Created new "Asociaciones" page with directory of neurodivergent-related organizations
- ✓ Filterable directory by neurodivergence type, location, and services
- ✓ Sample associations for TDAH, TEA, Dislexia, and general support
- ✓ Contact information and direct links to association websites
- ✓ Call-to-action for new associations to join the directory

### CRM Integration Capabilities
- ✓ Enhanced database models with CRM export tracking
- ✓ CSV and JSON export functionality for external CRM systems
- ✓ Export audit logging with timestamps and status tracking
- ✓ Ready-to-use formatters for HubSpot and Salesforce integration
- ✓ Automated marking of exported records to prevent duplicates