from conection.conexion import conectar_db

def crear_area(nombre,descripcion):
    conn=conectar_db()
    if conn:
        try:
            cursor=conn.cursor()
            cursor.execute("INSERT INTO area_legal (nombre,descripcion) VALUES (%s, %s)",(nombre,descripcion))
            conn.commit()
            conn.close()
            print('datos ingresados correctamente')
        except Exception as e:
            print('error al ingresar los datos')

def modificar_area(id_area, nuevo_nombre, nueva_descripcion):
    conn=conectar_db()
    if conn:
        try:
            cursor=conn.cursor()
            update_query = "UPDATE area_legal SET nombre = %s, descripcion = %s WHERE id_area = %s"
            cursor.execute(update_query,(nuevo_nombre, nueva_descripcion, id_area))
            conn.commit()
            cursor.close()
            conn.close()
            return True
        except Exception as e:
            print(f"Error al modificar el area:{e}")
        return False

def eliminar_area(id_area):
    conn=conectar_db()
    if conn:
        try:
            cursor=conn.cursor()
            delete_query="DELETE FROM area_legal WHERE id_area = %s"
            cursor.execute(delete_query,(id_area,))
            conn.commit()
            cursor.close()
            conn.close()
            return True
        except Exception as e:
            print(f"Error al eliminar el area:{e}")
        return False
    
def info_area_id(id_area):
    conn=conectar_db()
    if conn:
        try:
            cursor=conn.cursor(dictionary=True)
            select_query="SELECT * FROM area_legal WHERE id_area = %s"
            cursor.execute(select_query, (id_area,))
            area=cursor.fetchone()
            cursor.close()
            conn.close()
            return area
        except Exception as e:
            print(f"Error al obtener el area legal:{e}")
        return None

def listar_areas():
    conn = conectar_db()
    if conn:
        try:
            cursor = conn.cursor(dictionary=True)
            query="""
                SELECT
                    a.id_area,
                    a.nombre,
                    a.descripcion
                FROM
                    area_legal a
                """
            cursor.execute(query)
            lista_areas=cursor.fetchall()
            #print(lista_casos)
            cursor.close()
            conn.close()
            #print(lista_areas)
            return lista_areas
        except Exception as e:
            print(f"Error al obtener nombres de clientes: {e}")
            return None
