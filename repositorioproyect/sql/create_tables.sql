-- Creación de tablas de ejemplo
CREATE TABLE usuarios (
    id INT PRIMARY KEY AUTO_INCREMENT,
    nombre VARCHAR(100),
    email VARCHAR(100) UNIQUE
);

CREATE TABLE pedidos (
    id INT PRIMARY KEY AUTO_INCREMENT,
    usuario_id INT,
    fecha DATE,
    FOREIGN KEY (usuario_id) REFERENCES usuarios(id)
);
