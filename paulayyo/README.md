# FitHome Pro 💪

**Tu Entrenador Personal en Casa**

Una aplicación web integral que facilita el acceso a entrenamientos personalizados, seguimiento nutricional y actividades familiares desde casa.

## 🚀 Características Principales

- 🏠 **Dashboard Personalizado** - Resumen de tu progreso fitness
- 💪 **Entrenamientos Personalizados** - Rutinas adaptadas a tu nivel
- 📊 **Seguimiento de Progreso** - Análisis avanzado de datos
- 🍎 **Planes Nutricionales** - Alimentación saludable
- 👶 **Zona Infantil** - Actividades educativas para niños
- 🎬 **Contenido Premium** - Películas y documentales motivacionales
- 🏆 **Sistema de Logros** - Gamificación para mantener motivación

## 🛠️ Tecnologías Utilizadas

### Backend
- **Python 3.8+** - Lenguaje principal
- **Streamlit** - Framework web
- **SQLite** - Base de datos
- **Pandas** - Análisis de datos
- **Matplotlib/Plotly** - Visualización

### Frontend
- **Streamlit** - Interfaz de usuario
- **HTML/CSS** - Estilos personalizados
- **JavaScript** - Interactividad

### Herramientas
- **Git** - Control de versiones
- **VS Code** - Editor de código
- **GitHub** - Repositorio remoto

## 📦 Instalación

### Requisitos Previos
- Python 3.8 o superior
- pip (gestor de paquetes de Python)

### Pasos de Instalación

1. **Clonar el repositorio**
```bash
git clone https://github.com/[usuario]/fithome-pro.git
cd fithome-pro
```

2. **Instalar dependencias**
```bash
pip install -r requirements.txt
```

3. **Inicializar la base de datos**
```bash
python -c "import sqlite3; conn = sqlite3.connect('fithome_pro.db'); print('Base de datos creada')"
```

4. **Ejecutar la aplicación**
```bash
streamlit run src/main_app.py
```

5. **Abrir en el navegador**
La aplicación se abrirá automáticamente en `http://localhost:8501`

## 🏗️ Estructura del Proyecto

```
fithome-pro/
├── 📁 database/
│   └── fithome_pro_database.sql    # Script de base de datos
├── 📁 src/
│   ├── app_logic.py                # Lógica de la aplicación
│   ├── data_analysis.py           # Análisis de datos
│   └── main_app.py                # Aplicación principal
├── 📁 docs/
│   └── Informe_Frameworks_Web_FitHome_Pro.md
├── 📁 presentacion/
│   └── FitHome_Pro_Presentacion.md
├── 📄 requirements.txt             # Dependencias
├── 📄 README.md                   # Este archivo
└── 📄 main.py                    # Punto de entrada alternativo
```

## 🎯 Uso de la Aplicación

### 1. Registro e Inicio de Sesión
- Crea una cuenta nueva o inicia sesión
- Completa tu perfil personal
- Establece tus objetivos fitness

### 2. Dashboard Principal
- Visualiza tus estadísticas diarias
- Controla tu hidratación
- Accede a entrenamientos recomendados

### 3. Entrenamientos
- Explora el catálogo de rutinas
- Filtra por categoría y nivel
- Ejecuta entrenamientos paso a paso

### 4. Análisis de Progreso
- Revisa gráficos de progreso
- Analiza tendencias temporales
- Recibe recomendaciones personalizadas

### 5. Contenido Adicional
- Planes nutricionales
- Actividades para niños
- Contenido multimedia premium

## 📊 Base de Datos

### Tablas Principales
- **usuarios** - Información personal y perfil
- **entrenamientos** - Catálogo de rutinas
- **ejercicios** - Detalles de ejercicios
- **sesiones_entrenamiento** - Historial de entrenamientos
- **progreso_peso** - Seguimiento de peso
- **planes_nutricionales** - Planes alimentarios
- **actividades_infantiles** - Contenido para niños
- **contenido_multimedia** - Películas y documentales

### Características
- 15+ tablas relacionadas
- Índices optimizados
- Triggers para consistencia
- Procedimientos almacenados
- Vistas para consultas complejas

## 📈 Análisis de Datos

