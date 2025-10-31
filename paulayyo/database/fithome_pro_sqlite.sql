-- Base de Datos FitHome Pro - SQLite
-- Sistema de Gestión de Fitness y Bienestar

-- Tabla de usuarios
CREATE TABLE usuarios (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nombre VARCHAR(100) NOT NULL,
    email VARCHAR(150) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    edad INTEGER,
    genero TEXT CHECK(genero IN ('masculino', 'femenino', 'otro')),
    peso_actual DECIMAL(5,2),
    altura INTEGER,
    peso_objetivo DECIMAL(5,2),
    nivel_fitness TEXT CHECK(nivel_fitness IN ('principiante', 'intermedio', 'avanzado')),
    fecha_registro TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    es_premium BOOLEAN DEFAULT FALSE,
    activo BOOLEAN DEFAULT TRUE
);

-- Tabla de objetivos de usuario
CREATE TABLE objetivos_usuario (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    usuario_id INTEGER,
    objetivo TEXT CHECK(objetivo IN ('perder_peso', 'ganar_musculo', 'mantenerse', 'mejorar_resistencia', 'rehabilitacion', 'competir')),
    fecha_establecido TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (usuario_id) REFERENCES usuarios(id) ON DELETE CASCADE
);

-- Tabla de entrenamientos
CREATE TABLE entrenamientos (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nombre VARCHAR(150) NOT NULL,
    descripcion TEXT,
    duracion_minutos INTEGER NOT NULL,
    nivel TEXT CHECK(nivel IN ('principiante', 'intermedio', 'avanzado')),
    categoria TEXT CHECK(categoria IN ('cardio', 'fuerza', 'flexibilidad', 'core', 'yoga', 'pilates')),
    calorias_estimadas INTEGER,
    imagen_url VARCHAR(255),
    rating_promedio DECIMAL(3,2) DEFAULT 0.0,
    total_completados INTEGER DEFAULT 0,
    creado_por INTEGER,
    fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    activo BOOLEAN DEFAULT TRUE,
    FOREIGN KEY (creado_por) REFERENCES usuarios(id)
);

-- Tabla de ejercicios
CREATE TABLE ejercicios (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    entrenamiento_id INTEGER,
    nombre VARCHAR(150) NOT NULL,
    descripcion TEXT,
    duracion_segundos INTEGER,
    series INTEGER,
    repeticiones INTEGER,
    peso_sugerido DECIMAL(5,2),
    descanso_segundos INTEGER,
    orden_ejercicio INTEGER,
    instrucciones TEXT,
    FOREIGN KEY (entrenamiento_id) REFERENCES entrenamientos(id) ON DELETE CASCADE
);

-- Tabla de sesiones de entrenamiento
CREATE TABLE sesiones_entrenamiento (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    usuario_id INTEGER,
    entrenamiento_id INTEGER,
    fecha_inicio TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    fecha_fin TIMESTAMP NULL,
    duracion_real_minutos INTEGER,
    calorias_quemadas INTEGER,
    completado BOOLEAN DEFAULT FALSE,
    rating_usuario INTEGER CHECK (rating_usuario >= 1 AND rating_usuario <= 5),
    comentarios TEXT,
    FOREIGN KEY (usuario_id) REFERENCES usuarios(id),
    FOREIGN KEY (entrenamiento_id) REFERENCES entrenamientos(id)
);

-- Tabla de progreso de peso
CREATE TABLE progreso_peso (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    usuario_id INTEGER,
    peso DECIMAL(5,2) NOT NULL,
    fecha_registro TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    notas TEXT,
    FOREIGN KEY (usuario_id) REFERENCES usuarios(id)
);

-- Tabla de hidratación diaria
CREATE TABLE hidratacion_diaria (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    usuario_id INTEGER,
    fecha DATE NOT NULL,
    vasos_consumidos INTEGER DEFAULT 0,
    meta_vasos INTEGER DEFAULT 8,
    FOREIGN KEY (usuario_id) REFERENCES usuarios(id),
    UNIQUE(usuario_id, fecha)
);

