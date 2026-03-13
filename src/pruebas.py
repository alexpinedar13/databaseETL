import pandas as pd
import json
import sqlite3
import hashlib
import requests
import os

# Determinar la ruta base del proyecto (un nivel arriba de src/)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_RAW_DIR = os.path.join(BASE_DIR, "data", "raw")
DATA_PROCESSED_DIR = os.path.join(BASE_DIR, "data", "processed")


def run_etl():
    print("--- Iniciando Pipeline ETL ---")

    # 1. Cargar datos de ventas
    print("Paso 1: Cargando datos de ventas...")
    ventas_path = os.path.join(DATA_RAW_DIR, "ventas.csv")
    if not os.path.exists(ventas_path):
        print(f"Error: No se encontró {ventas_path}")
        return
    print(f'procesando ventas.csv')   
    df_ventas = pd.read_csv(ventas_path)
    print(df_ventas.head(10))
    print(df_ventas.shape) 
    
    # Verificar tipos y convertir a numérico las columnas que lo requieran
    
    columnas_numericas = ['precio', 'cantidad', 'descuento_pct', 'costo_unitario']
    for col in columnas_numericas:
        if col in df_ventas.columns:
            df_ventas[col] = pd.to_numeric(df_ventas[col], errors='coerce')
        else:print(f'No se encuentra la columna {col}')
    

    # 2. Convertir la columna fecha a tipo datetime
    print("Paso 2: Convirtiendo fecha a datetime...")
    if 'fecha' in df_ventas.columns:
        df_ventas['fecha'] = pd.to_datetime(df_ventas['fecha'])
    else:print(f'No se encuentra la columna fecha')

    print(f"Tipos de datos de ventas tras conversión:\n{df_ventas.dtypes}")

    # 3. Seleccionar columnas relevantes para reducir el uso de memoria
    print("Paso 3: Columnas necesarias en el pipeline")
    cols_a_mantener = ['id', 'id_cliente', 'producto', 'cantidad', 'precio', 'fecha', 'region', 'canal', 'costo_unitario'] #se conserva costo_unitario para calcular el margen por que es utilizada para el margen
    df_ventas = df_ventas[[c for c in cols_a_mantener if c in df_ventas.columns]]


    # 4. Filtrar filas con cantidad > 0 y eliminar duplicados
    print("Paso 4: Filtrando y eliminando duplicados...")
    df_ventas = df_ventas[df_ventas['cantidad'] > 0].drop_duplicates()
   
    print(df_ventas.head(10))
    print(df_ventas.shape) 

    # 5. Crear columnas calculadas: 'total' y 'margen'
    print("Paso 5: Creando columnas total y margen")
    df_ventas['total'] = df_ventas['precio'] * df_ventas['cantidad']
    if 'costo_unitario' in df_ventas.columns:
        df_ventas['margen'] = (df_ventas['precio'] - df_ventas['costo_unitario']) * df_ventas['cantidad']
    
    print(df_ventas.head(10))
    
     # 6. Filtrar por rango de fechas (ej. año 2023)
    print("Paso 6: Filtrando por el año 2023...")
    df_ventas = df_ventas[df_ventas['fecha'].dt.year == 2023]
    print(df_ventas.head(10))
    print(df_ventas.shape) 
 
    # 7. Cargar datos de clientes
    print("Paso 7: Cargando datos de clientes...")
    clientes_path = os.path.join(DATA_RAW_DIR, "clientes.json")
    if os.path.exists(clientes_path):
        with open(clientes_path, 'r', encoding='utf-8') as f: #lee el archivo json
            datos_clientes = json.load(f)   #convierte el json en python listas y diccionarios
        df_clientes = pd.DataFrame(datos_clientes)  #convierte el json en dataframe(una tabla)
        print(df_clientes.head(10))
        print(df_clientes.shape) 

        # Convertir id a entero y fecha_alta a datetime si es necesario
        if 'id' in df_clientes.columns:
            df_clientes['id'] = pd.to_numeric(df_clientes['id'], errors='coerce').astype('Int64')
        if 'fecha_alta' in df_clientes.columns:
            df_clientes['fecha_alta'] = pd.to_datetime(df_clientes['fecha_alta'])

        print(f"Tipos de datos de clientes tras conversión:\n{df_clientes.dtypes}")
        # 8. Seleccionar columnas de clientes necesarias para el enriquecimiento
        print("Paso 8: Seleccionando columnas de clientes...")
        cols_clientes = ['id', 'nombre', 'ciudad', 'segmento']
        df_clientes = df_clientes[[c for c in cols_clientes if c in df_clientes.columns]]

        # 9. Integrar ventas y clientes (Merge)
        print("Paso 9: Integrando ventas y clientes...")
        df_enriquecido = pd.merge(df_ventas, df_clientes, left_on='id_cliente', right_on='id', how='left')
        print(df_enriquecido.head(10))
        print(df_enriquecido.shape) 
    
    else:
        print(f"Advertencia: No se encontró {clientes_path}. por favor verificar este archivo *.json")
        df_enriquecido = df_ventas
    
    # 10. Guardar el resultado procesado en CSV
    print("Paso 10: Guardando datos procesados...")
    os.makedirs(DATA_PROCESSED_DIR, exist_ok=True)
    archivo_procesado = os.path.join(DATA_PROCESSED_DIR, "ventas_enriquecidas.csv")
    df_enriquecido.to_csv(archivo_procesado, index=False)
    print(f'archivo {archivo_procesado} creado con exito')

    # 11. Cargar el DataFrame en SQLite
    print("Paso 11: Cargando datos en SQLite...")
    db_path = os.path.join(BASE_DIR, "data", "ventas.db")
    conn = sqlite3.connect(db_path)
    df_enriquecido.to_sql('ventas_procesadas', conn, if_exists='replace', index=False)
    conn.close()
    print(f'archivo {db_path} creado con exito')

    # 12. Calcular el hash MD5 del dataset procesado
    print("Paso 12: Calculando hash MD5...")
    csv_str = df_enriquecido.to_csv(index=False)
    hash_dataset = hashlib.md5(csv_str.encode('utf-8')).hexdigest()
    print(f"Versión del dataset: {hash_dataset}")

    # 13. Simulación de lectura desde API REST
    print("Paso 13: Obteniendo datos de API REST...")
    try:
        respuesta = requests.get("https://jsonplaceholder.typicode.com/users")
        if respuesta.status_code == 200:
            datos_api = respuesta.json()
            df_api = pd.DataFrame(datos_api)
            # Filtrar y limpiar datos de la API
            df_api = df_api[['id', 'username', 'email', 'phone', 'website']]
            df_api.columns = ['api_id', 'api_username', 'api_email', 'api_phone', 'api_website']
            print(f"Tipos de datos de clientes tras conversión:\n{df_api.dtypes}")
            print(df_api.head(10))
            print(df_api.shape)
            # Simulación de enriquecimiento
            df_final = pd.concat([df_enriquecido, df_api.head(len(df_enriquecido))], axis=1)
            #df_final = pd.merge(df_enriquecido, df_api, left_on='id_x', right_on='api_id', how='left')
            print("Integración con datos de la API simulada con éxito.")
            print(df_final.head(50))
            print(df_final.shape)   
    except Exception as e:
        print(f"Error al obtener datos de la API: {e}")

    print(f"--- ETL completado con éxito. Se procesaron {len(df_enriquecido)} filas. ---")
    return hash_dataset


if __name__ == "__main__":
    run_etl()
