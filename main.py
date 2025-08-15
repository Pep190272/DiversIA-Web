from app import app
from api_endpoints import api
from chat_webhook import chat

# Register API and webhook blueprints
app.register_blueprint(api)
app.register_blueprint(chat)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
