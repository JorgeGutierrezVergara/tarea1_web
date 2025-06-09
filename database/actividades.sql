
USE `tarea2`;

SET FOREIGN_KEY_CHECKS = 0;
TRUNCATE TABLE actividad_tema;
TRUNCATE TABLE contactar_por;
TRUNCATE TABLE foto;
TRUNCATE TABLE actividad;
SET FOREIGN_KEY_CHECKS = 1;

-- ## Actividad 1: (Comuna: Santiago, ID: 130208)
INSERT INTO actividad (comuna_id, sector, nombre, email, celular, dia_hora_inicio, dia_hora_termino, descripcion)
VALUES (130208, 'Barrio Lastarria', 'Hernan Hernandez', 'fotos@email.com', '+569.87654321', '2025-07-15 10:00:00', '2025-07-15 13:00:00', 'Taller de fotografía');
SET @actividad_id_1 = LAST_INSERT_ID();
INSERT INTO foto (ruta_archivo, nombre_archivo, actividad_id) VALUES ('fotos1.jpeg', 'paseo_foto_01.jpg', @actividad_id_1);
INSERT INTO foto (ruta_archivo, nombre_archivo, actividad_id) VALUES ('fotos2.jpg', 'paseo_foto_02.jpg', @actividad_id_1);
INSERT INTO actividad_tema (tema, actividad_id) VALUES ('tecnología', @actividad_id_1);
INSERT INTO contactar_por (nombre, identificador, actividad_id) VALUES ('instagram', '@paseofoto.lastarria', @actividad_id_1);

-- ## Actividad 2: (Comuna: Providencia, ID: 130207)
 INSERT INTO actividad (comuna_id, sector, nombre, email, dia_hora_inicio, dia_hora_termino, descripcion)
 VALUES (130207, 'Inés de Suárez', 'Gordon Ramsey', 'cocina@email.com', '2025-07-15 10:00:00', '2025-07-15 13:00:00', 'Clase de Repostería');
 SET @actividad_id_2 = LAST_INSERT_ID();
 INSERT INTO foto (ruta_archivo, nombre_archivo, actividad_id) VALUES ('reposteria.jpeg', 'reposteria.jpeg', @actividad_id_2);
 INSERT INTO actividad_tema (tema, actividad_id) VALUES ('comida', @actividad_id_2);
 INSERT INTO actividad_tema (tema, glosa_otro, actividad_id) VALUES ('otro', 'Saludable', @actividad_id_2);
 INSERT INTO contactar_por (nombre, identificador, actividad_id) VALUES ('whatsapp', '+56911223344', @actividad_id_2);

-- ## Actividad 3: (Comuna: Maipú, ID: 130212)
INSERT INTO actividad (comuna_id, sector, nombre, email, dia_hora_inicio, dia_hora_termino, descripcion)
VALUES (130212, 'Plaza de Maipú', 'Chico Terry', 'pichanga@email.com', '2025-07-15 10:00:00', '2025-07-15 13:00:00', 'Pichanga en el Parque O\'Higgins');
SET @actividad_id_3 = LAST_INSERT_ID();
INSERT INTO foto (ruta_archivo, nombre_archivo, actividad_id) VALUES ('pichanga.png', 'pichanga.png', @actividad_id_3);
INSERT INTO actividad_tema (tema, actividad_id) VALUES ('deporte', @actividad_id_3);
INSERT INTO contactar_por (nombre, identificador, actividad_id) VALUES ('telegram', '@pichanga_ohiggins', @actividad_id_3);

-- ## Actividad 4: (Comuna: La Florida, ID: 130214)
INSERT INTO actividad (comuna_id, sector, nombre, email, dia_hora_inicio, descripcion)
VALUES (130214, 'San Jorge', 'Dagon', 'club.lectura.lovecraft@email.com', '2025-08-10 19:30:00', 'Club de Lectura: H.P Lovecraft');
SET @actividad_id_4 = LAST_INSERT_ID();
INSERT INTO foto (ruta_archivo, nombre_archivo, actividad_id) VALUES ('lovecraft.png', 'lovecraft.png', @actividad_id_4);
INSERT INTO actividad_tema (tema, glosa_otro, actividad_id) VALUES ('otro', 'Literatura', @actividad_id_4);

-- ## Actividad 5: (Comuna: Valparaíso, ID: 50506)
INSERT INTO actividad (comuna_id, sector, nombre, email, celular, dia_hora_inicio, dia_hora_termino, descripcion)
VALUES (50506, 'Laguna Verde', 'Shinji Ikari', 'manga@email.com', '+569.55667788', '2025-07-15 10:00:00', '2025-07-15 13:00:00', 'Taller de Manga');
SET @actividad_id_5 = LAST_INSERT_ID();
INSERT INTO foto (ruta_archivo, nombre_archivo, actividad_id) VALUES ('manga.jpg', 'manga.jpg', @actividad_id_5);
INSERT INTO actividad_tema (tema, glosa_otro, actividad_id) VALUES ('otro', 'Arte', @actividad_id_5);
INSERT INTO contactar_por (nombre, identificador, actividad_id) VALUES ('instagram', '@manga.valpo', @actividad_id_5);

-- ## Actividad 6: (Comuna: Ñuñoa, ID: 130210)
INSERT INTO actividad (comuna_id, sector, nombre, email, dia_hora_inicio, descripcion)
VALUES (130210, 'Plaza Ñuñoa', 'Totally not a dog', 'juegos.nunoa@email.com', '2025-08-22 20:00:00', 'Noche de Exploding kittens');
SET @actividad_id_6 = LAST_INSERT_ID();
INSERT INTO foto (ruta_archivo, nombre_archivo, actividad_id) VALUES ('ekittens.png', 'ekittens.png', @actividad_id_6);
INSERT INTO actividad_tema (tema, actividad_id) VALUES ('juegos', @actividad_id_6);

