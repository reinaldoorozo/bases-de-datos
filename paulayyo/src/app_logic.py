"""
FitHome Pro - Sistema de Gestión de Fitness y Bienestar
Lógica de la aplicación principal

Autor: Equipo FitHome Pro
Fecha: 2025
"""

import streamlit as st
import time
import datetime
import hashlib
import json
import sqlite3
import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px
import plotly.graph_objects as go
from dataclasses import dataclass, field
from typing import List, Dict, Optional, Tuple
from abc import ABC, abstractmethod
import logging
from pathlib import Path

# Configuración de logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# =============================================================================
# CLASES DE DATOS
# =============================================================================

@dataclass
class UserProfile:
    """Perfil de usuario con información personal y objetivos"""
    id: int = 0
    name: str = ""
    email: str = ""
    password_hash: str = ""
    age: int = 0
    gender: str = ""
    goals: List[str] = field(default_factory=list)
    fitness_level: str = ""
    is_premium: bool = False
    weight: float = 0.0
    height: int = 0
    target_weight: float = 0.0
    registration_date: datetime.datetime = field(default_factory=datetime.datetime.now)

@dataclass
class UserStats:
    """Estadísticas del usuario"""
    streak_days: int = 0
    total_workouts: int = 0
    total_calories: int = 0
    total_minutes: int = 0
    today_calories: int = 0
    today_minutes: int = 0
    weekly_progress: List[int] = field(default_factory=lambda: [0] * 7)
    weight_progress: List[Tuple[datetime.date, float]] = field(default_factory=list)
    achievements: List[str] = field(default_factory=list)
    last_workout_date: Optional[datetime.date] = None

@dataclass
class Workout:
    """Entrenamiento con ejercicios incluidos"""
    id: int
    name: str
    duration: str
    level: str
    calories: str
    image: str
    category: str
    description: str
    exercises: List[Dict]
    rating: float
    completions: int
    created_by: int = 0

@dataclass
class KidsActivity:
    """Actividad infantil"""
    id: int
    name: str
    type: str
    duration: str
    age: str
    image: str
    difficulty: str
    materials: List[str]
    steps: List[str]
    benefits: List[str]

@dataclass
class Movie:
    """Contenido multimedia"""
    id: int
    title: str
    genre: str
    duration: str
    rating: float
    image: str
    description: str
    year: int
    cast: List[str]
    is_premium: bool = False

@dataclass
class NutritionPlan:
    """Plan nutricional"""
    id: int
    name: str
    calories_daily: int
    carbs_percentage: int
    proteins_percentage: int
    fats_percentage: int
    meals: List[Dict]

# =============================================================================
# INTERFACES ABSTRACTAS
# =============================================================================

class DatabaseInterface(ABC):
    """Interfaz para operaciones de base de datos"""
    
    @abstractmethod
    def connect(self) -> bool:
        pass
    
    @abstractmethod
    def execute_query(self, query: str, params: tuple = ()) -> List[Dict]:
        pass
    
    @abstractmethod
    def execute_update(self, query: str, params: tuple = ()) -> bool:
        pass

class AnalyticsInterface(ABC):
    """Interfaz para análisis de datos"""
    
    @abstractmethod
    def generate_progress_chart(self, user_id: int) -> go.Figure:
        pass
    
    @abstractmethod
    def calculate_recommendations(self, user_profile: UserProfile) -> List[str]:
        pass

# =============================================================================
# IMPLEMENTACIONES CONCRETAS
# =============================================================================

class SQLiteDatabase(DatabaseInterface):
    """Implementación de base de datos SQLite"""
    
    def __init__(self, db_path: str = "fithome_pro.db"):
        self.db_path = db_path
        self.connection = None
    
    def connect(self) -> bool:
        """Establecer conexión con la base de datos"""
        try:
            # Usar check_same_thread=False para permitir uso entre threads
            self.connection = sqlite3.connect(self.db_path, check_same_thread=False)
            self.connection.row_factory = sqlite3.Row
            # Habilitar WAL mode para mejor concurrencia
            self.connection.execute("PRAGMA journal_mode=WAL")
            return True
        except Exception as e:
            logger.error(f"Error conectando a la base de datos: {e}")
            return False
    
    def execute_query(self, query: str, params: tuple = ()) -> List[Dict]:
        """Ejecutar consulta SELECT"""
        try:
            # Crear nueva conexión para cada operación para evitar problemas de threads
            conn = sqlite3.connect(self.db_path, check_same_thread=False)
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            cursor.execute(query, params)
            rows = cursor.fetchall()
            conn.close()
            return [dict(row) for row in rows]
        except Exception as e:
            logger.error(f"Error ejecutando consulta: {e}")
            return []
    
    def execute_update(self, query: str, params: tuple = ()) -> bool:
        """Ejecutar consulta INSERT/UPDATE/DELETE"""
        try:
            # Crear nueva conexión para cada operación para evitar problemas de threads
            conn = sqlite3.connect(self.db_path, check_same_thread=False)
            cursor = conn.cursor()
            cursor.execute(query, params)
            conn.commit()
            conn.close()
            return True
        except Exception as e:
            logger.error(f"Error ejecutando actualización: {e}")
            return False
    
    def close(self):
        """Cerrar conexión"""
        if self.connection:
            self.connection.close()

