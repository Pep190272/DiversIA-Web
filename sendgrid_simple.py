#!/usr/bin/env python3
"""
SendGrid helper simple - sin dependencias complejas
"""

def send_registration_notification(user_data, subject):
    """Función simple para notificaciones de registro"""
    print(f"📧 Notificación: {subject} - Usuario: {user_data.get('nombre', 'Sin nombre')}")
    return True

def send_company_registration_notification(company_data):
    """Función simple para notificaciones de empresa"""
    print(f"🏢 Empresa registrada: {company_data.get('nombre', 'Sin nombre')}")
    return True

def send_email(to_email, subject, content):
    """Función simple de email"""
    print(f"📧 Email: {to_email} - {subject}")
    return True