-- Tabla de actividades infantiles
CREATE TABLE actividades_infantiles (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nombre VARCHAR(150) NOT NULL,
    tipo TEXT CHECK(tipo IN ('diy', 'ejercicio', 'manualidad', 'juego', 'educativo')),
    duracion_minutos INTEGER,
    edad_minima INTEGER,
    edad_maxima INTEGER,
    dificultad TEXT CHECK(dificultad IN ('facil', 'intermedio', 'dificil')),
    materiales TEXT,
    instrucciones TEXT,
    beneficios TEXT,
    imagen_url VARCHAR(255),
    creado_por INTEGER,
    fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    activo BOOLEAN DEFAULT TRUE,
    FOREIGN KEY (creado_por) REFERENCES usuarios(id)
);

-- Tabla de películas/contenido multimedia
CREATE TABLE contenido_multimedia (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    titulo VARCHAR(200) NOT NULL,
    tipo TEXT CHECK(tipo IN ('pelicula', 'documental', 'serie', 'video_corto')),
    genero VARCHAR(100),
    duracion_minutos INTEGER,
    año_produccion INTEGER,
    rating_promedio DECIMAL(3,2) DEFAULT 0.0,
    descripcion TEXT,
    elenco TEXT,
    director VARCHAR(150),
    imagen_url VARCHAR(255),
    url_video VARCHAR(500),
    es_premium BOOLEAN DEFAULT FALSE,
    fecha_agregado TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    activo BOOLEAN DEFAULT TRUE
);

-- Tabla de estadísticas de usuario
CREATE TABLE estadisticas_usuario (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    usuario_id INTEGER,
    fecha DATE NOT NULL,
    entrenamientos_completados INTEGER DEFAULT 0,
    minutos_entrenamiento INTEGER DEFAULT 0,
    calorias_quemadas INTEGER DEFAULT 0,
    vasos_agua INTEGER DEFAULT 0,
    peso_registrado DECIMAL(5,2),
    FOREIGN KEY (usuario_id) REFERENCES usuarios(id),
    UNIQUE(usuario_id, fecha)
);

-- Tabla de logros
CREATE TABLE logros (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nombre VARCHAR(100) NOT NULL,
    descripcion TEXT,
    icono VARCHAR(10),
    criterio_tipo TEXT CHECK(criterio_tipo IN ('entrenamientos', 'calorias', 'racha', 'peso', 'tiempo')),
    criterio_valor INTEGER,
    puntos INTEGER DEFAULT 0
);

-- Tabla de logros de usuario
CREATE TABLE logros_usuario (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    usuario_id INTEGER,
    logro_id INTEGER,
    fecha_obtenido TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (usuario_id) REFERENCES usuarios(id),
    FOREIGN KEY (logro_id) REFERENCES logros(id),
    UNIQUE(usuario_id, logro_id)
);

-- Tabla de planes nutricionales
CREATE TABLE planes_nutricionales (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nombre VARCHAR(150) NOT NULL,
    descripcion TEXT,
    calorias_diarias INTEGER,
    carbohidratos_porcentaje INTEGER,
    proteinas_porcentaje INTEGER,
    grasas_porcentaje INTEGER,
    nivel_fitness TEXT CHECK(nivel_fitness IN ('principiante', 'intermedio', 'avanzado')),
    objetivo TEXT CHECK(objetivo IN ('perder_peso', 'ganar_musculo', 'mantenerse')),
    activo BOOLEAN DEFAULT TRUE
);

-- Tabla de comidas
CREATE TABLE comidas (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    plan_nutricional_id INTEGER,
    nombre VARCHAR(100) NOT NULL,
    tipo TEXT CHECK(tipo IN ('desayuno', 'almuerzo', 'cena', 'snack')),
    calorias INTEGER,
    carbohidratos_g DECIMAL(5,2),
    proteinas_g DECIMAL(5,2),
    grasas_g DECIMAL(5,2),
    ingredientes TEXT,
    instrucciones TEXT,
    tiempo_preparacion_minutos INTEGER,
    FOREIGN KEY (plan_nutricional_id) REFERENCES planes_nutricionales(id) ON DELETE CASCADE
);

