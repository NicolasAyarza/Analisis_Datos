"""
Generador de datos sintéticos — Healthcare Analytics & Predictive BI
=====================================================================
Genera ~220.000+ registros distribuidos en 7 tablas relacionadas,
simulando la operación de una clínica chilena.

Incluye correlaciones deliberadas entre variables para que los
modelos de Machine Learning posteriores (inasistencia y duración
de atención) tengan señal real que aprender, no ruido puro.
"""

import numpy as np
import pandas as pd
from faker import Faker
from datetime import date, timedelta
import random

SEED = 42
np.random.seed(SEED)
random.seed(SEED)
fake = Faker("es_CL")
Faker.seed(SEED)

OUT_DIR = "/home/claude/healthcare/data"

# ---------------------------------------------------------------------
# Parámetros de escala
# ---------------------------------------------------------------------
N_PACIENTES = 20_000
N_MEDICOS = 150
N_CITAS = 220_000

FECHA_INICIO = date(2023, 1, 1)
FECHA_FIN = date(2025, 12, 31)
DIAS_RANGO = (FECHA_FIN - FECHA_INICIO).days

COMUNAS_SANTIAGO = [
    "Santiago", "Providencia", "Las Condes", "Ñuñoa", "La Florida",
    "Maipú", "Puente Alto", "San Miguel", "La Reina", "Vitacura",
    "Recoleta", "Independencia", "Macul", "Peñalolén", "La Cisterna",
    "Estación Central", "Quinta Normal", "Cerro Navia", "Renca",
    "Conchalí", "Huechuraba", "Pudahuel", "San Bernardo", "El Bosque",
]

# ---------------------------------------------------------------------
# 1) ESPECIALIDADES
# ---------------------------------------------------------------------
especialidades_list = [
    "Medicina General", "Cardiología", "Pediatría", "Traumatología",
    "Dermatología", "Neurología", "Ginecología", "Oftalmología",
    "Kinesiología", "Otorrinolaringología", "Psiquiatría", "Endocrinología",
]
especialidades = pd.DataFrame({
    "especialidad_id": range(1, len(especialidades_list) + 1),
    "especialidad": especialidades_list,
})

# Pesos de demanda por especialidad (para citas) — Medicina General y
# especialidades más comunes concentran más volumen
esp_pesos = {
    "Medicina General": 0.22, "Pediatría": 0.13, "Traumatología": 0.11,
    "Cardiología": 0.10, "Ginecología": 0.09, "Dermatología": 0.08,
    "Otorrinolaringología": 0.07, "Kinesiología": 0.06, "Neurología": 0.05,
    "Oftalmología": 0.04, "Psiquiatría": 0.03, "Endocrinología": 0.02,
}

# Especialidades con mayor tiempo de espera (para el hallazgo de negocio)
esp_espera_base = {
    "Cardiología": 48, "Traumatología": 45, "Neurología": 40,
    "Endocrinología": 35, "Otorrinolaringología": 30, "Psiquiatría": 30,
    "Ginecología": 28, "Dermatología": 25, "Oftalmología": 24,
    "Kinesiología": 20, "Pediatría": 18, "Medicina General": 15,
}

