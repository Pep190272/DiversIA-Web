#!/usr/bin/env python3
"""
Importación limpia del CSV - Solo registros válidos
"""

import csv
from app import app, db
from models import EmailMarketing
from datetime import datetime

def import_clean_csv():
    with app.app_context():
        # Limpiar tabla
        EmailMarketing.query.delete()
        db.session.commit()
        
        imported_count = 0
        skipped_count = 0
        
        with open('attached_assets/Email Marketing España - ENVIADOS_1755860793507.csv', 'r', encoding='utf-8') as f:
            csv_reader = csv.DictReader(f)
            
            for row_num, row in enumerate(csv_reader, 1):
                # Validar datos esenciales
                asociacion = row.get('Asociación', '').strip()
                email = row.get('Email', '').strip()
                
                # Saltar filas vacías o sin datos válidos
                if not asociacion or len(asociacion) < 3:
                    print(f"Fila {row_num}: SALTADA - Sin asociación válida")
                    skipped_count += 1
                    continue
                
                # Limpiar email
                if email.startswith('mailto:'):
                    email = email[7:]
                
                # Validar email
                if not email or '@' not in email:
                    print(f"Fila {row_num}: SALTADA - Email inválido: '{email}'")
                    skipped_count += 1
                    continue
                
                # Crear contacto válido
                new_contact = EmailMarketing(
                    comunidad_autonoma = row.get('Comunidad Autónoma', '').strip(),
                    asociacion = asociacion,
                    email = email,
                    telefono = row.get('Teléfono', '').strip(),
                    direccion = row.get('Dirección', '').strip(),
                    servicios = row.get('Servicios', '').strip(),
                    fecha_enviado = row.get('Envios', '').strip(),
                    respuesta = row.get('Respuestas', '').strip(),
                    notas_especiales = ''
                )
                
                db.session.add(new_contact)
                imported_count += 1
                
                if imported_count <= 5:  # Mostrar primeros 5
                    print(f"✓ {imported_count:3d}. {asociacion} - {email}")
        
        db.session.commit()
        
        print(f"\n✅ IMPORTACIÓN COMPLETA:")
        print(f"   📊 Importados: {imported_count} contactos válidos")
        print(f"   ⚠️  Saltados: {skipped_count} filas vacías/inválidas")
        print(f"   📋 Total procesado: {imported_count + skipped_count} filas")
        
        # Verificar respuestas
        with_responses = EmailMarketing.query.filter(
            EmailMarketing.respuesta != ''
        ).filter(
            EmailMarketing.respuesta.isnot(None)
        ).all()
        
        print(f"   💬 Con respuestas: {len(with_responses)} contactos")
        
        return imported_count

if __name__ == "__main__":
    result = import_clean_csv()
    print(f"Resultado final: {result} contactos importados correctamente")