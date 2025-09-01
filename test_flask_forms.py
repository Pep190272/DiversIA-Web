#!/usr/bin/env python3
"""
Test automatizado de todos los formularios de DiversIA (Flask)
Este script probará que todos los formularios envíen emails correctamente
"""

import requests
import time
from datetime import datetime

# URL base del servidor Flask
BASE_URL = 'http://localhost:5000'

# Datos de prueba para cada formulario
test_data = {
    'registro': {
        'nombre': 'María',
        'apellidos': 'García López',
        'email': 'test.diversia.registro@gmail.com',
        'telefono': '555-0123',
        'ciudad': 'Madrid',
        'fecha_nacimiento': '1995-05-15',
        'tipo_neurodivergencia': 'tdah',
        'diagnostico_formal': 'si',
        'habilidades': 'Programación, análisis de datos',
        'experiencia_laboral': '3 años en desarrollo web',
        'formacion_academica': 'Ingeniería Informática',
        'intereses_laborales': 'Desarrollo frontend, UX/UI',
        'adaptaciones_necesarias': 'Horarios flexibles',
        'motivaciones': 'Busco un ambiente inclusivo',
        'aceptar_privacidad': 'y'
    },
    
    'registro-tdah': {
        'nombre': 'Carlos',
        'apellidos': 'Ruiz Martín',
        'email': 'test.diversia.tdah@gmail.com',
        'telefono': '555-0124',
        'ciudad': 'Barcelona',
        'fecha_nacimiento': '1992-08-20',
        'diagnostico_formal': 'si',
        'habilidades': 'Creatividad, resolución de problemas',
        'experiencia_laboral': '5 años en marketing digital',
        'formacion_academica': 'Licenciatura en Marketing',
        'intereses_laborales': 'Marketing creativo, estrategia digital',
        'adaptaciones_necesarias': 'Espacios sin distracciones',
        'motivaciones': 'Quiero usar mi creatividad al máximo',
        'tipo_tdah': 'combinado',
        'nivel_atencion': 'medio',
        'impulsividad': 'alto',
        'hiperactividad': 'medio',
        'medicacion': 'si'
    },

    'empresas': {
        'nombre_empresa': 'TechInclusiva SL',
        'email_contacto': 'test.diversia.empresa@gmail.com',
        'telefono': '555-0125',
        'ciudad': 'Valencia',
        'sector': 'tecnologia',
        'tamano_empresa': 'mediana',
        'website': 'https://techinclusiva.es',
        'descripcion': 'Empresa tecnológica comprometida con la diversidad',
        'experiencia_inclusion': 'Tenemos políticas específicas para neurodiversidad',
        'aceptar_privacidad': 'y'
    }
}

def test_form(form_name, data):
    """Probar un formulario específico"""
    url = f"{BASE_URL}/{form_name}"
    
    print(f"\n🧪 Probando formulario: {form_name}")
    print(f"   URL: {url}")
    
    try:
        # Hacer petición POST
        response = requests.post(url, data=data, allow_redirects=False)
        
        # Verificar respuesta
        if response.status_code in [200, 302]:  # Éxito o redirección
            print(f"✅ {form_name}: Formulario enviado correctamente")
            if response.status_code == 302:
                print(f"   → Redirigido a: {response.headers.get('Location', 'Desconocido')}")
            return True
        else:
            print(f"❌ {form_name}: Error HTTP {response.status_code}")
            print(f"   → Respuesta: {response.text[:200]}...")
            return False
            
    except requests.exceptions.ConnectionError:
        print(f"❌ {form_name}: Error de conexión - ¿Está el servidor corriendo?")
        return False
    except Exception as e:
        print(f"❌ {form_name}: Error inesperado - {e}")
        return False

def test_email_endpoint():
    """Probar el endpoint de test de emails"""
    try:
        # Importar y probar la función directamente
        from flask_email_service import test_email_service
        print("\n🧪 Probando servicio de emails...")
        
        if test_email_service():
            print("✅ Test de email: Email de prueba enviado correctamente")
            return True
        else:
            print("❌ Test de email: Error enviando email de prueba")
            return False
            
    except Exception as e:
        print(f"❌ Test de email: Error - {e}")
        return False

def main():
    """Función principal"""
    print("🚀 Iniciando pruebas de formularios DiversIA (Flask)")
    print("=" * 60)
    print(f"📧 Los emails se enviarán a: diversiaeternals@gmail.com")
    print(f"🔔 También se enviarán emails de bienvenida a cada usuario/empresa")
    print("=" * 60)
    
    # Probar servicio de emails primero
    email_working = test_email_endpoint()
    
    # Probar formularios
    results = []
    
    for form_name, data in test_data.items():
        success = test_form(form_name, data)
        results.append((form_name, success))
        
        # Esperar un poco entre pruebas
        time.sleep(2)
    
    # Mostrar resumen
    print("\n" + "=" * 60)
    print("📊 RESUMEN DE PRUEBAS")
    print("=" * 60)
    
    successful = 0
    for form_name, success in results:
        status = "✅ EXITOSO" if success else "❌ FALLIDO"
        print(f"{status:12} {form_name}")
        if success:
            successful += 1
    
    print("=" * 60)
    print(f"📧 Servicio de emails: {'✅ FUNCIONANDO' if email_working else '❌ FALLIDO'}")
    print(f"📝 Formularios: {successful}/{len(results)} funcionando correctamente")
    print(f"⏰ Hora de prueba: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}")
    
    if successful == len(results) and email_working:
        print("\n🎉 ¡TODOS LOS SISTEMAS ESTÁN FUNCIONANDO!")
        print("📧 Revisa la bandeja de entrada de diversiaeternals@gmail.com")
        print("✨ Sistema de emails automáticos completamente configurado")
    else:
        print("\n⚠️  Algunos sistemas necesitan atención")
        
        if not email_working:
            print("🔧 Revisar configuración de Gmail (GMAIL_USER y GMAIL_APP_PASSWORD)")
        
        failed_forms = [name for name, success in results if not success]
        if failed_forms:
            print(f"🔧 Formularios que requieren atención: {', '.join(failed_forms)}")

if __name__ == "__main__":
    main()