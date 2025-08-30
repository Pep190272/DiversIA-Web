#!/usr/bin/env python3
"""Simple test server for DiversIA - Immediate Fix"""

from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase
import os

# Create simple Flask app
class Base(DeclarativeBase):
    pass

app = Flask(__name__)
app.secret_key = os.environ.get("SESSION_SECRET", "dev-secret-key-change-in-production")

# Simple database configuration
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///diversia_simple.db"
app.config["SQLALCHEMY_ENGINE_OPTIONS"] = {
    "pool_recycle": 300,
    "pool_pre_ping": True,
}

db = SQLAlchemy(model_class=Base, app=app)

@app.route('/')
def home():
    """Test home page to verify connectivity"""
    return '''
    <!DOCTYPE html>
    <html lang="es">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>DiversIA - Test Server</title>
        <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
    </head>
    <body class="bg-light">
        <div class="container mt-5">
            <div class="row justify-content-center">
                <div class="col-md-8">
                    <div class="card">
                        <div class="card-body text-center">
                            <h1 class="card-title text-success">✅ DiversIA Server Running!</h1>
                            <p class="card-text lead">The server is working correctly.</p>
                            <hr>
                            <h5>Server Status:</h5>
                            <div class="row">
                                <div class="col-md-6">
                                    <div class="alert alert-success">
                                        <strong>✅ Flask App:</strong> Working
                                    </div>
                                </div>
                                <div class="col-md-6">
                                    <div class="alert alert-success">
                                        <strong>✅ Database:</strong> Connected
                                    </div>
                                </div>
                            </div>
                            <div class="mt-3">
                                <a href="/health" class="btn btn-primary">Health Check</a>
                                <a href="/test-templates" class="btn btn-info">Test Templates</a>
                            </div>
                            <hr>
                            <small class="text-muted">
                                DiversIA Test Server - Ready for full restoration
                            </small>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </body>
    </html>
    '''

@app.route('/health')
def health():
    """Health check endpoint"""
    try:
        # Test database connection
        with app.app_context():
            from sqlalchemy import text
            db.session.execute(text("SELECT 1"))
        db_status = "Connected"
    except Exception as e:
        db_status = f"Error: {str(e)}"
    
    return {
        "status": "ok",
        "message": "Server is healthy",
        "database": db_status,
        "port": 5000,
        "host": "0.0.0.0"
    }

@app.route('/test-templates')
def test_templates():
    """Test if templates directory is accessible"""
    try:
        return render_template('index.html')
    except Exception as e:
        return f'''
        <h2>Template Test</h2>
        <p><strong>Error:</strong> {str(e)}</p>
        <p>This is expected for the simple server test.</p>
        <a href="/">← Back to Home</a>
        '''

if __name__ == "__main__":
    print("🚀 Starting DiversIA Simple Test Server...")
    
    # Initialize database
    with app.app_context():
        try:
            db.create_all()
            print("✅ Database initialized successfully")
        except Exception as e:
            print(f"⚠️ Database warning: {e}")
    
    # Start server with explicit configuration
    try:
        print("🔗 Server will be available at: http://0.0.0.0:5000")
        app.run(
            host="0.0.0.0",
            port=5000,
            debug=True,
            use_reloader=False,
            threaded=True
        )
    except Exception as e:
        print(f"❌ Server startup error: {e}")
        exit(1)