### Tipos de Análisis
- **Métricas de Fitness** - Calorías, duración, frecuencia
- **Progreso Temporal** - Evolución en el tiempo
- **Análisis por Categorías** - Cardio, fuerza, flexibilidad
- **Reportes Comprensivos** - Recomendaciones personalizadas
- **Mapas de Calor** - Actividad por días del mes

### Gráficos Implementados
- Gráficos de líneas para progreso
- Gráficos de barras para comparaciones
- Gráficos de pastel para distribución
- Mapas de calor para patrones temporales
- Gráficos combinados para análisis múltiple

## 🔧 Desarrollo

### Patrones de Diseño
- **Repository Pattern** - Acceso a datos
- **Service Layer** - Lógica de negocio
- **Factory Pattern** - Creación de objetos
- **Observer Pattern** - Notificaciones

### Servicios Principales
- `UserService` - Gestión de usuarios
- `WorkoutService` - Manejo de entrenamientos
- `NutritionService` - Planes nutricionales
- `KidsActivityService` - Actividades infantiles
- `MediaService` - Contenido multimedia

### Análisis de Datos
- `FitnessDataAnalyzer` - Análisis estadístico
- `FitnessChartGenerator` - Generación de gráficos
- `ReportGenerator` - Reportes comprensivos

## 🧪 Testing

### Datos de Prueba
```python
# Crear datos de muestra
python -c "from src.data_analysis import create_sample_data; create_sample_data()"
```

### Pruebas de Funcionalidad
- Autenticación de usuarios
- Ejecución de entrenamientos
- Generación de reportes
- Análisis de datos

## 📚 Documentación

### Archivos de Documentación
- `docs/Informe_Frameworks_Web_FitHome_Pro.md` - Análisis de frameworks
- `presentacion/FitHome_Pro_Presentacion.md` - Presentación del proyecto
- `README.md` - Este archivo

### Comentarios en Código
- Documentación de funciones
- Explicación de algoritmos
- Ejemplos de uso
- Notas de implementación

## 🚀 Despliegue

### Desarrollo Local
```bash
streamlit run src/main_app.py
```

### Producción
```bash
# Configurar variables de entorno
export STREAMLIT_SERVER_PORT=8501
export STREAMLIT_SERVER_ADDRESS=0.0.0.0

# Ejecutar en producción
streamlit run src/main_app.py --server.port 8501
```

## 🤝 Contribución

### Cómo Contribuir
1. Fork el proyecto
2. Crea una rama para tu feature (`git checkout -b feature/AmazingFeature`)
3. Commit tus cambios (`git commit -m 'Add some AmazingFeature'`)
4. Push a la rama (`git push origin feature/AmazingFeature`)
5. Abre un Pull Request

### Estándares de Código
- Seguir PEP 8 para Python
- Documentar funciones y clases
- Incluir tests para nuevas funcionalidades
- Mantener compatibilidad con versiones anteriores

## 📝 Licencia

Este proyecto está bajo la Licencia MIT. Ver el archivo `LICENSE` para más detalles.

## 👥 Equipo

- **[Nombre Estudiante 1]** - Desarrollador Principal
- **[Nombre Estudiante 2]** - Analista de Datos
- **[Nombre Estudiante 3]** - Diseñador UI/UX
- **[Nombre Estudiante 4]** - Arquitecto de Software

## 📞 Contacto

- **Email:** [email del equipo]
- **GitHub:** [enlace al repositorio]
- **Proyecto:** [enlace al proyecto]

## 🙏 Agradecimientos

- Stack Overflow por las soluciones técnicas
- Comunidad Python por el soporte
- Streamlit por el framework excelente
- Pandas/Matplotlib por las herramientas de análisis

## 🔮 Roadmap

### Versión 2.0
- [ ] Aplicación móvil
- [ ] Integración con wearables
- [ ] IA para recomendaciones
- [ ] Sistema de comunidades

### Versión 3.0
- [ ] Streaming en vivo
- [ ] Realidad virtual
- [ ] Análisis predictivo
- [ ] Integración con servicios de salud

---

**¡Gracias por usar FitHome Pro! 💪**

*Desarrollado con ❤️ para mejorar tu salud y bienestar*
