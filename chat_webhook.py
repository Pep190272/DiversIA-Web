from flask import Blueprint, request, jsonify
from datetime import datetime
import json
import logging

# Importar sistema inteligente
try:
    from chat_intelligent_fallback import get_intelligent_response
    INTELLIGENT_FALLBACK_AVAILABLE = True
except ImportError:
    INTELLIGENT_FALLBACK_AVAILABLE = False

# Chat webhook for n8n integration
chat = Blueprint('chat', __name__, url_prefix='/webhook')

# Store conversation history (in production, use Redis or database)
conversations = {}

@chat.route('/n8n-chat', methods=['POST'])
def n8n_chat_webhook():
    """Webhook endpoint for n8n chatbot integration"""
    try:
        data = request.get_json()
        
        # Extract message data
        user_message = data.get('message', '')
        user_id = data.get('user_id', 'anonymous')
        session_id = data.get('session_id', f'session_{datetime.now().timestamp()}')
        
        # Log the incoming message
        logging.info(f"Received chat message from {user_id}: {user_message}")
        
        # Store conversation context
        if session_id not in conversations:
            conversations[session_id] = {
                'user_id': user_id,
                'started_at': datetime.now(),
                'messages': []
            }
        
        conversations[session_id]['messages'].append({
            'type': 'user',
            'message': user_message,
            'timestamp': datetime.now()
        })
        
        # Prepare context for n8n agent
        context = {
            'user_id': user_id,
            'session_id': session_id,
            'conversation_history': conversations[session_id]['messages'][-5:],  # Last 5 messages
            'platform_info': {
                'name': 'DiversIA',
                'purpose': 'Plataforma de inclusión laboral para personas neurodivergentes',
                'services': [
                    'Registro de candidatos neurodivergentes',
                    'Registro de empresas inclusivas',
                    'Matching inteligente',
                    'Tests de evaluación',
                    'Recursos de asociaciones'
                ]
            }
        }
        
        return jsonify({
            'success': True,
            'context': context,
            'message_received': user_message,
            'timestamp': datetime.now().isoformat()
        })
        
    except Exception as e:
        logging.error(f"Chat webhook error: {str(e)}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@chat.route('/bot-response', methods=['POST'])
def receive_bot_response():
    """Receive response from n8n chatbot"""
    try:
        data = request.get_json()
        
        session_id = data.get('session_id')
        bot_message = data.get('message', '')
        intent = data.get('intent', 'general')
        
        if session_id and session_id in conversations:
            conversations[session_id]['messages'].append({
                'type': 'bot',
                'message': bot_message,
                'intent': intent,
                'timestamp': datetime.now()
            })
        
        return jsonify({
            'success': True,
            'message_stored': True
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@chat.route('/user-action', methods=['POST'])
def track_user_action():
    """Track user actions for sales funnel"""
    try:
        data = request.get_json()
        
        action_data = {
            'user_id': data.get('user_id', 'anonymous'),
            'action': data.get('action'),  # 'page_view', 'form_start', 'form_complete', etc.
            'page': data.get('page'),
            'data': data.get('data', {}),
            'timestamp': datetime.now()
        }
        
        # Log action for analytics
        logging.info(f"User action: {action_data}")
        
        # Here you would typically save to database
        # For now, we'll return the tracked data
        
        return jsonify({
            'success': True,
            'action_tracked': action_data
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@chat.route('/funnel-data', methods=['GET'])
def get_funnel_data():
    """Get sales funnel data for n8n"""
    try:
        # This would typically come from database analytics
        funnel_data = {
            'visitors_today': 45,
            'form_starts': 8,
            'form_completions': 6,
            'conversion_rate': 75.0,
            'hot_leads': [
                {
                    'id': 1,
                    'email': 'usuario@example.com',
                    'stage': 'form_completed',
                    'score': 85,
                    'last_activity': datetime.now().isoformat()
                }
            ]
        }
        
        return jsonify({
            'success': True,
            'funnel_data': funnel_data
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500