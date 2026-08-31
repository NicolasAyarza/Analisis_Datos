# Diccionario de Datos — Healthcare Analytics & Predictive BI

Base de datos sintética de una clínica chilena. Todos los datos son
generados artificialmente (Faker + NumPy, semilla fija = 42) — no
corresponden a personas ni información médica real.

## Resumen de volumen

| Tabla | Registros |
|---|---|
| especialidades | 12 |
| servicios | 24 |
| medicos | 150 |
| pacientes | 20,000 |
| citas | 220,000 |
| atenciones | 168,530 |
| diagnosticos | 168,530 |
| **Total** | **577,246** |

## especialidades
| Campo | Tipo | Descripción |
|---|---|---|
| especialidad_id | INT (PK) | Identificador único |
| especialidad | VARCHAR | Nombre de la especialidad médica |

## servicios
| Campo | Tipo | Descripción |
|---|---|---|
| servicio_id | INT (PK) | Identificador único |
| servicio | VARCHAR | Nombre del servicio/prestación |
| categoria | VARCHAR | Consulta, Imagenología, Procedimiento, Terapia, Laboratorio |
| precio | DECIMAL | Precio base en CLP |

## medicos
| Campo | Tipo | Descripción |
|---|---|---|
| medico_id | INT (PK) | Identificador único |
| nombre | VARCHAR | Nombre del médico (sintético) |
| especialidad_id | INT (FK) | Referencia a especialidades |
| fecha_ingreso | DATE | Fecha de contratación |
| tipo_contrato | VARCHAR | Planta, Honorarios, Part-time |

## pacientes
| Campo | Tipo | Descripción |
|---|---|---|
| paciente_id | INT (PK) | Identificador único |
| nombre | VARCHAR | Nombre del paciente (sintético) |
| fecha_nacimiento | DATE | Fecha de nacimiento |
| sexo | VARCHAR | Femenino, Masculino |
| comuna | VARCHAR | Comuna de residencia (Región Metropolitana) |
| tipo_seguro | VARCHAR | Fonasa, Isapre, Particular |
| fecha_registro | DATE | Fecha de ingreso a la base de la clínica |

## citas
| Campo | Tipo | Descripción |
|---|---|---|
| cita_id | INT (PK) | Identificador único |
| paciente_id | INT (FK) | Referencia a pacientes |
| medico_id | INT (FK) | Referencia a medicos |
| servicio_id | INT (FK) | Referencia a servicios |
| fecha_cita | DATE | Fecha agendada |
| hora_agendada | TIME | Hora agendada |
| hora_atencion | TIME | Hora real de atención (solo si estado = Atendida) |
| estado | VARCHAR | Atendida, Cancelada, No asistió, Reprogramada |
| canal_reserva | VARCHAR | App, Web, Call Center, Presencial |

## atenciones
| Campo | Tipo | Descripción |
|---|---|---|
| atencion_id | INT (PK) | Identificador único |
| cita_id | INT (FK, único) | Referencia a citas (1:1) |
| fecha_atencion | DATE | Fecha de la atención |
| duracion_minutos | INT | Duración real de la atención |
| tiempo_espera | INT | Minutos de espera entre hora agendada y atención |
| costo_atencion | DECIMAL | Costo final cobrado (CLP) |
| satisfaccion | INT | Escala 1–5 |

## diagnosticos
| Campo | Tipo | Descripción |
|---|---|---|
| diagnostico_id | INT (PK) | Identificador único |
| atencion_id | INT (FK) | Referencia a atenciones |
| codigo_cie10 | VARCHAR | Código CIE-10 |
| diagnostico | VARCHAR | Descripción del diagnóstico |
| gravedad | VARCHAR | Leve, Moderada, Grave |

## Correlaciones incluidas deliberadamente (para EDA/ML)
- **Tiempo de espera por especialidad**: Cardiología y Traumatología tienen
  la mayor espera promedio; Medicina General la menor.
- **Inasistencia**: aumenta con el historial previo de inasistencias del
  paciente, con reservas por Call Center, y con citas los lunes/viernes o
  muy temprano en la mañana.
- **Duración de atención**: varía según especialidad y aumenta en pacientes
  mayores de 65 años y menores de 12 años.
- **Satisfacción**: correlacionada negativamente con el tiempo de espera.