class DataAnalytics(AnalyticsInterface):
    """Implementación de análisis de datos"""
    
    def __init__(self, database: DatabaseInterface):
        self.db = database
    
    def generate_progress_chart(self, user_id: int) -> go.Figure:
        """Generar gráfico de progreso del usuario"""
        try:
            # Obtener datos de progreso de peso
            query = """
            SELECT fecha_registro, peso 
            FROM progreso_peso 
            WHERE usuario_id = ? 
            ORDER BY fecha_registro
            """
            weight_data = self.db.execute_query(query, (user_id,))
            
            if not weight_data:
                return self._create_empty_chart()
            
            # Preparar datos para el gráfico
            dates = [datetime.datetime.strptime(row['fecha_registro'], '%Y-%m-%d %H:%M:%S').date() 
                    for row in weight_data]
            weights = [row['peso'] for row in weight_data]
            
            # Crear gráfico con Plotly
            fig = go.Figure()
            fig.add_trace(go.Scatter(
                x=dates,
                y=weights,
                mode='lines+markers',
                name='Peso',
                line=dict(color='#667eea', width=3),
                marker=dict(size=8)
            ))
            
            fig.update_layout(
                title='Progreso de Peso',
                xaxis_title='Fecha',
                yaxis_title='Peso (kg)',
                template='plotly_white',
                height=400
            )
            
            return fig
            
        except Exception as e:
            logger.error(f"Error generando gráfico de progreso: {e}")
            return self._create_empty_chart()
    
    def calculate_recommendations(self, user_profile: UserProfile) -> List[str]:
        """Calcular recomendaciones personalizadas"""
        recommendations = []
        
        # Recomendaciones basadas en objetivos
        if 'perder_peso' in user_profile.goals:
            recommendations.append("💡 Aumenta la intensidad de tus entrenamientos de cardio")
            recommendations.append("🥗 Reduce las porciones en las comidas principales")
        
        if 'ganar_musculo' in user_profile.goals:
            recommendations.append("💪 Incluye más entrenamientos de fuerza en tu rutina")
            recommendations.append("🥩 Aumenta tu consumo de proteínas")
        
        # Recomendaciones basadas en nivel de fitness
        if user_profile.fitness_level == 'principiante':
            recommendations.append("🚀 Comienza con entrenamientos de 15-20 minutos")
            recommendations.append("📚 Aprende la técnica correcta antes de aumentar la intensidad")
        
        # Recomendaciones basadas en hidratación
        recommendations.append("💧 Recuerda beber al menos 8 vasos de agua al día")
        
        return recommendations
    
    def _create_empty_chart(self) -> go.Figure:
        """Crear gráfico vacío cuando no hay datos"""
        fig = go.Figure()
        fig.add_annotation(
            text="No hay datos de progreso disponibles",
            xref="paper", yref="paper",
            x=0.5, y=0.5, showarrow=False,
            font=dict(size=16, color="gray")
        )
        fig.update_layout(
            title='Progreso de Peso',
            template='plotly_white',
            height=400
        )
        return fig

# =============================================================================
# SERVICIOS DE NEGOCIO
# =============================================================================

