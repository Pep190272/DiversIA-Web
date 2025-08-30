#!/usr/bin/env python3
"""Most basic Flask app test"""

from flask import Flask

app = Flask(__name__)

@app.route('/')
def hello():
    return '<h1>✅ Basic Flask Working!</h1><p>Server is running correctly.</p>'

@app.route('/health')
def health():
    return {"status": "ok", "message": "Basic server healthy"}

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)