#!/usr/bin/env python3
"""
Sistema de pruebas completo para DiversIA
Verifica email, CRM y base de datos
"""

import requests
import json
from datetime import datetime

def test_email_system():
    """Prueba el sistema de emails directamente"""
    print("📧 Probando sistema de emails...")
    try:
        from sendgrid_helper import send_email
        result = send_email(
            'diversiaeternals@gmail.com', 
            '🧪 Test DiversIA - Sistema Funcional', 
            '''
            <h2>✅ Sistema DiversIA Funcionando</h2>
            <p><strong>Fecha:</strong> {}</p>
            <p><strong>Base de datos:</strong> SQLite (Confiable)</p>
            <p><strong>CRM:</strong> Operacional</p>
            <p><strong>Emails:</strong> Funcionando</p>
            <hr>
            <p>Este es un email de prueba del sistema completo.</p>
            '''.format(datetime.now().strftime('%d/%m/%Y %H:%M'))
        )
        print(f"✅ Email enviado: {result}")
        return result
    except Exception as e:
        print(f"❌ Error email: {e}")
        return False

def test_crm_system():
    """Prueba el sistema CRM"""
    print("📊 Probando sistema CRM...")
    try:
        response = requests.get('http://localhost:5000/api/stats-working')
        if response.status_code == 200:
            data = response.json()
            print(f"✅ CRM Stats: {data}")
            return data
        else:
            print(f"❌ CRM Error: {response.status_code}")
            return None
    except Exception as e:
        print(f"❌ Error CRM: {e}")
        return None

def test_form_submission():
    """Simula envío de formulario de empresa"""
    print("📝 Probando envío de formulario...")
    try:
        form_data = {
            'nombre_empresa': 'Test Company Emails',
            'email_contacto': 'test@testcompany.com',
            'telefono': '600123456',
            'sector': 'Tecnología',
            'tamano_empresa': 'media',
            'ciudad': 'Madrid',
            'descripcion_empresa': 'Empresa de prueba del sistema de notificaciones',
            'aceptar_privacidad': 'on'
        }
        
        response = requests.post('http://localhost:5000/empresas', data=form_data)
        print(f"✅ Formulario enviado: {response.status_code}")
        return response.status_code == 302  # Redirect después de éxito
    except Exception as e:
        print(f"❌ Error formulario: {e}")
        return False

def test_job_offer_submission():
    """Simula envío de oferta de trabajo"""
    print("💼 Probando envío de oferta de trabajo...")
    try:
        offer_data = {
            'titulo_puesto': 'Desarrollador Python (Test)',
            'descripcion': 'Posición de prueba para verificar notificaciones por email',
            'tipo_contrato': 'indefinido',
            'modalidad_trabajo': 'remoto',
            'salario_min': '30000',
            'salario_max': '45000',
            'requisitos': 'Python, Flask, Experiencia con personas neurodivergentes',
            'adaptaciones_disponibles': 'Horarios flexibles, trabajo remoto, entorno silencioso',
            'neurodivergencias_target': ['tdah', 'tea']
        }
        
        response = requests.post('http://localhost:5000/ofertas-empleo', data=offer_data)
        print(f"✅ Oferta enviada: {response.status_code}")
        return response.status_code == 302
    except Exception as e:
        print(f"❌ Error oferta: {e}")
        return False

def main():
    print("🚀 INICIANDO PRUEBAS COMPLETAS DEL SISTEMA DIVERSIA")
    print("=" * 60)
    
    # Prueba 1: Sistema de emails
    email_ok = test_email_system()
    print()
    
    # Prueba 2: Sistema CRM
    crm_data = test_crm_system()
    print()
    
    # Prueba 3: Formulario empresa
    form_ok = test_form_submission()
    print()
    
    # Prueba 4: Oferta trabajo
    offer_ok = test_job_offer_submission()
    print()
    
    # Resumen
    print("📋 RESUMEN DE PRUEBAS:")
    print("=" * 30)
    print(f"📧 Emails: {'✅ OK' if email_ok else '❌ FAIL'}")
    print(f"📊 CRM: {'✅ OK' if crm_data else '❌ FAIL'}")
    print(f"📝 Formulario: {'✅ OK' if form_ok else '❌ FAIL'}")
    print(f"💼 Ofertas: {'✅ OK' if offer_ok else '❌ FAIL'}")
    
    if email_ok and crm_data and form_ok and offer_ok:
        print("\n🎉 SISTEMA COMPLETAMENTE FUNCIONAL")
        print("Revisa tu email: diversiaeternals@gmail.com")
    else:
        print("\n⚠️ ALGUNOS SISTEMAS REQUIEREN ATENCIÓN")

if __name__ == "__main__":
    main()