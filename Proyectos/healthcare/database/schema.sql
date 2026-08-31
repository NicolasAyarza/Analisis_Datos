-- =====================================================================
-- Healthcare Analytics & Predictive BI — Schema PostgreSQL
-- Base de datos sintética de una clínica chilena
-- =====================================================================

DROP TABLE IF EXISTS diagnosticos CASCADE;
DROP TABLE IF EXISTS atenciones CASCADE;
DROP TABLE IF EXISTS citas CASCADE;
DROP TABLE IF EXISTS servicios CASCADE;
DROP TABLE IF EXISTS medicos CASCADE;
DROP TABLE IF EXISTS especialidades CASCADE;
DROP TABLE IF EXISTS pacientes CASCADE;

-- =====================================================================
-- Tabla: especialidades
-- =====================================================================
CREATE TABLE especialidades (
    especialidad_id     SERIAL PRIMARY KEY,
    especialidad        VARCHAR(60) NOT NULL UNIQUE
);

-- =====================================================================
-- Tabla: medicos
-- =====================================================================
CREATE TABLE medicos (
    medico_id           SERIAL PRIMARY KEY,
    nombre              VARCHAR(120) NOT NULL,
    especialidad_id     INT NOT NULL REFERENCES especialidades(especialidad_id),
    fecha_ingreso        DATE NOT NULL,
    tipo_contrato        VARCHAR(30) NOT NULL CHECK (tipo_contrato IN ('Planta', 'Honorarios', 'Part-time'))
);

-- =====================================================================
-- Tabla: pacientes
-- =====================================================================
CREATE TABLE pacientes (
    paciente_id          SERIAL PRIMARY KEY,
    nombre               VARCHAR(120) NOT NULL,
    fecha_nacimiento     DATE NOT NULL,
    sexo                 VARCHAR(15) NOT NULL CHECK (sexo IN ('Femenino', 'Masculino')),
    comuna               VARCHAR(60) NOT NULL,
    tipo_seguro          VARCHAR(30) NOT NULL CHECK (tipo_seguro IN ('Fonasa', 'Isapre', 'Particular')),
    fecha_registro       DATE NOT NULL
);

-- =====================================================================
-- Tabla: servicios
-- =====================================================================
CREATE TABLE servicios (
    servicio_id          SERIAL PRIMARY KEY,
    servicio             VARCHAR(100) NOT NULL,
    categoria            VARCHAR(50) NOT NULL,
    precio               DECIMAL(10,0) NOT NULL
);

-- =====================================================================
-- Tabla: citas
-- =====================================================================
CREATE TABLE citas (
    cita_id              SERIAL PRIMARY KEY,
    paciente_id          INT NOT NULL REFERENCES pacientes(paciente_id),
    medico_id            INT NOT NULL REFERENCES medicos(medico_id),
    servicio_id          INT NOT NULL REFERENCES servicios(servicio_id),
    fecha_cita           DATE NOT NULL,
    hora_agendada        TIME NOT NULL,
    hora_atencion        TIME,
    estado               VARCHAR(20) NOT NULL CHECK (estado IN ('Atendida', 'Cancelada', 'No asistió', 'Reprogramada')),
    canal_reserva        VARCHAR(30) NOT NULL CHECK (canal_reserva IN ('App', 'Web', 'Call Center', 'Presencial'))
);

CREATE INDEX idx_citas_paciente ON citas(paciente_id);
CREATE INDEX idx_citas_medico ON citas(medico_id);
CREATE INDEX idx_citas_fecha ON citas(fecha_cita);
CREATE INDEX idx_citas_estado ON citas(estado);

-- =====================================================================
-- Tabla: atenciones
-- =====================================================================
CREATE TABLE atenciones (
    atencion_id          SERIAL PRIMARY KEY,
    cita_id              INT NOT NULL UNIQUE REFERENCES citas(cita_id),
    fecha_atencion       DATE NOT NULL,
    duracion_minutos     INT NOT NULL,
    tiempo_espera        INT NOT NULL,
    costo_atencion       DECIMAL(10,0) NOT NULL,
    satisfaccion         INT NOT NULL CHECK (satisfaccion BETWEEN 1 AND 5)
);

CREATE INDEX idx_atenciones_cita ON atenciones(cita_id);

-- =====================================================================
-- Tabla: diagnosticos
-- =====================================================================
CREATE TABLE diagnosticos (
    diagnostico_id       SERIAL PRIMARY KEY,
    atencion_id          INT NOT NULL REFERENCES atenciones(atencion_id),
    codigo_cie10          VARCHAR(10) NOT NULL,
    diagnostico          VARCHAR(150) NOT NULL,
    gravedad             VARCHAR(20) NOT NULL CHECK (gravedad IN ('Leve', 'Moderada', 'Grave'))
);

CREATE INDEX idx_diagnosticos_atencion ON diagnosticos(atencion_id);
