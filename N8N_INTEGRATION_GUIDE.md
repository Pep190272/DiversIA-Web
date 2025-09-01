# Guía de Integración n8n - DiversIA

## 🚀 Configuración del Agente Inteligente

### Endpoints API Disponibles

Todos los endpoints están disponibles en: `https://tu-dominio.replit.app/api/v1/`

#### 1. **Datos de Usuarios** 
```
GET /api/v1/users
```
Retorna todos los candidatos neurodivergentes registrados.

**Respuesta ejemplo:**
```json
{
  "success": true,
  "data": [
    {
      "id": 1,
      "nombre": "Juan",
      "email": "juan@example.com",
      "telefono": "123456789",
      "neurodivergencia": "TDAH",
      "ciudad": "Madrid",
      "experiencia": "3 años en desarrollo web",
      "fecha_registro": "2025-01-14T10:30:00",
      "disponible": true
    }
  ],
  "count": 1
}
```

#### 2. **Datos de Empresas**
```
GET /api/v1/companies
```
Retorna todas las empresas registradas.

#### 3. **Ofertas de Trabajo**
```
GET /api/v1/job-offers
```
Retorna todas las ofertas activas.

#### 4. **Matching Inteligente**
```
POST /api/v1/match-candidates
Content-Type: application/json

{
  "job_offer_id": 1
}
```
Encuentra candidatos compatibles para una oferta específica.

#### 5. **Insights de Usuarios**
```
GET /api/v1/user-insights
```
Estadísticas para el funnel de ventas.

#### 6. **Lead Scoring**
```
POST /api/v1/lead-scoring
Content-Type: application/json

{
  "type": "user",  // or "company"
  "id": 1
}
```
Puntúa leads para priorización de ventas.

### Webhooks Disponibles

Base URL: `https://tu-dominio.replit.app/webhook/`

#### 1. **Chat del Usuario**
```
POST /webhook/n8n-chat
Content-Type: application/json

{
  "message": "Hola, quiero registrarme",
  "user_id": "user_123",
  "session_id": "session_456"
}
```

#### 2. **Seguimiento de Acciones**
```
POST /webhook/user-action
Content-Type: application/json

{
  "user_id": "user_123",
  "action": "form_start",
  "page": "/registro-tdah",
  "data": {"section": "personal_info"}
}
```

#### 3. **Datos del Funnel**
```
GET /webhook/funnel-data
```
Métricas del funnel de conversión.

## 🤖 Configuración del Workflow n8n

### Nodo 1: Webhook Trigger
- URL: `https://tu-dominio.replit.app/webhook/n8n-chat`
- Method: POST
- Response: JSON

### Nodo 2: Procesamiento de Mensaje
```javascript
// En el nodo de código JavaScript
const userMessage = $input.first().json.body.message;
const context = $input.first().json.body.context;

let intent = 'general';
let response = '';

// Detección de intents
if (userMessage.toLowerCase().includes('registro')) {
  intent = 'registration';
  response = '¿Te gustaría registrarte como persona neurodivergente o como empresa?';
} else if (userMessage.toLowerCase().includes('tdah')) {
  intent = 'tdah_info';
  response = 'TDAH es una de las neurodivergencias que mejor apoyamos. ¿Quieres iniciar el proceso de registro especializado?';
} else if (userMessage.toLowerCase().includes('trabajo')) {
  intent = 'job_search';
  response = 'Tenemos un sistema de matching inteligente. ¿Cuál es tu área de experiencia?';
}

return {
  intent: intent,
  response: response,
  user_id: context.user_id,
  session_id: context.session_id
};
```

### Nodo 3: Consulta a la Base de Datos
```javascript
// Para obtener estadísticas en tiempo real
const response = await fetch('https://tu-dominio.replit.app/api/v1/user-insights');
const insights = await response.json();

return {
  total_users: insights.insights.total_users,
  recent_registrations: insights.insights.recent_registrations
};
```

### Nodo 4: Lead Scoring
```javascript
// Evaluar calidad del lead
const leadData = {
  type: 'user',
  id: $input.first().json.user_id
};

const response = await fetch('https://tu-dominio.replit.app/api/v1/lead-scoring', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify(leadData)
});

const score = await response.json();
return score;
```

## 📊 Casos de Uso del Funnel de Ventas

### 1. **Calificación Automática de Leads**
- Usuarios con score >60: Alta prioridad
- Usuarios con score 30-60: Media prioridad  
- Usuarios con score <30: Baja prioridad

### 2. **Respuestas Inteligentes por Contexto**
```javascript
// Personalizar respuestas según el perfil
if (user.neurodivergencia === 'TDAH') {
  response = 'Para personas con TDAH, ofrecemos formularios optimizados y tests gamificados...';
} else if (user.neurodivergencia === 'TEA') {
  response = 'Nuestro proceso para TEA incluye evaluaciones sensoriales adaptadas...';
}
```

### 3. **Seguimiento de Conversión**
- Visita inicial → Chat activado (+10 puntos)
- Pregunta específica → Interés medio (+20 puntos)
- Solicita registro → Interés alto (+40 puntos)
- Completa formulario → Lead calificado (+60 puntos)

## 🎯 Mejores Prácticas

### Personalización por Neurodivergencia
- **TDAH**: Respuestas concisas, opciones claras
- **TEA**: Información detallada, pasos específicos  
- **Dislexia**: Formato visual, evitar texto denso

### Timing de Respuestas
- Respuesta inmediata: Saludo y reconocimiento
- 2-3 segundos: Procesamiento y respuesta contextual
- Máximo 5 segundos: Respuestas complejas con datos

### Escalación Humana
```javascript
// Triggers para escalación
const escalationTriggers = [
  'hablar con humano',
  'atención personalizada', 
  'problema específico',
  'queja o reclamo'
];

if (escalationTriggers.some(trigger => userMessage.includes(trigger))) {
  return {
    action: 'escalate_to_human',
    priority: 'high'
  };
}
```

## 🔧 Testing y Debugging

### Datos de Prueba Disponibles
La aplicación incluye datos de ejemplo para testing:
- 5 usuarios con diferentes neurodivergencias
- 3 empresas en sectores variados
- 2 ofertas de trabajo activas

### Endpoints de Debug
```
GET /api/v1/users?limit=5          # Primeros 5 usuarios
GET /api/v1/companies?sector=tech  # Empresas tech
GET /api/v1/user-insights          # Métricas actuales
```

### Logs del Chat Widget
El widget incluye logging detallado:
```javascript
console.log('User action:', actionData);
console.log('Bot response:', botMessage);
```

## 🚀 Despliegue

Una vez configurado tu workflow n8n:

1. **Actualiza las URLs** en los webhooks con tu dominio de Replit
2. **Configura autenticación** si es necesaria
3. **Prueba cada endpoint** con datos reales
4. **Monitorea métricas** de conversión

¿Necesitas alguna configuración específica o tienes preguntas sobre la integración?