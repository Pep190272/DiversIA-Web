import os
import sys

# Asegurar que el directorio actual esté en el path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Importar la aplicación Flask
from main import app

# Para compatibilidad con Vercel
application = app

if __name__ == "__main__":
    app.run(debug=False)