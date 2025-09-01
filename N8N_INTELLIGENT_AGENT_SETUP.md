# 🤖 CONFIGURACIÓN DEL AGENTE INTELIGENTE N8N + MISTRAL

## 🎯 OBJETIVO

Convertir el workflow básico de n8n en un agente inteligente completo que use Mistral para procesamiento de lenguaje natural y acceso a múltiples fuentes de datos.

## 🏗️ ARQUITECTURA DEL AGENTE

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   CHAT WIDGET   │───▶│  n8n WEBHOOK    │───▶│  MISTRAL AI     │
└─────────────────┘    └─────────────────┘    └─────────────────┘
                                │                       │
                                ▼                       ▼
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│  GOOGLE DRIVE   │◀───│  DATA FUSION    │───▶│   POSTGRESQL    │
└─────────────────┘    └─────────────────┘    └─────────────────┘
                                │
                                ▼
                       ┌─────────────────┐
                       │  SMART RESPONSE │
                       └─────────────────┘
```

## 🔧 CONFIGURACIÓN N8N

### **Nodo 1: Webhook** (Ya configurado)
```json
{
  "httpMethod": "POST",
  "path": "/diversia-chat",
  "responseMode": "responseNode"
}
```

### **Nodo 2: Mistral AI Integration**
Reemplazar el nodo "Code" actual por:

```javascript
// Nodo: HTTP Request - Mistral AI
{
  "url": "https://api.mistral.ai/v1/chat/completions",
  "method": "POST",
  "headers": {
    "Authorization": "Bearer {{ $env.MISTRAL_API_KEY }}",
    "Content-Type": "application/json"
  },
  "body": {
    "model": "mistral-medium",
    "messages": [
      {
        "role": "system",
        "content": "Eres el asistente inteligente de DiversIA, especializado en inclusión laboral para personas neurodivergentes. Responde en español de manera empática y profesional."
      },
      {
        "role": "user", 
        "content": "{{ $json.body.message }}"
      }
    ],
    "max_tokens": 300,
    "temperature": 0.7
  }
}
```

### **Nodo 3: Data Collection Hub**
```javascript
// Nodo: Code - Data Fusion
const userMessage = $input.first().json.body.message;
const userId = $input.first().json.body.user_id;

// 1. Obtener datos de la base de datos
const dbResponse = await fetch('https://073083d2-dd14-424e-a549-4c03e48131b7-00-1vatfbc2lts0v.janeway.replit.dev/api/v1/user-insights', {
  method: 'GET',
  headers: {
    'Content-Type': 'application/json'
  }
});

const dbData = await dbResponse.json();

// 2. Obtener datos de Google Drive (si está configurado)
let driveData = {};
try {
  const driveResponse = await fetch('https://073083d2-dd14-424e-a549-4c03e48131b7-00-1vatfbc2lts0v.janeway.replit.dev/api/v2/analytics/user-insights', {
    method: 'GET',
    headers: {
      'Content-Type': 'application/json'
    }
  });
  driveData = await driveResponse.json();
} catch (error) {
  console.log('Drive data not available:', error);
}

// 3. Análisis de intención
let intent = 'general';
const message = userMessage.toLowerCase();

if (message.includes('registro') || message.includes('registrar')) {
  intent = 'registration';
} else if (message.includes('trabajo') || message.includes('empleo')) {
  intent = 'job_search';
} else if (message.includes('tdah') || message.includes('tea') || message.includes('dislexia')) {
  intent = 'neurodivergence_info';
} else if (message.includes('empresa') || message.includes('contratar')) {
  intent = 'company_registration';
}

// 4. Preparar contexto enriquecido para Mistral
const enrichedContext = {
  user_message: userMessage,
  intent: intent,
  database_stats: dbData,
  drive_insights: driveData,
  user_id: userId,
  timestamp: new Date().toISOString()
};

return {
  enriched_context: enrichedContext,
  original_message: userMessage,
  detected_intent: intent
};
```

### **Nodo 4: Response Enhancement**
```javascript
// Nodo: Code - Response Builder
const mistralResponse = $input.first().json.choices[0].message.content;
const context = $node["Data Collection Hub"].json.enriched_context;

// Enriquecer respuesta con datos específicos
let enhancedResponse = mistralResponse;

// Agregar estadísticas relevantes
if (context.database_stats && context.database_stats.total_users > 0) {
  enhancedResponse += `\n\n📊 Datos actualizados: ${context.database_stats.total_users} profesionales registrados`;
  
  if (context.database_stats.total_companies > 0) {
    enhancedResponse += ` y ${context.database_stats.total_companies} empresas inclusivas`;
  }
}

// Agregar llamadas a la acción específicas según intención
switch (context.detected_intent) {
  case 'registration':
    enhancedResponse += '\n\n🔗 ¿Te gustaría que te ayude con el proceso de registro?';
    break;
  case 'job_search':
    enhancedResponse += '\n\n💼 Puedo ayudarte a encontrar oportunidades específicas para tu perfil.';
    break;
  case 'neurodivergence_info':
    enhancedResponse += '\n\n🧠 ¿Necesitas información sobre recursos o evaluaciones específicas?';
    break;
  case 'company_registration':
    enhancedResponse += '\n\n🏢 ¿Te gustaría conocer cómo funciona nuestro sistema de matching?';
    break;
}