# ---------------------------------------------------------------------
# 2) SERVICIOS
# ---------------------------------------------------------------------
servicios_data = [
    ("Consulta General", "Consulta", 15000),
    ("Consulta Especialidad", "Consulta", 35000),
    ("Control Niño Sano", "Consulta", 20000),
    ("Consulta Preventiva", "Consulta", 18000),
    ("Ecografía Abdominal", "Imagenología", 45000),
    ("Ecografía Obstétrica", "Imagenología", 50000),
    ("Radiografía", "Imagenología", 25000),
    ("Electrocardiograma", "Procedimiento", 22000),
    ("Ecocardiograma", "Procedimiento", 60000),
    ("Test de Esfuerzo", "Procedimiento", 55000),
    ("Kinesiterapia", "Terapia", 20000),
    ("Sesión de Rehabilitación", "Terapia", 22000),
    ("Toma de Muestra Laboratorio", "Laboratorio", 8000),
    ("Perfil Bioquímico", "Laboratorio", 28000),
    ("Hemograma Completo", "Laboratorio", 12000),
    ("Curación", "Procedimiento", 10000),
    ("Vacunación", "Procedimiento", 9000),
    ("Endoscopía", "Procedimiento", 80000),
    ("Consulta Psiquiátrica", "Consulta", 40000),
    ("Consulta Dermatológica", "Consulta", 32000),
    ("Biopsia de Piel", "Procedimiento", 65000),
    ("Audiometría", "Procedimiento", 18000),
    ("Control Prenatal", "Consulta", 25000),
    ("Consulta Oftalmológica", "Consulta", 30000),
]
servicios = pd.DataFrame({
    "servicio_id": range(1, len(servicios_data) + 1),
    "servicio": [s[0] for s in servicios_data],
    "categoria": [s[1] for s in servicios_data],
    "precio": [s[2] for s in servicios_data],
})

print("Especialidades y servicios generados.")

# ---------------------------------------------------------------------
# 3) MEDICOS
# ---------------------------------------------------------------------
esp_ids_weighted = np.random.choice(
    especialidades["especialidad_id"],
    size=N_MEDICOS,
    p=[esp_pesos[e] for e in especialidades_list],
)

medicos = pd.DataFrame({
    "medico_id": range(1, N_MEDICOS + 1),
    "nombre": ["Dr(a). " + fake.name() for _ in range(N_MEDICOS)],
    "especialidad_id": esp_ids_weighted,
    "fecha_ingreso": [
        fake.date_between(start_date=date(2010, 1, 1), end_date=date(2025, 1, 1))
        for _ in range(N_MEDICOS)
    ],
    "tipo_contrato": np.random.choice(
        ["Planta", "Honorarios", "Part-time"], size=N_MEDICOS, p=[0.5, 0.3, 0.2]
    ),
})
print(f"Médicos generados: {len(medicos)}")

# ---------------------------------------------------------------------
# 4) PACIENTES
# ---------------------------------------------------------------------
def random_birthdate():
    return fake.date_of_birth(minimum_age=0, maximum_age=95)

sexo_arr = np.random.choice(["Femenino", "Masculino"], size=N_PACIENTES, p=[0.52, 0.48])
seguro_arr = np.random.choice(
    ["Fonasa", "Isapre", "Particular"], size=N_PACIENTES, p=[0.62, 0.30, 0.08]
)
comuna_arr = np.random.choice(COMUNAS_SANTIAGO, size=N_PACIENTES)

pacientes = pd.DataFrame({
    "paciente_id": range(1, N_PACIENTES + 1),
    "nombre": [fake.name() for _ in range(N_PACIENTES)],
    "fecha_nacimiento": [random_birthdate() for _ in range(N_PACIENTES)],
    "sexo": sexo_arr,
    "comuna": comuna_arr,
    "tipo_seguro": seguro_arr,
    "fecha_registro": [
        fake.date_between(start_date=FECHA_INICIO, end_date=FECHA_FIN)
        for _ in range(N_PACIENTES)
    ],
})
print(f"Pacientes generados: {len(pacientes)}")

# Historial de inasistencias previas por paciente (para dar señal al modelo)
hist_inasistencia = np.random.choice(
    [0, 1, 2, 3, 4, 5], size=N_PACIENTES, p=[0.45, 0.25, 0.15, 0.08, 0.05, 0.02]
)
pacientes_hist = dict(zip(pacientes["paciente_id"], hist_inasistencia))

# ---------------------------------------------------------------------
# 5) CITAS
# ---------------------------------------------------------------------
print("Generando citas (puede tardar unos segundos)...")

paciente_ids = np.random.choice(pacientes["paciente_id"], size=N_CITAS)

medico_esp_map = medicos.set_index("medico_id")["especialidad_id"].to_dict()
medico_ids_by_esp = {
    eid: medicos.loc[medicos["especialidad_id"] == eid, "medico_id"].values
    for eid in especialidades["especialidad_id"]
}

