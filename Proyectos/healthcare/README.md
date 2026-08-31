# Healthcare Analytics & Predictive BI — Base de Datos

Base de datos sintética de una clínica chilena, con **577.246 registros**
distribuidos en 7 tablas relacionadas. Generada con Python (Faker + NumPy,
semilla fija) — sin datos personales ni médicos reales.

## Contenido de esta entrega

```
healthcare/
├── data/                  # 7 CSV con los datos generados
│   ├── especialidades.csv
│   ├── servicios.csv
│   ├── medicos.csv
│   ├── pacientes.csv
│   ├── citas.csv
│   ├── atenciones.csv
│   └── diagnosticos.csv
├── database/
│   ├── schema.sql         # DDL completo para PostgreSQL
│   └── load_data.py       # Carga los CSV a PostgreSQL vía SQLAlchemy
├── docs/
│   └── diccionario_datos.md
├── generate_data.py       # Script que generó todos los datos (reproducible)
└── requirements.txt
```

## Cómo levantar la base de datos en PostgreSQL

1. **Instalar PostgreSQL** (si aún no lo tienes) y crear la base:
   ```bash
   createdb healthcare_analytics
   ```

2. **Crear las tablas** ejecutando el schema:
   ```bash
   psql -d healthcare_analytics -f database/schema.sql
   ```

3. **Instalar dependencias de Python**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Cargar los datos**: edita `database/load_data.py` con tu usuario/contraseña
   de PostgreSQL y ejecútalo:
   ```bash
   cd database
   python3 load_data.py
   ```

5. Verifica en `psql`:
   ```sql
   SELECT COUNT(*) FROM citas;        -- 220,000
   SELECT COUNT(*) FROM atenciones;   -- 168,530
   ```

## Regenerar los datos desde cero

Si quieres cambiar volúmenes, distribuciones o agregar variables, edita y
vuelve a correr `generate_data.py` (usa semilla fija = 42, así que los
resultados son reproducibles).

## Siguientes pasos del proyecto

Con la base ya cargada en PostgreSQL, el flujo natural es:
1. **SQL** (`database/queries.sql` — por construir): demanda por especialidad,
   tasa de inasistencia, tiempos de espera, CTEs y window functions.
2. **Python/EDA/Estadística**: conectar a PostgreSQL con SQLAlchemy o
   trabajar directamente sobre los CSV.
3. **Machine Learning**: modelo de inasistencia (clasificación) y modelo de
   duración de atención (regresión).
4. **Power BI**: modelo dimensional conectado directamente a PostgreSQL.
