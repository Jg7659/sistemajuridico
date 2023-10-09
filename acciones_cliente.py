from conection.conexion import conectar_db

def info_cliente_id(id_cliente):
    conn=conectar_db()
    if conn:
        try:
            cursor=conn.cursor(dictionary=True)
            select_query="SELECT * FROM cliente WHERE id_cliente = %s"
            cursor.execute(select_query, (id_cliente,))
            cliente=cursor.fetchone()
            cursor.close()
            conn.close()
            return cliente
        except Exception as e:
            print(f"Error al obtener el cliente:{e}")
        return None

def modificar_cliente(id_cliente, nuevo_nombre, nuevo_tipo, nuevo_email, nuevo_telefono, nueva_direccion):
    conn=conectar_db()
    if conn:
        try:
            cursor=conn.cursor()
            update_query = "UPDATE cliente SET nombre = %s, tipo = %s, email = %s, telefono = %s, direccion = %s WHERE id_cliente = %s"
            cursor.execute(update_query,(nuevo_nombre, nuevo_tipo, nuevo_email, nuevo_telefono, nueva_direccion, id_cliente))
            conn.commit()
            cursor.close()
            conn.close()
            return True
        except Exception as e:
            print(f"Error al modificar el cliente:{e}")
        return False

def eliminar_cliente(id_cliente):
    conn=conectar_db()
    if conn:
        try:
            cursor=conn.cursor()
            delete_query="DELETE FROM cliente WHERE id_cliente = %s"
            cursor.execute(delete_query,(id_cliente,))
            conn.commit()
            cursor.close()
            conn.close()
            return True
        except Exception as e:
            print(f"Error al eliminar el cliente:{e}")
        return False