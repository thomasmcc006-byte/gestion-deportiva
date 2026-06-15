CREATE DATABASE gestion_deportiva
USE gestion_deportiva;

CREATE TABLE disciplina (
    id_disciplina INT AUTO_INCREMENT PRIMARY KEY,
    nombre        VARCHAR(50) NOT NULL UNIQUE
);

CREATE TABLE espacio_deportivo (
    id_espacio  INT AUTO_INCREMENT PRIMARY KEY,
    nombre      VARCHAR(100) NOT NULL UNIQUE,
    descripcion VARCHAR(200)
);

CREATE TABLE estudiante (
    id_estudiante INT AUTO_INCREMENT PRIMARY KEY,
    documento     VARCHAR(12)  NOT NULL UNIQUE,
    nombre        VARCHAR(50)  NOT NULL,
    apellido      VARCHAR(50)  NOT NULL,
    email         VARCHAR(100) NOT NULL UNIQUE,
    carrera       VARCHAR(100) NOT NULL,
    facultad      VARCHAR(100) NOT NULL
);

CREATE TABLE actividad (
    id_actividad  INT AUTO_INCREMENT PRIMARY KEY,
    nombre        VARCHAR(100) NOT NULL,
    id_disciplina INT          NOT NULL,
    id_espacio    INT          NOT NULL,
    cupo_maximo   INT          NOT NULL CHECK (cupo_maximo > 0),
    dia           ENUM('Lunes','Martes','Miércoles','Jueves','Viernes','Sábado','Domingo') NOT NULL,
    horario       TIME         NOT NULL,
    estado        ENUM('abierta','cerrada','finalizada','cancelada') NOT NULL DEFAULT 'abierta',
    FOREIGN KEY (id_disciplina) REFERENCES disciplina(id_disciplina),
    FOREIGN KEY (id_espacio)    REFERENCES espacio_deportivo(id_espacio)
);

CREATE TABLE inscripcion (
    id_inscripcion    INT AUTO_INCREMENT PRIMARY KEY,
    id_estudiante     INT      NOT NULL,
    id_actividad      INT      NOT NULL,
    estado            ENUM('confirmada','lista_espera') NOT NULL,
    fecha_inscripcion DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    UNIQUE (id_estudiante, id_actividad),
    FOREIGN KEY (id_estudiante) REFERENCES estudiante(id_estudiante),
    FOREIGN KEY (id_actividad)  REFERENCES actividad(id_actividad)
);

CREATE TABLE asistencia (
    id_asistencia  INT  AUTO_INCREMENT PRIMARY KEY,
    id_inscripcion INT  NOT NULL,
    fecha          DATE NOT NULL,
    UNIQUE (id_inscripcion, fecha),
    FOREIGN KEY (id_inscripcion) REFERENCES inscripcion(id_inscripcion)
);

INSERT INTO disciplina (nombre) VALUES
('Futbol'),
('Basquetbol'),
('Atletismo'),
('Voleibol'),
('Yoga'),
('Funcional'),
('Gimnasio');

INSERT INTO espacio_deportivo (nombre, descripcion) VALUES
('Cancha de futbol A',   'Cancha de cesped sintetico, capacidad 22 personas'),
('Gimnasio principal',   'Gimnasio cubierto con equipamiento completo'),
('Pista de atletismo',   'Pista exterior de 400 metros'),
('Cancha de basquetbol', 'Cancha techada con tableros reglamentarios'),
('Salon multiusos',      'Salon interior para yoga y funcional');


INSERT INTO estudiante (documento, nombre, apellido, email, carrera, facultad) VALUES
('1.234.567-8', 'Agustina',  'Perez',     'agustina.perez@estudiantes.ucu.edu.uy',    'Ingenieria en Sistemas', 'Facultad de Ingenieria'),
('2.345.678-9', 'Mateo',     'Gonzalez',  'mateo.gonzalez@estudiantes.ucu.edu.uy',    'Contador Publico',       'Facultad de Ciencias Empresariales'),
('3.456.789-0', 'Valentina', 'Rodriguez', 'valentina.rodriguez@estudiantes.ucu.edu.uy','Psicologia',            'Facultad de Psicologia'),
('4.567.890-1', 'Santiago',  'Lopez',     'santiago.lopez@estudiantes.ucu.edu.uy',    'Derecho',                'Facultad de Derecho'),
('5.678.901-2', 'Sofia',     'Martinez',  'sofia.martinez@estudiantes.ucu.edu.uy',    'Ingenieria en Sistemas', 'Facultad de Ingenieria'),
('6.789.012-3', 'Nicolas',   'Fernandez', 'nicolas.fernandez@estudiantes.ucu.edu.uy', 'Administracion',         'Facultad de Ciencias Empresariales'),
('7.890.123-4', 'Lucia',     'Garcia',    'lucia.garcia@estudiantes.ucu.edu.uy',       'Comunicacion',          'Facultad de Comunicacion'),
('8.901.234-5', 'Tomas',     'Diaz',      'tomas.diaz@estudiantes.ucu.edu.uy',        'Derecho',                'Facultad de Derecho'),
('9.012.345-6', 'Camila',    'Torres',    'camila.torres@estudiantes.ucu.edu.uy',     'Psicologia',             'Facultad de Psicologia'),
('1.123.456-7', 'Ignacio',   'Suarez',    'ignacio.suarez@estudiantes.ucu.edu.uy',    'Ingenieria en Sistemas', 'Facultad de Ingenieria'),
('2.234.567-8', 'Florencia', 'Nunez',     'florencia.nunez@estudiantes.ucu.edu.uy',   'Contador Publico',       'Facultad de Ciencias Empresariales'),
('3.345.678-9', 'Andres',    'Cabrera',   'andres.cabrera@estudiantes.ucu.edu.uy',    'Comunicacion',           'Facultad de Comunicacion');

