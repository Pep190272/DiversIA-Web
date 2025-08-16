# 🔧 CONFIGURACIÓN N8N WEBHOOK - ANÁLISIS DEL FLUJO

## ✅ ESTADO ACTUAL DEL FLUJO

Tu flujo de n8n está **configurado correctamente**:

### **Webhook ID detectado**: `9ce397c7-bd6c-4a8f-ac2c-231c13b45cfa`
### **Path configurado**: `/diversia-chat`
### **URL completa**: `https://hooks.n8n.cloud/webhook/9ce397c7-bd6c-4a8f-ac2c-231c13b45cfa`

## 🔍 PROBLEMA IDENTIFICADO

En tu flujo n8n, el nodo HTTP Request tiene esta URL:
```
https://tu-dominio.replit.app/api/v1/user-insights
```

**NECESITAS CAMBIARLA** por la URL real de tu aplicación.

## 🛠️ SOLUCIÓN PASO A PASO

### **1. URL de tu aplicación Replit**
Tu aplicación está en:
```
https://073083d2-dd14-424e-a549-4c03e48131b7-00-1vatfbc2lts0v.janeway.replit.dev/
```

### **2. Actualizar el nodo HTTP Request en n8n**
Cambiar de:
```
https://tu-dominio.replit.app/api/v1/user-insights
```

A:
```
https://073083d2-dd14-424e-a549-4c03e48131b7-00-1vatfbc2lts0v.janeway.replit.dev/api/v1/user-insights
```

### **3. El chat ya está configurado**
El chat widget ya tiene la URL correcta del webhook:
```javascript
const n8nWebhookUrl = 'https://hooks.n8n.cloud/webhook/9ce397c7-bd6c-4a8f-ac2c-231c13b45cfa';
```

## 🔄 FLUJO DE FUNCIONAMIENTO

1. **Usuario escribe mensaje** → Chat widget
2. **Chat envía POST** → `https://hooks.n8n.cloud/webhook/9ce397c7-bd6c-4a8f-ac2c-231c13b45cfa`
3. **n8n procesa mensaje** → Nodo Code (detecta intención)
4. **n8n obtiene datos** → HTTP Request a tu API `/api/v1/user-insights`
5. **n8n combina respuesta** → Nodo Code1 (respuesta final)
6. **Chat recibe respuesta** → Muestra al usuario

## 🧪 CÓMO PROBAR

### **Paso 1**: Actualizar URL en n8n
1. Abre tu flujo en n8n
2. Clic en nodo "HTTP Request"
3. Cambia la URL por tu dominio real de Replit
4. Guarda el flujo

### **Paso 2**: Probar en DiversIA
1. Ve a tu aplicación
2. Haz clic en el chat widget (esquina inferior derecha)
3. Escribe: "Hola, quiero registrarme"
4. Deberías recibir respuesta del agente n8n

## 📋 RESPUESTAS ESPERADAS

El agente detecta estas intenciones:
- **"registro"** → Pregunta si eres persona neurodivergente o empresa
- **"tdah"** → Información sobre TDAH y formularios especializados
- **"tea"** → Información sobre TEA y matching
- **"dislexia"** → Información sobre dislexia y recursos
- **"empresa"** → Información para empresas inclusivas
- **General** → Mensaje de bienvenida con opciones

## 🚨 SI NO FUNCIONA

### **Verificar en n8n**:
1. ¿El workflow está activo? (botón "Activate")
2. ¿La URL del HTTP Request es correcta?
3. ¿Hay errores en la pestaña "Executions"?

### **Verificar en DiversIA**:
1. Abre herramientas de desarrollador (F12)
2. Ve a la pestaña "Network"
3. Envía un mensaje en el chat
4. ¿Aparece una petición al webhook?
5. ¿Cuál es el código de respuesta?

## 🎯 PRÓXIMOS PASOS

Una vez funcionando:
1. **Personalizar respuestas** en el nodo Code
2. **Añadir más endpoints** de tu API
3. **Configurar lead scoring** automático
4. **Integrar con CRM** si tienes uno

## 🎯 CONFIGURACIÓN FINAL

### **PASO 1: Actualizar n8n**
1. Ve a tu flujo en n8n
2. Haz clic en el nodo "HTTP Request" (el tercero)
3. Cambia la URL a: `https://073083d2-dd14-424e-a549-4c03e48131b7-00-1vatfbc2lts0v.janeway.replit.dev/api/v1/user-insights`
4. Guarda el flujo

### **PASO 2: Probar el chat**
1. Ve a tu aplicación DiversIA
2. Haz clic en el chat widget (esquina inferior derecha)
3. Escribe: "Hola, quiero información sobre registro"
4. Deberías recibir respuesta del agente n8n con estadísticas