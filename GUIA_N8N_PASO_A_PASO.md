# 🔧 CONFIGURACIÓN N8N - PASO A PASO

## ✅ VERIFICAR QUE TODO FUNCIONA

### 1. **Ver el Chat Widget**
El chat debería aparecer como un círculo morado en la esquina inferior derecha con "¡Hola!"

Si no lo ves:
- Abre las herramientas de desarrollador (F12)
- Ve a la consola y busca errores
- Debería aparecer: "Chat widget initialized"

### 2. **Probar los Endpoints**
Abre una nueva pestaña y prueba:
```
https://tu-dominio.replit.app/api/v1/users
```
Deberías ver 5 usuarios con datos reales.

## 🚀 CONFIGURACIÓN N8N

### **PASO 1: Crear Workflow**

1. **Entra a tu n8n**
2. **Crea nuevo workflow**
3. **Nombra el workflow**: "DiversIA Chat Bot"

### **PASO 2: Añadir Nodos**

#### **Nodo 1: Webhook**
```
Tipo: Webhook
HTTP Method: POST
Path: /diversia-chat
Authentication: None
```

#### **Nodo 2: Code (JavaScript)**
```javascript
// Código para procesar el mensaje
const mensaje = $input.first().json.body.message || '';
const usuario = $input.first().json.body.user_id || 'visitante';

let respuesta = '';
let intent = 'general';

// Detectar intención
if (mensaje.toLowerCase().includes('registro')) {
  intent = 'registro';
  respuesta = '¡Perfecto! ¿Eres una persona neurodivergente buscando empleo o una empresa que quiere contratar talento diverso?';
} else if (mensaje.toLowerCase().includes('tdah')) {
  intent = 'tdah';
  respuesta = 'TDAH es una neurodivergencia que apoyamos. Tenemos formularios especializados y tests gamificados. ¿Quieres registrarte?';
} else if (mensaje.toLowerCase().includes('tea') || mensaje.toLowerCase().includes('autismo')) {
  intent = 'tea';
  respuesta = 'Para TEA ofrecemos evaluaciones adaptadas y matching con empresas inclusivas. ¿Necesitas más información?';
} else if (mensaje.toLowerCase().includes('dislexia')) {
  intent = 'dislexia';
  respuesta = 'Tenemos tests especializados para dislexia y conexión con asociaciones como DISFAM. ¿Te interesa?';
} else if (mensaje.toLowerCase().includes('trabajo') || mensaje.toLowerCase().includes('empleo')) {
  intent = 'empleo';
  respuesta = 'Nuestro sistema de matching conecta candidatos con ofertas compatibles. ¿Cuál es tu experiencia?';
} else {
  respuesta = '¡Hola! Soy el asistente de DiversIA. Puedo ayudarte con registro, información sobre TDAH/TEA/Dislexia, o búsqueda de empleo. ¿En qué te ayudo?';
}

return {
  respuesta: respuesta,
  intent: intent,
  usuario: usuario,
  mensaje_original: mensaje
};
```

#### **Nodo 3: HTTP Request (Opcional - Datos dinámicos)**
```
Method: GET
URL: https://tu-dominio.replit.app/api/v1/user-insights
Headers: Content-Type: application/json
```

#### **Nodo 4: Code (Respuesta final)**
```javascript
const respuestaBase = $input.first().json.respuesta;
const intent = $input.first().json.intent;

// Intentar obtener estadísticas (si el HTTP Request funcionó)
let stats = '';
try {
  const insights = $input.last().json.insights;
  if (insights && intent === 'registro') {
    stats = `\n\n📊 Actualmente tenemos ${insights.total_users} profesionales registrados.`;
  }
} catch (e) {
  // Ignorar si no hay datos
}

return {
  response: respuestaBase + stats,
  final_response: respuestaBase + stats
};
```

### **PASO 3: Activar Webhook**

1. **Guarda el workflow**
2. **Activa el webhook** (botón "Activate")
3. **Copia la URL del webhook** - algo como:
   ```
   https://tu-n8n.com/webhook/diversia-chat
   ```

### **PASO 4: Configurar DiversIA**

Ahora necesito que me des la URL de tu webhook de n8n para configurarla en el chat widget.

Una vez que tengas la URL:

1. **Abre el archivo**: `static/js/chat-widget.js`
2. **Busca la línea**: `const n8nWebhookUrl = 'https://tu-n8n.webhook.url/chat';`
3. **Reemplaza** con tu URL real de n8n

### **PASO 5: Probar la Integración**

1. **Ve a tu aplicación DiversIA**
2. **Haz clic en el chat widget** (círculo morado)
3. **Escribe**: "Hola, quiero registrarme"
4. **Deberías recibir** respuesta de tu agente n8n

## 🔍 DIAGNÓSTICO DE PROBLEMAS

### **Si no ves el chat widget:**
```javascript
// Abrir consola del navegador (F12) y ejecutar:
console.log('Testing chat widget...');
const widget = document.getElementById('diversia-chat-widget');
console.log('Widget found:', widget);
```

### **Si no funciona la conexión:**
1. **Verifica** que el webhook de n8n esté activo
2. **Revisa** que la URL sea correcta
3. **Comprueba** en n8n si llegan las peticiones

### **URLs importantes para testing:**
```
https://tu-dominio.replit.app/api/v1/users
https://tu-dominio.replit.app/api/v1/companies  
https://tu-dominio.replit.app/api/v1/user-insights
https://tu-dominio.replit.app/webhook/funnel-data
```

## 🎯 PRÓXIMOS PASOS

Una vez funcionando:

1. **Añade más intents** al código JavaScript
2. **Conecta con APIs** de DiversIA para datos en tiempo real
3. **Configura lead scoring** automático
4. **Integra con tu CRM** si tienes uno

¿Cuál es la URL de tu webhook de n8n para que pueda configurar la conexión?