-- Tabla de seguimiento nutricional
CREATE TABLE seguimiento_nutricional (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    usuario_id INTEGER,
    fecha DATE NOT NULL,
    calorias_consumidas INTEGER DEFAULT 0,
    carbohidratos_g DECIMAL(5,2) DEFAULT 0,
    proteinas_g DECIMAL(5,2) DEFAULT 0,
    grasas_g DECIMAL(5,2) DEFAULT 0,
    FOREIGN KEY (usuario_id) REFERENCES usuarios(id),
    UNIQUE(usuario_id, fecha)
);

-- Tabla de configuraciones de usuario
CREATE TABLE configuraciones_usuario (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    usuario_id INTEGER,
    tema_preferido TEXT CHECK(tema_preferido IN ('claro', 'oscuro', 'auto')),
    idioma VARCHAR(5) DEFAULT 'es',
    notificaciones_entrenamiento BOOLEAN DEFAULT TRUE,
    notificaciones_hidratacion BOOLEAN DEFAULT TRUE,
    notificaciones_nutricion BOOLEAN DEFAULT TRUE,
    meta_calorias_diarias INTEGER DEFAULT 2000,
    meta_minutos_entrenamiento INTEGER DEFAULT 30,
    FOREIGN KEY (usuario_id) REFERENCES usuarios(id)
);

-- Insertar datos iniciales

-- Logros predefinidos
INSERT INTO logros (nombre, descripcion, icono, criterio_tipo, criterio_valor, puntos) VALUES
('Primer Paso', 'Completa tu primer entrenamiento', '🎉', 'entrenamientos', 1, 10),
('Consistencia', 'Completa 10 entrenamientos', '💪', 'entrenamientos', 10, 50),
('Maratonista', 'Completa 50 entrenamientos', '🏃‍♂️', 'entrenamientos', 50, 100),
('Quemador', 'Quema 1000 calorías', '🔥', 'calorias', 1000, 75),
('Racha de Fuego', '7 días consecutivos entrenando', '🔥', 'racha', 7, 100),
('Transformación', 'Pierde 5kg', '⚖️', 'peso', 5, 200);

-- Planes nutricionales básicos
INSERT INTO planes_nutricionales (nombre, descripcion, calorias_diarias, carbohidratos_porcentaje, proteinas_porcentaje, grasas_porcentaje, nivel_fitness, objetivo) VALUES
('Plan Pérdida de Peso', 'Plan equilibrado para perder peso de forma saludable', 1500, 40, 30, 30, 'intermedio', 'perder_peso'),
('Plan Ganancia Muscular', 'Plan alto en proteínas para ganar masa muscular', 2200, 35, 35, 30, 'avanzado', 'ganar_musculo'),
('Plan Mantenimiento', 'Plan equilibrado para mantener el peso actual', 2000, 45, 25, 30, 'principiante', 'mantenerse');

-- Entrenamientos básicos
INSERT INTO entrenamientos (nombre, descripcion, duracion_minutos, nivel, categoria, calorias_estimadas, rating_promedio, total_completados) VALUES
('Cardio HIIT Matutino', 'Quema grasa rápidamente con intervalos de alta intensidad', 20, 'intermedio', 'cardio', 200, 4.8, 1250),
('Fuerza Total Body', 'Rutina completa para todo el cuerpo sin equipos', 35, 'avanzado', 'fuerza', 280, 4.9, 890),
('Yoga Flow Relajante', 'Mejora tu flexibilidad y encuentra paz interior', 25, 'principiante', 'yoga', 120, 4.7, 2100),
('Abs Definidos', 'Fortalece tu core con ejercicios específicos', 15, 'intermedio', 'core', 140, 4.6, 1680);

