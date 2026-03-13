# Proyecto ETL y Dashboard de Ventas

Este proyecto demuestra un flujo completo de **Extracción, Transformación y Carga (ETL)** de datos de ventas y clientes, culminando en un **Dashboard interactivo** desarrollado en Streamlit.

## 🚀 Descripción del Proyecto

El sistema procesa información de dos fuentes primarias (`ventas.csv` y `clientes.json`), realiza una limpieza exhaustiva, calcula métricas de negocio, integra datos externos de una API y almacena los resultados en formatos estructurados (CSV y SQLite) para su análisis.

## 📋 Requisitos Previos

Asegúrate de tener instalado Python 3.8 o superior. Las dependencias necesarias son:

*   Pandas
*   Streamlit
*   Requests
*   Sqlite3 (incluido en Python)

Puedes instalarlas con el siguiente comando:
```bash
pip install pandas streamlit requests
```

## 📂 Estructura del Proyecto

```text
Solucion/
├── data/
│   ├── raw/                # Archivos de origen (ventas.csv, clientes.json)
│   ├── processed/          # Datos procesados (ventas_enriquecidas.csv)
│   └── ventas.db           # Base de datos SQLite generada
├── etl.py                  # Script del Pipeline ETL
├── app.py                  # Script del Dashboard (Streamlit)
└── README.md               # Este archivo
```

## 🛠️ Instrucciones de Ejecución Paso a Paso

### 1. Preparación de Datos
Verifica que los archivos `ventas.csv` y `clientes.json` se encuentren en la carpeta `data/raw/`.

### 2. Ejecutar el Pipeline ETL
Primero, debes procesar los datos ejecutando el script de ETL. Este paso limpiará los datos, realizará los cálculos y generará la base de datos.

```bash
python etl.py
```
**¿Qué sucede en este paso?**
*   Se cargan las ventas y se validan tipos numéricos.
*   Se filtran registros por el año 2023 y cantidades > 0.
*   Se calculan las columnas `total` y `margen`.
*   Se unen los datos de ventas con los de clientes.
*   Se consultan datos adicionales de una API REST.
*   Se genera un **Hash MD5** de versión del dataset.
*   Se guardan los resultados en `data/processed/ventas_enriquecidas.csv` y `data/ventas.db`.

### 3. Ejecutar el Dashboard
Una vez procesados los datos, puedes lanzar la interfaz gráfica:

```bash
streamlit run app.py
```

### 4. Explorar los Resultados
*   **Filtros**: Usa la barra lateral para filtrar por producto, región o rango de fechas.
*   **Métricas**: Observa el rendimiento total de ventas y márgenes en tiempo real.
*   **Versión**: Verifica el hash del dataset para asegurar que estás trabajando con la versión correcta.

## ⚙️ Tecnologías Utilizadas

*   **Python**: Lenguaje principal.
*   **Pandas**: Procesamiento y manipulación de datos.
*   **SQLite**: Almacenamiento persistente de datos procesados.
*   **Streamlit**: Visualización y creación del dashboard.
*   **Hashlib**: Generación de huellas digitales (Hash MD5) del dataset.

---
*Este proyecto fue desarrollado como parte del Taller de Bases de Datos Avanzada.*