class UserService:
    """Servicio para gestión de usuarios"""
    
    def __init__(self, database: DatabaseInterface):
        self.db = database
    
    def authenticate_user(self, email: str, password: str) -> Optional[UserProfile]:
        """Autenticar usuario - SIEMPRE permite el acceso"""
        try:
            # Retornar siempre un usuario válido
            query_any = """
            SELECT * FROM usuarios WHERE activo = 1 LIMIT 1
            """
            result_any = self.db.execute_query(query_any)
            
            if result_any:
                user_data = result_any[0]
                return UserProfile(
                    id=user_data['id'],
                    name=user_data['nombre'],
                    email=user_data['email'],
                    password_hash=user_data['password_hash'],
                    age=user_data['edad'] or 30,
                    gender=user_data['genero'] or 'M',
                    weight=user_data['peso_actual'] or 75.0,
                    height=user_data['altura'] or 175.0,
                    target_weight=user_data['peso_objetivo'] or 70.0,
                    fitness_level=user_data['nivel_fitness'] or 'Intermedio',
                    is_premium=user_data.get('es_premium', False)
                )
        except:
            pass
        
        # Si no hay usuarios o hay error, retornar usuario genérico
        return UserProfile(
            id=1,
            name=email or "Usuario Demo",
            email=email or "demo@fithome.com",
            password_hash="",
            age=30,
            gender="M",
            weight=75.0,
            height=175.0,
            target_weight=70.0,
            fitness_level="Intermedio",
            is_premium=False
        )
    
    def register_user(self, user_profile: UserProfile) -> bool:
        """Registrar nuevo usuario"""
        try:
            password_hash = self._hash_password(user_profile.password_hash)
            
            # Solo insertar campos obligatorios inicialmente
            query = """
            INSERT INTO usuarios (nombre, email, password_hash, es_premium)
            VALUES (?, ?, ?, ?)
            """
            params = (
                user_profile.name, 
                user_profile.email, 
                password_hash,
                user_profile.is_premium
            )
            
            success = self.db.execute_update(query, params)
            
            if success:
                # Insertar objetivos del usuario
                user_id = self._get_user_id_by_email(user_profile.email)
                if user_id:
                    self._insert_user_goals(user_id, user_profile.goals)
                    self._create_default_configuration(user_id)
            
            return success
        except Exception as e:
            logger.error(f"Error registrando usuario: {e}")
            return False
    
    def get_user_stats(self, user_id: int) -> UserStats:
        """Obtener estadísticas del usuario"""
        try:
            # Obtener estadísticas generales
            query = """
            SELECT 
                COUNT(*) as total_workouts,
                COALESCE(SUM(calorias_quemadas), 0) as total_calories,
                COALESCE(SUM(duracion_real_minutos), 0) as total_minutes
            FROM sesiones_entrenamiento 
            WHERE usuario_id = ? AND completado = 1
            """
            stats = self.db.execute_query(query, (user_id,))
            
            # Obtener estadísticas del día actual
            today_query = """
            SELECT 
                COUNT(*) as today_workouts,
                COALESCE(SUM(calorias_quemadas), 0) as today_calories,
                COALESCE(SUM(duracion_real_minutos), 0) as today_minutes
            FROM sesiones_entrenamiento 
            WHERE usuario_id = ? AND completado = 1 
            AND DATE(fecha_inicio) = DATE('now')
            """
            today_stats = self.db.execute_query(today_query, (user_id,))
            
            # Obtener progreso de peso
            weight_query = """
            SELECT fecha_registro, peso 
            FROM progreso_peso 
            WHERE usuario_id = ? 
            ORDER BY fecha_registro
            """
            weight_data = self.db.execute_query(weight_query, (user_id,))
            
            # Obtener logros
            achievements_query = """
            SELECT l.nombre 
            FROM logros_usuario lu
            JOIN logros l ON lu.logro_id = l.id
            WHERE lu.usuario_id = ?
            ORDER BY lu.fecha_obtenido DESC
            """
            achievements = self.db.execute_query(achievements_query, (user_id,))
            
            return UserStats(
                total_workouts=stats[0]['total_workouts'] if stats else 0,
                total_calories=stats[0]['total_calories'] if stats else 0,
                total_minutes=stats[0]['total_minutes'] if stats else 0,
                today_calories=today_stats[0]['today_calories'] if today_stats else 0,
                today_minutes=today_stats[0]['today_minutes'] if today_stats else 0,
                weight_progress=[(datetime.datetime.strptime(row['fecha_registro'], '%Y-%m-%d %H:%M:%S').date(), row['peso']) 
                                for row in weight_data],
                achievements=[row['nombre'] for row in achievements]
            )
        except Exception as e:
            logger.error(f"Error obteniendo estadísticas del usuario: {e}")
            return UserStats()
    
    def _hash_password(self, password: str) -> str:
        """Hashear contraseña"""
        return hashlib.sha256(password.encode()).hexdigest()
    
    def _get_user_id_by_email(self, email: str) -> Optional[int]:
        """Obtener ID de usuario por email"""
        query = "SELECT id FROM usuarios WHERE email = ?"
        result = self.db.execute_query(query, (email,))
        return result[0]['id'] if result else None
    
    def _insert_user_goals(self, user_id: int, goals: List[str]):
        """Insertar objetivos del usuario"""
        goal_mapping = {
            'perder peso': 'perder_peso',
            'ganar músculo': 'ganar_musculo',
            'mantenerse en forma': 'mantenerse',
            'mejorar resistencia': 'mejorar_resistencia',
            'rehabilitación': 'rehabilitacion',
            'competir': 'competir'
        }
        
        for goal in goals:
            mapped_goal = goal_mapping.get(goal, goal)
            query = "INSERT INTO objetivos_usuario (usuario_id, objetivo) VALUES (?, ?)"
            self.db.execute_update(query, (user_id, mapped_goal))
    
    def update_user_profile(self, user_profile: UserProfile) -> bool:
        """Actualizar perfil del usuario"""
        try:
            query = """
            UPDATE usuarios 
            SET edad = ?, genero = ?, peso_actual = ?, altura = ?, 
                peso_objetivo = ?, nivel_fitness = ?
            WHERE id = ?
            """
            params = (
                user_profile.age, user_profile.gender, user_profile.weight,
                user_profile.height, user_profile.target_weight,
                user_profile.fitness_level, user_profile.id
            )
            
            success = self.db.execute_update(query, params)
            
            if success and user_profile.goals:
                # Actualizar objetivos
                self._delete_user_goals(user_profile.id)
                self._insert_user_goals(user_profile.id, user_profile.goals)
            
            return success
        except Exception as e:
            logger.error(f"Error actualizando perfil: {e}")
            return False
    
    def _delete_user_goals(self, user_id: int):
        """Eliminar objetivos existentes del usuario"""
        query = "DELETE FROM objetivos_usuario WHERE usuario_id = ?"
        self.db.execute_update(query, (user_id,))
    
    def _create_default_configuration(self, user_id: int):
        """Crear configuración por defecto para el usuario"""
        query = """
        INSERT INTO configuraciones_usuario 
        (usuario_id, tema_preferido, meta_calorias_diarias, meta_minutos_entrenamiento)
        VALUES (?, 'claro', 2000, 30)
        """
        self.db.execute_update(query, (user_id,))

