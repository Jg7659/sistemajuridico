from conection.conexion import conectar_db

def agregar_expediente(nombre_expediente,descripcion,id_caso,correlativo_expediente):
    conn=conectar_db()
    if conn:
        try:
            cursor=conn.cursor()
            insert_query="INSERT INTO expediente (nombre_expediente,descripcion,fecha_creacion,id_caso_vinculado,correlativo_expediente) VALUES (%s, %s, NOW(),%s,%s)"
            cursor.execute(insert_query,(nombre_expediente,descripcion,id_caso,correlativo_expediente))
            conn.commit()
            cursor.close()
            conn.close()

            return True
        except Exception as e:
            print(f"Error al obtener el cliente:{e}")
        return False

def obtener_nombres_clientes():
    conn = conectar_db()
    nombres_clientes = []

    if conn:
        try:
            cursor = conn.cursor()
            select_query = "SELECT id_cliente, nombre FROM cliente"
            cursor.execute(select_query)
            resultados = cursor.fetchall()

            for resultado in resultados:
                id_cliente, nombre_cliente = resultado
                nombres_clientes.append((id_cliente, nombre_cliente))

            cursor.close()
            conn.close()
            #print("Nombres de clientes obtenidos correctamente:", nombres_clientes)
        except Exception as e:
            print(f"Error al obtener nombres de clientes: {e}")

    return nombres_clientes

def obtener_expedientes_del_caso(id_caso):
    conn = conectar_db()
    expedientes = []

    if conn:
        try:
            cursor = conn.cursor(dictionary=True)
            select_query = "SELECT * FROM expediente WHERE id_caso_vinculado = %s"
            cursor.execute(select_query, (id_caso,))
            expedientes = cursor.fetchall()
            cursor.close()
            conn.close()
        except Exception as e:
            print(f"Error al obtener expedientes del caso: {e}")

    return expedientes
        
def eliminar_expediente(id_expediente):
    conn=conectar_db()
    if conn:
        try:
            cursor=conn.cursor()
            delete_query="DELETE FROM expediente WHERE id_expediente = %s"
            cursor.execute(delete_query,(id_expediente,))
            conn.commit()
            cursor.close()
            conn.close()
            return True
        except Exception as e:
            print(f"Error al eliminar el caso:{e}")
        return False
    
def modificar_expediente(id_expediente, nuevo_nombre, nueva_descripcion,nuevo_corre_expediente):
    conn=conectar_db()
    if conn:
        try:
            cursor=conn.cursor()
            update_query = "UPDATE expediente SET nombre_expediente = %s, descripcion = %s, correlativo_expediente = %s WHERE id_expediente = %s"
            cursor.execute(update_query,(nuevo_nombre, nueva_descripcion,nuevo_corre_expediente, id_expediente))
            conn.commit()
            cursor.close()
            conn.close()
            return True
        except Exception as e:
            print(f"Error al modificar el cliente:{e}")
        return False
    
def info_expediente_id(id_expediente):
    conn=conectar_db()
    if conn:
        try:
            cursor=conn.cursor(dictionary=True)
            select_query="SELECT * FROM expediente WHERE id_expediente = %s"
            cursor.execute(select_query, (id_expediente,))
            cliente=cursor.fetchone()
            cursor.close()
            conn.close()
            return cliente
        except Exception as e:
            print(f"Error al obtener el caso:{e}")
        return None
    
def obtener_id_caso_expediente(id_expediente):
    conn = conectar_db()
    if conn:
            try:
                cursor = conn.cursor()
                select_query = "SELECT id_caso_vinculado FROM expediente WHERE id_expediente = %s"
                cursor.execute(select_query, (id_expediente,))
                result = cursor.fetchone()
                if result:
                    id_caso = result[0]
                    
                    return id_caso
                else:
                    return None
            except Exception as e:
                print(f"Error al obtener el área: {e}")
            finally:
                cursor.close()
                conn.close()
    return None