-- Ejercicios para los entrenamientos
INSERT INTO ejercicios (entrenamiento_id, nombre, descripcion, duracion_segundos, series, repeticiones, descanso_segundos, orden_ejercicio, instrucciones) VALUES
-- Ejercicios para Cardio HIIT
(1, 'Saltos de tijera', 'Salta abriendo y cerrando las piernas mientras mueves los brazos', 45, NULL, NULL, 15, 1, 'Mantén el ritmo constante y respira profundamente'),
(1, 'Burpees', 'Ejercicio completo que combina sentadilla, flexión y salto', 30, NULL, NULL, 30, 2, 'Controla el movimiento y mantén la espalda recta'),
(1, 'Mountain climbers', 'Corre en el lugar llevando las rodillas al pecho', 45, NULL, NULL, 15, 3, 'Mantén el core activado durante todo el ejercicio'),
(1, 'Rodillas al pecho', 'Salta llevando las rodillas hacia el pecho', 45, NULL, NULL, 15, 4, 'Aterriza suavemente para proteger las articulaciones'),

-- Ejercicios para Fuerza Total Body
(2, 'Push-ups', 'Flexiones tradicionales para fortalecer pecho y brazos', NULL, 3, 12, 60, 1, 'Mantén el cuerpo en línea recta y baja hasta casi tocar el suelo'),
(2, 'Squats', 'Sentadillas para fortalecer piernas y glúteos', NULL, 3, 15, 60, 2, 'Baja hasta que los muslos estén paralelos al suelo'),
(2, 'Plancha', 'Mantén la posición de plancha para fortalecer el core', 60, NULL, NULL, 30, 3, 'Mantén el cuerpo recto y respira normalmente'),
(2, 'Lunges', 'Zancadas alternadas para trabajar piernas', NULL, 3, 10, 45, 4, 'Baja hasta que la rodilla trasera casi toque el suelo'),

-- Ejercicios para Yoga Flow
(3, 'Saludo al sol', 'Secuencia completa de yoga para calentar', 300, NULL, NULL, NULL, 1, 'Sigue el ritmo de tu respiración'),
(3, 'Guerrero I y II', 'Posturas de pie para fortalecer y estirar', 480, NULL, NULL, NULL, 2, 'Mantén la postura estable y respira profundamente'),
(3, 'Postura del niño', 'Postura de descanso y relajación', 180, NULL, NULL, NULL, 3, 'Relaja completamente el cuerpo'),
(3, 'Savasana', 'Relajación final en posición tumbada', 540, NULL, NULL, NULL, 4, 'Permite que el cuerpo se relaje completamente'),

-- Ejercicios para Abs Definidos
(4, 'Crunches', 'Abdominales tradicionales para el recto abdominal', NULL, 3, 20, 30, 1, 'Levanta solo los hombros del suelo'),
(4, 'Plancha lateral', 'Plancha de lado para trabajar oblicuos', 30, NULL, NULL, 30, 2, 'Mantén el cuerpo en línea recta'),
(4, 'Bicicleta', 'Ejercicio dinámico para abdominales', NULL, 3, 15, 30, 3, 'Alterna las rodillas hacia el pecho'),
(4, 'Dead bug', 'Ejercicio de estabilización del core', NULL, 3, 10, 30, 4, 'Mantén la espalda baja pegada al suelo');

-- Actividades infantiles
INSERT INTO actividades_infantiles (nombre, tipo, duracion_minutos, edad_minima, edad_maxima, dificultad, materiales, instrucciones, beneficios, creado_por) VALUES
('Torre de Bloques Gigante', 'diy', 45, 6, 12, 'facil', 'Cajas de cartón, Cinta adhesiva, Marcadores, Tijeras', 
'1. Reúne cajas de diferentes tamaños\n2. Decora cada caja con colores y patrones\n3. Apila las cajas de mayor a menor\n4. Prueba diferentes combinaciones\n5. ¡Crea la torre más alta!',
'Coordinación, Creatividad, Paciencia, Planificación', 1),

('Baile de los Animales', 'ejercicio', 20, 3, 10, 'facil', 'Música divertida, Espacio libre',
'1. Elige un animal (oso, rana, pájaro)\n2. Imita sus movimientos\n3. Añade música de fondo\n4. Cambia de animal cada 2 minutos\n5. ¡Inventa nuevos movimientos!',
'Ejercicio cardiovascular, Coordinación, Imaginación, Diversión', 1),

