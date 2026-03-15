# Proyecto ETL y Dashboard de Ventas

Este proyecto demuestra un flujo completo de **Extracción, Transformación y Carga (ETL)** de datos de ventas y clientes, culminando en un **Dashboard interactivo** desarrollado en Streamlit.

## 🚀 Descripción del Proyecto

El sistema procesa información de dos fuentes primarias (`ventas.csv` y `clientes.json`), realiza una limpieza exhaustiva, calcula métricas de negocio, integra datos externos de una API y almacena los resultados en formatos estructurados (CSV y SQLite) para su análisis.

## 📋 Requisitos Previos

Asegurarse de tener instalado Python 3.8 o superior, pero la recomendacion especial es crear un entorno virtual de python para este proyecto asi no generar problemas con nuevas librerias o dependencias propias de python que pueden dañar elementos propios del sistema operativo

Crear entorno virtual: python3 -m venv .venv
Cargar entorno virtual: .venv\Scripts\activate
Verificar que este operativo el entorno virtual evidenciando el prefijo (.venv) en la linea de comandos


Caegas todas los paquetes, librerias o dependencias necesarias con el comando: 
```bash
pip install -r src/requirements.txt
```

## 📂 Estructura del Proyecto

```text
Solucion/
├── data/
│   ├── raw/                # Archivos de origen (ventas.csv, clientes.json)
│   ├── processed/          # Datos procesados (ventas_enriquecidas.csv)
│   └── ventas.db           # Base de datos SQLite generada
├── src/                    # Código fuente
│   ├── etl.py              # Script del Pipeline ETL
│   ├── app.py              # Script del Dashboard (Streamlit)
│   └── requirements.txt    # Dependencias del proyecto
└── README.md               # Este archivo
```

## 🛠️ Instrucciones de Ejecución Paso a Paso

### 1. Preparación de Datos
Verifica que los archivos `ventas.csv` y `clientes.json` se encuentren en la carpeta `data/raw/`.

### 2. Ejecutar el Pipeline ETL
Primero, debes procesar los datos ejecutando el script de ETL desde la raíz del proyecto. resuelve los puntos desde el 1 hasta el 13

```bash
python src/etl.py
```
**¿Qué sucede en este paso?**
*   **Limpieza Inteligente**: El script elimina duplicados y registros con cantidad cero usando: `df_ventas = df_ventas[df_ventas['cantidad'] > 0].drop_duplicates()`.
*   **Selección Robusta**: Solo se cargan las columnas necesarias, lo que ahorra memoria RAM.
*   **Cálculo de Negocio**: Se generan las columnas `total` y `margen`.
*   **Versión del Dataset**: Se genera un **Hash MD5** único para asegurar la integridad de los datos.

### 3. Ejecutar el Dashboard
Una vez procesados los datos, lanza la interfaz gráfica desde la raíz del proyecto; resuleve el punto 14:

```bash
streamlit run src/app.py
```
---

## 🖥️ Explicación del Dashboard (`app.py`)

El archivo `app.py` crea una aplicación web interactiva que permite explorar los resultados del ETL de forma visual.

### ¿Cómo funciona?
1.  **Carga con Caché (`@st.cache_data`)**: Lee el archivo procesado una sola vez y lo mantiene en memoria para que el dashboard sea instantáneo al usar filtros.
2.  **Barra Lateral de Filtros**: Permite segmentar los datos por **Producto**, **Región** y **Rango de Fechas**. Estos filtros actualizan todos los gráficos y métricas automáticamente.
3.  **Métricas en Tiempo Real**: Muestra el total facturado y el margen de ganancia calculado durante el ETL.
4.  **Validación**: Muestra el Hash MD5 del dataset en la parte inferior para garantizar que estás viendo la versión de datos más reciente.
5. Esta aplicacion se visualiza desde un navegador con la url http://localhost:8501

