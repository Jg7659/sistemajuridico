from conection.conexion import conectar_db

def crear_notificacion(mensaje,id_expediente_asociado,fecha_limite,estado,prioridad):
    conn=conectar_db()
    if conn:
        try:
            cursor=conn.cursor()
            cursor.execute("INSERT INTO notificacion (mensaje, id_expediente_asociado, fecha_limite,estado,prioridad) VALUES (%s,%s,%s,%s,%s)",(mensaje, id_expediente_asociado, fecha_limite,estado,prioridad))
            conn.commit()
            conn.close()
            cursor.close()
            #print('datos ingresados correctamente')
            return True
        except Exception as e:
            print('error al ingresar los datos')
        return False

def lista_de_recordatorio():
    conn = conectar_db()
    if conn:
        try:
            cursor = conn.cursor(dictionary=True)
            query="""
                SELECT
                    n.id_notificacion,
                    n.mensaje,
                    n.fecha_limite,
                    n.prioridad,
                    n.estado,
                    e.nombre_expediente,
                    e.correlativo_expediente,
                    c.titulo,
                    cl.nombre                    
                FROM
                    notificacion n
                INNER JOIN
                    expediente e ON n.id_expediente_asociado = e.id_expediente
                INNER JOIN
                    caso c ON e.id_caso_vinculado = c.id_caso
                INNER JOIN
                    cliente cl ON c.id_cliente_asociado = cl.id_cliente
                WHERE n.estado !='finalizado'
                AND n.estado !='cancelado'
                AND
                    n.fecha_limite >= NOW()
                ORDER BY
                    n.fecha_limite ASC
                """
            cursor.execute(query)
            lista_record=cursor.fetchall()
            #print(lista_casos)
            cursor.close()
            conn.close()
            #print(lista_record)
            return lista_record
        except Exception as e:
            print(f"Error al obtener los datos {e}")
            return None
        
def lista_de_recordatorio_all():
    conn = conectar_db()
    if conn:
        try:
            cursor = conn.cursor(dictionary=True)
            query="""
                SELECT
                    n.id_notificacion,
                    n.mensaje,
                    n.fecha_limite,
                    n.prioridad,
                    n.estado,
                    e.nombre_expediente,
                    e.correlativo_expediente,
                    c.titulo,
                    cl.nombre                    
                FROM
                    notificacion n
                INNER JOIN
                    expediente e ON n.id_expediente_asociado = e.id_expediente
                INNER JOIN
                    caso c ON e.id_caso_vinculado = c.id_caso
                INNER JOIN
                    cliente cl ON c.id_cliente_asociado = cl.id_cliente
                """
            cursor.execute(query)
            lista_record_all=cursor.fetchall()
            #print(lista_casos)
            cursor.close()
            conn.close()
            #print(lista_record_all)
            return lista_record_all
        except Exception as e:
            print(f"Error al obtener los datos {e}")
            return

def modificar_record(id_notificacion, nuevo_mensaje,nueva_fl,nueva_prioridad):
    conn=conectar_db()
    if conn:
        try:
            cursor=conn.cursor()
            update_query = "UPDATE notificacion SET mensaje = %s, fecha_limite = %s, prioridad = %s WHERE id_notificacion = %s"
            cursor.execute(update_query,(nuevo_mensaje, nueva_fl, nueva_prioridad, id_notificacion))
            conn.commit()
            cursor.close()
            conn.close()
            return True
        except Exception as e:
            print(f"Error al modificar el recordatorio:{e}")
        return False
    
def info_noti_id(id_notificacion):
    conn=conectar_db()
    if conn:
        try:
            cursor=conn.cursor(dictionary=True)
            select_query="SELECT * FROM notificacion WHERE id_notificacion = %s"
            cursor.execute(select_query, (id_notificacion,))
            cliente=cursor.fetchone()
            cursor.close()
            conn.close()
            return cliente
        except Exception as e:
            print(f"Error al obtener el recordatorio:{e}")
        return None
    
def eliminar_record(id_notificacion):
    conn=conectar_db()
    if conn:
        try:
            cursor=conn.cursor()
            delete_query="DELETE FROM notificacion WHERE id_notificacion = %s"
            cursor.execute(delete_query,(id_notificacion,))
            conn.commit()
            cursor.close()
            conn.close()
            return True
        except Exception as e:
            print(f"Error al eliminar el recordatorio:{e}")
        return False
    
def modificar_record_estado(id_notificacion, nuevo_estado):
    conn=conectar_db()
    if conn:
        try:
            cursor=conn.cursor()
            update_query = "UPDATE notificacion SET estado = %s WHERE id_notificacion = %s"
            cursor.execute(update_query,(nuevo_estado, id_notificacion))
            conn.commit()
            cursor.close()
            conn.close()
            return True
        except Exception as e:
            print(f"Error al modificar el estado:{e}")
        return False