('Origami Mariposa', 'manualidad', 30, 8, 14, 'intermedio', 'Papel cuadrado colorido, Marcadores (opcional)',
'1. Dobla el papel por la mitad en diagonal\n2. Abre y dobla por la otra diagonal\n3. Forma un triángulo base\n4. Crea las alas con pliegues\n5. ¡Decora tu mariposa!',
'Concentración, Precisión, Paciencia, Habilidades motoras finas', 1);

-- Contenido multimedia
INSERT INTO contenido_multimedia (titulo, tipo, genero, duracion_minutos, año_produccion, rating_promedio, descripcion, elenco, director, es_premium) VALUES
('El Poder de la Mente', 'documental', 'Motivacional', 95, 2023, 4.8, 'Descubre cómo atletas de élite utilizan la mentalidad para superar límites', 'Dr. Michael Johnson, Serena Williams, LeBron James', 'Dr. Sarah Martinez', 1),
('Cocina Mediterránea Saludable', 'documental', 'Educativo Gastronómico', 120, 2023, 4.6, 'Aprende secretos de la cocina mediterránea para una vida más saludable', 'Chef María González, Dr. Antonio López', 'Chef María González', 1),
('Mindfulness: El Arte de Vivir', 'documental', 'Bienestar y Meditación', 80, 2024, 4.9, 'Una guía completa para incorporar mindfulness en tu vida diaria', 'Monje Thich Nhat Hanh, Dr. Jon Kabat-Zinn', 'Dr. Elena Rodriguez', 1);

-- Crear índices para optimizar consultas
CREATE INDEX idx_usuarios_email ON usuarios(email);
CREATE INDEX idx_sesiones_usuario_fecha ON sesiones_entrenamiento(usuario_id, fecha_inicio);
CREATE INDEX idx_progreso_peso_usuario_fecha ON progreso_peso(usuario_id, fecha_registro);
CREATE INDEX idx_estadisticas_usuario_fecha ON estadisticas_usuario(usuario_id, fecha);
CREATE INDEX idx_entrenamientos_categoria ON entrenamientos(categoria);
CREATE INDEX idx_entrenamientos_nivel ON entrenamientos(nivel);

-- Insertar usuario de prueba
INSERT INTO usuarios (nombre, email, password_hash, edad, genero, peso_actual, altura, peso_objetivo, nivel_fitness, es_premium) VALUES
('Usuario Demo', 'demo@fithome.com', 'a665a45920422f9d417e4867efdc4fb8a04a1f3fff1fa07e998e86f7f7a27ae3', 28, 'masculino', 75.5, 175, 70.0, 'intermedio', 1);

-- Insertar objetivos del usuario demo
INSERT INTO objetivos_usuario (usuario_id, objetivo) VALUES
(1, 'perder_peso'),
(1, 'mejorar_resistencia');

-- Insertar configuración del usuario demo
INSERT INTO configuraciones_usuario (usuario_id, tema_preferido, meta_calorias_diarias, meta_minutos_entrenamiento) VALUES
(1, 'claro', 1800, 30);

-- Insertar algunas estadísticas de ejemplo
INSERT INTO estadisticas_usuario (usuario_id, fecha, entrenamientos_completados, minutos_entrenamiento, calorias_quemadas, vasos_agua) VALUES
(1, date('now'), 1, 25, 200, 6),
(1, date('now', '-1 day'), 1, 30, 250, 8),
(1, date('now', '-2 days'), 0, 0, 0, 5);

-- Insertar progreso de peso
INSERT INTO progreso_peso (usuario_id, peso, fecha_registro) VALUES
(1, 76.0, datetime('now', '-7 days')),
(1, 75.8, datetime('now', '-5 days')),
(1, 75.5, datetime('now'));

-- Insertar hidratación diaria
INSERT INTO hidratacion_diaria (usuario_id, fecha, vasos_consumidos, meta_vasos) VALUES
(1, date('now'), 6, 8),
(1, date('now', '-1 day'), 8, 8),
(1, date('now', '-2 days'), 5, 8);
