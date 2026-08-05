
# 🐍 30 Días de Preparación — Data Analyst Junior

Bitácora pública de mi plan de estudio de 30 días para prepararme como analista de datos junior. 
Documento aquí el progreso diario: teoría, práctica y entregables.

## Objetivo del plan

Consolidar bases de Python, análisis de datos con NumPy/Pandas, SQL, visualización (Excel/Power BI) 
y construir un portafolio de proyectos en GitHub que respalde mi búsqueda de un primer rol como 
analista de datos junior.

---

**Por su tamaño, los datasets no están incluidos en este repositorio.**

## 📅 Progreso diario

### Día 1 — Configuración y repaso de Python
**Objetivo:** Dejar el entorno listo y repasar bases del lenguaje.

- **Teoría:** Instalación y verificación de Python, VS Code y Jupyter. Creación de entorno virtual. Cuenta y repositorio inicial en GitHub.
- **Práctica:** Repaso de variables, tipos de datos, estructuras de control (`if`/`for`/`while`) y funciones, con ejercicios cortos.
- **Repaso:** Documentación del objetivo del plan de 30 días en este README.
- **Recurso:** [Curso COMPLETO de Python DESDE CERO para Principiantes 2025](https://github.com/midudev/curso-python)(https://www.youtube.com/watch?v=TkN2i-_4N4g&pp=ygUGcHl0aG9u) (YouTube, gratuito)
- **Entregable:** ✅ Repositorio de GitHub creado con README inicial.

### Día 2 — NumPy: arrays y operaciones vectorizadas
**Objetivo:** Manejar arrays de NumPy como base de todo análisis numérico.

- **Teoría:** Creación de arrays, indexing, slicing y broadcasting.
- **Práctica:** Operaciones vectorizadas, funciones estadísticas (`mean`, `std`, `sum`) y comparación de rendimiento vs. listas de Python.
- **Repaso:** 10 ejercicios cortos de manipulación de arrays (Kaggle/Exercism).
- **Recurso:** [NumPy Quickstart](https://numpy.org/doc/stable/user/quickstart.html) (docs oficiales) + Kaggle "Intro to Programming"
- **Entregable:** ✅ Notebook [`01_numpy_basics.ipynb`](./01_numpy_basics.ipynb) subido a GitHub.

### Día 3 — Pandas: Series y DataFrame
**Objetivo:** Cargar y explorar datos tabulares con Pandas.

- **Teoría:** Series vs DataFrame, lectura de CSV/Excel, exploración con `head()`, `info()`, `describe()`.
- **Práctica:** Selección e indexado (`loc`, `iloc`), filtros booleanos, ordenamiento.
- **Repaso:** Práctica con un dataset público explorando su estructura.
- **Recurso:** [Kaggle Learn – "Pandas"](https://www.kaggle.com/learn/pandas) (curso gratis, ~4h)
- **Entregable:** ✅ Notebook [`02_pandas_intro.ipynb`](./02_pandas_intro.ipynb) subido a GitHub.

### Día 4 — Limpieza de datos con Pandas
**Objetivo:** Dejar un dataset listo para análisis.

- **Teoría:** Valores nulos (`isnull`, `fillna`, `dropna`), duplicados, corrección de tipos de datos.
- **Práctica:** Normalización de texto, manejo de outliers, creación de columnas derivadas.
- **Repaso:** Limpieza completa aplicada a un dataset con errores reales (NFL Play by Play 2009-2016).
- **Recurso:** [Kaggle Learn – "Data Cleaning"](https://www.kaggle.com/learn/data-cleaning) (curso gratis)
- **Entregable:** ✅ Notebook [`03_data_cleaning.ipynb`](./03_data_cleaning.ipynb) con dataset limpio exportado a CSV.

## 📦 Datasets utilizados en 03_data_cleaning.ipynb

**NFL Play by Play 2009-2016 (v3):**
1. Descarga desde Kaggle: https://www.kaggle.com/datasets/maxhorowitz/nflplaybyplay2009to2016
2. Colócalo en `data/data_cleaning/NFL Play by Play 2009-2016 (v3).csv`

**Landslides catalog (catalog.csv):**
1. Descarga desde el notebook de Kaggle: https://www.kaggle.com/code/alexisbcook/parsing-dates/data
2. Colócalo en `data/data_cleaning/catalog.csv`

**Kickstarter Projects (ks-projects-201612.csv):**
1. Descarga desde el notebook de Kaggle: https://www.kaggle.com/code/alexisbcook/character-encodings/data
2. Colócalo en `data/data_cleaning/ks-projects-201612.csv`

**Pakistan Intellectual Capital (pakistan_intellectual_capital.csv):**
1. Descarga desde el notebook de Kaggle: https://www.kaggle.com/code/alexisbcook/inconsistent-data-entry/data
2. Colócalo en `data/data_cleaning/pakistan_intellectual_capital.csv`

**Dataset limpio:**
Se genera automáticamente al ejecutar `03_data_cleaning.ipynb` de principio a fin — 
no requiere descarga aparte. El notebook lo guarda en `data/nfl_play_by_play_clean.csv`.

### Día 5 — Transformación: groupby, pivot, merge
**Objetivo:** Combinar y resumir datos como en un caso de negocio real.

- **Teoría:** `groupby()` con agregaciones múltiples, `pivot_table()`.
- **Práctica:** `merge()`/`join()` de múltiples tablas (simular relación tipo base de datos).
- **Repaso:** Respuesta a 5 preguntas de negocio sobre un dataset (ej. "¿qué categoría vende más por región?").
- **Recurso:** [Real Python – "Pandas GroupBy"](https://realpython.com/pandas-groupby/) (artículo gratis)
- **Entregable:** ✅ Notebook [`04_groupby_merge.ipynb`](./04_groupby_merge.ipynb) con 5 respuestas documentadas.

## 📦 Datasets utilizados en 04_groupby_merge.ipynb

**Datasets del tutorial "Pandas GroupBy" (Real Python):**
1. Se descargan directamente desde el artículo: https://realpython.com/pandas-groupby/
2. Colócalos en `data/data_groupby/`