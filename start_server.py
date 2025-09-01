#!/usr/bin/env python3
"""Script para iniciar el servidor Flask directamente"""

if __name__ == '__main__':
    from main import app
    print("🚀 Iniciando DiversIA server...")
    app.run(host='0.0.0.0', port=5000, debug=False, threaded=True)