-- Base de Datos FitHome Pro
-- Sistema de Gestión de Fitness y Bienestar

-- Crear base de datos
CREATE DATABASE IF NOT EXISTS fithome_pro;
USE fithome_pro;

-- Tabla de usuarios
CREATE TABLE usuarios (
    id INT PRIMARY KEY AUTO_INCREMENT,
    nombre VARCHAR(100) NOT NULL,
    email VARCHAR(150) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    edad INT,
    genero ENUM('masculino', 'femenino', 'otro'),
    peso_actual DECIMAL(5,2),
    altura INT,
    peso_objetivo DECIMAL(5,2),
    nivel_fitness ENUM('principiante', 'intermedio', 'avanzado'),
    fecha_registro TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    es_premium BOOLEAN DEFAULT FALSE,
    activo BOOLEAN DEFAULT TRUE
);

-- Tabla de objetivos de usuario
CREATE TABLE objetivos_usuario (
    id INT PRIMARY KEY AUTO_INCREMENT,
    usuario_id INT,
    objetivo ENUM('perder_peso', 'ganar_musculo', 'mantenerse', 'mejorar_resistencia', 'rehabilitacion', 'competir'),
    fecha_establecido TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (usuario_id) REFERENCES usuarios(id) ON DELETE CASCADE
);

-- Tabla de entrenamientos
CREATE TABLE entrenamientos (
    id INT PRIMARY KEY AUTO_INCREMENT,
    nombre VARCHAR(150) NOT NULL,
    descripcion TEXT,
    duracion_minutos INT NOT NULL,
    nivel ENUM('principiante', 'intermedio', 'avanzado'),
    categoria ENUM('cardio', 'fuerza', 'flexibilidad', 'core', 'yoga', 'pilates'),
    calorias_estimadas INT,
    imagen_url VARCHAR(255),
    rating_promedio DECIMAL(3,2) DEFAULT 0.0,
    total_completados INT DEFAULT 0,
    creado_por INT,
    fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    activo BOOLEAN DEFAULT TRUE,
    FOREIGN KEY (creado_por) REFERENCES usuarios(id)
);

-- Tabla de ejercicios
CREATE TABLE ejercicios (
    id INT PRIMARY KEY AUTO_INCREMENT,
    entrenamiento_id INT,
    nombre VARCHAR(150) NOT NULL,
    descripcion TEXT,
    duracion_segundos INT,
    series INT,
    repeticiones INT,
    peso_sugerido DECIMAL(5,2),
    descanso_segundos INT,
    orden_ejercicio INT,
    instrucciones TEXT,
    FOREIGN KEY (entrenamiento_id) REFERENCES entrenamientos(id) ON DELETE CASCADE
);

-- Tabla de sesiones de entrenamiento
CREATE TABLE sesiones_entrenamiento (
    id INT PRIMARY KEY AUTO_INCREMENT,
    usuario_id INT,
    entrenamiento_id INT,
    fecha_inicio TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    fecha_fin TIMESTAMP NULL,
    duracion_real_minutos INT,
    calorias_quemadas INT,
    completado BOOLEAN DEFAULT FALSE,
    rating_usuario INT CHECK (rating_usuario >= 1 AND rating_usuario <= 5),
    comentarios TEXT,
    FOREIGN KEY (usuario_id) REFERENCES usuarios(id),
    FOREIGN KEY (entrenamiento_id) REFERENCES entrenamientos(id)
);

-- Tabla de progreso de peso
CREATE TABLE progreso_peso (
    id INT PRIMARY KEY AUTO_INCREMENT,
    usuario_id INT,
    peso DECIMAL(5,2) NOT NULL,
    fecha_registro TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    notas TEXT,
    FOREIGN KEY (usuario_id) REFERENCES usuarios(id)
);

-- Tabla de hidratación diaria
CREATE TABLE hidratacion_diaria (
    id INT PRIMARY KEY AUTO_INCREMENT,
    usuario_id INT,
    fecha DATE NOT NULL,
    vasos_consumidos INT DEFAULT 0,
    meta_vasos INT DEFAULT 8,
    FOREIGN KEY (usuario_id) REFERENCES usuarios(id),
    UNIQUE KEY unique_user_date (usuario_id, fecha)
);