// Respuesta final estructurada
return {
  final_response: enhancedResponse,
  response: enhancedResponse,
  intent: context.detected_intent,
  confidence: 0.95,
  powered_by: 'DiversIA AI Agent v2.0',
  processing_time: new Date().toISOString()
};
```

## 🔑 CONFIGURACIÓN DE SECRETOS

### **En n8n.cloud - Variables de Entorno:**

1. **MISTRAL_API_KEY**: Tu clave de API de Mistral
   - Obtener en: https://console.mistral.ai/
   - Formato: `mistral_xxx...`

2. **REPLIT_APP_URL**: 
   ```
   https://073083d2-dd14-424e-a549-4c03e48131b7-00-1vatfbc2lts0v.janeway.replit.dev
   ```

3. **GOOGLE_DRIVE_SERVICE_ACCOUNT** (opcional):
   - Credenciales de service account de Google

## 🚀 FLUJO DE DATOS INTELIGENTE

### **Entrada del Usuario**
```json
{
  "message": "Tengo TDAH y busco trabajo en programación",
  "user_id": "user_123",
  "session_id": "session_456",
  "page": "/"
}
```

### **Procesamiento Inteligente**
1. **Análisis de Intención**: Detecta "job_search" + "TDAH"
2. **Consulta a Base de Datos**: Estadísticas de usuarios con TDAH
3. **Consulta a Google Drive**: Documentos relevantes (si disponible)
4. **Procesamiento Mistral**: Comprensión del contexto completo
5. **Enriquecimiento**: Agregar datos específicos y CTAs

### **Respuesta Enriquecida**
```json
{
  "final_response": "Entiendo que tienes TDAH y buscas oportunidades en programación. DiversIA cuenta con formularios especializados para TDAH y conectamos con empresas que valoran este tipo de neurodivergencia. Actualmente tenemos 45 profesionales con TDAH registrados y 12 empresas que específicamente buscan este perfil.\n\n💼 Puedo ayudarte a encontrar oportunidades específicas para tu perfil.\n\n¿Te gustaría que te ayude con el proceso de registro especializado para TDAH?",
  "intent": "job_search",
  "confidence": 0.95,
  "powered_by": "DiversIA AI Agent v2.0"
}
```

## 📊 MÉTRICAS Y MONITOREO

### **Indicadores de Rendimiento**
- **Tiempo de Respuesta**: < 3 segundos
- **Precisión de Intención**: > 90%
- **Satisfacción Usuario**: Medida por feedback
- **Conversiones**: Registros completados post-chat

### **Dashboard de Análisis**
- Intenciones más comunes
- Temas de neurodivergencia consultados
- Tasa de conversión por tipo de consulta
- Rendimiento del modelo Mistral

## 🔒 CONSIDERACIONES DE SEGURIDAD

### **Datos Sensibles**
- Todos los mensajes se procesan de forma anónima
- No se almacenan datos personales en n8n
- Cumplimiento GDPR para datos europeos

### **API Keys**
- Rotación automática de claves cada 30 días
- Monitoreo de uso y límites
- Alertas por uso anómalo

## 🛠️ TESTING Y VALIDACIÓN

### **Casos de Prueba**
1. **Registro Candidato**: "Quiero registrarme, tengo TEA"
2. **Búsqueda Empleo**: "Busco trabajo remoto en diseño"
3. **Info Neurodivergencia**: "¿Qué adaptaciones necesita alguien con TDAH?"
4. **Registro Empresa**: "Somos empresa y queremos contratar talento autista"

### **Respuestas Esperadas**
- Contextualmente relevantes
- Con datos estadísticos actualizados
- CTAs específicos por intención
- Tiempo de respuesta < 3 segundos

## 📋 CHECKLIST DE IMPLEMENTACIÓN

- [ ] Obtener API Key de Mistral
- [ ] Configurar variables de entorno en n8n
- [ ] Actualizar nodos según especificaciones
- [ ] Probar cada tipo de intención
- [ ] Verificar integración con base de datos
- [ ] Configurar Google Drive (opcional)
- [ ] Implementar monitoreo de errores
- [ ] Documentar casos edge

## 🎯 PRÓXIMOS PASOS

1. **Fase 1**: Implementar Mistral + Data Fusion
2. **Fase 2**: Agregar Google Drive integration
3. **Fase 3**: Sistema de aprendizaje continuo
4. **Fase 4**: Matching predictivo en tiempo real

## 💡 TIPS DE OPTIMIZACIÓN

- **Caché Responses**: Para consultas comunes
- **Fallback Inteligente**: Si Mistral no está disponible
- **Rate Limiting**: Prevenir abuso del sistema
- **A/B Testing**: Probar diferentes prompts