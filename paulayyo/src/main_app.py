"""
FitHome Pro - Interfaz Web Principal
Aplicación web completa con Streamlit

Autor: Equipo FitHome Pro
Fecha: 2024
"""

import streamlit as st
import time
import datetime
from datetime import date, timedelta
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import sqlite3
import hashlib
import json
from typing import List, Dict, Optional
import logging

# Importar módulos propios
from src.app_logic import *
from src.data_analysis import FitnessDataAnalyzer, FitnessChartGenerator, ReportGenerator

# Configuración de logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# =============================================================================
# CONFIGURACIÓN DE LA PÁGINA
# =============================================================================

st.set_page_config(
    page_title="FitHome Pro",
    page_icon="💪",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Estilos CSS personalizados - Diseño Premium Clase Mundial
st.markdown("""
<style>
    /* Importar fuente moderna */
    @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;600;700;800&display=swap');
    
    /* Variables globales */
    :root {
        --primary-gradient: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        --secondary-gradient: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
        --success-gradient: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%);
        --warning-gradient: linear-gradient(135deg, #fa709a 0%, #fee140 100%);
        --danger-gradient: linear-gradient(135deg, #ff6b6b 0%, #ee5a6f 100%);
        --dark-gradient: linear-gradient(135deg, #434343 0%, #000000 100%);
        --gold-gradient: linear-gradient(135deg, #f6d365 0%, #fda085 100%);
        --shadow-soft: 0 10px 40px rgba(0,0,0,0.08);
        --shadow-medium: 0 15px 50px rgba(0,0,0,0.12);
        --shadow-hard: 0 20px 60px rgba(0,0,0,0.16);
    }
    
    /* Reset general */
    * {
        margin: 0;
        padding: 0;
        box-sizing: border-box;
    }
    
    body {
        font-family: 'Poppins', sans-serif !important;
        background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
    }
    
    /* Header principal con animación */
    .main-header {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 3rem 2rem;
        border-radius: 20px;
        color: white;
        margin-bottom: 2rem;
        text-align: center;
        box-shadow: var(--shadow-medium);
        position: relative;
        overflow: hidden;
        animation: fadeInDown 0.8s ease-out;
    }
    
    .main-header::before {
        content: '';
        position: absolute;
        top: -50%;
        left: -50%;
        width: 200%;
        height: 200%;
        background: radial-gradient(circle, rgba(255,255,255,0.1) 1px, transparent 1px);
        background-size: 50px 50px;
        animation: drift 20s linear infinite;
    }
    
    @keyframes fadeInDown {
        from {
            opacity: 0;
            transform: translateY(-30px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }
    
    @keyframes drift {
        0% { transform: translate(0, 0); }
        100% { transform: translate(50px, 50px); }
    }
    
    /* Cards de workout modernos con glassmorphism */
    .workout-card {
        background: rgba(255, 255, 255, 0.95);
        backdrop-filter: blur(10px);
        padding: 2rem;
        border-radius: 20px;
        box-shadow: var(--shadow-soft);
        margin-bottom: 1.5rem;
        border-left: 5px solid;
        border-image: linear-gradient(135deg, #667eea, #764ba2) 1;
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        position: relative;
        overflow: hidden;
    }
    
    .workout-card::before {
        content: '';
        position: absolute;
        top: 0;
        left: -100%;
        width: 100%;
        height: 100%;
        background: linear-gradient(90deg, transparent, rgba(255,255,255,0.3), transparent);
        transition: left 0.5s;
    }
    
    .workout-card:hover::before {
        left: 100%;
    }
    
    .workout-card:hover {
        transform: translateY(-8px) scale(1.02);
        box-shadow: var(--shadow-hard);
        border-left-width: 8px;
    }
    
    /* Cards de estadísticas premium */
    .stats-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 2.5rem;
        border-radius: 20px;
        color: white;
        text-align: center;
        margin-bottom: 1.5rem;
        box-shadow: var(--shadow-medium);
        position: relative;
        overflow: hidden;
        transition: all 0.4s ease;
    }
    
    .stats-card::after {
        content: '';
        position: absolute;
        top: -50%;
        right: -50%;
        width: 100%;
        height: 100%;
        background: radial-gradient(circle, rgba(255,255,255,0.15) 0%, transparent 70%);
        border-radius: 50%;
    }
    
    .stats-card:hover {
        transform: scale(1.05) rotate(2deg);
        box-shadow: var(--shadow-hard);
    }
    
    /* Card kids divertida */
    .kids-card {
        background: linear-gradient(135deg, #ffeaa7 0%, #fab1a0 100%);
        padding: 2rem;
        border-radius: 25px;
        color: #2d3436;
        margin-bottom: 1.5rem;
        box-shadow: var(--shadow-medium);
        animation: bounce 2s infinite;
    }
    
    @keyframes bounce {
        0%, 20%, 50%, 80%, 100% { transform: translateY(0); }
        40% { transform: translateY(-10px); }
        60% { transform: translateY(-5px); }
    }
    
    /* Card premium dorada */
    .premium-card {
        background: linear-gradient(135deg, #f6d365 0%, #fda085 100%);
        padding: 3rem;
        border-radius: 25px;
        color: white;
        text-align: center;
        margin-bottom: 2rem;
        box-shadow: var(--shadow-hard);
        position: relative;
        overflow: hidden;
    }
    
    .premium-card::before {
        content: '👑';
        font-size: 4rem;
        position: absolute;
        top: -20px;
        right: -20px;
        opacity: 0.2;
        transform: rotate(25deg);
    }
    
    /* Container de métricas moderno */
    .metric-container {
        background: rgba(255, 255, 255, 0.9);
        backdrop-filter: blur(10px);
        padding: 2rem;
        border-radius: 15px;
        box-shadow: var(--shadow-soft);
        text-align: center;
        border: 1px solid rgba(255,255,255,0.2);
        transition: all 0.3s ease;
    }
    
    .metric-container:hover {
        transform: translateY(-5px);
        box-shadow: var(--shadow-medium);
    }
    
    /* Badges de logros premium */
    .achievement-badge {
        background: linear-gradient(135deg, #ffd700 0%, #ffed4e 100%);
        color: #2d3436;
        padding: 1rem 1.5rem;
        border-radius: 50px;
        font-weight: 700;
        margin: 0.5rem;
        display: inline-block;
        box-shadow: 0 8px 20px rgba(255, 215, 0, 0.3);
        transition: all 0.3s ease;
        text-transform: uppercase;
        letter-spacing: 1px;
        font-size: 0.85rem;
    }
    
    .achievement-badge:hover {
        transform: scale(1.1) rotate(5deg);
        box-shadow: 0 12px 30px rgba(255, 215, 0, 0.5);
    }
    
    /* Barra de progreso moderna */
    .progress-bar {
        background: rgba(0,0,0,0.1);
        border-radius: 50px;
        height: 15px;
        overflow: hidden;
        margin: 1rem 0;
        box-shadow: inset 0 2px 4px rgba(0,0,0,0.1);
    }
    
    .progress-fill {
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        height: 100%;
        border-radius: 50px;
        transition: width 1s cubic-bezier(0.4, 0, 0.2, 1);
        position: relative;
        overflow: hidden;
    }
    
    .progress-fill::after {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        bottom: 0;
        background: linear-gradient(90deg, transparent, rgba(255,255,255,0.3), transparent);
        animation: shimmer 2s infinite;
    }
    
    @keyframes shimmer {
        0% { transform: translateX(-100%); }
        100% { transform: translateX(100%); }
    }
    
    /* Sidebar con gradiente */
    .sidebar-user-info {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 2rem;
        border-radius: 20px;
        color: white;
        margin-bottom: 1.5rem;
        text-align: center;
        box-shadow: var(--shadow-medium);
        position: relative;
        overflow: hidden;
    }
    
    /* Contenedor de gráficos */
    .chart-container {
        background: rgba(255, 255, 255, 0.95);
        backdrop-filter: blur(10px);
        padding: 2rem;
        border-radius: 20px;
        box-shadow: var(--shadow-soft);
        margin-bottom: 2rem;
        transition: all 0.3s ease;
    }
    
    .chart-container:hover {
        box-shadow: var(--shadow-medium);
        transform: translateY(-3px);
    }
    
    /* Cards de recomendaciones elegantes */
    .recommendation-card {
        background: linear-gradient(135deg, #a8edea 0%, #fed6e3 100%);
        padding: 1.5rem;
        border-radius: 15px;
        margin: 1rem 0;
        border-left: 5px solid;
        border-image: linear-gradient(135deg, #667eea, #764ba2) 1;
        box-shadow: var(--shadow-soft);
        transition: all 0.3s ease;
    }
    
    .recommendation-card:hover {
        transform: translateX(10px);
        box-shadow: var(--shadow-medium);
    }
    
    /* Botones modernos premium */
    .stButton > button {
        width: 100%;
        border-radius: 50px;
        border: none;
        padding: 1rem 2rem;
        font-weight: 700;
        font-size: 1rem;
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        box-shadow: 0 8px 20px rgba(102, 126, 234, 0.3);
        position: relative;
        overflow: hidden;
        text-transform: uppercase;
        letter-spacing: 1px;
    }
    
    .stButton > button::before {
        content: '';
        position: absolute;
        top: 50%;
        left: 50%;
        width: 0;
        height: 0;
        border-radius: 50%;
        background: rgba(255, 255, 255, 0.2);
        transform: translate(-50%, -50%);
        transition: width 0.6s, height 0.6s;
    }
    
    .stButton > button:hover::before {
        width: 300px;
        height: 300px;
    }
    
    .stButton > button:hover {
        transform: translateY(-3px);
        box-shadow: 0 15px 40px rgba(102, 126, 234, 0.5);
    }
    
    .stButton > button:active {
        transform: translateY(-1px);
        box-shadow: 0 5px 15px rgba(102, 126, 234, 0.4);
    }
    
    /* Mensajes de éxito elegantes */
    .success-message {
        background: linear-gradient(135deg, #00b894 0%, #00cec9 100%);
        color: white;
        padding: 1.5rem;
        border-radius: 15px;
        border-left: 5px solid rgba(255,255,255,0.5);
        margin: 1rem 0;
        box-shadow: var(--shadow-soft);
        animation: slideInRight 0.5s ease-out;
    }
    
    @keyframes slideInRight {
        from {
            opacity: 0;
            transform: translateX(-30px);
        }
        to {
            opacity: 1;
            transform: translateX(0);
        }
    }
    
    /* Mensajes de advertencia modernos */
    .warning-message {
        background: linear-gradient(135deg, #fdcb6e 0%, #e17055 100%);
        color: white;
        padding: 1.5rem;
        border-radius: 15px;
        border-left: 5px solid rgba(255,255,255,0.5);
        margin: 1rem 0;
        box-shadow: var(--shadow-soft);
        animation: slideInRight 0.5s ease-out;
    }
    
    /* Mejoras adicionales */
    h1, h2, h3 {
        font-family: 'Poppins', sans-serif !important;
        font-weight: 700 !important;
    }
    
    /* Inputs modernos */
    .stTextInput > div > div > input {
        border-radius: 15px !important;
        border: 2px solid #e0e0e0 !important;
        padding: 12px 20px !important;
        transition: all 0.3s ease !important;
    }
    
    .stTextInput > div > div > input:focus {
        border-color: #667eea !important;
        box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1) !important;
    }
    
    /* Selectboxes modernos */
    .stSelectbox > div > div > select {
        border-radius: 15px !important;
        padding: 12px 20px !important;
    }
</style>
""", unsafe_allow_html=True)

# =============================================================================
# INICIALIZACIÓN DE SERVICIOS
# =============================================================================

@st.cache_resource
def initialize_services():
    """Inicializar servicios de la aplicación"""
    try:
        database = SQLiteDatabase()
        if not database.connect():
            st.error("Error conectando a la base de datos")
            return None
        
        return {
            'database': database,
            'user_service': UserService(database),
            'workout_service': WorkoutService(database),
            'nutrition_service': NutritionService(database),
            'analytics': DataAnalytics(database),
            'data_analyzer': FitnessDataAnalyzer(),
            'chart_generator': FitnessChartGenerator(FitnessDataAnalyzer()),
            'report_generator': ReportGenerator(FitnessDataAnalyzer())
        }
    except Exception as e:
        logger.error(f"Error inicializando servicios: {e}")
        return None

# =============================================================================
# INICIALIZACIÓN DEL ESTADO DE SESIÓN
# =============================================================================

def init_session_state():
    """Inicializar estado de la sesión"""
    if 'current_screen' not in st.session_state:
        st.session_state.current_screen = 'loading'
    if 'user' not in st.session_state:
        st.session_state.user = None
    if 'user_profile' not in st.session_state:
        st.session_state.user_profile = UserProfile()
    if 'user_stats' not in st.session_state:
        st.session_state.user_stats = UserStats()
    if 'dark_mode' not in st.session_state:
        st.session_state.dark_mode = False
    if 'notifications' not in st.session_state:
        st.session_state.notifications = [
            "Bienvenido a FitHome Pro ✨",
            "Sugerencia: completa tu primer entrenamiento 💪",
            "Tip: registra tu peso semanalmente para ver tendencias ⚖️"
        ]
    if 'onboarding_step' not in st.session_state:
        st.session_state.onboarding_step = 0
    if 'water_intake' not in st.session_state:
        st.session_state.water_intake = 0
    if 'selected_workout' not in st.session_state:
        st.session_state.selected_workout = None
    if 'workout_in_progress' not in st.session_state:
        st.session_state.workout_in_progress = False
    if 'current_exercise' not in st.session_state:
        st.session_state.current_exercise = 0
    if 'exercise_timer' not in st.session_state:
        st.session_state.exercise_timer = 30
    if 'services' not in st.session_state:
        st.session_state.services = initialize_services()
    if 'habits' not in st.session_state:
        st.session_state.habits = [
            {"name": "Beber agua", "target_per_week": 14, "completed": 0},
            {"name": "Caminar 30m", "target_per_week": 5, "completed": 0},
        ]
    if 'goals_list' not in st.session_state:
        st.session_state.goals_list = [
            {"title": "Entrenar 3 veces/semana", "done": False},
            {"title": "Perder 1 kg este mes", "done": False},
        ]
    if 'accent_color' not in st.session_state:
        st.session_state.accent_color = '#667eea'
    if 'community_posts' not in st.session_state:
        st.session_state.community_posts = [
            {"user": "Ana", "content": "Hoy completé 20 minutos de HIIT!", "likes": 3, "comments": ["¡Grande!", "🔥"]},
            {"user": "Luis", "content": "Mi receta post-entreno: avena + frutos rojos", "likes": 2, "comments": []},
        ]
    if 'shop_cart' not in st.session_state:
        st.session_state.shop_cart = []

# =============================================================================
# PANTALLAS DE LA APLICACIÓN
# =============================================================================

def show_loading_screen():
    """Pantalla de carga"""
    st.markdown("""
    <div style="text-align: center; padding: 4rem 0;">
        <div style="font-size: 4rem; margin-bottom: 2rem;">💪</div>
        <h1 style="color: #667eea; margin-bottom: 1rem;">FitHome Pro</h1>
        <p style="color: #666; margin-bottom: 2rem;">Tu entrenador personal en casa</p>
        <div style="display: flex; justify-content: center; gap: 0.5rem;">
            <div style="width: 12px; height: 12px; background: #667eea; border-radius: 50%; animation: pulse 1.5s infinite;"></div>
            <div style="width: 12px; height: 12px; background: #667eea; border-radius: 50%; animation: pulse 1.5s infinite 0.3s;"></div>
            <div style="width: 12px; height: 12px; background: #667eea; border-radius: 50%; animation: pulse 1.5s infinite 0.6s;"></div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Simular carga
    time.sleep(2)
    st.session_state.current_screen = 'auth'
    st.rerun()

def show_auth_screen(services):
    """Pantalla de autenticación"""
    st.markdown("""
    <div style="text-align: center; margin-bottom: 3rem;">
        <div style="font-size: 3rem; margin-bottom: 1rem;">💪</div>
        <h1 style="color: #667eea;">FitHome Pro</h1>
        <p style="color: #666;">Tu entrenador personal en casa</p>
    </div>
    """, unsafe_allow_html=True)
    
    tab1, tab2 = st.tabs(["Iniciar Sesión", "Registrarse"])
    
    with tab1:
        st.subheader("Bienvenido de vuelta")
        email = st.text_input("Correo electrónico", value="demo@fithome.com", key="login_email")
        password = st.text_input("Contraseña", type="password", value="hello", key="login_password")
        
        if st.button("Iniciar Sesión", key="login_btn"):
            # Autenticar - ahora siempre retorna un usuario
            user_profile = services['user_service'].authenticate_user(email or "demo@test.com", password or "demo")
            
            # Configurar sesión
            st.session_state.user_profile = user_profile
            st.session_state.user = {"email": user_profile.email, "id": user_profile.id}
            st.session_state.user_stats = services['user_service'].get_user_stats(user_profile.id)
            st.session_state.current_screen = 'dashboard'
            st.rerun()
    
    with tab2:
        st.subheader("Únete a la familia fitness")
        name = st.text_input("Nombre completo", key="register_name")
        email = st.text_input("Correo electrónico", key="register_email")
        password = st.text_input("Contraseña", type="password", key="register_password")
        
        if st.button("Registrarse", key="register_btn"):
            if name and email and password:
                # Validar email
                if not ValidationUtils.validate_email(email):
                    st.error("Formato de email inválido")
                    return
                
                # Validar contraseña
                is_valid, message = ValidationUtils.validate_password(password)
                if not is_valid:
                    st.error(message)
                    return
                
                user_profile = UserProfile(
                    name=name,
                    email=email,
                    password_hash=password,
                    is_premium=False
                )
                
                if services['user_service'].register_user(user_profile):
                    st.success("¡Registro exitoso! Completa tu perfil.")
                    st.session_state.user_profile = user_profile
                    st.session_state.current_screen = 'onboarding'
                    st.rerun()
                else:
                    st.error("Error en el registro. Intenta nuevamente.")
            else:
                st.warning("Por favor, completa todos los campos")

def show_onboarding_screen(services):
    """Pantalla de configuración inicial"""
    questions = [
        {
            "title": "¿Cuál es tu género?",
            "type": "gender",
            "options": ["masculino", "femenino", "otro"]
        },
        {
            "title": "¿Cuál es tu edad?",
            "type": "age",
            "input": True
        },
        {
            "title": "¿Cuánto pesas actualmente?",
            "type": "weight",
            "input": True,
            "unit": "kg"
        },
        {
            "title": "¿Cuál es tu estatura?",
            "type": "height",
            "input": True,
            "unit": "cm"
        },
        {
            "title": "¿Cuál es tu nivel de fitness?",
            "type": "fitness_level",
            "options": ["principiante", "intermedio", "avanzado"]
        },
        {
            "title": "¿Cuáles son tus objetivos principales?",
            "type": "goals",
            "options": ["perder peso", "ganar músculo", "mantenerse en forma", "mejorar resistencia", "rehabilitación", "competir"],
            "multiple": True
        }
    ]
    
    current_question = questions[st.session_state.onboarding_step]
    
    st.markdown(f"""
    <div style="text-align: center; margin-bottom: 2rem;">
        <h2>Configuración de Perfil</h2>
        <p>Paso {st.session_state.onboarding_step + 1} de {len(questions)}</p>
        <div style="background: #e5e7eb; height: 8px; border-radius: 4px; margin: 1rem 0;">
            <div style="background: #667eea; height: 8px; border-radius: 4px; width: {((st.session_state.onboarding_step + 1) / len(questions)) * 100}%;"></div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    st.subheader(current_question["title"])
    
    if current_question.get("input"):
        value = st.number_input(
            f"Tu {current_question['type']}",
            min_value=0.0,
            step=0.1 if current_question['type'] in ['weight'] else 1,
            key=f"onboarding_{current_question['type']}"
        )
        if value > 0:
            setattr(st.session_state.user_profile, current_question["type"], value)
    
    elif current_question.get("multiple"):
        selected_options = st.multiselect(
            "Selecciona tus objetivos:",
            current_question["options"],
            default=st.session_state.user_profile.goals
        )
        st.session_state.user_profile.goals = selected_options
    
    else:
        selected = st.radio(
            "Selecciona una opción:",
            current_question["options"],
            key=f"onboarding_{current_question['type']}"
        )
        setattr(st.session_state.user_profile, current_question["type"], selected)
    
    col1, col2 = st.columns([1, 1])
    
    with col1:
        if st.session_state.onboarding_step > 0:
            if st.button("Anterior"):
                st.session_state.onboarding_step -= 1
                st.rerun()
    
    with col2:
        current_value = getattr(st.session_state.user_profile, current_question["type"])
        is_answered = (
            (current_question.get("multiple") and len(current_value) > 0) or
            (not current_question.get("multiple") and current_value)
        )
        
        if is_answered:
            if st.session_state.onboarding_step < len(questions) - 1:
                if st.button("Siguiente"):
                    st.session_state.onboarding_step += 1
                    st.rerun()
            else:
                if st.button("Empezar mi Viaje"):
                    # Obtener el ID del usuario registrado
                    user_id = services['user_service']._get_user_id_by_email(st.session_state.user_profile.email)
                    if user_id:
                        st.session_state.user_profile.id = user_id
                        # Actualizar perfil en la base de datos
                        if services['user_service'].update_user_profile(st.session_state.user_profile):
                            st.session_state.user = {"email": st.session_state.user_profile.email, "id": user_id}
                            st.session_state.user_stats = services['user_service'].get_user_stats(user_id)
                            st.session_state.current_screen = 'dashboard'
                            st.success("¡Perfil completado! Bienvenido a FitHome Pro.")
                            st.rerun()
                        else:
                            st.error("Error actualizando perfil. Intenta nuevamente.")
                    else:
                        st.error("Error obteniendo ID de usuario. Intenta registrarte nuevamente.")

def show_dashboard(services):
    """Dashboard principal"""
    # Sidebar para navegación
    with st.sidebar:
        # Toggle de Dark Mode, color acento y centro de notificaciones
        col_dm, col_badge = st.columns([3, 1])
        with col_dm:
            st.session_state.dark_mode = st.toggle("🌙 Modo Oscuro", value=st.session_state.dark_mode)
        with col_badge:
            notif_count = len(st.session_state.notifications)
            st.markdown(f"<div style='text-align:right;'>🔔 <span style='background:#ef4444;color:white;padding:2px 6px;border-radius:12px;font-size:0.8rem;'>{notif_count}</span></div>", unsafe_allow_html=True)

        st.session_state.accent_color = st.color_picker("Color de acento", value=st.session_state.accent_color)

        st.markdown(f"""
        <div class="sidebar-user-info">
            <h3>¡Hola {st.session_state.user_profile.name or 'Usuario'}! 👋</h3>
            <p>Racha: {st.session_state.user_stats.streak_days} días 🔥</p>
            <p>Entrenamientos: {st.session_state.user_stats.total_workouts}</p>
        </div>
        """, unsafe_allow_html=True)
        with st.expander("Notificaciones"):
            if st.session_state.notifications:
                for note in list(st.session_state.notifications):
                    st.write(f"• {note}")
                if st.button("Limpiar notificaciones"):
                    st.session_state.notifications.clear()
                    st.rerun()
            else:
                st.caption("Sin notificaciones")
        
        page = st.selectbox(
            "Navegación",
            [
                "🏠 Inicio",
                "📅 Calendario",
                "🎯 Hábitos y Metas",
                "👥 Comunidad",
                "🛒 Tienda",
                "💪 Entrenamientos",
                "🍎 Nutrición",
                "👶 Zona Infantil",
                "🎬 Películas",
                "📊 Progreso",
                "📈 Análisis Avanzado"
            ]
        )
        
        # Botón de cerrar sesión
        if st.button("🚪 Cerrar Sesión"):
            for key in st.session_state.keys():
                del st.session_state[key]
            st.session_state.current_screen = 'auth'
            st.rerun()
    
    # Contenido principal basado en la página seleccionada
    if page == "🏠 Inicio":
        show_home_tab(services)
    elif page == "📅 Calendario":
        show_calendar_tab(services)
    elif page == "🎯 Hábitos y Metas":
        show_habits_tab(services)
    elif page == "👥 Comunidad":
        show_community_tab(services)
    elif page == "🛒 Tienda":
        show_shop_tab(services)
    elif page == "💪 Entrenamientos":
        show_workouts_tab(services)
    elif page == "🍎 Nutrición":
        show_nutrition_tab(services)
    elif page == "👶 Zona Infantil":
        show_kids_tab(services)
    elif page == "🎬 Películas":
        show_movies_tab(services)
    elif page == "📊 Progreso":
        show_stats_tab(services)
    elif page == "📈 Análisis Avanzado":
        show_advanced_analysis_tab(services)

def show_home_tab(services):
    """Pestaña de inicio"""
    st.title("Dashboard Principal")
    
    # Header con estadísticas
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown(f"""
        <div class="metric-container">
            <h3>{st.session_state.user_stats.streak_days}</h3>
            <p>Racha (días)</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
        <div class="metric-container">
            <h3>{st.session_state.user_stats.today_calories}</h3>
            <p>Kcal hoy</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown(f"""
        <div class="metric-container">
            <h3>{st.session_state.user_stats.today_minutes}</h3>
            <p>Min hoy</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        st.markdown(f"""
        <div class="metric-container">
            <h3>{st.session_state.user_stats.total_workouts}</h3>
            <p>Entrenamientos</p>
        </div>
        """, unsafe_allow_html=True)
    
    # Hidratación diaria
    st.subheader("💧 Hidratación Diaria")
    col1, col2 = st.columns([3, 1])
    
    with col1:
        water_progress = st.session_state.water_intake / 8
        st.progress(water_progress)
        st.write(f"{st.session_state.water_intake}/8 vasos")
    
    with col2:
        if st.button("+ Vaso"):
            if st.session_state.water_intake < 8:
                st.session_state.water_intake += 1
                st.rerun()
        if st.button("- Vaso"):
            if st.session_state.water_intake > 0:
                st.session_state.water_intake -= 1
                st.rerun()
    
    # Entrenamientos recomendados
    st.subheader("🔥 Entrenamientos Recomendados")
    workouts = services['workout_service'].get_workouts()[:2]
    
    for workout in workouts:
        with st.container():
            st.markdown(f"""
            <div class="workout-card">
                <div style="display: flex; justify-content: space-between; align-items: center;">
                    <div>
                        <h4>{workout.image} {workout.name}</h4>
                        <p>{workout.duration} • {workout.level} • {workout.calories} kcal</p>
                        <p style="color: #666; font-size: 0.9rem;">{workout.description}</p>
                        <p style="color: #999; font-size: 0.8rem;">⭐ {workout.rating} • {workout.completions:,} completados</p>
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)
            
            if st.button(f"▶️ Iniciar {workout.name}", key=f"start_{workout.id}"):
                st.session_state.selected_workout = workout
                st.rerun()
    
    # Logros recientes
    if st.session_state.user_stats.achievements:
        st.subheader("🏆 Logros Recientes")
        for achievement in st.session_state.user_stats.achievements[-3:]:
            st.markdown(f'<div class="achievement-badge">{achievement}</div>', unsafe_allow_html=True)
    
    # Estado inicial sin entrenamientos
    if st.session_state.user_stats.total_workouts == 0:
        st.markdown("""
        <div style="text-align: center; padding: 2rem; background: white; border-radius: 1rem; margin: 2rem 0;">
            <div style="font-size: 3rem; margin-bottom: 1rem;">🏃‍♀️</div>
            <h3>¡Comienza tu Viaje Fitness!</h3>
            <p>Completa tu primer entrenamiento para empezar a ver tus estadísticas</p>
        </div>
        """, unsafe_allow_html=True)

    # Exportar Reporte (JSON)
    st.subheader("📤 Exportar Reporte")
    col_dl, _ = st.columns([1,3])
    with col_dl:
        if st.button("Exportar Reporte (JSON)"):
            report = services['report_generator'].generate_comprehensive_report(st.session_state.user_profile.id)
            import json as _json
            data = _json.dumps(report, ensure_ascii=False, indent=2)
            st.download_button(
                label="Descargar JSON",
                data=data,
                file_name="reporte_fithome.json",
                mime="application/json"
            )

    # Exportar Reporte (JSON)
    st.subheader("📤 Exportar Reporte")
    if st.button("Exportar Reporte (JSON)"):
        report = services['report_generator'].generate_comprehensive_report(st.session_state.user_profile.id)
        import json as _json
        data = _json.dumps(report, ensure_ascii=False, indent=2)
        st.download_button(
            label="Descargar JSON",
            data=data,
            file_name="reporte_fithome.json",
            mime="application/json"
        )

def show_workouts_tab(services):
    """Pestaña de entrenamientos"""
    st.title("💪 Mis Entrenamientos")
    
    # Filtros
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        filter_all = st.button("Todos", key="filter_all")
    with col2:
        filter_cardio = st.button("Cardio", key="filter_cardio")
    with col3:
        filter_strength = st.button("Fuerza", key="filter_strength")
    with col4:
        filter_flexibility = st.button("Flexibilidad", key="filter_flexibility")
    
    # Determinar filtro activo
    active_filter = None
    if filter_cardio:
        active_filter = "cardio"
    elif filter_strength:
        active_filter = "fuerza"
    elif filter_flexibility:
        active_filter = "flexibilidad"
    
    workouts = services['workout_service'].get_workouts(category=active_filter)
    
    for workout in workouts:
        with st.container():
            st.markdown(f"""
            <div class="workout-card">
                <div style="display: flex; justify-content: space-between; align-items: start;">
                    <div style="flex: 1;">
                        <h4>{workout.image} {workout.name}</h4>
                        <p><strong>{workout.category}</strong> • {workout.level}</p>
                        <p style="color: #666; margin: 0.5rem 0;">{workout.description}</p>
                        <div style="display: flex; gap: 1rem; font-size: 0.9rem; color: #999;">
                            <span>⏱️ {workout.duration}</span>
                            <span>⚡ {workout.calories} kcal</span>
                            <span>⭐ {workout.rating}</span>
                        </div>
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)
            
            col1, col2 = st.columns([3, 1])
            with col2:
                if st.button(f"▶️ Iniciar", key=f"workout_{workout.id}"):
                    st.session_state.selected_workout = workout
                    st.rerun()

def show_nutrition_tab(services):
    """Pestaña de nutrición"""
    st.title("🍎 Nutrición")
    
    # Obtener planes nutricionales
    nutrition_plans = services['nutrition_service'].get_nutrition_plans()
    
    if nutrition_plans:
        plan = nutrition_plans[0]  # Usar el primer plan disponible
        
        st.markdown(f"""
        <div style="background: linear-gradient(135deg, #10b981 0%, #059669 100%); padding: 2rem; border-radius: 1rem; color: white; margin-bottom: 2rem;">
            <h3>{plan.name}</h3>
            <p>{plan.calories_daily} kcal/día</p>
            <div style="display: grid; grid-template-columns: 1fr 1fr 1fr; gap: 1rem; margin-top: 1rem;">
                <div style="background: rgba(255,255,255,0.2); padding: 1rem; border-radius: 0.5rem; text-align: center;">
                    <div style="font-weight: bold;">{plan.carbs_percentage}%</div>
                    <div style="font-size: 0.9rem;">Carbohidratos</div>
                </div>
                <div style="background: rgba(255,255,255,0.2); padding: 1rem; border-radius: 0.5rem; text-align: center;">
                    <div style="font-weight: bold;">{plan.proteins_percentage}%</div>
                    <div style="font-size: 0.9rem;">Proteínas</div>
                </div>
                <div style="background: rgba(255,255,255,0.2); padding: 1rem; border-radius: 0.5rem; text-align: center;">
                    <div style="font-weight: bold;">{plan.fats_percentage}%</div>
                    <div style="font-size: 0.9rem;">Grasas</div>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    # Comidas del día
    meals = [
        {
            "name": "Desayuno",
            "time": "07:00 - 09:00",
            "calories": "350 kcal",
            "items": [
                "Avena con frutas y nueces (250 kcal)",
                "Yogurt griego bajo en grasa (100 kcal)"
            ]
        },
        {
            "name": "Almuerzo",
            "time": "12:00 - 14:00",
            "calories": "450 kcal",
            "items": [
                "Ensalada de pollo a la plancha (300 kcal)",
                "Arroz integral (100 kcal)",
                "Vegetales al vapor (50 kcal)"
            ]
        },
        {
            "name": "Cena",
            "time": "19:00 - 21:00",
            "calories": "400 kcal",
            "items": [
                "Salmón a la plancha (250 kcal)",
                "Verduras salteadas (100 kcal)",
                "Quinoa (50 kcal)"
            ]
        }
    ]
    
    for meal in meals:
        with st.expander(f"🍽️ {meal['name']} - {meal['calories']}"):
            st.write(f"**Horario:** {meal['time']}")
            st.write("**Alimentos:**")
            for item in meal['items']:
                st.write(f"• {item}")
            if st.button(f"Ver receta de {meal['name']}", key=f"recipe_{meal['name']}"):
                st.info(f"Receta detallada para {meal['name']} - ¡Próximamente!")
    
    # Tips nutricionales
    st.subheader("💡 Tips del Día")
    tips = [
        "Bebe al menos 8 vasos de agua al día",
        "Evita azúcares refinados",
        "Come cada 3-4 horas"
    ]
    
    for tip in tips:
        st.markdown(f'<div class="recommendation-card">• {tip}</div>', unsafe_allow_html=True)

def show_kids_tab(services):
    """Pestaña de zona infantil"""
    st.title("👶 Zona Infantil")
    
    # Filtros
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.button("Todos", key="kids_all")
    with col2:
        st.button("DIY", key="kids_diy")
    with col3:
        st.button("Ejercicio", key="kids_exercise")
    with col4:
        st.button("Manualidades", key="kids_crafts")
    
    activities = services['kids_service'].get_kids_activities()
    
    for activity in activities:
        with st.container():
            st.markdown(f"""
            <div class="kids-card">
                <div style="display: flex; justify-content: space-between; align-items: start; margin-bottom: 1rem;">
                    <div style="flex: 1;">
                        <h4>{activity.image} {activity.name}</h4>
                        <p><strong>{activity.type}</strong> • {activity.age}</p>
                        <p style="margin: 0.5rem 0;">{activity.duration}</p>
                        <span style="background: rgba(255,255,255,0.3); padding: 0.25rem 0.5rem; border-radius: 1rem; font-size: 0.8rem;">
                            {activity.difficulty}
                        </span>
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)
            
            with st.expander(f"Ver detalles de {activity.name}"):
                st.write("**Materiales necesarios:**")
                for material in activity.materials:
                    st.write(f"• {material}")
                
                st.write("**Pasos a seguir:**")
                for i, step in enumerate(activity.steps, 1):
                    st.write(f"{i}. {step}")
                
                st.write("**Beneficios:**")
                for benefit in activity.benefits:
                    st.success(benefit)

def show_movies_tab(services):
    """Pestaña de películas"""
    st.title("🎬 Películas Premium")
    
    if not st.session_state.user_profile.is_premium:
        st.markdown("""
        <div class="premium-card">
            <div style="font-size: 3rem; margin-bottom: 1rem;">👑</div>
            <h3>Contenido Premium</h3>
            <p>Accede a nuestra biblioteca completa de películas motivacionales y documentales educativos</p>
            <div style="margin: 1rem 0;">
                <p>✨ Más de 50 documentales</p>
                <p>🎬 Contenido exclusivo</p>
                <p>📱 Sin anuncios</p>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        if st.button("🔓 Obtener Premium - $9.99/mes", key="get_premium"):
            st.session_state.user_profile.is_premium = True
            st.success("¡Bienvenido a Premium! 🎉")
            st.rerun()
    else:
        movies = services['media_service'].get_movies()
        
        for movie in movies:
            with st.container():
                st.markdown(f"""
                <div class="workout-card">
                    <div style="display: flex; justify-content: space-between; align-items: start;">
                        <div style="flex: 1;">
                            <h4>{movie.image} {movie.title}</h4>
                            <p><strong>{movie.genre}</strong> • {movie.year}</p>
                            <p style="color: #666; margin: 0.5rem 0;">{movie.description}</p>
                            <div style="display: flex; gap: 1rem; font-size: 0.9rem; color: #999;">
                                <span>⏱️ {movie.duration}</span>
                                <span>⭐ {movie.rating}</span>
                            </div>
                            <p style="font-size: 0.8rem; color: #999; margin-top: 0.5rem;">
                                Con: {', '.join(movie.cast)}
                            </p>
                        </div>
                    </div>
                </div>
                """, unsafe_allow_html=True)
                
                col1, col2, col3 = st.columns([2, 1, 1])
                with col1:
                    if st.button(f"▶️ Reproducir", key=f"play_{movie.id}"):
                        st.success(f"Reproduciendo: {movie.title}")
                with col2:
                    if st.button("📥", key=f"download_{movie.id}"):
                        st.info("Descarga iniciada")
                with col3:
                    if st.button("📤", key=f"share_{movie.id}"):
                        st.info("Enlace copiado")

def show_community_tab(services):
    """Pestaña de comunidad local"""
    st.title("👥 Comunidad")
    with st.form("new_post"):
        content = st.text_area("Comparte tu progreso o un tip")
        submitted = st.form_submit_button("Publicar")
        if submitted and content.strip():
            st.session_state.community_posts.insert(0, {"user": st.session_state.user_profile.name or "Tú", "content": content.strip(), "likes": 0, "comments": []})
            st.success("Publicado")
            st.rerun()
    st.divider()
    for idx, post in enumerate(st.session_state.community_posts):
        st.markdown(f"**{post['user']}**: {post['content']}")
        col1, col2, col3 = st.columns([1,1,6])
        with col1:
            if st.button(f"👍 {post['likes']}", key=f"like_{idx}"):
                st.session_state.community_posts[idx]['likes'] += 1
                st.rerun()
        with col2:
            if st.button("💬", key=f"cmt_btn_{idx}"):
                st.session_state.notifications.append("Nuevo comentario en tu publicación")
        with col3:
            comment = st.text_input("", key=f"cmt_{idx}", placeholder="Escribe un comentario")
            if comment:
                st.session_state.community_posts[idx]['comments'].append(comment)
                st.success("Comentario agregado")
                st.rerun()
        if post['comments']:
            for c in post['comments'][-3:]:
                st.caption(f"• {c}")

def show_shop_tab(services):
    """Pestaña de tienda mock"""
    st.title("🛒 Tienda")
    items = [
        {"name": "Banda de Resistencia", "price": 14.99, "emoji": "🟣"},
        {"name": "Mancuernas 5kg", "price": 39.99, "emoji": "🏋️"},
        {"name": "Esterilla Yoga", "price": 24.99, "emoji": "🧘"},
    ]
    col_a, col_b = st.columns([3,1])
    with col_a:
        for i, it in enumerate(items):
            box = st.container()
            with box:
                st.markdown(f"{it['emoji']} **{it['name']}** - ${it['price']}")
                if st.button("Añadir al carrito", key=f"add_{i}"):
                    st.session_state.shop_cart.append(it)
                    st.success("Añadido al carrito")
    with col_b:
        st.subheader("🧺 Carrito")
        total = 0.0
        for j, it in enumerate(list(st.session_state.shop_cart)):
            st.write(f"{it['name']} - ${it['price']}")
            total += it['price']
        st.write(f"**Total: ${total:.2f}**")
        if st.button("Pagar"):
            st.info("Pago simulado exitoso ✅")
            st.session_state.shop_cart.clear()

def show_stats_tab(services):
    """Pestaña de progreso"""
    st.title("📊 Progreso")
    
    if st.session_state.user_stats.total_workouts == 0:
        st.markdown("""
        <div style="text-align: center; padding: 3rem; background: white; border-radius: 1rem;">
            <div style="font-size: 4rem; margin-bottom: 1rem;">📊</div>
            <h3>Sin datos aún</h3>
            <p>Completa algunos entrenamientos para ver tus estadísticas y gráficas de progreso</p>
        </div>
        """, unsafe_allow_html=True)
        
        if st.button("💪 Empezar Entrenando"):
            st.session_state.current_screen = 'workouts'
            st.rerun()
    else:
        # Estadísticas generales
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown(f"""
            <div class="stats-card">
                <h2>{st.session_state.user_stats.total_workouts}</h2>
                <p>Entrenamientos</p>
                <small>Total completados</small>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.markdown(f"""
            <div style="background: linear-gradient(135deg, #10b981 0%, #059669 100%); padding: 1.5rem; border-radius: 1rem; color: white; text-align: center;">
                <h2>{st.session_state.user_stats.total_calories:,}</h2>
                <p>Calorías</p>
                <small>Quemadas</small>
            </div>
            """, unsafe_allow_html=True)
        
        # Gráfico de progreso de peso
        if st.session_state.user_stats.weight_progress:
            st.subheader("📈 Progreso de Peso")
            weight_chart = services['chart_generator'].create_weight_progress_chart(st.session_state.user_profile.id)
            st.plotly_chart(weight_chart, use_container_width=True)
        
        # Metas del mes
        st.subheader("🎯 Metas del Mes")
        
        # Meta de entrenamientos
        workout_progress = min(100, (st.session_state.user_stats.total_workouts / 20) * 100)
        st.write(f"Entrenamientos ({st.session_state.user_stats.total_workouts}/20)")
        st.progress(workout_progress / 100)
        st.write(f"{workout_progress:.0f}% completado")
        
        # Botón para registrar peso
        if st.button("⚖️ Registrar Peso Actual"):
            weight = st.number_input("Peso actual (kg):", min_value=0.0, step=0.1)
            if weight > 0:
                if weight not in [w[1] for w in st.session_state.user_stats.weight_progress]:
                    st.session_state.user_stats.weight_progress.append((date.today(), weight))
                    st.success(f"Peso registrado: {weight} kg")
                    st.rerun()

def show_advanced_analysis_tab(services):
    """Pestaña de análisis avanzado"""
    st.title("📈 Análisis Avanzado")
    
    if st.session_state.user_stats.total_workouts == 0:
        st.markdown("""
        <div style="text-align: center; padding: 3rem; background: white; border-radius: 1rem;">
            <div style="font-size: 4rem; margin-bottom: 1rem;">📈</div>
            <h3>Análisis no disponible</h3>
            <p>Completa algunos entrenamientos para acceder al análisis avanzado de datos</p>
        </div>
        """, unsafe_allow_html=True)
    else:
        # Métricas calculadas
        metrics = services['data_analyzer'].calculate_fitness_metrics(st.session_state.user_profile.id)
        
        st.subheader("📊 Métricas de Fitness")
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("Entrenamientos Totales", metrics.total_workouts)
        with col2:
            st.metric("Calorías Totales", f"{metrics.total_calories_burned:,}")
        with col3:
            st.metric("Minutos Totales", f"{metrics.total_minutes:,}")
        with col4:
            st.metric("Racha Actual", f"{metrics.streak_days} días")
        
        # Gráficos de análisis
        st.subheader("📈 Análisis de Progreso")
        
        # Gráfico de resumen
        progress_chart = services['chart_generator'].create_progress_overview(st.session_state.user_profile.id)
        st.plotly_chart(progress_chart, use_container_width=True)
        
        # Gráfico de comparación semanal
        weekly_chart = services['chart_generator'].create_weekly_comparison(st.session_state.user_profile.id)
        st.plotly_chart(weekly_chart, use_container_width=True)
        
        # Análisis por categorías
        category_chart = services['chart_generator'].create_category_analysis(st.session_state.user_profile.id)
        st.plotly_chart(category_chart, use_container_width=True)
        
        # Reporte comprensivo
        if st.button("📋 Generar Reporte Completo"):
            with st.spinner("Generando reporte..."):
                report = services['report_generator'].generate_comprehensive_report(st.session_state.user_profile.id)
                
                st.subheader("📋 Reporte Comprensivo")
                st.write("**Resumen:**", report.get('summary', 'No disponible'))
                
                st.write("**Recomendaciones:**")
                for recommendation in report.get('recommendations', []):
                    st.markdown(f'<div class="recommendation-card">{recommendation}</div>', unsafe_allow_html=True)

def show_calendar_tab(services):
    """Pestaña de calendario de entrenamientos"""
    st.title("📅 Calendario de Entrenamientos")

    col1, col2 = st.columns([1,1])
    with col1:
        st.subheader("Vista Mensual (Heatmap)")
        # Reutilizamos el heatmap de calorías por día
        try:
            fig = services['chart_generator'].create_progress_overview(st.session_state.user_profile.id)
            st.plotly_chart(fig, use_container_width=True)
        except Exception:
            st.info("Sin datos suficientes para el calendario.")

    with col2:
        st.subheader("Semana Actual")
        # Mock de semana con quick start
        from datetime import datetime, timedelta
        today = datetime.now().date()
        week_days = [(today - timedelta(days=(today.weekday()-i))).strftime('%a %d') for i in range(7)]
        for d in week_days:
            col_l, col_r = st.columns([3,1])
            with col_l:
                st.write(d)
            with col_r:
                if st.button("▶️", key=f"quick_{d}"):
                    # Abrir lista de entrenamientos
                    st.session_state.current_screen = 'dashboard'
                    st.session_state.selected_workout = services['workout_service'].get_workouts()[:1][0]
                    st.rerun()

def show_habits_tab(services):
    """Pestaña de hábitos y metas"""
    st.title("🎯 Hábitos y Metas")

    st.subheader("Hábitos Semanales")
    for i, habit in enumerate(st.session_state.habits):
        target = habit["target_per_week"]
        done = habit["completed"]
        progress = min(1.0, done/target if target else 0)
        col_l, col_m, col_r = st.columns([2,2,1])
        with col_l:
            st.write(f"{habit['name']} ({done}/{target})")
            st.progress(progress)
        with col_m:
            if st.button("+1", key=f"inc_{i}"):
                st.session_state.habits[i]["completed"] = min(target, done+1)
                st.rerun()
            if st.button("-1", key=f"dec_{i}"):
                st.session_state.habits[i]["completed"] = max(0, done-1)
                st.rerun()
        with col_r:
            if st.button("↺", key=f"reset_{i}"):
                st.session_state.habits[i]["completed"] = 0
                st.rerun()

    st.divider()
    st.subheader("Metas")
    for i, goal in enumerate(st.session_state.goals_list):
        col_a, col_b = st.columns([6,1])
        with col_a:
            st.write(goal["title"])
        with col_b:
            toggled = st.checkbox("Hecha", value=goal["done"], key=f"goal_{i}")
            st.session_state.goals_list[i]["done"] = toggled
    
    st.divider()
    with st.expander("Añadir nuevo hábito/meta"):
        tabh, tabg = st.tabs(["Hábito", "Meta"])
        with tabh:
            name = st.text_input("Nombre del hábito")
            target = st.number_input("Objetivo semanal", min_value=1, value=5)
            if st.button("Añadir hábito") and name:
                st.session_state.habits.append({"name": name, "target_per_week": int(target), "completed": 0})
                st.rerun()
        with tabg:
            title = st.text_input("Título de la meta")
            if st.button("Añadir meta") and title:
                st.session_state.goals_list.append({"title": title, "done": False})
                st.rerun()

# =============================================================================
# PANTALLA DE ENTRENAMIENTO
# =============================================================================

def show_workout_screen(services):
    """Pantalla de entrenamiento en progreso"""
    workout = st.session_state.selected_workout
    
    if not st.session_state.workout_in_progress:
        # Vista previa del entrenamiento
        st.markdown(f"""
        <div style="text-align: center; padding: 2rem; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; border-radius: 1rem; margin-bottom: 2rem;">
            <div style="font-size: 4rem; margin-bottom: 1rem;">{workout.image}</div>
            <h2>{workout.name}</h2>
            <p>{workout.description}</p>
        </div>
        """, unsafe_allow_html=True)
        
        # Información del entrenamiento
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("Duración", workout.duration)
        with col2:
            st.metric("Calorías", workout.calories)
        with col3:
            st.metric("Nivel", workout.level)
        with col4:
            st.metric("Rating", f"⭐ {workout.rating}")
        
        # Lista de ejercicios
        st.subheader(f"Ejercicios ({len(workout.exercises)})")
        for i, exercise in enumerate(workout.exercises, 1):
            with st.container():
                st.markdown(f"""
                <div style="background: #f8f9fa; padding: 1rem; border-radius: 0.5rem; margin-bottom: 0.5rem; display: flex; align-items: center;">
                    <div style="background: #6c757d; color: white; width: 2rem; height: 2rem; border-radius: 50%; display: flex; align-items: center; justify-content: center; margin-right: 1rem; font-weight: bold;">
                        {i}
                    </div>
                    <div>
                        <strong>{exercise['name']}</strong><br>
                        <small>{exercise.get('duration', exercise.get('sets', ''))}</small>
                        {f" • Descanso: {exercise['rest']}" if 'rest' in exercise else ""}
                    </div>
                </div>
                """, unsafe_allow_html=True)
        
        # Botones de acción
        col1, col2 = st.columns([1, 1])
        with col1:
            if st.button("⬅️ Volver"):
                st.session_state.selected_workout = None
                st.rerun()
        
        with col2:
            if st.button("▶️ Comenzar Entrenamiento"):
                st.session_state.workout_in_progress = True
                st.session_state.current_exercise = 0
                st.session_state.exercise_timer = 30
                st.rerun()
    
    else:
        # Entrenamiento en progreso
        current_ex = workout.exercises[st.session_state.current_exercise]
        
        st.markdown(f"""
        <div style="text-align: center; background: #000; color: white; padding: 2rem; border-radius: 1rem;">
            <h3>Ejercicio {st.session_state.current_exercise + 1}/{len(workout.exercises)}</h3>
            <h2>{current_ex['name']}</h2>
            <div style="font-size: 4rem; margin: 2rem 0;">{st.session_state.exercise_timer}</div>
            <div style="font-size: 2rem; margin-bottom: 2rem;">💪</div>
            <p>{current_ex.get('duration', current_ex.get('sets', ''))}</p>
        </div>
        """, unsafe_allow_html=True)
        
        col1, col2, col3 = st.columns([1, 1, 1])
        
        with col1:
            if st.button("⏸️ Pausar"):
                st.session_state.workout_in_progress = False
                st.rerun()
        
        with col2:
            if st.button("+10s"):
                st.session_state.exercise_timer += 10
                st.rerun()
        
        with col3:
            if st.session_state.current_exercise < len(workout.exercises) - 1:
                if st.button("⏭️ Siguiente"):
                    st.session_state.current_exercise += 1
                    st.session_state.exercise_timer = 30
                    st.rerun()
            else:
                if st.button("✅ Finalizar"):
                    # Completar entrenamiento
                    duration_minutes = int(workout.duration.split()[0])
                    calories_burned = int(workout.calories.split('-')[1]) if '-' in workout.calories else 200
                    
                    services['workout_service'].complete_workout_session(
                        st.session_state.user_profile.id,
                        workout.id,
                        duration_minutes,
                        calories_burned,
                        4  # Rating por defecto
                    )
                    
                    st.session_state.workout_in_progress = False
                    st.session_state.selected_workout = None
                    st.session_state.current_exercise = 0
                    st.success(f"¡Felicitaciones! Has completado '{workout.name}'. +{calories_burned} kcal quemadas.")
                    time.sleep(2)
                    st.rerun()

# =============================================================================
# FUNCIÓN PRINCIPAL
# =============================================================================

def main():
    """Función principal de la aplicación"""
    try:
        # Inicializar estado de sesión
        init_session_state()
        
        if not st.session_state.services:
            st.error("Error inicializando servicios. Por favor, recarga la página.")
            return
        
        services = st.session_state.services

        # Tema oscuro dinámico
        if st.session_state.dark_mode:
            st.markdown(
                """
                <style>
                body { background: #0b1120 !important; }
                .main-header { background: linear-gradient(135deg, #0f172a 0%, #111827 100%) !important; }
                .workout-card, .chart-container, .metric-container { background: rgba(15, 23, 42, 0.92) !important; color: #e5e7eb !important; }
                .kids-card { background: linear-gradient(135deg, #334155 0%, #0f172a 100%) !important; color: #e5e7eb !important; }
                .premium-card { background: linear-gradient(135deg, #1f2937 0%, #111827 100%) !important; }
                .stButton > button { background: linear-gradient(135deg, #4f46e5 0%, #7c3aed 100%) !important; }
                .stTextInput > div > div > input { background: #0b1220 !important; color: #e5e7eb !important; border-color: #374151 !important; }
                .stSelectbox > div > div > select { background: #0b1220 !important; color: #e5e7eb !important; }
                </style>
                """,
                unsafe_allow_html=True,
            )
        
        # Aplicar color de acento
        accent = st.session_state.accent_color
        st.markdown(f"""
            <style>
            :root {{ --accent: {accent}; }}
            .stButton > button {{ box-shadow: 0 8px 20px {accent}55; }}
            .progress-fill {{ background: linear-gradient(90deg, {accent} 0%, #764ba2 100%); }}
            .metric-container:hover {{ box-shadow: 0 15px 35px {accent}33; }}
            .recommendation-card {{ border-image: linear-gradient(135deg, {accent}, #764ba2) 1; }}
            .sidebar-user-info {{ box-shadow: 0 10px 30px {accent}33; }}
            </style>
        """, unsafe_allow_html=True)
        
        # Verificar si hay un entrenamiento seleccionado
        if st.session_state.selected_workout:
            show_workout_screen(services)
            return
        
        # Navegación principal
        if st.session_state.current_screen == 'loading':
            show_loading_screen()
        elif st.session_state.current_screen == 'auth':
            show_auth_screen(services)
        elif st.session_state.current_screen == 'onboarding':
            show_onboarding_screen(services)
        elif st.session_state.current_screen == 'dashboard':
            show_dashboard(services)
        
    except Exception as e:
        logger.error(f"Error en función principal: {e}")
        st.error("Ha ocurrido un error inesperado. Por favor, recarga la página.")

if __name__ == "__main__":
    main()