esp_ids_for_citas = np.random.choice(
    especialidades["especialidad_id"],
    size=N_CITAS,
    p=[esp_pesos[e] for e in especialidades_list],
)
medico_ids_for_citas = np.array([
    np.random.choice(medico_ids_by_esp[eid]) for eid in esp_ids_for_citas
])

servicio_ids_for_citas = np.random.choice(servicios["servicio_id"], size=N_CITAS)

fecha_cita_offsets = np.random.randint(0, DIAS_RANGO, size=N_CITAS)
fechas_cita = [FECHA_INICIO + timedelta(days=int(d)) for d in fecha_cita_offsets]
dias_semana = np.array([f.weekday() for f in fechas_cita])  # 0=Lunes ... 6=Domingo

horas_agendadas = np.random.randint(8, 19, size=N_CITAS)  # 08:00 a 18:00
minutos_agendados = np.random.choice([0, 15, 30, 45], size=N_CITAS)

canal_reserva_arr = np.random.choice(
    ["App", "Web", "Call Center", "Presencial"], size=N_CITAS, p=[0.35, 0.30, 0.20, 0.15]
)

hist_arr = np.array([pacientes_hist[pid] for pid in paciente_ids])

# --- Probabilidad de inasistencia con señal real ---
# Base + efecto historial + efecto canal + efecto día de semana + efecto hora
p_base = 0.08
p_hist = hist_arr * 0.035
p_canal = np.where(canal_reserva_arr == "Call Center", 0.03,
           np.where(canal_reserva_arr == "Presencial", -0.02, 0.0))
p_dia = np.where(np.isin(dias_semana, [0, 4]), 0.02, 0.0)  # lunes/viernes más inasistencia
p_hora_temprana = np.where(horas_agendadas < 9, 0.03, 0.0)

p_no_show = np.clip(p_base + p_hist + p_canal + p_dia + p_hora_temprana, 0.02, 0.55)
es_no_show = np.random.binomial(1, p_no_show)

p_cancelada = 0.07
p_reprogramada = 0.05
rand_estado = np.random.rand(N_CITAS)

estado_arr = np.empty(N_CITAS, dtype=object)
estado_arr[:] = "Atendida"
estado_arr[es_no_show == 1] = "No asistió"
mask_restante = es_no_show == 0
idx_restante = np.where(mask_restante)[0]
sub_rand = np.random.rand(len(idx_restante))
estado_arr[idx_restante[sub_rand < p_cancelada]] = "Cancelada"
estado_arr[idx_restante[(sub_rand >= p_cancelada) & (sub_rand < p_cancelada + p_reprogramada)]] = "Reprogramada"

hora_agendada_str = [f"{h:02d}:{m:02d}:00" for h, m in zip(horas_agendadas, minutos_agendados)]

citas = pd.DataFrame({
    "cita_id": range(1, N_CITAS + 1),
    "paciente_id": paciente_ids,
    "medico_id": medico_ids_for_citas,
    "servicio_id": servicio_ids_for_citas,
    "fecha_cita": fechas_cita,
    "hora_agendada": hora_agendada_str,
    "estado": estado_arr,
    "canal_reserva": canal_reserva_arr,
})

# hora_atencion: solo para Atendida, con variación respecto a la agendada
citas["hora_atencion"] = None
mask_atendida = citas["estado"] == "Atendida"
n_atendida = mask_atendida.sum()

esp_for_atendida = esp_ids_for_citas[mask_atendida.values]
esp_name_for_atendida = especialidades.set_index("especialidad_id")["especialidad"].loc[esp_for_atendida].values
espera_base_arr = np.array([esp_espera_base[e] for e in esp_name_for_atendida])
tiempo_espera_min = np.clip(
    np.random.normal(loc=espera_base_arr, scale=espera_base_arr * 0.4), 2, 180
).astype(int)