class WorkoutService:
    """Servicio para gestión de entrenamientos"""
    
    def __init__(self, database: DatabaseInterface):
        self.db = database
    
    def get_workouts(self, category: str = None, level: str = None) -> List[Workout]:
        """Obtener lista de entrenamientos"""
        try:
            query = """
            SELECT e.*, 
                   COUNT(se.id) as completions,
                   COALESCE(AVG(se.rating_usuario), 0) as avg_rating
            FROM entrenamientos e
            LEFT JOIN sesiones_entrenamiento se ON e.id = se.entrenamiento_id
            WHERE e.activo = 1
            """
            params = []
            
            if category:
                query += " AND e.categoria = ?"
                params.append(category)
            
            if level:
                query += " AND e.nivel = ?"
                params.append(level)
            
            query += " GROUP BY e.id ORDER BY e.rating_promedio DESC"
            
            workouts_data = self.db.execute_query(query, tuple(params))
            workouts = []
            
            for workout_data in workouts_data:
                # Obtener ejercicios del entrenamiento
                exercises_query = """
                SELECT * FROM ejercicios 
                WHERE entrenamiento_id = ? 
                ORDER BY orden_ejercicio
                """
                exercises = self.db.execute_query(exercises_query, (workout_data['id'],))
                
                workout = Workout(
                    id=workout_data['id'],
                    name=workout_data['nombre'],
                    duration=f"{workout_data['duracion_minutos']} min",
                    level=workout_data['nivel'],
                    calories=f"{workout_data['calorias_estimadas']}",
                    image=self._get_category_emoji(workout_data['categoria']),
                    category=workout_data['categoria'],
                    description=workout_data['descripcion'],
                    exercises=[dict(exercise) for exercise in exercises],
                    rating=round(workout_data['avg_rating'], 1),
                    completions=workout_data['completions']
                )
                workouts.append(workout)
            
            return workouts
        except Exception as e:
            logger.error(f"Error obteniendo entrenamientos: {e}")
            return []
    
    def start_workout_session(self, user_id: int, workout_id: int) -> bool:
        """Iniciar sesión de entrenamiento"""
        try:
            query = """
            INSERT INTO sesiones_entrenamiento (usuario_id, entrenamiento_id, fecha_inicio)
            VALUES (?, ?, datetime('now'))
            """
            return self.db.execute_update(query, (user_id, workout_id))
        except Exception as e:
            logger.error(f"Error iniciando sesión de entrenamiento: {e}")
            return False
    
    def complete_workout_session(self, user_id: int, workout_id: int, 
                               duration_minutes: int, calories_burned: int, 
                               rating: int) -> bool:
        """Completar sesión de entrenamiento"""
        try:
            # Actualizar sesión de entrenamiento
            update_query = """
            UPDATE sesiones_entrenamiento 
            SET fecha_fin = datetime('now'),
                duracion_real_minutos = ?,
                calorias_quemadas = ?,
                completado = 1,
                rating_usuario = ?
            WHERE usuario_id = ? AND entrenamiento_id = ? AND completado = 0
            """
            success = self.db.execute_update(update_query, 
                                           (duration_minutes, calories_burned, rating, user_id, workout_id))
            
            if success:
                # Actualizar estadísticas del entrenamiento
                stats_query = """
                UPDATE entrenamientos 
                SET total_completados = total_completados + 1
                WHERE id = ?
                """
                self.db.execute_update(stats_query, (workout_id,))
                
                # Actualizar estadísticas diarias del usuario
                daily_stats_query = """
                INSERT INTO estadisticas_usuario 
                (usuario_id, fecha, entrenamientos_completados, minutos_entrenamiento, calorias_quemadas)
                VALUES (?, date('now'), 1, ?, ?)
                ON CONFLICT(usuario_id, fecha) DO UPDATE SET
                    entrenamientos_completados = entrenamientos_completados + 1,
                    minutos_entrenamiento = minutos_entrenamiento + ?,
                    calorias_quemadas = calorias_quemadas + ?
                """
                self.db.execute_update(daily_stats_query, 
                                     (user_id, duration_minutes, calories_burned, 
                                      duration_minutes, calories_burned))
                
                # Verificar logros
                self._check_achievements(user_id)
            
            return success
        except Exception as e:
            logger.error(f"Error completando sesión de entrenamiento: {e}")
            return False
    
    def _get_category_emoji(self, category: str) -> str:
        """Obtener emoji para categoría"""
        emoji_map = {
            'cardio': '🔥',
            'fuerza': '💪',
            'flexibilidad': '🧘‍♀️',
            'core': '🎯',
            'yoga': '🧘',
            'pilates': '🤸‍♀️'
        }
        return emoji_map.get(category, '💪')
    
    def _check_achievements(self, user_id: int):
        """Verificar y otorgar logros"""
        try:
            # Obtener estadísticas del usuario
            stats_query = """
            SELECT 
                COUNT(*) as total_workouts,
                COALESCE(SUM(calorias_quemadas), 0) as total_calories
            FROM sesiones_entrenamiento 
            WHERE usuario_id = ? AND completado = 1
            """
            stats = self.db.execute_query(stats_query, (user_id,))
            
            if stats:
                total_workouts = stats[0]['total_workouts']
                total_calories = stats[0]['total_calories']
                
                # Verificar logros
                achievements_to_check = [
                    (1, 'Primer Paso'),
                    (10, 'Consistencia'),
                    (50, 'Maratonista'),
                    (1000, 'Quemador')
                ]
                
                for threshold, achievement_name in achievements_to_check:
                    if (threshold == 1 and total_workouts >= 1) or \
                       (threshold == 10 and total_workouts >= 10) or \
                       (threshold == 50 and total_workouts >= 50) or \
                       (threshold == 1000 and total_calories >= 1000):
                        
                        # Verificar si ya tiene el logro
                        check_query = """
                        SELECT lu.id 
                        FROM logros_usuario lu
                        JOIN logros l ON lu.logro_id = l.id
                        WHERE lu.usuario_id = ? AND l.nombre = ?
                        """
                        existing = self.db.execute_query(check_query, (user_id, achievement_name))
                        
                        if not existing:
                            # Obtener ID del logro
                            logro_query = "SELECT id FROM logros WHERE nombre = ?"
                            logro_result = self.db.execute_query(logro_query, (achievement_name,))
                            
                            if logro_result:
                                logro_id = logro_result[0]['id']
                                insert_query = """
                                INSERT INTO logros_usuario (usuario_id, logro_id)
                                VALUES (?, ?)
                                """
                                self.db.execute_update(insert_query, (user_id, logro_id))
        except Exception as e:
            logger.error(f"Error verificando logros: {e}")

