import psycopg2
import requests

# Obtener datos de la API de Rest Countries
def obtener_datos_api():
    url = "https://restcountries.com/v3.1/all"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    else:
        print("Error al obtener datos de la API:", response.status_code)
        return None

# Conectar a la base de datos PostgreSQL
def conectar_postgresql():
    try:
        conn = psycopg2.connect(
            host="localhost",
            user="tu_usuario",
            password="tu_contraseña",
            database="tu_base_de_datos"
        )
        return conn
    except psycopg2.Error as e:
        print("Error al conectar a la base de datos PostgreSQL:", e)
        return None

# Crear una tabla en la base de datos PostgreSQL
def crear_tabla(conn):
    try:
        cursor = conn.cursor()
        cursor.execute('''CREATE TABLE IF NOT EXISTS paises (
                            id SERIAL PRIMARY KEY,
                            nombre VARCHAR(255),
                            capital VARCHAR(255),
                            poblacion INT,
                            region VARCHAR(255),
                            subregion VARCHAR(255)
                        )''')
        conn.commit()
        cursor.close()
    except psycopg2.Error as e:
        print("Error al crear la tabla en la base de datos PostgreSQL:", e)

# Insertar datos en la tabla PostgreSQL
def insertar_datos_en_tabla(conn, datos):
    try:
        cursor = conn.cursor()
        for dato in datos:
            cursor.execute('''INSERT INTO paises (nombre, capital, poblacion, region, subregion)
                              VALUES (%s, %s, %s, %s, %s)''', 
                           (dato['name']['common'], dato.get('capital', ''), dato.get('population', 0), 
                            dato.get('region', ''), dato.get('subregion', '')))
        conn.commit()
        cursor.close()
        print("Datos insertados correctamente en la tabla PostgreSQL.")
    except psycopg2.Error as e:
        print("Error al insertar datos en la tabla PostgreSQL:", e)

# Obtener datos de la API de Rest Countries
datos_api = obtener_datos_api()

if datos_api:
    # Conectar a la base de datos PostgreSQL
    conn = conectar_postgresql()
    if conn:
        # Crear tabla en la base de datos PostgreSQL
        crear_tabla(conn)
        
        # Insertar datos en la tabla PostgreSQL
        insertar_datos_en_tabla(conn, datos_api)
        
        # Cerrar la conexión a la base de datos PostgreSQL
        conn.close()
else:
    print("No se pudieron obtener los datos de la API de Rest Countries.")
