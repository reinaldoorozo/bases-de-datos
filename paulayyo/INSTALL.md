# FitHome Pro - Guía de Instalación y Configuración

## 🚀 Instalación Rápida

### Opción 1: Instalación Automática
```bash
# Clonar el repositorio
git clone https://github.com/[usuario]/fithome-pro.git
cd fithome-pro

# Instalar dependencias
pip install -r requirements.txt

# Ejecutar la aplicación
streamlit run src/main_app.py
```

### Opción 2: Instalación Manual
```bash
# Instalar Streamlit
pip install streamlit

# Instalar dependencias de análisis
pip install pandas matplotlib plotly seaborn numpy

# Ejecutar la aplicación
streamlit run src/main_app.py
```

## 🔧 Configuración

### Variables de Entorno
```bash
# Puerto de la aplicación
export STREAMLIT_SERVER_PORT=8501

# Dirección del servidor
export STREAMLIT_SERVER_ADDRESS=0.0.0.0

# Configuración de la base de datos
export DATABASE_PATH=fithome_pro.db
```

### Configuración de Streamlit
Crear archivo `.streamlit/config.toml`:
```toml
[server]
port = 8501
address = "0.0.0.0"

[browser]
gatherUsageStats = false

[theme]
primaryColor = "#667eea"
backgroundColor = "#ffffff"
secondaryBackgroundColor = "#f0f2f6"
textColor = "#262730"
```

## 🗄️ Base de Datos

### Inicialización Automática
La base de datos se crea automáticamente al ejecutar la aplicación por primera vez.

### Inicialización Manual
```bash
# Ejecutar script de base de datos
sqlite3 fithome_pro.db < database/fithome_pro_database.sql
```

### Datos de Prueba
```python
# Crear datos de muestra
python -c "from src.data_analysis import create_sample_data; create_sample_data()"
```

## 🐛 Solución de Problemas

### Error: "No module named 'streamlit'"
```bash
pip install streamlit
```

### Error: "Database is locked"
```bash
# Cerrar otras instancias de la aplicación
# O cambiar el nombre de la base de datos
export DATABASE_PATH=fithome_pro_new.db
```

### Error: "Port already in use"
```bash
# Cambiar el puerto
streamlit run src/main_app.py --server.port 8502
```

### Error de Importación
```bash
# Verificar que estás en el directorio correcto
pwd
# Debe mostrar: /path/to/fithome-pro

# Verificar estructura de archivos
ls -la src/
```

## 📱 Acceso a la Aplicación

### Desarrollo Local
- URL: `http://localhost:8501`
- La aplicación se abre automáticamente en el navegador

### Red Local
- URL: `http://[tu-ip]:8501`
- Accesible desde otros dispositivos en la misma red

## 🔒 Seguridad

### Configuración de Producción
```bash
# Usar HTTPS en producción
export STREAMLIT_SERVER_HEADLESS=true
export STREAMLIT_SERVER_ENABLE_CORS=false
```

### Variables Sensibles
```bash
# No incluir en el repositorio
export SECRET_KEY="tu-clave-secreta"
export DATABASE_URL="postgresql://user:pass@host/db"
```

## 📊 Monitoreo

### Logs de la Aplicación
```bash
# Ver logs en tiempo real
tail -f ~/.streamlit/logs/streamlit.log
```

### Métricas de Rendimiento
- La aplicación incluye logging integrado
- Métricas disponibles en el dashboard de administración

## 🚀 Despliegue

### Docker
```dockerfile
FROM python:3.9-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .
EXPOSE 8501

CMD ["streamlit", "run", "src/main_app.py"]
```

### Heroku
```bash
# Crear Procfile
echo "web: streamlit run src/main_app.py --server.port \$PORT --server.address 0.0.0.0" > Procfile

# Desplegar
git push heroku main
```

## 📞 Soporte

### Problemas Comunes
1. **Aplicación no inicia**: Verificar dependencias instaladas
2. **Error de base de datos**: Verificar permisos de archivo
3. **Puerto ocupado**: Cambiar puerto o cerrar otras instancias

### Contacto
- **Email**: [email del equipo]
- **GitHub Issues**: [enlace a issues]
- **Documentación**: [enlace a docs]

---

*Para más información, consulta el README.md principal*
