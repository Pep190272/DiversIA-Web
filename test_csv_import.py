#!/usr/bin/env python3
"""
Script para probar importación del CSV con respuestas
"""

import csv
import io
from app import app, db
from models import EmailMarketing
from datetime import datetime

# Datos de prueba simulando el CSV
test_csv_data = '''Comunidad Autónoma,Asociación,Email,Teléfono,Dirección,Servicios,ENVIADOS,RESPUESTA
Cantabria,ACAL Cantabria,contacto@acalcantabria.org,+34942222334,Santander,"Asociación de altas capacidades Cantabria, talleres educativos",31/07/2025,ESTAN DE VACACIONES HASTA 24 AGOSTO
Andalucía,ACODAH Córdoba,acodah@gmail.com,+34625263515,"Av. La Alameda 1, Puente Genil, Córdoba","Apoyo a familias, talleres",30/07/2025,VACACIONES HASTA EL 1 SEPTIEMBRE
Galicia,ADAHPO Pontevedra,adahpo@hotmail.es,886204436,"C/ Rosalía de Castro 36, Pontevedra","Apoyo global, formación, defensa de derechos",30/07/2025,HAY UN CORREO NUEVO LO ENVIO DE NUEVO'''

def test_csv_import():
    with app.app_context():
        print("🧪 PROBANDO IMPORTACIÓN CSV")
        
        # Limpiar tabla
        EmailMarketing.query.delete()
        db.session.commit()
        
        # Simular archivo CSV
        csv_file = io.StringIO(test_csv_data)
        csv_reader = csv.DictReader(csv_file)
        
        imported_count = 0
        
        for row in csv_reader:
            new_contact = EmailMarketing(
                comunidad_autonoma = row.get('Comunidad Autónoma', ''),
                asociacion = row.get('Asociación', ''),
                email = row.get('Email', '').strip(),
                telefono = row.get('Teléfono', ''),
                direccion = row.get('Dirección', ''),
                servicios = row.get('Servicios', ''),
                fecha_enviado = row.get('ENVIADOS', ''),
                respuesta = row.get('RESPUESTA', ''),  # CLAVE: Columna respuesta
                notas_especiales = ''
            )
            db.session.add(new_contact)
            imported_count += 1
            print(f"  ✓ Importado: {new_contact.asociacion} - Respuesta: '{new_contact.respuesta}'")
        
        db.session.commit()
        print(f"✅ IMPORTADOS: {imported_count} contactos con respuestas")
        
        # Verificar
        all_contacts = EmailMarketing.query.all()
        print(f"✅ TOTAL EN DB: {len(all_contacts)} contactos")
        
        for contact in all_contacts:
            if contact.respuesta:
                print(f"  📧 {contact.asociacion}: '{contact.respuesta}'")

if __name__ == "__main__":
    test_csv_import()