-- Tabla de estadísticas de usuario
CREATE TABLE estadisticas_usuario (
    id INT PRIMARY KEY AUTO_INCREMENT,
    usuario_id INT,
    fecha DATE NOT NULL,
    entrenamientos_completados INT DEFAULT 0,
    minutos_entrenamiento INT DEFAULT 0,
    calorias_quemadas INT DEFAULT 0,
    vasos_agua INT DEFAULT 0,
    peso_registrado DECIMAL(5,2),
    FOREIGN KEY (usuario_id) REFERENCES usuarios(id),
    UNIQUE KEY unique_user_date (usuario_id, fecha)
);

-- Tabla de logros
CREATE TABLE logros (
    id INT PRIMARY KEY AUTO_INCREMENT,
    nombre VARCHAR(100) NOT NULL,
    descripcion TEXT,
    icono VARCHAR(10),
    criterio_tipo ENUM('entrenamientos', 'calorias', 'racha', 'peso', 'tiempo'),
    criterio_valor INT,
    puntos INT DEFAULT 0
);

-- Tabla de logros de usuario
CREATE TABLE logros_usuario (
    id INT PRIMARY KEY AUTO_INCREMENT,
    usuario_id INT,
    logro_id INT,
    fecha_obtenido TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (usuario_id) REFERENCES usuarios(id),
    FOREIGN KEY (logro_id) REFERENCES logros(id),
    UNIQUE KEY unique_user_achievement (usuario_id, logro_id)
);

-- Tabla de planes nutricionales
CREATE TABLE planes_nutricionales (
    id INT PRIMARY KEY AUTO_INCREMENT,
    nombre VARCHAR(150) NOT NULL,
    descripcion TEXT,
    calorias_diarias INT,
    carbohidratos_porcentaje INT,
    proteinas_porcentaje INT,
    grasas_porcentaje INT,
    nivel_fitness ENUM('principiante', 'intermedio', 'avanzado'),
    objetivo ENUM('perder_peso', 'ganar_musculo', 'mantenerse'),
    activo BOOLEAN DEFAULT TRUE
);

-- Tabla de comidas
CREATE TABLE comidas (
    id INT PRIMARY KEY AUTO_INCREMENT,
    plan_nutricional_id INT,
    nombre VARCHAR(100) NOT NULL,
    tipo ENUM('desayuno', 'almuerzo', 'cena', 'snack'),
    calorias INT,
    carbohidratos_g DECIMAL(5,2),
    proteinas_g DECIMAL(5,2),
    grasas_g DECIMAL(5,2),
    ingredientes TEXT,
    instrucciones TEXT,
    tiempo_preparacion_minutos INT,
    FOREIGN KEY (plan_nutricional_id) REFERENCES planes_nutricionales(id) ON DELETE CASCADE
);

-- Tabla de seguimiento nutricional
CREATE TABLE seguimiento_nutricional (
    id INT PRIMARY KEY AUTO_INCREMENT,
    usuario_id INT,
    fecha DATE NOT NULL,
    calorias_consumidas INT DEFAULT 0,
    carbohidratos_g DECIMAL(5,2) DEFAULT 0,
    proteinas_g DECIMAL(5,2) DEFAULT 0,
    grasas_g DECIMAL(5,2) DEFAULT 0,
    FOREIGN KEY (usuario_id) REFERENCES usuarios(id),
    UNIQUE KEY unique_user_date (usuario_id, fecha)
);

