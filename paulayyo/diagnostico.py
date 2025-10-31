#!/usr/bin/env python3
"""
FitHome Pro - Script de Diagnóstico
Verifica el estado de la aplicación y soluciona problemas comunes
"""

import subprocess
import sys
import os
import requests
import sqlite3
from pathlib import Path

def check_python():
    """Verificar instalación de Python"""
    try:
        version = sys.version_info
        print(f"✅ Python {version.major}.{version.minor}.{version.micro} instalado")
        return True
    except Exception as e:
        print(f"❌ Error con Python: {e}")
        return False

def check_dependencies():
    """Verificar dependencias instaladas"""
    required_packages = [
        'streamlit', 'pandas', 'matplotlib', 
        'plotly', 'seaborn', 'numpy'
    ]
    
    missing = []
    for package in required_packages:
        try:
            __import__(package)
            print(f"✅ {package} instalado")
        except ImportError:
            print(f"❌ {package} faltante")
            missing.append(package)
    
    if missing:
        print(f"\n🔧 Instalando dependencias faltantes...")
        try:
            subprocess.run([sys.executable, '-m', 'pip', 'install'] + missing, check=True)
            print("✅ Dependencias instaladas correctamente")
            return True
        except subprocess.CalledProcessError:
            print("❌ Error instalando dependencias")
            return False
    
    return True

def check_database():
    """Verificar base de datos"""
    if os.path.exists('fithome_pro.db'):
        try:
            conn = sqlite3.connect('fithome_pro.db')
            cursor = conn.cursor()
            cursor.execute("SELECT COUNT(*) FROM usuarios")
            user_count = cursor.fetchone()[0]
            cursor.execute("SELECT COUNT(*) FROM entrenamientos")
            workout_count = cursor.fetchone()[0]
            conn.close()
            
            print(f"✅ Base de datos encontrada ({user_count} usuarios, {workout_count} entrenamientos)")
            return True
        except Exception as e:
            print(f"❌ Error con base de datos: {e}")
            return False
    else:
        print("❌ Base de datos no encontrada")
        return False

def check_files():
    """Verificar archivos necesarios"""
    required_files = [
        'main.py', 'src/main_app.py', 'src/app_logic.py', 
        'src/data_analysis.py', 'requirements.txt'
    ]
    
    missing_files = []
    for file in required_files:
        if os.path.exists(file):
            print(f"✅ {file} encontrado")
        else:
            print(f"❌ {file} faltante")
            missing_files.append(file)
    
    return len(missing_files) == 0

def check_server():
    """Verificar si el servidor está ejecutándose"""
    try:
        response = requests.get('http://localhost:8501', timeout=5)
        if response.status_code == 200:
            print("✅ Servidor ejecutándose en puerto 8501")
            return True
        else:
            print(f"⚠️ Servidor respondiendo con código {response.status_code}")
            return False
    except requests.exceptions.RequestException:
        print("❌ Servidor no está ejecutándose")
        return False

def check_ports():
    """Verificar puertos disponibles"""
    import socket
    
    ports_to_check = [8501, 8502, 8503]
    available_ports = []
    
    for port in ports_to_check:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        result = sock.connect_ex(('localhost', port))
        sock.close()
        
        if result != 0:
            available_ports.append(port)
            print(f"✅ Puerto {port} disponible")
        else:
            print(f"❌ Puerto {port} ocupado")
    
    return available_ports

def fix_database():
    """Reparar base de datos"""
    print("🔧 Reparando base de datos...")
    try:
        subprocess.run([sys.executable, 'init_database.py'], check=True)
        print("✅ Base de datos reparada")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Error reparando base de datos: {e}")
        return False

def start_server(port=8501):
    """Iniciar servidor"""
    print(f"🚀 Iniciando servidor en puerto {port}...")
    try:
        cmd = [
            sys.executable, '-m', 'streamlit', 'run', 'main.py',
            '--server.port', str(port),
            '--server.address', '0.0.0.0',
            '--server.headless', 'true'
        ]
        
        process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        
        # Esperar un momento para que el servidor inicie
        import time
        time.sleep(3)
        
        # Verificar si el servidor está funcionando
        try:
            response = requests.get(f'http://localhost:{port}', timeout=5)
            if response.status_code == 200:
                print(f"✅ Servidor iniciado correctamente en puerto {port}")
                print(f"🌐 URL: http://localhost:{port}")
                return True
            else:
                print(f"❌ Servidor no responde correctamente")
                return False
        except requests.exceptions.RequestException:
            print(f"❌ No se puede conectar al servidor")
            return False
            
    except Exception as e:
        print(f"❌ Error iniciando servidor: {e}")
        return False

def main():
    """Función principal de diagnóstico"""
    print("🔍 FitHome Pro - Diagnóstico del Sistema")
    print("=" * 50)
    
    # Verificaciones básicas
    checks = {
        'Python': check_python(),
        'Dependencias': check_dependencies(),
        'Archivos': check_files(),
        'Base de datos': check_database(),
        'Servidor': check_server()
    }
    
    print("\n📊 Resumen de Verificaciones:")
    print("-" * 30)
    
    all_good = True
    for check, result in checks.items():
        status = "✅" if result else "❌"
        print(f"{status} {check}")
        if not result:
            all_good = False
    
    # Soluciones automáticas
    if not checks['Base de datos']:
        print("\n🔧 Solucionando problemas de base de datos...")
        if fix_database():
            checks['Base de datos'] = True
    
    if not checks['Servidor']:
        print("\n🔧 Solucionando problemas de servidor...")
        available_ports = check_ports()
        if available_ports:
            port = available_ports[0]
            if start_server(port):
                checks['Servidor'] = True
        else:
            print("❌ No hay puertos disponibles")
    
    # Resultado final
    print("\n" + "=" * 50)
    if all_good:
        print("🎉 ¡Todo está funcionando correctamente!")
        print("🌐 Accede a: http://localhost:8501")
        print("👤 Usuario demo: demo@fithome.com")
        print("🔑 Contraseña: hello")
    else:
        print("⚠️ Se encontraron problemas que requieren atención manual")
        print("📞 Revisa los errores anteriores y ejecuta las soluciones sugeridas")

if __name__ == "__main__":
    main()
