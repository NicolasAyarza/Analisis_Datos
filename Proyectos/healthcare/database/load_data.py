"""
Carga los CSV generados en /data hacia PostgreSQL, respetando el
orden de dependencias de llaves foráneas.

Uso:
    1. Crear la base de datos:  createdb healthcare_analytics
    2. Definir la variable de entorno DATABASE_URL con tus credenciales:
         export DATABASE_URL="postgresql://postgres:TU_PASSWORD@localhost:5432/healthcare_analytics"
    3. Ejecutar:  python3 load_data.py

Nota: la conexión se lee desde la variable de entorno DATABASE_URL para
evitar dejar contraseñas escritas en el código (importante antes de subir
el proyecto a GitHub).
"""

import os
import sys
import pandas as pd
from sqlalchemy import create_engine

DB_URL = os.environ.get("DATABASE_URL")
if not DB_URL:
    sys.exit(
        "ERROR: falta la variable de entorno DATABASE_URL.\n"
        'Ejecuta antes: export DATABASE_URL="postgresql://postgres:TU_PASSWORD@localhost:5432/healthcare_analytics"'
    )

DATA_DIR = "../data"

# Orden importante: tablas padre antes que tablas hijas (FKs)
TABLES_IN_ORDER = [
    "especialidades",
    "servicios",
    "medicos",
    "pacientes",
    "citas",
    "atenciones",
    "diagnosticos",
]

def main():
    engine = create_engine(DB_URL)
    with engine.begin() as conn:
        for table in TABLES_IN_ORDER:
            path = f"{DATA_DIR}/{table}.csv"
            print(f"Cargando {table} desde {path} ...")
            df = pd.read_csv(path)
            df.to_sql(table, conn, if_exists="append", index=False, chunksize=5000, method="multi")
            print(f"  -> {len(df):,} filas cargadas en '{table}'")
    print("\nCarga completa.")

if __name__ == "__main__":
    main()
