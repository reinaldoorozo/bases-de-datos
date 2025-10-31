"""
FitHome Pro - Módulo de Análisis de Datos
Análisis estadístico y visualización de datos de fitness

Autor: Equipo FitHome Pro
Fecha: 2024
"""

import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import seaborn as sns
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import numpy as np
from datetime import datetime, timedelta, date
from typing import List, Dict, Tuple, Optional
import sqlite3
import logging
from dataclasses import dataclass
import warnings
warnings.filterwarnings('ignore')

# Configurar estilo de matplotlib
try:
    plt.style.use('seaborn-v0_8')
except (OSError, ValueError):
    try:
        plt.style.use('seaborn')
    except (OSError, ValueError):
        plt.style.use('default')
sns.set_palette("husl")

logger = logging.getLogger(__name__)

# =============================================================================
# CLASES DE DATOS PARA ANÁLISIS
# =============================================================================

@dataclass
class FitnessMetrics:
    """Métricas de fitness calculadas"""
    total_workouts: int
    total_calories_burned: int
    total_minutes: int
    average_workout_duration: float
    calories_per_minute: float
    workout_frequency: float
    streak_days: int
    weight_loss: float
    bmi_change: float

@dataclass
class WeeklyProgress:
    """Progreso semanal"""
    week_start: date
    week_end: date
    workouts_completed: int
    calories_burned: int
    minutes_trained: int
    average_rating: float

@dataclass
class MonthlyReport:
    """Reporte mensual"""
    month: str
    year: int
    total_workouts: int
    total_calories: int
    total_minutes: int
    weight_change: float
    achievements_unlocked: int
    favorite_category: str
    improvement_areas: List[str]

# =============================================================================
# CLASE PRINCIPAL DE ANÁLISIS
# =============================================================================

