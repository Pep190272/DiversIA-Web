# DiversIA - Plataforma de Inclusión Laboral

## Overview

DiversIA is a comprehensive web platform designed to connect neurodivergent individuals with inclusive employment opportunities. The system serves as a bridge between neurodivergent job seekers and companies committed to diversity and inclusion. **MIGRATED TO NEXT.JS** - The platform now features a modern React-based frontend with specialized registration forms for different types of neurodivergence (ADHD, Autism, Dyslexia, etc.), a comprehensive CRM system for managing leads and companies, and administrative tools for content management.

## User Preferences

Preferred communication style: Simple, everyday language.

## System Architecture

### Backend Architecture - MIGRATED TO NEXT.JS
- **Framework**: Next.js 15 with App Router and TypeScript
- **Database**: PostgreSQL with Prisma ORM (migrated from SQLAlchemy)
- **API Routes**: Next.js API routes replacing Flask endpoints
- **Authentication**: Ready for NextAuth.js integration (currently pending)
- **File Structure**: Modern Next.js app structure with clear separation of concerns

### Frontend Architecture - COMPLETELY REBUILT
- **Framework**: React 18 with Next.js App Router
- **Styling**: Tailwind CSS for utility-first responsive design
- **Components**: Reusable React components with TypeScript
- **Forms**: React Hook Form with Zod validation (replaced WTForms)
- **State Management**: React hooks and client-side state
- **Responsive Design**: Mobile-first approach with Tailwind CSS responsive utilities

### Data Management - MIGRATED TO PRISMA
- **Models**: Prisma schema with all original models (GeneralLead, NeurodivergentProfile, Company, Employee, Task, EmailMarketing, Admin)
- **Form Handling**: React Hook Form with Zod validation for type-safe form handling
- **Data Export**: API endpoints ready for CSV export functionality 
- **Type Safety**: Full TypeScript integration with Prisma client
- **Database Operations**: Prisma ORM with improved query performance

### Authentication and Security - MODERNIZED
- **Admin System**: Prepared for NextAuth.js integration with secure JWT tokens
- **API Security**: TypeScript type checking and Zod validation on all inputs
- **Data Protection**: Client and server-side validation with sanitization
- **Modern Security**: Built-in Next.js security features and best practices

### CRM and Lead Management - REACT COMPONENTS
- **Modern Dashboard**: React-based CRM dashboard with real-time statistics
- **API Integration**: RESTful API endpoints for all CRM operations
- **Company Management**: Full company registration and management with React forms
- **Statistics Display**: Live data visualization with modern UI components
- **Responsive CRM**: Mobile-friendly administration interface

### Specialized Registration System - FULLY MIGRATED
- **Universal Registration**: Modern React form for all neurodivergence types
- **Specialized Forms**: TypeScript-powered forms for ADHD, Autism, Dyslexia, Dyscalculia, and other conditions
- **Form Validation**: Real-time validation with error handling and user feedback
- **Profile Management**: Advanced profile creation and management system
- **User Experience**: Improved UX with loading states, success messages, and error handling

## External Dependencies

### Required Services
- **PostgreSQL Database**: Primary data storage (DATABASE_URL environment variable required)
- **Prisma**: Modern ORM for database operations and migrations
- **SendGrid**: Email notification system (SENDGRID_API_KEY for automated notifications)

### Frontend Libraries - MODERNIZED STACK
- **Next.js 15**: React framework with App Router
- **React 18**: Modern React with hooks and concurrent features
- **TypeScript**: Type safety throughout the application
- **Tailwind CSS**: Utility-first CSS framework
- **Heroicons**: Modern SVG icon library for React
- **React Hook Form**: Performant forms with easy validation
- **Zod**: TypeScript-first schema validation

### Development Tools - UPDATED
- **Next.js DevTools**: Built-in development and debugging tools
- **Prisma Studio**: Database management and visualization
- **TypeScript Compiler**: Real-time type checking and error detection
- **Tailwind IntelliSense**: Enhanced CSS development experience

### Migration Status
- **✅ Database Schema**: Fully migrated from SQLAlchemy to Prisma
- **✅ API Routes**: All Flask routes converted to Next.js API routes
- **✅ Frontend Components**: All templates converted to React components
- **✅ Forms**: All WTForms migrated to React Hook Form with Zod
- **✅ CRM System**: Complete admin dashboard in React
- **⏳ Authentication**: Ready for NextAuth.js implementation
- **✅ Responsive Design**: Improved mobile experience with Tailwind

### Project Structure
```
diversia-nextjs/
├── src/
│   ├── app/                 # Next.js App Router pages
│   │   ├── api/            # API routes (replacing Flask routes)
│   │   ├── admin/          # Admin dashboard
│   │   ├── registro/       # Registration pages
│   │   └── ...             # Other pages
│   ├── components/         # Reusable React components
│   └── lib/               # Utilities and configurations
├── prisma/                # Database schema and migrations
└── public/               # Static assets
```