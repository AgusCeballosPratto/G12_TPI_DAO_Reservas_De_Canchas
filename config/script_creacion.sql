-- ELIMINACION DE DATOS PREVIOS Y REINICIO DE SECUENCIAS

-- Tabla Estado
DELETE FROM Estado;
DELETE FROM sqlite_sequence WHERE name = 'Estado';

-- Tabla Servicio
DELETE FROM Servicio;
DELETE FROM sqlite_sequence WHERE name = 'Servicio';

-- Tabla Cancha
DELETE FROM Cancha;
DELETE FROM sqlite_sequence WHERE name = 'Cancha';

-- INSERTS DE TABLAS 

-- Tabla Estado
INSERT INTO Estado (nombre, ambito) VALUES
('Disponible', 1),  
('Ocupado', 1),     
('Confirmada', 2), 
('Pendiente', 2),   
('Cancelada', 2),  
('Pagado', 3),      
('Pendiente', 3),   
('Anulado', 3);     

-- Tabla Servicio
INSERT INTO Servicio (nombre, costo) VALUES
('Iluminacion', 2500),
('Arbitro', 5000);

-- Tabla Cancha 
INSERT INTO Cancha (nombre, tipo, costo_por_hora, capacidad, id_estado) VALUES
('Cancha de Futbol 5', 'Futbol', 15000, 10, 1),
('Cancha de Futbol 7 Norte', 'Futbol', 20000, 14, 1),
('Cancha de Futbol 7 Sur', 'Futbol', 20000, 14, 1),
('Cancha de Padel', 'Padel', 10000, 4, 1),
('Cancha de Basket', 'Basket', 14000, 6, 1);