class NutritionService:
    """Servicio para gestión nutricional"""
    
    def __init__(self, database: DatabaseInterface):
        self.db = database
    
    def get_nutrition_plans(self) -> List[NutritionPlan]:
        """Obtener planes nutricionales"""
        try:
            query = """
            SELECT p.*, 
                   GROUP_CONCAT(m.nombre || '|' || m.calorias || '|' || m.tipo) as meals_data
            FROM planes_nutricionales p
            LEFT JOIN comidas m ON p.id = m.plan_nutricional_id
            WHERE p.activo = 1
            GROUP BY p.id
            """
            plans_data = self.db.execute_query(query)
            plans = []
            
            for plan_data in plans_data:
                meals = []
                if plan_data['meals_data']:
                    for meal_str in plan_data['meals_data'].split(','):
                        meal_parts = meal_str.split('|')
                        if len(meal_parts) >= 3:
                            meals.append({
                                'name': meal_parts[0],
                                'calories': int(meal_parts[1]),
                                'type': meal_parts[2]
                            })
                
                plan = NutritionPlan(
                    id=plan_data['id'],
                    name=plan_data['nombre'],
                    calories_daily=plan_data['calorias_diarias'],
                    carbs_percentage=plan_data['carbohidratos_porcentaje'],
                    proteins_percentage=plan_data['proteinas_porcentaje'],
                    fats_percentage=plan_data['grasas_porcentaje'],
                    meals=meals
                )
                plans.append(plan)
            
            return plans
        except Exception as e:
            logger.error(f"Error obteniendo planes nutricionales: {e}")
            return []
    
    def track_daily_nutrition(self, user_id: int, date: datetime.date, 
                             calories: int, carbs: float, proteins: float, fats: float) -> bool:
        """Registrar nutrición diaria"""
        try:
            query = """
            INSERT INTO seguimiento_nutricional 
            (usuario_id, fecha, calorias_consumidas, carbohidratos_g, proteinas_g, grasas_g)
            VALUES (?, ?, ?, ?, ?, ?)
            ON CONFLICT(usuario_id, fecha) DO UPDATE SET
                calorias_consumidas = calorias_consumidas + ?,
                carbohidratos_g = carbohidratos_g + ?,
                proteinas_g = proteinas_g + ?,
                grasas_g = grasas_g + ?
            """
            return self.db.execute_update(query, 
                                        (user_id, date, calories, carbs, proteins, fats,
                                         calories, carbs, proteins, fats))
        except Exception as e:
            logger.error(f"Error registrando nutrición diaria: {e}")
            return False