def sumar_minutos(hora_str, minutos):
    h, m, s = map(int, hora_str.split(":"))
    total = h * 60 + m + int(minutos)
    total = total % (24 * 60)
    return f"{total // 60:02d}:{total % 60:02d}:00"

horas_agendadas_atendida = citas.loc[mask_atendida, "hora_agendada"].values
horas_atencion_calc = [
    sumar_minutos(h, m) for h, m in zip(horas_agendadas_atendida, tiempo_espera_min)
]
citas.loc[mask_atendida, "hora_atencion"] = horas_atencion_calc

print(f"Citas generadas: {len(citas)}  |  Atendidas: {n_atendida}")
print(citas["estado"].value_counts(normalize=True).round(3))

# ---------------------------------------------------------------------
# 6) ATENCIONES (una por cada cita "Atendida")
# ---------------------------------------------------------------------
print("Generando atenciones...")

citas_atendidas = citas[mask_atendida].reset_index(drop=True)
n_at = len(citas_atendidas)

edad_paciente = pacientes.set_index("paciente_id")["fecha_nacimiento"]
fechas_at = pd.to_datetime(citas_atendidas["fecha_cita"])
nacimientos = pd.to_datetime(edad_paciente.loc[citas_atendidas["paciente_id"]].values)
edad_en_atencion = ((fechas_at.values - nacimientos.values).astype('timedelta64[D]').astype(int) / 365.25)

# Duración de atención: depende de especialidad, edad, y tiene ruido
esp_dur_base = {
    "Cardiología": 35, "Traumatología": 30, "Neurología": 35,
    "Endocrinología": 25, "Otorrinolaringología": 20, "Psiquiatría": 45,
    "Ginecología": 25, "Dermatología": 18, "Oftalmología": 20,
    "Kinesiología": 40, "Pediatría": 20, "Medicina General": 15,
}
esp_ids_at = esp_ids_for_citas[mask_atendida.values]
esp_name_at = especialidades.set_index("especialidad_id")["especialidad"].loc[esp_ids_at].values
dur_base_arr = np.array([esp_dur_base[e] for e in esp_name_at])
efecto_edad = np.where(edad_en_atencion > 65, 8, np.where(edad_en_atencion < 12, 5, 0))
duracion_minutos = np.clip(
    np.random.normal(loc=dur_base_arr + efecto_edad, scale=6), 5, 120
).astype(int)

servicio_ids_at = citas_atendidas["servicio_id"].values
precio_map = servicios.set_index("servicio_id")["precio"].to_dict()
costo_atencion = np.array([precio_map[s] for s in servicio_ids_at]) * np.random.uniform(0.9, 1.15, size=n_at)
costo_atencion = np.round(costo_atencion, -2)

tiempo_espera_at = tiempo_espera_min  # calculado arriba, mismo orden que citas_atendidas

# Satisfacción correlacionada negativamente con tiempo de espera
satisf_base = 5 - (tiempo_espera_at / 60)
satisfaccion = np.clip(np.round(satisf_base + np.random.normal(0, 0.6, n_at)), 1, 5).astype(int)

atenciones = pd.DataFrame({
    "atencion_id": range(1, n_at + 1),
    "cita_id": citas_atendidas["cita_id"].values,
    "fecha_atencion": citas_atendidas["fecha_cita"].values,
    "duracion_minutos": duracion_minutos,
    "tiempo_espera": tiempo_espera_at,
    "costo_atencion": costo_atencion.astype(int),
    "satisfaccion": satisfaccion,
})
print(f"Atenciones generadas: {len(atenciones)}")

# ---------------------------------------------------------------------
# 7) DIAGNOSTICOS
# ---------------------------------------------------------------------
print("Generando diagnósticos...")

