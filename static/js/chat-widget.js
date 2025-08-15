// Chat Widget for n8n Integration
(function() {
    'use strict';
    
    let chatWidget = null;
    let isOpen = false;
    let sessionId = null;
    
    // Initialize chat widget
    function initChatWidget() {
        // Generate session ID
        sessionId = 'session_' + Date.now() + '_' + Math.random().toString(36).substr(2, 9);
        
        // Create chat widget HTML
        const widgetHTML = `
            <div id="diversia-chat-widget" class="chat-widget">
                <div id="chat-toggle" class="chat-toggle">
                    <i data-lucide="message-circle"></i>
                    <span class="chat-badge">¡Hola!</span>
                </div>
                
                <div id="chat-window" class="chat-window" style="display: none;">
                    <div class="chat-header">
                        <div class="chat-title">
                            <i data-lucide="bot"></i>
                            <span>Asistente DiversIA</span>
                        </div>
                        <button id="chat-close" class="chat-close">
                            <i data-lucide="x"></i>
                        </button>
                    </div>
                    
                    <div id="chat-messages" class="chat-messages">
                        <div class="message bot-message">
                            <div class="message-content">
                                ¡Hola! Soy el asistente de DiversIA. ¿En qué puedo ayudarte hoy?
                                <br><br>
                                Puedo ayudarte con:
                                <ul>
                                    <li>Información sobre registro</li>
                                    <li>Tipos de neurodivergencia</li>
                                    <li>Proceso de matching</li>
                                    <li>Recursos disponibles</li>
                                </ul>
                            </div>
                            <div class="message-time">${new Date().toLocaleTimeString()}</div>
                        </div>
                    </div>
                    
                    <div class="chat-input-container">
                        <div class="chat-input-wrapper">
                            <input type="text" id="chat-input" placeholder="Escribe tu mensaje..." maxlength="500">
                            <button id="chat-send" type="button">
                                <i data-lucide="send"></i>
                            </button>
                        </div>
                        <div class="chat-powered">
                            <small>Powered by DiversIA AI</small>
                        </div>
                    </div>
                </div>
            </div>
        `;
        
        // Add to page
        document.body.insertAdjacentHTML('beforeend', widgetHTML);
        
        // Add styles
        addChatStyles();
        
        // Bind events
        bindChatEvents();
        
        // Initialize icons
        if (typeof lucide !== 'undefined') {
            lucide.createIcons();
        }
        
        console.log('Chat widget initialized with session:', sessionId);
    }
    
    function addChatStyles() {
        const styles = `
            <style>
            .chat-widget {
                position: fixed;
                bottom: 20px;
                right: 20px;
                z-index: 9999;
                font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            }
            
            .chat-toggle {
                width: 60px;
                height: 60px;
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                border-radius: 50%;
                display: flex;
                align-items: center;
                justify-content: center;
                cursor: pointer;
                box-shadow: 0 4px 12px rgba(0,0,0,0.15);
                transition: transform 0.3s ease;
                position: relative;
            }
            
            .chat-toggle:hover {
                transform: scale(1.1);
            }
            
            .chat-toggle svg {
                color: white;
                width: 24px;
                height: 24px;
            }
            
            .chat-badge {
                position: absolute;
                top: -10px;
                right: -10px;
                background: #ff4757;
                color: white;
                padding: 4px 8px;
                border-radius: 12px;
                font-size: 12px;
                font-weight: 500;
                animation: bounce 2s infinite;
            }
            
            @keyframes bounce {
                0%, 20%, 53%, 80%, 100% { transform: translate3d(0,0,0); }
                40%, 43% { transform: translate3d(0, -8px, 0); }
                70% { transform: translate3d(0, -4px, 0); }
            }
            
            .chat-window {
                position: absolute;
                bottom: 80px;
                right: 0;
                width: 350px;
                height: 500px;
                background: white;
                border-radius: 12px;
                box-shadow: 0 8px 24px rgba(0,0,0,0.15);
                display: flex;
                flex-direction: column;
                overflow: hidden;
            }
            
            .chat-header {
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                color: white;
                padding: 16px;
                display: flex;
                justify-content: space-between;
                align-items: center;
            }
            
            .chat-title {
                display: flex;
                align-items: center;
                gap: 8px;
                font-weight: 600;
            }
            
            .chat-close {
                background: none;
                border: none;
                color: white;
                cursor: pointer;
                padding: 4px;
                border-radius: 4px;
            }
            
            .chat-close:hover {
                background: rgba(255,255,255,0.1);
            }
            
            .chat-messages {
                flex: 1;
                padding: 16px;
                overflow-y: auto;
                display: flex;
                flex-direction: column;
                gap: 12px;
            }
            
            .message {
                max-width: 80%;
            }
            
            .bot-message {
                align-self: flex-start;
            }
            
            .user-message {
                align-self: flex-end;
            }
            
            .message-content {
                background: #f1f3f4;
                padding: 12px;
                border-radius: 12px;
                font-size: 14px;
                line-height: 1.4;
            }
            
            .user-message .message-content {
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                color: white;
            }
            
            .message-time {
                font-size: 11px;
                color: #666;
                margin-top: 4px;
                text-align: right;
            }
            
            .user-message .message-time {
                text-align: left;
            }
            
            .chat-input-container {
                border-top: 1px solid #eee;
                padding: 16px;
            }
            
            .chat-input-wrapper {
                display: flex;
                gap: 8px;
                align-items: center;
            }
            
            #chat-input {
                flex: 1;
                border: 1px solid #ddd;
                border-radius: 20px;
                padding: 10px 16px;
                font-size: 14px;
                outline: none;
            }
            
            #chat-input:focus {
                border-color: #667eea;
            }
            
            #chat-send {
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                border: none;
                border-radius: 50%;
                width: 40px;
                height: 40px;
                display: flex;
                align-items: center;
                justify-content: center;
                cursor: pointer;
                color: white;
            }
            
            #chat-send:hover {
                opacity: 0.9;
            }
            
            .chat-powered {
                text-align: center;
                margin-top: 8px;
                color: #999;
            }
            
            .typing-indicator {
                display: flex;
                align-items: center;
                gap: 4px;
                padding: 12px;
                background: #f1f3f4;
                border-radius: 12px;
                align-self: flex-start;
                max-width: 80px;
            }
            
            .typing-dot {
                width: 8px;
                height: 8px;
                background: #666;
                border-radius: 50%;
                animation: typing 1.4s infinite ease-in-out;
            }
            
            .typing-dot:nth-child(1) { animation-delay: -0.32s; }
            .typing-dot:nth-child(2) { animation-delay: -0.16s; }
            
            @keyframes typing {
                0%, 80%, 100% { transform: scale(0); opacity: 0.5; }
                40% { transform: scale(1); opacity: 1; }
            }
            
            @media (max-width: 480px) {
                .chat-window {
                    width: calc(100vw - 40px);
                    right: -10px;
                }
            }
            </style>
        `;
        
        document.head.insertAdjacentHTML('beforeend', styles);
    }
    
    function bindChatEvents() {
        const toggle = document.getElementById('chat-toggle');
        const closeBtn = document.getElementById('chat-close');
        const chatWindow = document.getElementById('chat-window');
        const chatInput = document.getElementById('chat-input');
        const sendBtn = document.getElementById('chat-send');
        
        // Toggle chat
        toggle.addEventListener('click', toggleChat);
        closeBtn.addEventListener('click', closeChat);
        
        // Send message
        sendBtn.addEventListener('click', sendMessage);
        chatInput.addEventListener('keypress', function(e) {
            if (e.key === 'Enter') {
                sendMessage();
            }
        });
        
        // Hide badge after first interaction
        toggle.addEventListener('click', function() {
            const badge = document.querySelector('.chat-badge');
            if (badge) {
                badge.style.display = 'none';
            }
        }, { once: true });
    }
    
    function toggleChat() {
        const chatWindow = document.getElementById('chat-window');
        isOpen = !isOpen;
        chatWindow.style.display = isOpen ? 'flex' : 'none';
        
        if (isOpen) {
            document.getElementById('chat-input').focus();
            trackUserAction('chat_opened');
        }
    }
    
    function closeChat() {
        const chatWindow = document.getElementById('chat-window');
        isOpen = false;
        chatWindow.style.display = 'none';
        trackUserAction('chat_closed');
    }
    
    function sendMessage() {
        const input = document.getElementById('chat-input');
        const message = input.value.trim();
        
        if (!message) return;
        
        // Add user message to chat
        addMessage(message, 'user');
        
        // Clear input
        input.value = '';
        
        // Show typing indicator
        showTypingIndicator();
        
        // Send to n8n webhook
        sendToWebhook(message);
        
        // Track action
        trackUserAction('message_sent', { message: message });
    }
    
    function addMessage(text, sender) {
        const messagesContainer = document.getElementById('chat-messages');
        const messageDiv = document.createElement('div');
        const time = new Date().toLocaleTimeString();
        
        messageDiv.className = `message ${sender}-message`;
        messageDiv.innerHTML = `
            <div class="message-content">${text}</div>
            <div class="message-time">${time}</div>
        `;
        
        messagesContainer.appendChild(messageDiv);
        messagesContainer.scrollTop = messagesContainer.scrollHeight;
    }
    
    function showTypingIndicator() {
        const messagesContainer = document.getElementById('chat-messages');
        const typingDiv = document.createElement('div');
        typingDiv.id = 'typing-indicator';
        typingDiv.className = 'typing-indicator';
        typingDiv.innerHTML = `
            <div class="typing-dot"></div>
            <div class="typing-dot"></div>
            <div class="typing-dot"></div>
        `;
        
        messagesContainer.appendChild(typingDiv);
        messagesContainer.scrollTop = messagesContainer.scrollHeight;
    }
    
    function hideTypingIndicator() {
        const typingDiv = document.getElementById('typing-indicator');
        if (typingDiv) {
            typingDiv.remove();
        }
    }
    
    async function sendToWebhook(message) {
        try {
            const response = await fetch('/webhook/n8n-chat', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    message: message,
                    user_id: getUserId(),
                    session_id: sessionId,
                    page: window.location.pathname
                })
            });
            
            const data = await response.json();
            
            if (data.success) {
                // Simulate bot response (in production, this would come from n8n)
                setTimeout(() => {
                    hideTypingIndicator();
                    addBotResponse(message);
                }, 2000);
            }
            
        } catch (error) {
            console.error('Error sending message:', error);
            hideTypingIndicator();
            addMessage('Lo siento, hubo un error. Por favor, intenta de nuevo.', 'bot');
        }
    }
    
    function addBotResponse(userMessage) {
        // Simple response logic (in production, responses come from n8n)
        let response = '';
        
        const message = userMessage.toLowerCase();
        
        if (message.includes('registro') || message.includes('registrar')) {
            response = 'Para registrarte en DiversIA, puedes elegir entre:<br><br>• <strong>Personas neurodivergentes</strong>: Crea tu perfil profesional<br>• <strong>Empresas inclusivas</strong>: Registra tu empresa para contratar talento diverso<br><br>¿Cuál te interesa más?';
        } else if (message.includes('tdah') || message.includes('adhd')) {
            response = 'El TDAH (Trastorno por Déficit de Atención e Hiperactividad) es una de las neurodivergencias que apoyamos. Tenemos formularios especializados y recursos específicos para personas con TDAH. ¿Te gustaría conocer más sobre el proceso de registro?';
        } else if (message.includes('tea') || message.includes('autismo')) {
            response = 'Apoyamos a personas con TEA (Trastorno del Espectro Autista). Nuestro proceso incluye evaluaciones adaptadas y matching con empresas que valoran la diversidad cognitiva. ¿Qué aspecto te interesa más?';
        } else if (message.includes('dislexia')) {
            response = 'Para personas con dislexia, ofrecemos tests especializados y recursos de apoyo. También conectamos con asociaciones como DISFAM que pueden proporcionar evaluaciones profesionales. ¿Necesitas más información?';
        } else if (message.includes('empresa') || message.includes('contratar')) {
            response = 'Ayudamos a empresas a encontrar talento neurodivergente excepcional. Nuestro proceso incluye:<br><br>• Matching inteligente<br>• Orientación sobre inclusión<br>• Seguimiento del proceso<br><br>¿Te gustaría registrar tu empresa?';
        } else if (message.includes('hola') || message.includes('ayuda')) {
            response = '¡Hola! Estoy aquí para ayudarte con cualquier duda sobre DiversIA. Puedo contarte sobre nuestros servicios, el proceso de registro, o cualquier información que necesites. ¿En qué puedo asistirte?';
        } else {
            response = 'Gracias por tu mensaje. Puedo ayudarte con información sobre:<br><br>• Registro de personas neurodivergentes<br>• Registro de empresas<br>• Tipos de neurodivergencia (TDAH, TEA, Dislexia)<br>• Proceso de matching<br><br>¿Sobre qué te gustaría saber más?';
        }
        
        addMessage(response, 'bot');
    }
    
    function trackUserAction(action, data = {}) {
        fetch('/webhook/user-action', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                user_id: getUserId(),
                action: action,
                page: window.location.pathname,
                data: data
            })
        }).catch(error => console.error('Error tracking action:', error));
    }
    
    function getUserId() {
        let userId = localStorage.getItem('diversia_user_id');
        if (!userId) {
            userId = 'visitor_' + Date.now() + '_' + Math.random().toString(36).substr(2, 9);
            localStorage.setItem('diversia_user_id', userId);
        }
        return userId;
    }
    
    // Initialize when DOM is ready
    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', initChatWidget);
    } else {
        initChatWidget();
    }
    
})();