
#!/usr/bin/env python3
"""
Script de migración de DiversIA de Replit a Vercel
Exporta datos actuales y prepara configuración para despliegue
"""

import os
import json
import sys
from datetime import datetime

def main():
    print("🚀 MIGRACIÓN DIVERSIA: REPLIT → VERCEL")
    print("=" * 50)
    
    # 1. Verificar conexión actual a BD
    print("\n📊 1. VERIFICANDO CONEXIÓN ACTUAL...")
    db_url = os.getenv("REPLIT_DB_URL")
    if db_url:
        print(f"✅ BD Replit conectada: {db_url[:50]}...")
    else:
        print("❌ No se encuentra REPLIT_DB_URL")
        return
    
    # 2. Exportar configuración actual
    print("\n⚙️ 2. EXPORTANDO CONFIGURACIÓN...")
    
    config_export = {
        "migration_date": datetime.now().isoformat(),
        "source": "Replit",
        "target": "Vercel",
        "database_type": "PostgreSQL", 
        "replit_db_url": db_url,
        "environment_vars": {
            "SESSION_SECRET": "REQUIRED_TO_SET_IN_VERCEL",
            "GMAIL_USER": os.getenv("GMAIL_USER", "NOT_SET"),
            "GMAIL_APP_PASSWORD": "REQUIRED_TO_SET_IN_VERCEL",
            "SENDGRID_API_KEY": "REQUIRED_TO_SET_IN_VERCEL"
        },
        "required_services": [
            "Neon PostgreSQL",
            "Vercel Hosting",
            "GitHub Repository"
        ]
    }
    
    with open("migration_config.json", "w") as f:
        json.dump(config_export, f, indent=2)
    print("✅ Configuración exportada a migration_config.json")
    
    # 3. Generar comandos de migración
    print("\n📝 3. GENERANDO COMANDOS DE MIGRACIÓN...")
    
    migration_commands = f"""
# PASOS PARA MIGRAR A VERCEL

## 1. CREAR BASE DE DATOS EN NEON
# Ve a https://neon.tech
# Crea nuevo proyecto PostgreSQL
# Copia la DATABASE_URL que se genere

## 2. EXPORTAR DATOS DESDE REPLIT
# Ejecuta estos comandos en el Shell de Replit:
pg_dump "{db_url}" > diversia_backup.sql

## 3. CONFIGURAR GITHUB
git init
git add .
git commit -m "Initial commit: DiversIA migration to Vercel"
git remote add origin https://github.com/TU_USUARIO/diversia-vercel.git
git push -u origin main

## 4. CONFIGURAR VERCEL
# Ve a https://vercel.com
# Conecta tu repositorio GitHub
# Configura estas variables de entorno:

DATABASE_URL=postgresql://usuario:password@host:puerto/neon_db
SESSION_SECRET=una_clave_muy_segura_de_32_caracteres_minimo
GMAIL_USER=tu_email@gmail.com
GMAIL_APP_PASSWORD=tu_password_de_aplicacion_gmail
SENDGRID_API_KEY=SG.tu_api_key_de_sendgrid

## 5. IMPORTAR DATOS A NEON
psql "postgresql://usuario:password@host:puerto/neon_db" < diversia_backup.sql

## 6. VERIFICAR DESPLIEGUE
# Tu app estará en: https://tu-proyecto.vercel.app
"""
    
    with open("MIGRATION_STEPS.md", "w") as f:
        f.write(migration_commands)
    print("✅ Pasos de migración generados en MIGRATION_STEPS.md")
    
    # 4. Verificar archivos necesarios para Vercel
    print("\n🔍 4. VERIFICANDO ARCHIVOS PARA VERCEL...")
    
    required_files = [
        "vercel.json",
        "requirements_vercel.txt", 
        "app_vercel.py",
        "main.py"
    ]
    
    for file in required_files:
        if os.path.exists(file):
            print(f"✅ {file} - OK")
        else:
            print(f"❌ {file} - FALTA")
    
    # 5. Mostrar resumen
    print("\n📋 5. RESUMEN DE MIGRACIÓN")
    print("=" * 30)
    print("✅ Configuración exportada")
    print("✅ Comandos de migración generados") 
    print("✅ Archivos de Vercel verificados")
    print("\n🎯 PRÓXIMOS PASOS:")
    print("1. Lee el archivo MIGRATION_STEPS.md")
    print("2. Crea una base de datos en Neon (https://neon.tech)")
    print("3. Sube tu código a GitHub")
    print("4. Configura el proyecto en Vercel")
    print("5. Importa los datos a la nueva BD")
    
    print("\n🌟 Tu aplicación DiversIA está lista para ser migrada!")

if __name__ == "__main__":
    main()
