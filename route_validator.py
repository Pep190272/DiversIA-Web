#!/usr/bin/env python3
"""
Sistema de validación automática de rutas para prevenir errores 500
Este script verifica que todas las rutas principales funcionen correctamente
"""

import subprocess
import sys

# Rutas críticas que NUNCA deben fallar
CRITICAL_ROUTES = [
    '/',
    '/empresas', 
    '/personas-nd',
    '/comunidad',
    '/registro',
    '/registro-tdah',
    '/registro-tea', 
    '/registro-dislexia',
    '/test',
    '/comenzar'
]

def validate_routes(base_url="http://localhost:5000"):
    """Valida todas las rutas críticas usando curl"""
    results = {}
    errors = []
    
    print("🔍 Validando rutas críticas...")
    
    for route in CRITICAL_ROUTES:
        url = f"{base_url}{route}"
        try:
            # Usar curl para verificar el status code
            result = subprocess.run(['curl', '-s', '-o', '/dev/null', '-w', '%{http_code}', url], 
                                  capture_output=True, text=True, timeout=5)
            status_code = int(result.stdout.strip())
            results[route] = status_code
            
            # 200 = OK, 302 = Redirect (también válido)
            if status_code in [200, 302]:
                print(f"✅ {route}: {status_code}")
            else:
                errors.append(f"❌ {route}: {status_code}")
                print(f"❌ {route}: {status_code}")
                
        except Exception as e:
            results[route] = f"ERROR: {e}"
            errors.append(f"❌ {route}: {e}")
            print(f"❌ {route}: {e}")
    
    if errors:
        print(f"\n🚨 {len(errors)} ERRORES ENCONTRADOS:")
        for error in errors:
            print(error)
        return False
    else:
        print(f"\n🎉 TODAS LAS {len(CRITICAL_ROUTES)} RUTAS FUNCIONAN CORRECTAMENTE")
        return True

if __name__ == "__main__":
    validate_routes()