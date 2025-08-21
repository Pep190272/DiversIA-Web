#!/usr/bin/env python3
"""
Monitor de salud del sistema DiversIA
Previene errores 500 detectando campos faltantes ANTES de que causen fallos
"""

import os
import re
from pathlib import Path

def check_template_form_fields():
    """Verifica que todos los campos usados en templates estén definidos en forms.py"""
    templates_dir = Path('templates')
    forms_file = Path('forms.py')
    
    if not forms_file.exists():
        print("❌ forms.py no encontrado!")
        return False
    
    # Leer el contenido de forms.py
    with open(forms_file, 'r', encoding='utf-8') as f:
        forms_content = f.read()
    
    errors = []
    success_count = 0
    
    # Verificar cada template HTML
    for template_file in templates_dir.glob('*.html'):
        if template_file.name.startswith('base.'):
            continue
            
        with open(template_file, 'r', encoding='utf-8') as f:
            template_content = f.read()
        
        # Buscar referencias a campos de formularios (form.campo)
        field_pattern = r'form\.([a-zA-Z_][a-zA-Z0-9_]*)'
        fields_used = set(re.findall(field_pattern, template_content))
        
        # Filtrar campos especiales que no son campos de datos
        special_fields = {'hidden_tag', 'csrf_token', 'errors', 'data'}
        fields_used = fields_used - special_fields
        
        template_errors = []
        for field in fields_used:
            # Verificar si el campo está definido en forms.py
            if f'{field} =' not in forms_content and f'{field}(' not in forms_content:
                template_errors.append(field)
        
        if template_errors:
            errors.append(f"❌ {template_file.name}: campos faltantes {template_errors}")
        else:
            success_count += 1
            print(f"✅ {template_file.name}: OK")
    
    if errors:
        print(f"\n🚨 {len(errors)} TEMPLATES CON ERRORES:")
        for error in errors:
            print(error)
        return False
    else:
        print(f"\n🎉 TODOS LOS {success_count} TEMPLATES VERIFICADOS - SIN ERRORES")
        return True

def check_route_existence():
    """Verifica que todas las rutas críticas estén definidas"""
    routes_file = Path('routes.py')
    
    critical_routes = [
        '/test', '/comenzar', '/registro', '/registro-tdah', 
        '/registro-tea', '/registro-dislexia', '/empresas'
    ]
    
    if not routes_file.exists():
        print("❌ routes.py no encontrado!")
        return False
    
    with open(routes_file, 'r', encoding='utf-8') as f:
        routes_content = f.read()
    
    missing_routes = []
    for route in critical_routes:
        if f"@app.route('{route}'" not in routes_content:
            missing_routes.append(route)
    
    if missing_routes:
        print(f"❌ Rutas faltantes: {missing_routes}")
        return False
    else:
        print("✅ Todas las rutas críticas están definidas")
        return True

def main():
    """Ejecuta todas las verificaciones de salud del sistema"""
    print("🏥 MONITOR DE SALUD DEL SISTEMA DIVERSIA")
    print("=" * 50)
    
    all_checks_passed = True
    
    print("\n1. Verificando campos de formularios...")
    if not check_template_form_fields():
        all_checks_passed = False
    
    print("\n2. Verificando rutas críticas...")
    if not check_route_existence():
        all_checks_passed = False
    
    print("\n" + "=" * 50)
    if all_checks_passed:
        print("🎉 SISTEMA SALUDABLE - TODOS LOS CHECKS PASARON")
        return True
    else:
        print("🚨 SISTEMA CON PROBLEMAS - REVISAR ERRORES ARRIBA")
        return False

if __name__ == "__main__":
    main()