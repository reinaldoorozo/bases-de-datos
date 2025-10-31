#!/usr/bin/env python3
"""
FitHome Pro - Launcher Script
Simple launcher for both desktop and mobile access
"""

import subprocess
import sys
import os
import webbrowser
import time
import threading
from pathlib import Path

def check_dependencies():
    """Check if all required dependencies are installed"""
    try:
        import streamlit
        import pandas
        import matplotlib
        import plotly
        import seaborn
        import numpy
        print("✅ All dependencies are installed")
        return True
    except ImportError as e:
        print(f"❌ Missing dependency: {e}")
        print("Please run: pip install -r requirements.txt")
        return False

def check_database():
    """Check if database exists"""
    if os.path.exists('fithome_pro.db'):
        print("✅ Database found")
        return True
    else:
        print("❌ Database not found")
        print("Please run: python init_database.py")
        return False

def start_streamlit():
    """Start the Streamlit application"""
    print("🚀 Starting FitHome Pro...")
    
    # Check if already running
    try:
        import requests
        response = requests.get('http://localhost:8501', timeout=2)
        print("⚠️  Application is already running at http://localhost:8501")
        webbrowser.open('http://localhost:8501')
        return
    except:
        pass
    
    # Start the application
    try:
        # Use streamlit run command
        cmd = [sys.executable, '-m', 'streamlit', 'run', 'main.py', '--server.port', '8501', '--server.address', '0.0.0.0']
        
        print("Starting server...")
        process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        
        # Wait a moment for the server to start
        time.sleep(3)
        
        # Check if server started successfully
        try:
            import requests
            response = requests.get('http://localhost:8501', timeout=5)
            if response.status_code == 200:
                print("✅ Server started successfully!")
                print("🌐 Application URL: http://localhost:8501")
                print("📱 Mobile access: http://[your-ip]:8501")
                print("🔄 Press Ctrl+C to stop the server")
                
                # Open browser
                webbrowser.open('http://localhost:8501')
                
                # Keep the process running
                try:
                    process.wait()
                except KeyboardInterrupt:
                    print("\n🛑 Stopping server...")
                    process.terminate()
                    process.wait()
                    print("✅ Server stopped")
            else:
                print("❌ Server failed to start properly")
                process.terminate()
        except Exception as e:
            print(f"❌ Error checking server status: {e}")
            process.terminate()
            
    except Exception as e:
        print(f"❌ Error starting server: {e}")

def get_local_ip():
    """Get the local IP address for mobile access"""
    try:
        import socket
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
        s.close()
        return ip
    except:
        return "localhost"

def show_instructions():
    """Show usage instructions"""
    local_ip = get_local_ip()
    
    print("\n" + "="*60)
    print("🏠 FITHOME PRO - FITNESS PORTAL")
    print("="*60)
    print()
    print("📱 ACCESS METHODS:")
    print(f"   • Desktop: http://localhost:8501")
    print(f"   • Mobile:  http://{local_ip}:8501")
    print()
    print("🔧 FEATURES:")
    print("   • 💪 Workout tracking and routines")
    print("   • 🍎 Nutrition planning")
    print("   • 👶 Kids activities")
    print("   • 🎬 Premium content")
    print("   • 📊 Progress analytics")
    print()
    print("👤 DEMO ACCOUNT:")
    print("   • Email: demo@fithome.com")
    print("   • Password: hello")
    print()
    print("="*60)

def main():
    """Main launcher function"""
    print("🏠 FitHome Pro Launcher")
    print("=" * 30)
    
    # Check dependencies
    if not check_dependencies():
        return
    
    # Check database
    if not check_database():
        print("Creating database...")
        try:
            subprocess.run([sys.executable, 'init_database.py'], check=True)
            print("✅ Database created successfully")
        except subprocess.CalledProcessError:
            print("❌ Failed to create database")
            return
    
    # Show instructions
    show_instructions()
    
    # Start the application
    start_streamlit()

if __name__ == "__main__":
    main()