cie10_por_especialidad = {
    "Medicina General": [("J00", "Rinofaringitis aguda", "Leve"), ("R51", "Cefalea", "Leve"), ("K59.1", "Diarrea funcional", "Leve")],
    "Cardiología": [("I10", "Hipertensión esencial", "Moderada"), ("I25.9", "Enfermedad isquémica crónica", "Grave"), ("I48", "Fibrilación auricular", "Grave")],
    "Pediatría": [("J06.9", "Infección respiratoria aguda", "Leve"), ("R50.9", "Fiebre no especificada", "Leve"), ("P59.9", "Ictericia neonatal", "Moderada")],
    "Traumatología": [("S93.4", "Esguince de tobillo", "Moderada"), ("M54.5", "Lumbago", "Leve"), ("S52.5", "Fractura de radio distal", "Grave")],
    "Dermatología": [("L20", "Dermatitis atópica", "Leve"), ("L70", "Acné", "Leve"), ("C44", "Carcinoma de piel", "Grave")],
    "Neurología": [("G43", "Migraña", "Moderada"), ("G40", "Epilepsia", "Grave"), ("G45", "Isquemia cerebral transitoria", "Grave")],
    "Ginecología": [("N76", "Vaginitis aguda", "Leve"), ("N92", "Menstruación excesiva", "Moderada"), ("O26.9", "Complicación del embarazo", "Moderada")],
    "Oftalmología": [("H52.1", "Miopía", "Leve"), ("H25", "Catarata senil", "Moderada"), ("H40", "Glaucoma", "Grave")],
    "Kinesiología": [("M25.5", "Dolor articular", "Leve"), ("M62.8", "Trastorno muscular", "Leve"), ("S83.5", "Esguince de rodilla", "Moderada")],
    "Otorrinolaringología": [("H66.9", "Otitis media", "Leve"), ("J32", "Sinusitis crónica", "Moderada"), ("H81", "Vértigo", "Moderada")],
    "Psiquiatría": [("F32", "Episodio depresivo", "Moderada"), ("F41.1", "Trastorno de ansiedad", "Moderada"), ("F31", "Trastorno bipolar", "Grave")],
    "Endocrinología": [("E11", "Diabetes tipo 2", "Grave"), ("E03", "Hipotiroidismo", "Moderada"), ("E66", "Obesidad", "Moderada")],
}

diag_options_per_row = [cie10_por_especialidad[e] for e in esp_name_at]
diag_choice_idx = [random.randrange(len(opts)) for opts in diag_options_per_row]
diag_chosen = [opts[i] for opts, i in zip(diag_options_per_row, diag_choice_idx)]

diagnosticos = pd.DataFrame({
    "diagnostico_id": range(1, n_at + 1),
    "atencion_id": atenciones["atencion_id"].values,
    "codigo_cie10": [d[0] for d in diag_chosen],
    "diagnostico": [d[1] for d in diag_chosen],
    "gravedad": [d[2] for d in diag_chosen],
})
print(f"Diagnósticos generados: {len(diagnosticos)}")

# ---------------------------------------------------------------------
# GUARDAR CSVs
# ---------------------------------------------------------------------
especialidades.to_csv(f"{OUT_DIR}/especialidades.csv", index=False)
servicios.to_csv(f"{OUT_DIR}/servicios.csv", index=False)
medicos.to_csv(f"{OUT_DIR}/medicos.csv", index=False)
pacientes.to_csv(f"{OUT_DIR}/pacientes.csv", index=False)
citas.to_csv(f"{OUT_DIR}/citas.csv", index=False)
atenciones.to_csv(f"{OUT_DIR}/atenciones.csv", index=False)
diagnosticos.to_csv(f"{OUT_DIR}/diagnosticos.csv", index=False)

total = sum(len(df) for df in [especialidades, servicios, medicos, pacientes, citas, atenciones, diagnosticos])
print("\n=== RESUMEN FINAL ===")
print(f"especialidades : {len(especialidades):>8,}")
print(f"servicios      : {len(servicios):>8,}")
print(f"medicos        : {len(medicos):>8,}")
print(f"pacientes      : {len(pacientes):>8,}")
print(f"citas          : {len(citas):>8,}")
print(f"atenciones     : {len(atenciones):>8,}")
print(f"diagnosticos   : {len(diagnosticos):>8,}")
print(f"TOTAL          : {total:>8,}")
