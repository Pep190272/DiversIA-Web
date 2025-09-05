# 🚀 Guía de Despliegue DiversIA en Vercel

## 📋 Preparación Previa

### 1. **Configurar Repositorio GitHub**
```bash
# Inicializar repositorio Git
git init
git add .
git commit -m "Initial commit: DiversIA Flask App"

# Conectar con GitHub
git remote add origin https://github.com/tu-usuario/diversia-flask.git
git branch -M main
git push -u origin main
```

### 2. **Verificar Archivos Necesarios**
Asegúrate de que estos archivos estén en tu repositorio:
- ✅ `vercel.json` - Configuración de Vercel
- ✅ `requirements_vercel.txt` - Dependencias Python
- ✅ `app_vercel.py` - Punto de entrada para Vercel
- ✅ `.env.example` - Ejemplo de variables de entorno
- ✅ `main.py` - Aplicación Flask principal

## 🌐 Configuración en Vercel

### **Paso 1: Crear Proyecto en Vercel**
1. Ve a [vercel.com](https://vercel.com) y registrate/inicia sesión
2. Haz clic en "New Project"
3. Selecciona tu repositorio GitHub `diversia-flask`
4. Configura las siguientes opciones:

```json
Framework Preset: Other
Build Command: pip install -r requirements_vercel.txt
Output Directory: .
Install Command: pip install -r requirements_vercel.txt
```

### **Paso 2: Variables de Entorno en Vercel**
En el dashboard de Vercel, ve a Settings > Environment Variables:

```env
DATABASE_URL = postgresql://usuario:password@host:puerto/diversia_db
SESSION_SECRET = una_clave_secreta_muy_segura_de_32_caracteres
GMAIL_USER = tu_email@gmail.com
GMAIL_APP_PASSWORD = tu_password_de_app_gmail
SENDGRID_API_KEY = SG.tu_api_key_sendgrid
PYTHON_VERSION = 3.11
```

### **Paso 3: Configurar Dominio Personalizado (Opcional)**
1. En Vercel Dashboard → Settings → Domains
2. Agregar tu dominio personalizado
3. Configurar DNS según las instrucciones

## 🗄️ Migración de Base de Datos

### **Opción 1: Neon (Recomendado para Vercel)**

#### **1. Crear Base de Datos en Neon**
```bash
# Ir a https://neon.tech
# Crear nueva base de datos PostgreSQL
# Copiar la DATABASE_URL
```

#### **2. Exportar Datos desde Replit**
```sql
-- Conectar a tu base de datos actual en Replit
-- Exportar esquema y datos

-- 1. Exportar estructura de tablas
pg_dump --schema-only --no-owner --no-privileges DATABASE_URL > schema.sql

-- 2. Exportar datos
pg_dump --data-only --no-owner --no-privileges DATABASE_URL > data.sql

-- Alternativamente, exportar todo:
pg_dump --no-owner --no-privileges DATABASE_URL > full_backup.sql
```

#### **3. Importar a Neon**
```bash
# Usar la nueva DATABASE_URL de Neon
psql "postgresql://usuario:password@host:puerto/neon_db" < full_backup.sql
```

### **Opción 2: Railway**

#### **1. Crear Proyecto en Railway**
```bash
# Ir a https://railway.app
# Crear nuevo proyecto PostgreSQL
# Copiar variables de conexión
```

#### **2. Migrar Datos**
```bash
# Usar railway CLI o conexión directa
psql $RAILWAY_DATABASE_URL < full_backup.sql
```

### **Opción 3: Supabase**

#### **1. Crear Proyecto en Supabase**
```bash
# Ir a https://supabase.com
# Crear nuevo proyecto
# Ir a Settings > Database
# Copiar URI de conexión
```

#### **2. Migrar Datos**
```sql
-- Conectar con psql
psql "postgresql://postgres:password@host:port/postgres"

-- Importar backup
\i full_backup.sql
```

## 📊 Backup Manual de Datos Críticos

### **Exportar Datos de Tareas**
```sql
-- Exportar tabla de tareas
COPY tareas_empresa TO '/tmp/tareas_backup.csv' DELIMITER ',' CSV HEADER;

-- Exportar empleados
COPY empleados TO '/tmp/empleados_backup.csv' DELIMITER ',' CSV HEADER;

-- Exportar leads generales
COPY general_leads TO '/tmp/leads_backup.csv' DELIMITER ',' CSV HEADER;

-- Exportar perfiles neurodivergentes
COPY neurodivergent_profiles TO '/tmp/profiles_backup.csv' DELIMITER ',' CSV HEADER;

-- Exportar empresas
COPY companies TO '/tmp/companies_backup.csv' DELIMITER ',' CSV HEADER;
```

### **Importar Datos Manuales**
```sql
-- Importar en nueva base de datos
COPY tareas_empresa FROM '/tmp/tareas_backup.csv' DELIMITER ',' CSV HEADER;
COPY empleados FROM '/tmp/empleados_backup.csv' DELIMITER ',' CSV HEADER;
COPY general_leads FROM '/tmp/leads_backup.csv' DELIMITER ',' CSV HEADER;
COPY neurodivergent_profiles FROM '/tmp/profiles_backup.csv' DELIMITER ',' CSV HEADER;
COPY companies FROM '/tmp/companies_backup.csv' DELIMITER ',' CSV HEADER;
```

## 🔧 Script de Migración Automática

### **migration_script.py**
```python
import os
import psycopg2
from psycopg2 import sql

# URLs de base de datos
SOURCE_DB = "postgresql://user:pass@host:port/replit_db"
TARGET_DB = "postgresql://user:pass@host:port/neon_db"

def migrate_database():
    # Conectar a base origen
    source_conn = psycopg2.connect(SOURCE_DB)
    target_conn = psycopg2.connect(TARGET_DB)
    
    # Lista de tablas a migrar
    tables = [
        'tareas_empresa',
        'empleados', 
        'general_leads',
        'neurodivergent_profiles',
        'companies',
        'admins',
        'email_marketing_campaigns'
    ]
    
    for table in tables:
        print(f"Migrando tabla: {table}")
        
        # Leer datos de origen
        with source_conn.cursor() as src_cursor:
            src_cursor.execute(f"SELECT * FROM {table}")
            rows = src_cursor.fetchall()
            columns = [desc[0] for desc in src_cursor.description]
        
        # Insertar en destino
        with target_conn.cursor() as tgt_cursor:
            if rows:
                insert_query = sql.SQL("INSERT INTO {} ({}) VALUES ({})").format(
                    sql.Identifier(table),
                    sql.SQL(', ').join(map(sql.Identifier, columns)),
                    sql.SQL(', ').join(sql.Placeholder() * len(columns))
                )
                tgt_cursor.executemany(insert_query, rows)
        
        target_conn.commit()
        print(f"✅ {table}: {len(rows)} filas migradas")
    
    source_conn.close()
    target_conn.close()
    print("🎉 Migración completada!")

if __name__ == "__main__":
    migrate_database()
```

## ⚙️ Configuración Post-Despliegue

### **1. Verificar Aplicación**
```bash
# Vercel desplegará automáticamente
# URL temporal: https://tu-proyecto.vercel.app
# Verificar que carga correctamente
```

### **2. Configurar Base de Datos**
```python
# La aplicación creará tablas automáticamente
# Verificar en logs de Vercel
```

### **3. Crear Usuario Admin**
```python
# El sistema crea automáticamente:
# Usuario: admin
# Password: (configurado en el código)
```

## 🚨 Solución de Problemas

### **Error de Conexión BD**
```bash
# Verificar DATABASE_URL en Vercel
# Asegurar que la BD esté accesible públicamente
# Verificar firewall/whitelist de IP
```

### **Error de Dependencias**
```bash
# Verificar requirements_vercel.txt
# Asegurar que todas las dependencias estén listadas
# Verificar versiones compatibles
```

### **Error de Variables de Entorno**
```bash
# Verificar que SESSION_SECRET esté configurada
# Verificar DATABASE_URL válida
# Redeploy después de cambiar variables
```

## 📚 Recursos Adicionales

- **Documentación Vercel**: https://vercel.com/docs
- **Neon PostgreSQL**: https://neon.tech/docs
- **Railway**: https://docs.railway.app
- **Supabase**: https://supabase.com/docs

## 🎯 Checklist Final

- [ ] Repositorio GitHub configurado
- [ ] Archivos de Vercel creados
- [ ] Variables de entorno configuradas
- [ ] Base de datos migrada
- [ ] Aplicación desplegada
- [ ] Usuario admin verificado
- [ ] Funcionalidades probadas
- [ ] Dominio personalizado (opcional)

---

**¡Tu aplicación DiversIA estará lista en producción!** 🚀