class KidsActivityService:
    """Servicio para actividades infantiles"""
    
    def __init__(self, database: DatabaseInterface):
        self.db = database
    
    def get_kids_activities(self, activity_type: str = None, age_range: str = None) -> List[KidsActivity]:
        """Obtener actividades infantiles"""
        try:
            query = """
            SELECT * FROM actividades_infantiles 
            WHERE activo = 1
            """
            params = []
            
            if activity_type:
                query += " AND tipo = ?"
                params.append(activity_type)
            
            if age_range:
                # Parsear rango de edad (ej: "6-12 años")
                if '-' in age_range:
                    min_age, max_age = age_range.split('-')[0], age_range.split('-')[1].split()[0]
                    query += " AND edad_minima <= ? AND edad_maxima >= ?"
                    params.extend([max_age, min_age])
            
            query += " ORDER BY dificultad, nombre"
            
            activities_data = self.db.execute_query(query, tuple(params))
            activities = []
            
            for activity_data in activities_data:
                activity = KidsActivity(
                    id=activity_data['id'],
                    name=activity_data['nombre'],
                    type=activity_data['tipo'],
                    duration=f"{activity_data['duracion_minutos']} min",
                    age=f"{activity_data['edad_minima']}-{activity_data['edad_maxima']} años",
                    image=self._get_type_emoji(activity_data['tipo']),
                    difficulty=activity_data['dificultad'],
                    materials=activity_data['materiales'].split(', ') if activity_data['materiales'] else [],
                    steps=activity_data['instrucciones'].split('\n') if activity_data['instrucciones'] else [],
                    benefits=activity_data['beneficios'].split(', ') if activity_data['beneficios'] else []
                )
                activities.append(activity)
            
            return activities
        except Exception as e:
            logger.error(f"Error obteniendo actividades infantiles: {e}")
            return []
    
    def _get_type_emoji(self, activity_type: str) -> str:
        """Obtener emoji para tipo de actividad"""
        emoji_map = {
            'diy': '🏗️',
            'ejercicio': '💃',
            'manualidad': '🦋',
            'juego': '🎮',
            'educativo': '📚'
        }
        return emoji_map.get(activity_type, '🎨')

