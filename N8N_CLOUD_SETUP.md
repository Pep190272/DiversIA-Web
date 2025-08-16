# 🌐 CONFIGURACIÓN N8N CLOUD - GUÍA PASO A PASO

## 🔍 INFORMACIÓN NECESARIA

Cuando subes un flujo a n8n.cloud, el webhook automáticamente recibe una nueva URL.

### **Formato de URL de n8n.cloud**:
```
https://hooks.n8n.cloud/webhook/[webhook-id]
```

## 🛠️ CÓMO ENCONTRAR TU WEBHOOK URL

### **Opción 1: Desde el flujo**
1. Abre tu flujo en n8n.cloud
2. Haz clic en el nodo "Webhook" (el primero)
3. En la configuración verás "Webhook URLs"
4. Copia la URL de **Production**

### **Opción 2: Desde el panel**
1. Ve a tu workflow en n8n.cloud
2. En la pestaña "Settings" o "Webhook"
3. Busca la URL del webhook

## 🧪 CONFIGURACIÓN ACTUAL

**El chat ahora usa**: `https://pepmorenocreador.app.n8n.cloud/webhook-test/diversia-chat`

**Estado**: ✅ CONFIGURADO CORRECTAMENTE

## 🔧 PASOS PARA ACTUALIZAR

1. **Encuentra tu webhook URL en n8n.cloud**
2. **Cópiala aquí para que la configure**
3. **Verificar que el workflow esté activo**
4. **Probar el chat**

## ⚡ VERIFICACIONES ADICIONALES

### **En n8n.cloud**:
- ✅ ¿El workflow está "Active"?
- ✅ ¿El nodo Webhook está configurado correctamente?
- ✅ ¿El path es `/diversia-chat`?

### **En tu flujo**:
- ✅ ¿El nodo HTTP Request tiene la URL correcta de tu Replit?
- ✅ ¿Los nodos están conectados correctamente?

## 🎯 LO QUE NECESITO

**Por favor, comparte**:
1. La URL del webhook que te dio n8n.cloud
2. ¿El workflow aparece como "Active" en n8n.cloud?
3. ¿Hay algún error en la pestaña "Executions"?

Con esta información podré configurar todo correctamente.