-- ## Actividad 7: (Comuna: Vitacura, ID: 130219)
INSERT INTO actividad (comuna_id, sector, nombre, email, dia_hora_inicio, descripcion)
VALUES (130219, 'Alonso de Córdova', 'J.R.R. Tolkien', 'trek.mordor@email.com', '2025-09-05 08:00:00', 'Trekking a Mordor');
SET @actividad_id_7 = LAST_INSERT_ID();
INSERT INTO foto (ruta_archivo, nombre_archivo, actividad_id) VALUES ('mordor.jpg', 'mordor.jpg', @actividad_id_7);
INSERT INTO actividad_tema (tema, actividad_id) VALUES ('deporte', @actividad_id_7);
INSERT INTO contactar_por (nombre, identificador, actividad_id) VALUES ('whatsapp', '+56998765432', @actividad_id_7);

-- ## Actividad 8: (Comuna: Las Condes, ID: 130204)
INSERT INTO actividad (comuna_id, sector, nombre, email, dia_hora_inicio, descripcion)
VALUES (130204, 'Parque Araucano', 'Mr. Beast', 'eng.speak@email.com', '2025-09-10 19:00:00', 'Práctica de inglés');
SET @actividad_id_8 = LAST_INSERT_ID();
INSERT INTO foto (ruta_archivo, nombre_archivo, actividad_id) VALUES ('english.png', 'english.png', @actividad_id_8);
INSERT INTO actividad_tema (tema, glosa_otro, actividad_id) VALUES ('otro', 'Educación', @actividad_id_8);

-- ## Actividad 9: (Comuna: Santiago, ID: 130208)
INSERT INTO actividad (comuna_id, sector, nombre, email, dia_hora_inicio, descripcion)
VALUES (130208, 'Barrio Italia', 'Louis Armstrong', 'jazz.club.stgo@email.com', '2025-09-12 21:00:00', 'The Jazz Corner');
SET @actividad_id_9 = LAST_INSERT_ID();
INSERT INTO foto (ruta_archivo, nombre_archivo, actividad_id) VALUES ('jazz.jpeg', 'jazz.jpeg', @actividad_id_9);
INSERT INTO actividad_tema (tema, actividad_id) VALUES ('música', @actividad_id_9);

-- ## Actividad 10: (Comuna: Santiago, ID: 130208) 
INSERT INTO actividad (comuna_id, sector, nombre, email, dia_hora_inicio, dia_hora_termino, descripcion)
VALUES (130208, 'Beauchef 851', 'Hacker McHack', 'python.dcc@email.com', '2025-09-20 14:00:00', '2025-09-20 18:00:00', 'Taller de Programación con Python');
SET @actividad_id_10 = LAST_INSERT_ID();
INSERT INTO foto (ruta_archivo, nombre_archivo, actividad_id) VALUES ('python.png', 'python.png', @actividad_id_10);
INSERT INTO actividad_tema (tema, actividad_id) VALUES ('tecnología', @actividad_id_10);

-- ## Actividad 11: (Comuna: Valparaíso, ID: 50506)
INSERT INTO actividad (comuna_id, sector, nombre, email, dia_hora_inicio, descripcion)
VALUES (50506, 'Plaza Sotomayor', 'Doña María', 'feria.valpo@email.com', '2025-09-27 10:00:00', 'Feria de las Pulgas');
SET @actividad_id_11 = LAST_INSERT_ID();
INSERT INTO foto (ruta_archivo, nombre_archivo, actividad_id) VALUES ('feria.jpeg', 'feria.jpeg', @actividad_id_11);
INSERT INTO actividad_tema (tema, glosa_otro, actividad_id) VALUES ('otro', 'Compras', @actividad_id_11);

-- ## Actividad 12: (Comuna: Viña del Mar, ID: 50503)
INSERT INTO actividad (comuna_id, sector, nombre, email, dia_hora_inicio, descripcion)
VALUES (50503, 'Playa Reñaca', 'Truli Maluli', 'metal.vina@email.com', '2025-10-04 20:00:00', 'Concierto metal');
SET @actividad_id_12 = LAST_INSERT_ID();
INSERT INTO foto (ruta_archivo, nombre_archivo, actividad_id) VALUES ('merol.jpeg', 'merol.jpeg', @actividad_id_12);
INSERT INTO actividad_tema (tema, actividad_id) VALUES ('música', @actividad_id_12);






INSERT INTO comentario (nombre, texto, fecha, actividad_id) VALUES
('Peter Parker', 'Llevaré mi cámara!', '2025-06-01 10:00:00', 1),

('Remy', 'Ramtatuil', '2025-06-02 10:00:00', 2),

('El bicho', 'siuuuuuu', '2025-06-02 10:00:00', 3),

('Edgar Poe', 'Puedo llevar mi Necronomicon :)', '2025-06-02 10:00:00', 4),

('Azuka', 'Feliz jueves!', '2025-06-02 10:00:00', 5),

('Señor Gato', 'Te voy a funar', '2025-06-02 10:00:00', 6),

('Gandalf', 'Les sale más fácil ir en Águilas...', '2025-06-02 10:00:00', 7),

('sub n° 19281928', 'misterbis', '2025-06-02 10:00:00', 8),

('Neil Armstrong', 'Tú eres el que fue a la luna, o no?', '2025-06-02 10:00:00', 9),

('H4ck3r', 'Buena actividad, lamentablemente tengo tu ip', '2025-06-02 10:00:00', 10),

('Punketa', 'Pasao a chela', '2025-06-02 10:00:00', 11);