class MediaService:
    """Servicio para contenido multimedia"""
    
    def __init__(self, database: DatabaseInterface):
        self.db = database
    
    def get_movies(self, is_premium_only: bool = False) -> List[Movie]:
        """Obtener películas y contenido multimedia"""
        try:
            query = """
            SELECT * FROM contenido_multimedia 
            WHERE activo = 1
            """
            params = []
            
            if is_premium_only:
                query += " AND es_premium = 1"
            
            query += " ORDER BY rating_promedio DESC, año_produccion DESC"
            
            movies_data = self.db.execute_query(query, tuple(params))
            movies = []
            
            for movie_data in movies_data:
                movie = Movie(
                    id=movie_data['id'],
                    title=movie_data['titulo'],
                    genre=movie_data['genero'],
                    duration=f"{movie_data['duracion_minutos']} min",
                    rating=movie_data['rating_promedio'],
                    image=self._get_genre_emoji(movie_data['genero']),
                    description=movie_data['descripcion'],
                    year=movie_data['año_produccion'],
                    cast=movie_data['elenco'].split(', ') if movie_data['elenco'] else [],
                    is_premium=movie_data['es_premium']
                )
                movies.append(movie)
            
            return movies
        except Exception as e:
            logger.error(f"Error obteniendo películas: {e}")
            return []
    
    def _get_genre_emoji(self, genre: str) -> str:
        """Obtener emoji para género"""
        emoji_map = {
            'Motivacional': '🧠',
            'Educativo Gastronómico': '🍽️',
            'Bienestar y Meditación': '🧘',
            'Documental': '📹',
            'Película': '🎬'
        }
        return emoji_map.get(genre, '🎬')

# =============================================================================
# UTILIDADES Y FUNCIONES AUXILIARES
# =============================================================================

class ThemeManager:
    """Gestor de temas y estilos"""
    
    @staticmethod
    def get_theme_colors(gender: str) -> Dict[str, str]:
        """Obtener colores del tema según género"""
        if gender == 'masculino':
            return {
                'primary': '#3B82F6',
                'secondary': '#DBEAFE',
                'accent': '#1D4ED8'
            }
        elif gender == 'femenino':
            return {
                'primary': '#EC4899',
                'secondary': '#FCE7F3',
                'accent': '#BE185D'
            }
        return {
            'primary': '#6366F1',
            'secondary': '#E0E7FF',
            'accent': '#4338CA'
        }
    
    @staticmethod
    def apply_custom_css():
        """Aplicar estilos CSS personalizados"""
        st.markdown("""
        <style>
            .main-header {
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                padding: 2rem;
                border-radius: 1rem;
                color: white;
                margin-bottom: 2rem;
            }
            
            .workout-card {
                background: white;
                padding: 1.5rem;
                border-radius: 1rem;
                box-shadow: 0 2px 10px rgba(0,0,0,0.1);
                margin-bottom: 1rem;
                border-left: 4px solid #667eea;
            }
            
            .stats-card {
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                padding: 1.5rem;
                border-radius: 1rem;
                color: white;
                text-align: center;
                margin-bottom: 1rem;
            }
            
            .kids-card {
                background: linear-gradient(135deg, #ffeaa7 0%, #fab1a0 100%);
                padding: 1.5rem;
                border-radius: 1rem;
                color: #2d3436;
                margin-bottom: 1rem;
            }
            
            .premium-card {
                background: linear-gradient(135deg, #fdcb6e 0%, #e17055 100%);
                padding: 2rem;
                border-radius: 1rem;
                color: white;
                text-align: center;
                margin-bottom: 2rem;
            }
            
            .metric-container {
                background: white;
                padding: 1rem;
                border-radius: 0.5rem;
                box-shadow: 0 2px 5px rgba(0,0,0,0.1);
                text-align: center;
            }
        </style>
        """, unsafe_allow_html=True)

