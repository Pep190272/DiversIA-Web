#!/usr/bin/env python3
"""Servidor simplificado para DiversIA"""

import os
import signal
import sys
from werkzeug.serving import run_simple

def signal_handler(sig, frame):
    print('\n🛑 Cerrando servidor...')
    sys.exit(0)

if __name__ == '__main__':
    # Manejar señales de cierre limpio
    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)
    
    print("🚀 Iniciando DiversIA server estable...")
    
    from main import app
    
    # Configuración más robusta
    app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0
    
    try:
        run_simple(
            hostname='0.0.0.0',
            port=5000,
            application=app,
            use_reloader=False,
            use_debugger=False,
            threaded=True,
            processes=1
        )
    except Exception as e:
        print(f"❌ Error iniciando servidor: {e}")
        sys.exit(1)