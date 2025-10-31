"""
FitHome Pro - Punto de Entrada Principal
Aplicación web de fitness y bienestar

Autor: Equipo FitHome Pro
Fecha: 2024
"""

import sys
import os

# Agregar el directorio src al path
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

# Importar y ejecutar la aplicación principal
if __name__ == "__main__":
    try:
        from src.main_app import main
        main()
    except ImportError as e:
        print(f"Error importando módulos: {e}")
        print("Asegúrate de instalar las dependencias con: pip install -r requirements.txt")
    except Exception as e:
        print(f"Error ejecutando la aplicación: {e}")
        print("Verifica que todos los archivos estén en su lugar correcto")
