-- Consultas de ejemplo
SELECT * FROM usuarios;
SELECT u.nombre, p.fecha FROM usuarios u
JOIN pedidos p ON u.id = p.usuario_id;
