#!/usr/bin/env python3
"""Servidor Flask para Web Preview de DiversIA"""

import os
import signal
import sys

def signal_handler(sig, frame):
    print('\n🛑 Cerrando servidor web preview...')
    sys.exit(0)

if __name__ == '__main__':
    # Configurar señales
    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)
    
    print("🌐 Iniciando DiversIA Web Preview Server...")
    
    # Importar la aplicación
    from main import app
    
    # Configuración específica para web preview
    app.config['DEBUG'] = True
    app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0
    app.config['TEMPLATES_AUTO_RELOAD'] = True
    
    try:
        # Usar Flask development server para web preview
        app.run(
            host='0.0.0.0',
            port=5000,
            debug=True,
            use_reloader=False,  # No reloader para evitar conflictos
            threaded=True
        )
    except Exception as e:
        print(f"❌ Error iniciando web preview server: {e}")
        sys.exit(1)