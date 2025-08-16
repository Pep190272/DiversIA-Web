# 🚀 CONFIGURACIÓN N8N - GUÍA VISUAL PASO A PASO

## ✅ TU CONFIGURACIÓN DETECTADA

**URL de tu aplicación**: `https://073083d2-dd14-424e-a549-4c03e48131b7-00-1vatfbc2lts0v.janeway.replit.dev/`

**Webhook ID**: `9ce397c7-bd6c-4a8f-ac2c-231c13b45cfa`

## 🎯 LO QUE TIENES QUE HACER

### **PASO 1: Ir a tu flujo n8n**
1. Abre tu cuenta de n8n
2. Busca el flujo "Diversia Chatbot"
3. Ábrelo para editarlo

### **PASO 2: Localizar el nodo HTTP Request**
En tu flujo verás **4 nodos en línea**:

```
[Webhook] → [Code] → [HTTP Request] → [Code1]
```

**Haz clic en el nodo "HTTP Request"** (el tercero)

### **PASO 3: Cambiar la URL**
En el nodo HTTP Request verás un campo "URL" que contiene:
```
https://tu-dominio.replit.app/api/v1/user-insights
```

**BÓRRALA COMPLETAMENTE** y escribe esta nueva URL:
```
https://073083d2-dd14-424e-a549-4c03e48131b7-00-1vatfbc2lts0v.janeway.replit.dev/api/v1/user-insights
```

### **PASO 4: Guardar y activar**
1. Haz clic en "Save" para guardar los cambios
2. Asegúrate de que el flujo esté "Active" (botón en la esquina superior)

## 🧪 PROBAR QUE FUNCIONA

### **En DiversIA**:
1. Ve a tu aplicación: `https://073083d2-dd14-424e-a549-4c03e48131b7-00-1vatfbc2lts0v.janeway.replit.dev/`
2. Haz clic en el chat widget (esquina inferior derecha)
3. Escribe: **"Hola, quiero registrarme"**
4. Deberías recibir: *"¡Perfecto! ¿Eres una persona neurodivergente buscando empleo o una empresa que quiere contratar talento diverso? 📊 Actualmente tenemos X profesionales registrados."*

### **Si NO funciona, revisa**:
1. **En n8n**: ¿Hay errores en la pestaña "Executions"?
2. **En DiversIA**: Abre F12 → Network, envía mensaje, ¿aparece petición al webhook?
3. **El flujo**: ¿Está activo el workflow?

## 🎉 SI FUNCIONA

El agente n8n ya puede:
- Detectar intenciones (registro, TDAH, TEA, dislexia, empleo)
- Obtener estadísticas reales de tu base de datos
- Dar respuestas personalizadas e inteligentes
- Tracking de usuarios para lead scoring

## 📞 TIPOS DE MENSAJES QUE ENTIENDE

| **Escribe esto** | **Respuesta del agente** |
|------------------|--------------------------|
| "registro" | Pregunta si eres persona neurodivergente o empresa |
| "tdah" | Información sobre formularios TDAH especializados |
| "tea" o "autismo" | Info sobre evaluaciones TEA y matching |
| "dislexia" | Tests especializados y conexión con DISFAM |
| "trabajo" o "empleo" | Sistema de matching de candidatos |
| Cualquier otro | Mensaje de bienvenida con opciones |

¡Todo está listo para funcionar! Solo necesitas cambiar esa URL en n8n.