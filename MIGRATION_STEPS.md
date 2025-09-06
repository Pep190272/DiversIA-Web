
# PASOS PARA MIGRAR A VERCEL

## 1. CREAR BASE DE DATOS EN NEON
# Ve a https://neon.tech
# Crea nuevo proyecto PostgreSQL
# Copia la DATABASE_URL que se genere

## 2. EXPORTAR DATOS DESDE REPLIT
# Ejecuta estos comandos en el Shell de Replit:
pg_dump "https://kv.replit.com/v0/eyJhbGciOiJIUzUxMiIsImlzcyI6ImNvbm1hbiIsImtpZCI6InByb2Q6MSIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJjb25tYW4iLCJleHAiOjE3NTcyNTgxNTIsImlhdCI6MTc1NzE0NjU1MiwiZGF0YWJhc2VfaWQiOiIwNzMwODNkMi1kZDE0LTQyNGUtYTU0OS00YzAzZTQ4MTMxYjcifQ.0dKO0xmW-K9JdMOAOpEj1qv2wxCIKkKQPDHnmqHUOdpEYyqeJBtWBWukqkZBTV2B1bQ1JUfdKM7dnPqjtXQSBw" > diversia_backup.sql

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