-- Tabla de configuraciones de usuario
CREATE TABLE configuraciones_usuario (
    id INT PRIMARY KEY AUTO_INCREMENT,
    usuario_id INT,
    tema_preferido ENUM('claro', 'oscuro', 'auto'),
    idioma VARCHAR(5) DEFAULT 'es',
    notificaciones_entrenamiento BOOLEAN DEFAULT TRUE,
    notificaciones_hidratacion BOOLEAN DEFAULT TRUE,
    notificaciones_nutricion BOOLEAN DEFAULT TRUE,
    meta_calorias_diarias INT DEFAULT 2000,
    meta_minutos_entrenamiento INT DEFAULT 30,
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
('El Poder de la Mente', 'documental', 'Motivacional', 95, 2023, 4.8, 'Descubre cómo atletas de élite utilizan la mentalidad para superar límites', 'Dr. Michael Johnson, Serena Williams, LeBron James', 'Dr. Sarah Martinez', TRUE),
('Cocina Mediterránea Saludable', 'documental', 'Educativo Gastronómico', 120, 2023, 4.6, 'Aprende secretos de la cocina mediterránea para una vida más saludable', 'Chef María González, Dr. Antonio López', 'Chef María González', TRUE),
('Mindfulness: El Arte de Vivir', 'documental', 'Bienestar y Meditación', 80, 2024, 4.9, 'Una guía completa para incorporar mindfulness en tu vida diaria', 'Monje Thich Nhat Hanh, Dr. Jon Kabat-Zinn', 'Dr. Elena Rodriguez', TRUE);

-- Crear índices para optimizar consultas
CREATE INDEX idx_usuarios_email ON usuarios(email);
CREATE INDEX idx_sesiones_usuario_fecha ON sesiones_entrenamiento(usuario_id, fecha_inicio);
CREATE INDEX idx_progreso_peso_usuario_fecha ON progreso_peso(usuario_id, fecha_registro);
CREATE INDEX idx_estadisticas_usuario_fecha ON estadisticas_usuario(usuario_id, fecha);
CREATE INDEX idx_entrenamientos_categoria ON entrenamientos(categoria);
CREATE INDEX idx_entrenamientos_nivel ON entrenamientos(nivel);

-- Crear vistas útiles
CREATE VIEW vista_progreso_usuario AS
SELECT 
    u.id,
    u.nombre,
    u.email,
    COUNT(DISTINCT se.id) as total_entrenamientos,
    COALESCE(SUM(se.calorias_quemadas), 0) as total_calorias,
    COALESCE(SUM(se.duracion_real_minutos), 0) as total_minutos,
    COALESCE(AVG(se.rating_usuario), 0) as rating_promedio
FROM usuarios u
LEFT JOIN sesiones_entrenamiento se ON u.id = se.usuario_id
WHERE se.completado = TRUE
GROUP BY u.id, u.nombre, u.email;

CREATE VIEW vista_entrenamientos_populares AS
SELECT 
    e.id,
    e.nombre,
    e.categoria,
    e.nivel,
    e.rating_promedio,
    e.total_completados,
    COUNT(se.id) as sesiones_mes_actual
FROM entrenamientos e
LEFT JOIN sesiones_entrenamiento se ON e.id = se.entrenamiento_id 
    AND se.fecha_inicio >= DATE_SUB(CURDATE(), INTERVAL 1 MONTH)
GROUP BY e.id, e.nombre, e.categoria, e.nivel, e.rating_promedio, e.total_completados
ORDER BY e.rating_promedio DESC, e.total_completados DESC;

-- Procedimientos almacenados útiles
DELIMITER //

CREATE PROCEDURE RegistrarEntrenamientoCompletado(
    IN p_usuario_id INT,
    IN p_entrenamiento_id INT,
    IN p_duracion_minutos INT,
    IN p_calorias_quemadas INT,
    IN p_rating INT
)
BEGIN
    DECLARE EXIT HANDLER FOR SQLEXCEPTION
    BEGIN
        ROLLBACK;
        RESIGNAL;
    END;
    
    START TRANSACTION;
    
    -- Actualizar sesión de entrenamiento
    UPDATE sesiones_entrenamiento 
    SET fecha_fin = NOW(),
        duracion_real_minutos = p_duracion_minutos,
        calorias_quemadas = p_calorias_quemadas,
        completado = TRUE,
        rating_usuario = p_rating
    WHERE usuario_id = p_usuario_id 
        AND entrenamiento_id = p_entrenamiento_id 
        AND completado = FALSE;
    
    -- Actualizar estadísticas del entrenamiento
    UPDATE entrenamientos 
    SET total_completados = total_completados + 1,
        rating_promedio = (rating_promedio * total_completados + p_rating) / (total_completados + 1)
    WHERE id = p_entrenamiento_id;
    
    -- Actualizar estadísticas diarias del usuario
    INSERT INTO estadisticas_usuario (usuario_id, fecha, entrenamientos_completados, minutos_entrenamiento, calorias_quemadas)
    VALUES (p_usuario_id, CURDATE(), 1, p_duracion_minutos, p_calorias_quemadas)
    ON DUPLICATE KEY UPDATE
        entrenamientos_completados = entrenamientos_completados + 1,
        minutos_entrenamiento = minutos_entrenamiento + p_duracion_minutos,
        calorias_quemadas = calorias_quemadas + p_calorias_quemadas;
    
    COMMIT;
END //

CREATE PROCEDURE CalcularRachaUsuario(IN p_usuario_id INT)
BEGIN
    DECLARE v_racha INT DEFAULT 0;
    DECLARE v_fecha_actual DATE DEFAULT CURDATE();
    DECLARE v_fecha_entrenamiento DATE;
    DECLARE v_dias_diferencia INT;
    
    -- Obtener la fecha del último entrenamiento
    SELECT DATE(fecha_inicio) INTO v_fecha_entrenamiento
    FROM sesiones_entrenamiento 
    WHERE usuario_id = p_usuario_id 
        AND completado = TRUE
    ORDER BY fecha_inicio DESC 
    LIMIT 1;
    
    -- Calcular racha si hay entrenamientos
    IF v_fecha_entrenamiento IS NOT NULL THEN
        SET v_dias_diferencia = DATEDIFF(v_fecha_actual, v_fecha_entrenamiento);
        
        -- Si el último entrenamiento fue ayer o hoy, calcular racha
        IF v_dias_diferencia <= 1 THEN
            -- Contar días consecutivos hacia atrás
            WHILE v_fecha_entrenamiento IS NOT NULL DO
                SELECT DATE(fecha_inicio) INTO v_fecha_entrenamiento
                FROM sesiones_entrenamiento 
                WHERE usuario_id = p_usuario_id 
                    AND completado = TRUE
                    AND DATE(fecha_inicio) = DATE_SUB(v_fecha_entrenamiento, INTERVAL 1 DAY)
                LIMIT 1;
                
                IF v_fecha_entrenamiento IS NOT NULL THEN
                    SET v_racha = v_racha + 1;
                END IF;
            END WHILE;
            
            SET v_racha = v_racha + 1; -- Incluir el último entrenamiento
        END IF;
    END IF;
    
    SELECT v_racha as racha_dias;
END //

DELIMITER ;

-- Triggers para mantener consistencia de datos
DELIMITER //

CREATE TRIGGER tr_actualizar_estadisticas_entrenamiento
AFTER INSERT ON sesiones_entrenamiento
FOR EACH ROW
BEGIN
    IF NEW.completado = TRUE THEN
        UPDATE estadisticas_usuario 
        SET entrenamientos_completados = entrenamientos_completados + 1,
            minutos_entrenamiento = minutos_entrenamiento + NEW.duracion_real_minutos,
            calorias_quemadas = calorias_quemadas + NEW.calorias_quemadas
        WHERE usuario_id = NEW.usuario_id 
            AND fecha = DATE(NEW.fecha_inicio);
    END IF;
END //

DELIMITER ;

-- Insertar usuario de prueba
INSERT INTO usuarios (nombre, email, password_hash, edad, genero, peso_actual, altura, peso_objetivo, nivel_fitness, es_premium) VALUES
('Usuario Demo', 'demo@fithome.com', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewdBPj4V7K5Q5Q5O', 28, 'masculino', 75.5, 175, 70.0, 'intermedio', TRUE);

-- Insertar objetivos del usuario demo
INSERT INTO objetivos_usuario (usuario_id, objetivo) VALUES
(1, 'perder_peso'),
(1, 'mejorar_resistencia');

-- Insertar configuración del usuario demo
INSERT INTO configuraciones_usuario (usuario_id, tema_preferido, meta_calorias_diarias, meta_minutos_entrenamiento) VALUES
(1, 'claro', 1800, 30);

-- Insertar algunas estadísticas de ejemplo
INSERT INTO estadisticas_usuario (usuario_id, fecha, entrenamientos_completados, minutos_entrenamiento, calorias_quemadas, vasos_agua) VALUES
(1, CURDATE(), 1, 25, 200, 6),
(1, DATE_SUB(CURDATE(), INTERVAL 1 DAY), 1, 30, 250, 8),
(1, DATE_SUB(CURDATE(), INTERVAL 2 DAY), 0, 0, 0, 5);

-- Insertar progreso de peso
INSERT INTO progreso_peso (usuario_id, peso, fecha_registro) VALUES
(1, 76.0, DATE_SUB(CURDATE(), INTERVAL 7 DAY)),
(1, 75.8, DATE_SUB(CURDATE(), INTERVAL 5 DAY)),
(1, 75.5, CURDATE());

-- Insertar hidratación diaria
INSERT INTO hidratacion_diaria (usuario_id, fecha, vasos_consumidos, meta_vasos) VALUES
(1, CURDATE(), 6, 8),
(1, DATE_SUB(CURDATE(), INTERVAL 1 DAY), 8, 8),
(1, DATE_SUB(CURDATE(), INTERVAL 2 DAY), 5, 8);

COMMIT;