### Lógica de Selección de Columnas
En ambos scripts (`etl.py` y `app.py`), se utiliza una técnica de selección segura:
`df = df[[c for c in columnas if c in df.columns]]`
Esto permite que el código sea **robusto**: si una columna opcional falta en el origen, el programa no se detiene con un error, sino que simplemente ignora esa columna y continúa procesando las demás.

---

## ⚙️ Tecnologías Utilizadas

*   **Python & Pandas**: Extracción y transformación de datos.
*   **SQLite**: Almacenamiento persistente SQL.
*   **Streamlit**: Interfaz de usuario y dashboard web.
*   **Hashlib**: Control de versiones de datos mediante MD5.

---
*Este proyecto fue desarrollado como parte del Taller de Bases de Datos Avanzada.*

Evaluacion
1.	¿Qué significan las siglas ETL?
ETL significa Extract, Transform, Load.
•	Extract: se extraen datos desde diferentes fuentes (bases de datos, APIs, archivos).
•	Transform: se limpian, validan y transforman los datos (cambios de formato, filtros, joins).
•	Load: se cargan los datos procesados en el sistema destino (data warehouse, base de datos, archivos).
2.	Diferencia entre ETL y ELT
•	ETL: los datos se transforman antes de cargarse en el sistema destino.
•	ELT: los datos se cargan primero y luego se transforman dentro del sistema destino.
ELT se usa más en entornos:
•	Cloud
•	Big Data
•	Data Warehouses modernos (ej. Snowflake, BigQuery)
porque tienen gran capacidad de procesamiento.
3.	Tipos de fuentes de datos
Tipo	Ejemplo
Estructurado	Base de datos SQL (tabla de clientes)
Semi-estructurado	Archivo JSON o XML
No estructurado	Imágenes, audio o documentos PDF

4.	¿Por qué usar index=False en to_csv()?
Porque evita que Pandas guarde el índice del DataFrame como una columna adicional en el archivo CSV.
Si no se usa, el CSV tendrá una columna extra innecesaria con los números de fila.
5.	Diferencia entre inner join y left join
Inner Join
•	Solo mantiene las filas que tienen coincidencia en ambas tablas.
•	Se usa cuando quiero solo registros que existen en ambas fuentes.
Left Join
•	Mantiene todas las filas de la tabla izquierda.
•	Si no hay coincidencia, se rellenan valores con NaN.
•	Se usa cuando quiero conservar todos los registros principales y agregar información si existe.

6.	¿Para qué sirve calcular un hash (MD5) en ETL?
Sirve para identificar cambios en los datos.
Usos comunes:
•	Detectar duplicados en datasets.
•	Verificar integridad de los datos.
•	Detectar registros modificados entre cargas.
•	Validar que un dataset no cambió después del procesamiento.

7.	¿Qué es data staging y por qué separar raw y processed?
Data staging es un área temporal donde los datos se almacenan antes de ser transformados.
Separar carpetas:
•	raw: contiene datos originales sin modificar.
•	processed: contiene datos ya transformados y listos para análisis.
Esto permite:
•	mantener trazabilidad
•	reproducir el proceso ETL
•	evitar perder datos originales.
8.	¿Qué hace response.raise_for_status()?
Lanza una excepción si la respuesta HTTP de la API indica un error (códigos 4xx o 5xx).
Es importante porque:
•	Detecta errores de conexión o del servidor
•	Evita procesar datos inválidos
•	Permite manejar errores en el pipeline ETL.
9.	¿Qué hace df[df["a"] > 0]?
Es una operación de filtrado usando indexación booleana.
Resultado:
•	devuelve un DataFrame
•	contiene solo las filas donde la columna "a" es mayor que 0
•	mantiene las mismas columnas ["a","b","c"].

10.	Valor de how en merge
df1.merge(df2, on="id", how="left")
El valor es:
left
Este tipo de join se llama:
LEFT JOIN
y mantiene todas las filas de df1, agregando datos de df2 cuando existe coincidencia y colocando NaN cuando no la hay.