INSERT INTO actividad (nombre, id_disciplina, id_espacio, cupo_maximo, dia, horario, estado) VALUES
('Futbol recreativo mixto',  1, 1, 3,  'Lunes',     '18:00:00', 'abierta'),
('Futbol competitivo',       1, 1, 10, 'Miercoles', '19:00:00', 'abierta'),
('Basquetbol inicial',       2, 4, 12, 'Martes',    '17:00:00', 'abierta'),
('Atletismo inicial',        3, 3, 20, 'Jueves',    '07:00:00', 'abierta'),
('Voleibol recreativo',      4, 4, 14, 'Viernes',   '18:00:00', 'cerrada'),
('Yoga turno manana',        5, 5, 15, 'Martes',    '08:00:00', 'abierta'),
('Funcional turno manana',   6, 5, 10, 'Lunes',     '07:00:00', 'abierta'),
('Funcional turno noche',    6, 5, 10, 'Miercoles', '20:00:00', 'cancelada'),
('Gimnasio libre',           7, 2, 25, 'Lunes',     '06:00:00', 'abierta'),
('Atletismo avanzado',       3, 3, 15, 'Sabado',    '09:00:00', 'finalizada');

INSERT INTO inscripcion (id_estudiante, id_actividad, estado) VALUES
(1,  1, 'confirmada'),
(2,  1, 'confirmada'),
(3,  1, 'confirmada'),
(4,  1, 'lista_espera'),
(5,  1, 'lista_espera'),
(1,  2, 'confirmada'),
(2,  3, 'confirmada'),
(3,  4, 'confirmada'),
(4,  4, 'confirmada'),
(5,  6, 'confirmada'),
(6,  6, 'confirmada'),
(7,  7, 'confirmada'),
(8,  7, 'confirmada'),
(9,  9, 'confirmada'),
(10, 9, 'confirmada'),
(11, 9, 'confirmada'),
(12, 2, 'confirmada');


INSERT INTO asistencia (id_inscripcion, fecha) VALUES
(1,  '2026-06-02'),
(1,  '2026-06-09'),
(2,  '2026-06-02'),
(6,  '2026-06-04'),
(6,  '2026-06-11'),
(7,  '2026-06-03'),
(8,  '2026-06-05'),
(9,  '2026-06-05'),
(10, '2026-06-03'),
(11, '2026-06-03'),
(12, '2026-06-02'),
(13, '2026-06-02'),
(14, '2026-06-02'),
(15, '2026-06-02');

ALTER TABLE actividad
MODIFY dia ENUM('Lunes','Martes','Miercoles','Jueves','Viernes','Sabado','Domingo') NOT NULL;

-- Usuarios y permisos por rol
-- ------------------------------------------------------------

-- Crea los 3 usuarios de MySQL, uno por cada rol del sistema, con contraseña simple
CREATE USER 'admin_user'@'localhost' IDENTIFIED BY 'admin123';
CREATE USER 'docente_user'@'localhost' IDENTIFIED BY 'docente123';
CREATE USER 'estudiante_user'@'localhost' IDENTIFIED BY 'estudiante123';

-- ADMINISTRADOR: acceso total a todas las tablas de la base (igual que root)
GRANT ALL PRIVILEGES ON gestion_deportiva.* TO 'admin_user'@'localhost';

-- DOCENTE: puede consultar (SELECT) cualquier tabla, para ver datos y reportes
GRANT SELECT ON gestion_deportiva.* TO 'docente_user'@'localhost';
-- ademas puede insertar y modificar registros de asistencia (regla de negocio 5)
GRANT INSERT, UPDATE ON gestion_deportiva.asistencia TO 'docente_user'@'localhost';

-- ESTUDIANTE: puede ver el catalogo de disciplinas disponibles
GRANT SELECT ON gestion_deportiva.disciplina TO 'estudiante_user'@'localhost';
-- puede ver los espacios deportivos
GRANT SELECT ON gestion_deportiva.espacio_deportivo TO 'estudiante_user'@'localhost';
-- puede ver las actividades disponibles para inscribirse
GRANT SELECT ON gestion_deportiva.actividad TO 'estudiante_user'@'localhost';
-- puede ver, crear y cancelar sus propias inscripciones
GRANT SELECT, INSERT, DELETE ON gestion_deportiva.inscripcion TO 'estudiante_user'@'localhost';
-- puede ver sus registros de asistencia (no puede modificarlos)
GRANT SELECT ON gestion_deportiva.asistencia TO 'estudiante_user'@'localhost';

-- Aplica los cambios de permisos inmediatamente
FLUSH PRIVILEGES;