class FitnessDataAnalyzer:
    """Analizador principal de datos de fitness"""
    
    def __init__(self, database_path: str = "fithome_pro.db"):
        self.db_path = database_path
        self.connection = None
        self._connect()
    
    def _connect(self):
        """Conectar a la base de datos"""
        try:
            self.connection = sqlite3.connect(self.db_path, check_same_thread=False)
            self.connection.row_factory = sqlite3.Row
            # Habilitar WAL mode para mejor concurrencia
            self.connection.execute("PRAGMA journal_mode=WAL")
        except Exception as e:
            logger.error(f"Error conectando a la base de datos: {e}")
    
    def get_user_data(self, user_id: int) -> pd.DataFrame:
        """Obtener datos completos del usuario"""
        try:
            query = """
            SELECT 
                se.fecha_inicio,
                se.fecha_fin,
                se.duracion_real_minutos,
                se.calorias_quemadas,
                se.rating_usuario,
                se.completado,
                e.nombre as workout_name,
                e.categoria,
                e.nivel,
                e.calorias_estimadas
            FROM sesiones_entrenamiento se
            JOIN entrenamientos e ON se.entrenamiento_id = e.id
            WHERE se.usuario_id = ? AND se.completado = 1
            ORDER BY se.fecha_inicio
            """
            
            df = pd.read_sql_query(query, self.connection, params=(user_id,))
            
            if not df.empty:
                df['fecha_inicio'] = pd.to_datetime(df['fecha_inicio'])
                df['fecha_fin'] = pd.to_datetime(df['fecha_fin'])
                df['date'] = df['fecha_inicio'].dt.date
                df['week'] = df['fecha_inicio'].dt.isocalendar().week
                df['month'] = df['fecha_inicio'].dt.month
                df['year'] = df['fecha_inicio'].dt.year
            
            return df
        except Exception as e:
            logger.error(f"Error obteniendo datos del usuario: {e}")
            return pd.DataFrame()
    
    def get_weight_progress(self, user_id: int) -> pd.DataFrame:
        """Obtener progreso de peso del usuario"""
        try:
            query = """
            SELECT fecha_registro, peso
            FROM progreso_peso
            WHERE usuario_id = ?
            ORDER BY fecha_registro
            """
            
            df = pd.read_sql_query(query, self.connection, params=(user_id,))
            
            if not df.empty:
                df['fecha_registro'] = pd.to_datetime(df['fecha_registro'])
                df['date'] = df['fecha_registro'].dt.date
                df['weight_change'] = df['peso'].diff()
                df['weight_change_pct'] = (df['peso'].pct_change() * 100).round(2)
            
            return df
        except Exception as e:
            logger.error(f"Error obteniendo progreso de peso: {e}")
            return pd.DataFrame()
    
    def calculate_fitness_metrics(self, user_id: int) -> FitnessMetrics:
        """Calcular métricas principales de fitness"""
        try:
            df = self.get_user_data(user_id)
            
            if df.empty:
                return FitnessMetrics(0, 0, 0, 0, 0, 0, 0, 0, 0)
            
            total_workouts = len(df)
            total_calories = df['calorias_quemadas'].sum()
            total_minutes = df['duracion_real_minutos'].sum()
            avg_duration = df['duracion_real_minutos'].mean()
            calories_per_minute = total_calories / total_minutes if total_minutes > 0 else 0
            
            # Calcular frecuencia de entrenamientos
            if len(df) > 1:
                date_range = (df['date'].max() - df['date'].min()).days
                workout_frequency = total_workouts / max(date_range, 1) * 7  # entrenamientos por semana
            else:
                workout_frequency = 0
            
            # Calcular racha actual
            streak_days = self._calculate_streak(df)
            
            # Calcular pérdida de peso
            weight_df = self.get_weight_progress(user_id)
            weight_loss = 0
            if not weight_df.empty and len(weight_df) > 1:
                weight_loss = weight_df['peso'].iloc[0] - weight_df['peso'].iloc[-1]
            
            return FitnessMetrics(
                total_workouts=total_workouts,
                total_calories_burned=int(total_calories),
                total_minutes=int(total_minutes),
                average_workout_duration=round(avg_duration, 1),
                calories_per_minute=round(calories_per_minute, 2),
                workout_frequency=round(workout_frequency, 1),
                streak_days=streak_days,
                weight_loss=round(weight_loss, 2),
                bmi_change=0  # Se calculará por separado si se necesita
            )
        except Exception as e:
            logger.error(f"Error calculando métricas de fitness: {e}")
            return FitnessMetrics(0, 0, 0, 0, 0, 0, 0, 0, 0)
    
    def _calculate_streak(self, df: pd.DataFrame) -> int:
        """Calcular racha de entrenamientos"""
        if df.empty:
            return 0
        
        # Ordenar por fecha
        df_sorted = df.sort_values('date')
        dates = df_sorted['date'].unique()
        
        if len(dates) == 0:
            return 0
        
        # Calcular racha hacia atrás desde hoy
        today = date.today()
        streak = 0
        
        for i in range(len(dates)):
            check_date = today - timedelta(days=i)
            if check_date in dates:
                streak += 1
            else:
                break
        
        return streak
    
    def generate_weekly_progress(self, user_id: int, weeks: int = 8) -> List[WeeklyProgress]:
        """Generar progreso semanal"""
        try:
            df = self.get_user_data(user_id)
            
            if df.empty:
                return []
            
            weekly_data = []
            
            for i in range(weeks):
                week_start = today - timedelta(weeks=i+1)
                week_end = today - timedelta(weeks=i)
                
                week_df = df[(df['date'] >= week_start) & (df['date'] < week_end)]
                
                if not week_df.empty:
                    progress = WeeklyProgress(
                        week_start=week_start,
                        week_end=week_end,
                        workouts_completed=len(week_df),
                        calories_burned=int(week_df['calorias_quemadas'].sum()),
                        minutes_trained=int(week_df['duracion_real_minutos'].sum()),
                        average_rating=round(week_df['rating_usuario'].mean(), 1)
                    )
                    weekly_data.append(progress)
            
            return weekly_data
        except Exception as e:
            logger.error(f"Error generando progreso semanal: {e}")
            return []
    
    def generate_monthly_report(self, user_id: int, months: int = 6) -> List[MonthlyReport]:
        """Generar reporte mensual"""
        try:
            df = self.get_user_data(user_id)
            
            if df.empty:
                return []
            
            monthly_reports = []
            
            for i in range(months):
                month_date = today - timedelta(days=30*i)
                month_start = month_date.replace(day=1)
                
                if i == 0:
                    month_end = today
                else:
                    next_month = month_start + timedelta(days=32)
                    month_end = next_month.replace(day=1) - timedelta(days=1)
                
                month_df = df[(df['date'] >= month_start) & (df['date'] <= month_end)]
                
                if not month_df.empty:
                    # Calcular categoría favorita
                    favorite_category = month_df['categoria'].mode().iloc[0] if not month_df['categoria'].mode().empty else "N/A"
                    
                    # Calcular áreas de mejora
                    improvement_areas = self._identify_improvement_areas(month_df)
                    
                    report = MonthlyReport(
                        month=month_start.strftime('%B'),
                        year=month_start.year,
                        total_workouts=len(month_df),
                        total_calories=int(month_df['calorias_quemadas'].sum()),
                        total_minutes=int(month_df['duracion_real_minutos'].sum()),
                        weight_change=0,  # Se calculará por separado
                        achievements_unlocked=0,  # Se calculará por separado
                        favorite_category=favorite_category,
                        improvement_areas=improvement_areas
                    )
                    monthly_reports.append(report)
            
            return monthly_reports
        except Exception as e:
            logger.error(f"Error generando reporte mensual: {e}")
            return []
    
    def _identify_improvement_areas(self, df: pd.DataFrame) -> List[str]:
        """Identificar áreas de mejora"""
        improvements = []
        
        if df.empty:
            return improvements
        
        # Análisis de duración promedio
        avg_duration = df['duracion_real_minutos'].mean()
        if avg_duration < 20:
            improvements.append("Aumentar duración de entrenamientos")
        
        # Análisis de frecuencia
        if len(df) < 3:
            improvements.append("Aumentar frecuencia de entrenamientos")
        
        # Análisis de variedad
        unique_categories = df['categoria'].nunique()
        if unique_categories < 2:
            improvements.append("Variar tipos de entrenamiento")
        
        # Análisis de intensidad (calorías por minuto)
        calories_per_min = df['calorias_quemadas'].sum() / df['duracion_real_minutos'].sum()
        if calories_per_min < 8:
            improvements.append("Aumentar intensidad de entrenamientos")
        
        return improvements