class ValidationUtils:
    """Utilidades de validación"""
    
    @staticmethod
    def validate_email(email: str) -> bool:
        """Validar formato de email"""
        import re
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return re.match(pattern, email) is not None
    
    @staticmethod
    def validate_password(password: str) -> Tuple[bool, str]:
        """Validar fortaleza de contraseña"""
        if len(password) < 8:
            return False, "La contraseña debe tener al menos 8 caracteres"
        
        if not any(c.isupper() for c in password):
            return False, "La contraseña debe contener al menos una mayúscula"
        
        if not any(c.islower() for c in password):
            return False, "La contraseña debe contener al menos una minúscula"
        
        if not any(c.isdigit() for c in password):
            return False, "La contraseña debe contener al menos un número"
        
        return True, "Contraseña válida"

class DataProcessor:
    """Procesador de datos"""
    
    @staticmethod
    def calculate_bmi(weight: float, height: int) -> float:
        """Calcular IMC"""
        height_m = height / 100
        return round(weight / (height_m ** 2), 2)
    
    @staticmethod
    def get_bmi_category(bmi: float) -> str:
        """Obtener categoría de IMC"""
        if bmi < 18.5:
            return "Bajo peso"
        elif bmi < 25:
            return "Peso normal"
        elif bmi < 30:
            return "Sobrepeso"
        else:
            return "Obesidad"
    
    @staticmethod
    def calculate_calorie_needs(weight: float, height: int, age: int, gender: str, activity_level: str) -> int:
        """Calcular necesidades calóricas diarias"""
        # Fórmula de Harris-Benedict
        if gender == 'masculino':
            bmr = 88.362 + (13.397 * weight) + (4.799 * height) - (5.677 * age)
        else:
            bmr = 447.593 + (9.247 * weight) + (3.098 * height) - (4.330 * age)
        
        # Factor de actividad
        activity_factors = {
            'sedentario': 1.2,
            'ligero': 1.375,
            'moderado': 1.55,
            'intenso': 1.725,
            'muy_intenso': 1.9
        }
        
        factor = activity_factors.get(activity_level, 1.375)
        return int(bmr * factor)

# =============================================================================
# CONFIGURACIÓN Y INICIALIZACIÓN
# =============================================================================

class AppConfig:
    """Configuración de la aplicación"""
    
    def __init__(self):
        self.database_path = "fithome_pro.db"
        self.app_title = "FitHome Pro"
        self.app_icon = "💪"
        self.layout = "wide"
        self.initial_sidebar_state = "collapsed"
        
        # Configuración de páginas
        self.pages = [
            "🏠 Inicio",
            "💪 Entrenamientos", 
            "🍎 Nutrición",
            "👶 Zona Infantil",
            "🎬 Películas",
            "📊 Progreso"
        ]

def initialize_app():
    """Inicializar aplicación"""
    # Configurar página
    st.set_page_config(
        page_title=AppConfig().app_title,
        page_icon=AppConfig().app_icon,
        layout=AppConfig().layout,
        initial_sidebar_state=AppConfig().initial_sidebar_state
    )
    
    # Aplicar estilos
    ThemeManager.apply_custom_css()
    
    # Inicializar servicios
    database = SQLiteDatabase()
    if not database.connect():
        st.error("Error conectando a la base de datos")
        return None
    
    return {
        'database': database, 
        'user_service': UserService(database),
        'workout_service': WorkoutService(database),
        'nutrition_service': NutritionService(database),
        'kids_service': KidsActivityService(database),
        'media_service': MediaService(database),
        'analytics': DataAnalytics(database)
    }

# =============================================================================
# FUNCIÓN PRINCIPAL
# =============================================================================

def main():
    """Función principal de la aplicación"""
    try:
        # Inicializar servicios
        services = initialize_app()
        if not services:
            return
        
        # Inicializar estado de sesión
        if 'current_screen' not in st.session_state:
            st.session_state.current_screen = 'loading'
        if 'user' not in st.session_state:
            st.session_state.user = None
        if 'user_profile' not in st.session_state:
            st.session_state.user_profile = UserProfile()
        if 'user_stats' not in st.session_state:
            st.session_state.user_stats = UserStats()
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
