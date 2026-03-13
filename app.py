import streamlit as st
import pandas as pd
import os

# Configuración de la página
st.set_page_config(page_title="Dashboard de Ventas Enriquecidas", layout="wide")

# Título y descripción personalizados
st.title("🚀 Dashboard de Ventas y Clientes")
st.markdown("""
Esta aplicación permite visualizar los datos de ventas enriquecidos con información de clientes y datos simulados de una API REST.
El pipeline ETL procesa los archivos `ventas.csv` y `clientes.json`.
""")

# Función para cargar los datos procesados
@st.cache_data
def cargar_datos():
    ruta_archivo = r"d:\Maestria\Bases de datos Avanzada\Taller1\Solucion\data\processed\ventas_enriquecidas.csv"
    ruta_hash = r"d:\Maestria\Bases de datos Avanzada\Taller1\Solucion\data\processed\dataset_hash.txt"
    
    if os.path.exists(ruta_archivo):
        df = pd.read_csv(ruta_archivo)
        df['fecha'] = pd.to_datetime(df['fecha'])
        
        # Cargar el hash del dataset
        hash_dataset = "Desconocido"
        if os.path.exists(ruta_hash):
            with open(ruta_hash, 'r') as f:
                hash_dataset = f.read().strip()
                
        return df, hash_dataset
    else:
        return None, None

df, hash_dataset = cargar_datos()

if df is not None:
    # Barra lateral para filtros
    st.sidebar.header("🔍 Filtros")
    
    # Filtro por Producto
    productos = sorted(df['producto'].unique().tolist())
    producto_seleccionado = st.sidebar.multiselect("Seleccionar Producto", options=productos, default=[])
    
    # Filtro por Región
    regiones = sorted(df['region'].unique().tolist())
    region_seleccionada = st.sidebar.multiselect("Seleccionar Región", options=regiones, default=[])

    # Filtro por Rango de Fechas
    fecha_min = df['fecha'].min().date()
    fecha_max = df['fecha'].max().date()
    rango_fechas = st.sidebar.date_input("Rango de Fechas", [fecha_min, fecha_max])

    # Aplicar filtros al DataFrame
    df_filtrado = df.copy()
    if producto_seleccionado:
        df_filtrado = df_filtrado[df_filtrado['producto'].isin(producto_seleccionado)]
    if region_seleccionada:
        df_filtrado = df_filtrado[df_filtrado['region'].isin(region_seleccionada)]
    if len(rango_fechas) == 2:
        inicio, fin = rango_fechas
        df_filtrado = df_filtrado[(df_filtrado['fecha'].dt.date >= inicio) & 
                                  (df_filtrado['fecha'].dt.date <= fin)]

    # Métricas principales
    col1, col2, col3 = st.columns(3)
    col1.metric("Ventas Totales", f"${df_filtrado['total'].sum():,.2f}")
    col2.metric("Margen Total", f"${df_filtrado['margen'].sum():,.2f}")
    col3.metric("Versión del Dataset", hash_dataset[:8] + "...")

    # Tabla de datos
    st.subheader("📊 Datos Procesados")
    st.dataframe(df_filtrado, use_container_width=True)
    
    # Pie de página en la barra lateral con la versión
    st.sidebar.markdown(f"**Hash del Dataset:** `{hash_dataset}`")
    
    # Nota sobre la simulación de API
    st.info("Nota: Los datos de la API se integran de forma simulada en el pipeline ETL para demostrar el enriquecimiento externo.")

else:
    st.error("No se encontró el archivo de datos procesados. Por favor, ejecuta `etl.py` primero para generar los datos.")