# =============================================================================
# GENERADORES DE GRÁFICOS
# =============================================================================

class FitnessChartGenerator:
    """Generador de gráficos para análisis de fitness"""
    
    def __init__(self, analyzer: FitnessDataAnalyzer):
        self.analyzer = analyzer
    
    def create_progress_overview(self, user_id: int) -> go.Figure:
        """Crear gráfico de resumen de progreso"""
        try:
            df = self.analyzer.get_user_data(user_id)
            
            if df.empty:
                return self._create_empty_chart("No hay datos de entrenamientos")
            
            # Crear subplots
            fig = make_subplots(
                rows=2, cols=2,
                subplot_titles=('Calorías Quemadas por Día', 'Duración de Entrenamientos', 
                               'Rating Promedio', 'Categorías de Entrenamiento'),
                specs=[[{"secondary_y": False}, {"secondary_y": False}],
                       [{"secondary_y": False}, {"type": "pie"}]]
            )
            
            # Gráfico 1: Calorías por día
            daily_calories = df.groupby('date')['calorias_quemadas'].sum().reset_index()
            fig.add_trace(
                go.Scatter(x=daily_calories['date'], y=daily_calories['calorias_quemadas'],
                          mode='lines+markers', name='Calorías', line=dict(color='#FF6B6B')),
                row=1, col=1
            )
            
            # Gráfico 2: Duración de entrenamientos
            daily_duration = df.groupby('date')['duracion_real_minutos'].sum().reset_index()
            fig.add_trace(
                go.Scatter(x=daily_duration['date'], y=daily_duration['duracion_real_minutos'],
                          mode='lines+markers', name='Minutos', line=dict(color='#4ECDC4')),
                row=1, col=2
            )
            
            # Gráfico 3: Rating promedio
            daily_rating = df.groupby('date')['rating_usuario'].mean().reset_index()
            fig.add_trace(
                go.Scatter(x=daily_rating['date'], y=daily_rating['rating_usuario'],
                          mode='lines+markers', name='Rating', line=dict(color='#45B7D1')),
                row=2, col=1
            )
            
            # Gráfico 4: Distribución por categorías
            category_counts = df['categoria'].value_counts()
            fig.add_trace(
                go.Pie(labels=category_counts.index, values=category_counts.values,
                      name="Categorías"),
                row=2, col=2
            )
            
            fig.update_layout(
                title_text="Resumen de Progreso de Entrenamientos",
                showlegend=False,
                height=600
            )
            
            return fig
        except Exception as e:
            logger.error(f"Error creando gráfico de resumen: {e}")
            return self._create_empty_chart("Error generando gráfico")
    
    def create_weight_progress_chart(self, user_id: int) -> go.Figure:
        """Crear gráfico de progreso de peso"""
        try:
            weight_df = self.analyzer.get_weight_progress(user_id)
            
            if weight_df.empty:
                return self._create_empty_chart("No hay datos de peso registrados")
            
            fig = go.Figure()
            
            # Línea principal de peso
            fig.add_trace(go.Scatter(
                x=weight_df['date'],
                y=weight_df['peso'],
                mode='lines+markers',
                name='Peso',
                line=dict(color='#667eea', width=3),
                marker=dict(size=8)
            ))
            
            # Línea de tendencia
            if len(weight_df) > 2:
                z = np.polyfit(range(len(weight_df)), weight_df['peso'], 1)
                p = np.poly1d(z)
                fig.add_trace(go.Scatter(
                    x=weight_df['date'],
                    y=p(range(len(weight_df))),
                    mode='lines',
                    name='Tendencia',
                    line=dict(color='red', dash='dash')
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
            logger.error(f"Error creando gráfico de peso: {e}")
            return self._create_empty_chart("Error generando gráfico de peso")
    
    def create_weekly_comparison(self, user_id: int) -> go.Figure:
        """Crear gráfico de comparación semanal"""
        try:
            weekly_data = self.analyzer.generate_weekly_progress(user_id, 8)
            
            if not weekly_data:
                return self._create_empty_chart("No hay datos semanales disponibles")
            
            weeks = [f"Semana {i+1}" for i in range(len(weekly_data))]
            workouts = [w.workouts_completed for w in weekly_data]
            calories = [w.calories_burned for w in weekly_data]
            minutes = [w.minutes_trained for w in weekly_data]
            
            fig = make_subplots(
                rows=1, cols=3,
                subplot_titles=('Entrenamientos Completados', 'Calorías Quemadas', 'Minutos Entrenados')
            )
            
            # Entrenamientos
            fig.add_trace(
                go.Bar(x=weeks, y=workouts, name='Entrenamientos', marker_color='#FF6B6B'),
                row=1, col=1
            )
            
            # Calorías
            fig.add_trace(
                go.Bar(x=weeks, y=calories, name='Calorías', marker_color='#4ECDC4'),
                row=1, col=2
            )
            
            # Minutos
            fig.add_trace(
                go.Bar(x=weeks, y=minutes, name='Minutos', marker_color='#45B7D1'),
                row=1, col=3
            )
            
            fig.update_layout(
                title_text="Comparación Semanal de Actividad",
                showlegend=False,
                height=400
            )
            
            return fig
        except Exception as e:
            logger.error(f"Error creando gráfico semanal: {e}")
            return self._create_empty_chart("Error generando gráfico semanal")
    
    def create_category_analysis(self, user_id: int) -> go.Figure:
        """Crear análisis por categorías de entrenamiento"""
        try:
            df = self.analyzer.get_user_data(user_id)
            
            if df.empty:
                return self._create_empty_chart("No hay datos de entrenamientos")
            
            # Análisis por categoría
            category_stats = df.groupby('categoria').agg({
                'calorias_quemadas': ['sum', 'mean'],
                'duracion_real_minutos': ['sum', 'mean'],
                'rating_usuario': 'mean',
                'workout_name': 'count'
            }).round(2)
            
            category_stats.columns = ['Total_Calorias', 'Promedio_Calorias', 
                                    'Total_Minutos', 'Promedio_Minutos', 
                                    'Rating_Promedio', 'Total_Entrenamientos']
            
            # Crear gráfico de barras múltiples
            fig = make_subplots(
                rows=2, cols=2,
                subplot_titles=('Total Calorías por Categoría', 'Promedio Calorías por Entrenamiento',
                               'Total Minutos por Categoría', 'Rating Promedio por Categoría')
            )
            
            categories = category_stats.index
            
            # Total calorías
            fig.add_trace(
                go.Bar(x=categories, y=category_stats['Total_Calorias'], 
                      name='Total Calorías', marker_color='#FF6B6B'),
                row=1, col=1
            )
            
            # Promedio calorías
            fig.add_trace(
                go.Bar(x=categories, y=category_stats['Promedio_Calorias'], 
                      name='Promedio Calorías', marker_color='#4ECDC4'),
                row=1, col=2
            )
            
            # Total minutos
            fig.add_trace(
                go.Bar(x=categories, y=category_stats['Total_Minutos'], 
                      name='Total Minutos', marker_color='#45B7D1'),
                row=2, col=1
            )
            
            # Rating promedio
            fig.add_trace(
                go.Bar(x=categories, y=category_stats['Rating_Promedio'], 
                      name='Rating Promedio', marker_color='#96CEB4'),
                row=2, col=2
            )
            
            fig.update_layout(
                title_text="Análisis por Categorías de Entrenamiento",
                showlegend=False,
                height=600
            )
            
            return fig
        except Exception as e:
            logger.error(f"Error creando análisis de categorías: {e}")
            return self._create_empty_chart("Error generando análisis de categorías")
    
    def create_heatmap_calendar(self, user_id: int) -> go.Figure:
        """Crear mapa de calor del calendario de entrenamientos"""
        try:
            df = self.analyzer.get_user_data(user_id)
            
            if df.empty:
                return self._create_empty_chart("No hay datos de entrenamientos")
            
            # Preparar datos para el calendario
            df['year'] = df['fecha_inicio'].dt.year
            df['month'] = df['fecha_inicio'].dt.month
            df['day'] = df['fecha_inicio'].dt.day
            
            # Crear matriz de calor
            calendar_data = df.groupby(['year', 'month', 'day'])['calorias_quemadas'].sum().reset_index()
            
            # Crear gráfico de calor
            fig = go.Figure(data=go.Heatmap(
                z=calendar_data['calorias_quemadas'],
                x=calendar_data['day'],
                y=calendar_data['month'],
                colorscale='Viridis',
                showscale=True
            ))
            
            fig.update_layout(
                title='Mapa de Calor - Calorías Quemadas por Día',
                xaxis_title='Día del Mes',
                yaxis_title='Mes',
                height=400
            )
            
            return fig
        except Exception as e:
            logger.error(f"Error creando mapa de calor: {e}")
            return self._create_empty_chart("Error generando mapa de calor")
    
    def _create_empty_chart(self, message: str) -> go.Figure:
        """Crear gráfico vacío con mensaje"""
        fig = go.Figure()
        fig.add_annotation(
            text=message,
            xref="paper", yref="paper",
            x=0.5, y=0.5, showarrow=False,
            font=dict(size=16, color="gray")
        )
        fig.update_layout(
            template='plotly_white',
            height=400
        )
        return fig

# =============================================================================
# GENERADOR DE REPORTES
# =============================================================================

class ReportGenerator:
    """Generador de reportes detallados"""
    
    def __init__(self, analyzer: FitnessDataAnalyzer):
        self.analyzer = analyzer
    
    def generate_comprehensive_report(self, user_id: int) -> Dict:
        """Generar reporte comprensivo del usuario"""
        try:
            # Obtener métricas principales
            metrics = self.analyzer.calculate_fitness_metrics(user_id)
            
            # Obtener datos detallados
            df = self.analyzer.get_user_data(user_id)
            weight_df = self.analyzer.get_weight_progress(user_id)
            
            # Generar análisis semanal y mensual
            weekly_progress = self.analyzer.generate_weekly_progress(user_id)
            monthly_reports = self.analyzer.generate_monthly_report(user_id)
            
            # Calcular estadísticas adicionales
            if not df.empty:
                # Análisis de tendencias
                trend_analysis = self._analyze_trends(df)
                
                # Análisis de patrones
                pattern_analysis = self._analyze_patterns(df)
                
                # Recomendaciones
                recommendations = self._generate_recommendations(metrics, df, weight_df)
            else:
                trend_analysis = {}
                pattern_analysis = {}
                recommendations = ["Comienza registrando tus primeros entrenamientos"]
            
            report = {
                'user_id': user_id,
                'generated_date': datetime.now().isoformat(),
                'metrics': metrics,
                'weekly_progress': weekly_progress,
                'monthly_reports': monthly_reports,
                'trend_analysis': trend_analysis,
                'pattern_analysis': pattern_analysis,
                'recommendations': recommendations,
                'summary': self._generate_summary(metrics, df, weight_df)
            }
            
            return report
        except Exception as e:
            logger.error(f"Error generando reporte comprensivo: {e}")
            return {}
    
    def _analyze_trends(self, df: pd.DataFrame) -> Dict:
        """Analizar tendencias en los datos"""
        trends = {}
        
        if df.empty:
            return trends
        
        # Tendencia de calorías
        if len(df) > 1:
            calories_trend = np.polyfit(range(len(df)), df['calorias_quemadas'], 1)[0]
            trends['calories_trend'] = 'increasing' if calories_trend > 0 else 'decreasing'
        
        # Tendencia de duración
        if len(df) > 1:
            duration_trend = np.polyfit(range(len(df)), df['duracion_real_minutos'], 1)[0]
            trends['duration_trend'] = 'increasing' if duration_trend > 0 else 'decreasing'
        
        # Tendencia de rating
        if len(df) > 1:
            rating_trend = np.polyfit(range(len(df)), df['rating_usuario'], 1)[0]
            trends['rating_trend'] = 'improving' if rating_trend > 0 else 'declining'
        
        return trends
    
    def _analyze_patterns(self, df: pd.DataFrame) -> Dict:
        """Analizar patrones en los datos"""
        patterns = {}
        
        if df.empty:
            return patterns
        
        # Día de la semana más activo
        df['day_of_week'] = df['fecha_inicio'].dt.day_name()
        most_active_day = df.groupby('day_of_week')['calorias_quemadas'].sum().idxmax()
        patterns['most_active_day'] = most_active_day
        
        # Hora del día más activa
        df['hour'] = df['fecha_inicio'].dt.hour
        most_active_hour = df.groupby('hour')['calorias_quemadas'].sum().idxmax()
        patterns['most_active_hour'] = most_active_hour
        
        # Categoría más frecuente
        most_frequent_category = df['categoria'].mode().iloc[0]
        patterns['most_frequent_category'] = most_frequent_category
        
        # Nivel de entrenamiento más común
        most_common_level = df['nivel'].mode().iloc[0]
        patterns['most_common_level'] = most_common_level
        
        return patterns
    
    def _generate_recommendations(self, metrics: FitnessMetrics, 
                                 df: pd.DataFrame, weight_df: pd.DataFrame) -> List[str]:
        """Generar recomendaciones personalizadas"""
        recommendations = []
        
        # Recomendaciones basadas en frecuencia
        if metrics.workout_frequency < 3:
            recommendations.append("💡 Intenta entrenar al menos 3 veces por semana para mejores resultados")
        
        # Recomendaciones basadas en duración
        if metrics.average_workout_duration < 20:
            recommendations.append("⏱️ Considera aumentar la duración de tus entrenamientos a 20-30 minutos")
        
        # Recomendaciones basadas en intensidad
        if metrics.calories_per_minute < 8:
            recommendations.append("🔥 Aumenta la intensidad de tus entrenamientos para quemar más calorías")
        
        # Recomendaciones basadas en variedad
        if not df.empty:
            unique_categories = df['categoria'].nunique()
            if unique_categories < 3:
                recommendations.append("🎯 Varía tus entrenamientos incluyendo diferentes categorías")
        
        # Recomendaciones basadas en progreso de peso
        if not weight_df.empty and len(weight_df) > 1:
            weight_change = weight_df['peso'].iloc[-1] - weight_df['peso'].iloc[0]
            if abs(weight_change) < 0.5:
                recommendations.append("⚖️ Considera ajustar tu plan nutricional para acelerar el progreso")
        
        # Recomendaciones generales
        recommendations.extend([
            "💧 Mantén una hidratación adecuada durante todo el día",
            "😴 Asegúrate de dormir 7-9 horas para una recuperación óptima",
            "📊 Registra tus entrenamientos regularmente para seguir tu progreso"
        ])
        
        return recommendations
    
    def _generate_summary(self, metrics: FitnessMetrics, 
                         df: pd.DataFrame, weight_df: pd.DataFrame) -> str:
        """Generar resumen ejecutivo"""
        summary_parts = []
        
        # Resumen de actividad
        if metrics.total_workouts > 0:
            summary_parts.append(f"Has completado {metrics.total_workouts} entrenamientos")
            summary_parts.append(f"quemando un total de {metrics.total_calories_burned:,} calorías")
            summary_parts.append(f"en {metrics.total_minutes:,} minutos de actividad.")
        
        # Resumen de progreso de peso
        if not weight_df.empty and len(weight_df) > 1:
            weight_change = weight_df['peso'].iloc[-1] - weight_df['peso'].iloc[0]
            if weight_change > 0:
                summary_parts.append(f"Tu peso ha aumentado {abs(weight_change):.1f} kg.")
            elif weight_change < 0:
                summary_parts.append(f"¡Excelente! Has perdido {abs(weight_change):.1f} kg.")
            else:
                summary_parts.append("Tu peso se ha mantenido estable.")
        
        # Resumen de racha
        if metrics.streak_days > 0:
            summary_parts.append(f"Tienes una racha de {metrics.streak_days} días consecutivos.")
        
        return " ".join(summary_parts) if summary_parts else "Comienza tu viaje fitness registrando tu primer entrenamiento."

# =============================================================================
# FUNCIONES DE UTILIDAD
# =============================================================================

def create_sample_data():
    """Crear datos de muestra para testing"""
    try:
        # Conectar a la base de datos
        conn = sqlite3.connect("fithome_pro.db")
        
        # Crear datos de muestra
        sample_workouts = [
            ('2024-01-01 08:00:00', '2024-01-01 08:25:00', 25, 200, 4, 1, 1),
            ('2024-01-02 18:00:00', '2024-01-02 18:35:00', 35, 280, 5, 1, 2),
            ('2024-01-03 07:30:00', '2024-01-03 07:55:00', 25, 120, 4, 1, 3),
            ('2024-01-05 19:00:00', '2024-01-05 19:15:00', 15, 140, 4, 1, 4),
            ('2024-01-07 09:00:00', '2024-01-07 09:25:00', 25, 200, 5, 1, 1),
        ]
        
        for workout in sample_workouts:
            conn.execute("""
                INSERT INTO sesiones_entrenamiento 
                (fecha_inicio, fecha_fin, duracion_real_minutos, calorias_quemadas, 
                 rating_usuario, completado, usuario_id, entrenamiento_id)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """, workout)
        
        # Crear datos de peso de muestra
        sample_weights = [
            ('2024-01-01', 75.5),
            ('2024-01-08', 75.2),
            ('2024-01-15', 74.8),
            ('2024-01-22', 74.5),
        ]
        
        for weight_data in sample_weights:
            conn.execute("""
                INSERT INTO progreso_peso (usuario_id, fecha_registro, peso)
                VALUES (?, ?, ?)
            """, (1, weight_data[0], weight_data[1]))
        
        conn.commit()
        conn.close()
        
        print("Datos de muestra creados exitosamente")
        
    except Exception as e:
        print(f"Error creando datos de muestra: {e}")

# =============================================================================
# FUNCIÓN PRINCIPAL DE TESTING
# =============================================================================

def test_analysis():
    """Función para probar el análisis de datos"""
    try:
        # Crear datos de muestra
        create_sample_data()
        
        # Inicializar analizador
        analyzer = FitnessDataAnalyzer()
        chart_generator = FitnessChartGenerator(analyzer)
        report_generator = ReportGenerator(analyzer)
        
        # Probar análisis
        user_id = 1
        metrics = analyzer.calculate_fitness_metrics(user_id)
        print(f"Métricas calculadas: {metrics}")
        
        # Generar gráficos
        progress_chart = chart_generator.create_progress_overview(user_id)
        weight_chart = chart_generator.create_weight_progress_chart(user_id)
        
        print("Gráficos generados exitosamente")
        
        # Generar reporte
        report = report_generator.generate_comprehensive_report(user_id)
        print(f"Reporte generado: {len(report)} secciones")
        
    except Exception as e:
        print(f"Error en testing: {e}")

if __name__ == "__main__":
    test_analysis()
