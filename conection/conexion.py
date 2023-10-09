import mysql.connector

def conectar_db():
    try:
        conn = mysql.connector.connect(
            host='localhost',
            user='root',
            password='Josh7659.',
            database='sistema_juridico'
        )
        if conn.is_connected():
            print('Conexión exitosa')
            return conn
    except mysql.connector.Error as e:
        print('Error al conectar la base de datos:', e)
        return None

# Llamamos a la función para establecer la conexión
conn = conectar_db()

# Asegúrate de cerrar la conexión cuando hayas terminado de usarla
if conn:
    conn.close()
