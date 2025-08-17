"""
Endpoint inteligente separado para el chat de DiversIA
"""

from flask import Blueprint, request, jsonify
from datetime import datetime
import logging

# Importar sistema inteligente
try:
    from chat_intelligent_fallback import get_intelligent_response
    INTELLIGENT_FALLBACK_AVAILABLE = True
except ImportError:
    INTELLIGENT_FALLBACK_AVAILABLE = False

# Blueprint para respuestas inteligentes
intelligent_chat = Blueprint('intelligent_chat', __name__, url_prefix='/webhook')

@intelligent_chat.route('/intelligent-response', methods=['POST'])
def intelligent_response():
    """Endpoint para respuestas inteligentes locales"""
    try:
        data = request.get_json()
        
        message = data.get('message', '')
        user_id = data.get('user_id', 'anonymous')
        session_id = data.get('session_id', 'default')
        
        if not message:
            return jsonify({'error': 'Message is required'}), 400
        
        if INTELLIGENT_FALLBACK_AVAILABLE:
            # Usar sistema inteligente local
            response = get_intelligent_response(message, {
                'user_id': user_id,
                'session_id': session_id
            })
            return jsonify(response)
        else:
            # Fallback básico
            return jsonify({
                'final_response': 'Sistema de chat en mantenimiento. Usa el formulario de contacto.',
                'response': 'Sistema de chat en mantenimiento. Usa el formulario de contacto.',
                'intent': 'fallback',
                'confidence': 0.5
            })
    
    except Exception as e:
        logging.error(f"Error in intelligent response: {e}")
        return jsonify({
            'error': 'Error processing message',
            'final_response': 'Lo siento, hay un problema técnico. Intenta de nuevo.'
        }), 500