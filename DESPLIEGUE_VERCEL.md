# Guía de Despliegue en Vercel

## ✅ Preparación para Vercel

### Archivos creados:
1. **vercel.json** - Configuración de Vercel para Flask
2. **Páginas legales** - Política de Privacidad, Términos y Aviso Legal
3. **Casillas de privacidad** - Agregadas a todos los formularios

### ⚙️ Variables de entorno requeridas en Vercel:

```bash
# Base de datos
DATABASE_URL=postgresql://...

# Email
SENDGRID_API_KEY=tu_clave_sendgrid

# Flask
FLASK_ENV=production
SESSION_SECRET=clave_secreta_aleatoria

# AI (opcional)
MISTRAL_API_KEY=tu_clave_mistral

# Notion (opcional)
NOTION_INTEGRATION_SECRET=tu_secreto_notion
NOTION_DATABASE_ID=tu_id_base_datos
```

## 🚀 Pasos para desplegar:

### 1. Configurar base de datos:
- Crear base de datos PostgreSQL en Supabase, Railway o Neon
- Copiar la URL de conexión

### 2. Configurar Vercel:
1. Conecta tu repositorio GitHub a Vercel
2. Agrega las variables de entorno
3. Deploy automático

### 3. Verificar funcionalidades:
- [ ] Chat funcionando
- [ ] Formularios con casillas de privacidad
- [ ] Metricool detectando visitas
- [ ] n8n recibiendo datos

## 🔧 Post-despliegue:

### Para Metricool:
1. Ve a "Conectar tu Web" en Metricool
2. Usa el dominio real de Vercel para verificación
3. El script ya está integrado y funcionará automáticamente

### Para n8n:
1. Cambia a "Production URL" en el webhook
2. Actualiza la URL en el JavaScript si es necesario
3. Activa el workflow en modo producción

## 📋 Checklist final:
- [ ] Base de datos configurada
- [ ] Variables de entorno en Vercel
- [ ] Dominio personalizado (opcional)
- [ ] SSL activo (automático en Vercel)
- [ ] Metricool verificado
- [ ] n8n webhook activo
- [ ] Chat respondiendo con información de DiversIA
- [ ] Formularios funcionando con políticas

La aplicación está lista para producción con todas las funcionalidades implementadas.