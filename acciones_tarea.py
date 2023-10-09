from conection.conexion import conectar_db

def crear_tarea(descripcion_tarea,fecha_creacion,fecha_limite,estado,id_expediente_tarea,prioridad):
    conn=conectar_db()
    if conn:
        try:
            cursor=conn.cursor()
            cursor.execute("INSERT INTO tarea (descripcion_tarea,fecha_creacion,fecha_limite,estado,id_expediente_tarea,prioridad) VALUES (%s,%s,%s,%s,%s,%s)",(descripcion_tarea,fecha_creacion,fecha_limite,estado,id_expediente_tarea,prioridad))
            conn.commit()
            conn.close()
            cursor.close()
            #print('datos ingresados correctamente')
            return True
        except Exception as e:
            print('error al ingresar los datos')
        return False

def lista_de_tareas():
    conn = conectar_db()
    if conn:
        try:
            cursor = conn.cursor(dictionary=True)
            query="""
                SELECT
                    t.id_tarea,
                    t.descripcion_tarea,
                    t.fecha_limite,
                    t.prioridad,
                    e.nombre_expediente,
                    e.correlativo_expediente,
                    c.titulo,
                    cl.nombre,
                    t.estado                    
                FROM
                    tarea t
                INNER JOIN
                    expediente e ON t.id_expediente_tarea = e.id_expediente
                INNER JOIN
                    caso c ON e.id_caso_vinculado = c.id_caso
                INNER JOIN
                    cliente cl ON c.id_cliente_asociado = cl.id_cliente
                WHERE t.estado !='finalizado'
                ORDER BY
                    CASE
                        WHEN t.prioridad = 'alta' THEN 1
                        WHEN t.prioridad = 'media' THEN 2
                        WHEN t.prioridad = 'baja' THEN 3
                        ELSE 4
                    END;
                """
            cursor.execute(query)
            lista_tarea=cursor.fetchall()
            #print(lista_casos)
            cursor.close()
            conn.close()
            #print(lista_tarea)
            return lista_tarea
        except Exception as e:
            print(f"Error al obtener los datos {e}")
            return

def modificar_tarea_estado(id_tarea, nuevo_estado):
    conn=conectar_db()
    if conn:
        try:
            cursor=conn.cursor()
            update_query = "UPDATE tarea SET estado = %s WHERE id_tarea = %s"
            cursor.execute(update_query,(nuevo_estado, id_tarea))
            conn.commit()
            cursor.close()
            conn.close()
            return True
        except Exception as e:
            print(f"Error al modificar el estado:{e}")
        return False
    
def lista_de_tareas2():
    conn = conectar_db()
    if conn:
        try:
            cursor = conn.cursor(dictionary=True)
            query="""
                SELECT
                    t.id_tarea,
                    t.descripcion_tarea,
                    t.fecha_limite,
                    t.prioridad,
                    e.nombre_expediente,
                    e.correlativo_expediente,
                    c.titulo,
                    cl.nombre,
                    t.estado                    
                FROM
                    tarea t
                INNER JOIN
                    expediente e ON t.id_expediente_tarea = e.id_expediente
                INNER JOIN
                    caso c ON e.id_caso_vinculado = c.id_caso
                INNER JOIN
                    cliente cl ON c.id_cliente_asociado = cl.id_cliente
                ORDER BY
                    CASE
                        WHEN t.estado = 'en curso' THEN 1
                        WHEN t.estado = 'no iniciado' THEN 2
                        WHEN t.estado = 'finalizado' THEN 3
                        ELSE 4
                    END;    
                    """
            cursor.execute(query)
            lista_tarea2=cursor.fetchall()
            #print(lista_casos)
            cursor.close()
            conn.close()
            #print(lista_tarea2)
            return lista_tarea2
        except Exception as e:
            print(f"Error al obtener los datos {e}")
            return
        
def modificar_tarea(id_tarea, nueva_descripcion, nueva_fc,nueva_fl,nueva_prioridad):
    conn=conectar_db()
    if conn:
        try:
            cursor=conn.cursor()
            update_query = "UPDATE tarea SET descripcion_tarea = %s, fecha_creacion = %s, fecha_limite = %s, prioridad = %s WHERE id_tarea = %s"
            cursor.execute(update_query,(nueva_descripcion, nueva_fc, nueva_fl, nueva_prioridad, id_tarea))
            conn.commit()
            cursor.close()
            conn.close()
            return True
        except Exception as e:
            print(f"Error al modificar la tarea:{e}")
        return False
    
def info_tarea_id(id_tarea):
    conn=conectar_db()
    if conn:
        try:
            cursor=conn.cursor(dictionary=True)
            select_query="SELECT * FROM tarea WHERE id_tarea = %s"
            cursor.execute(select_query, (id_tarea,))
            cliente=cursor.fetchone()
            cursor.close()
            conn.close()
            return cliente
        except Exception as e:
            print(f"Error al obtener la tarea:{e}")
        return None
    
def eliminar_tarea(id_tarea):
    conn=conectar_db()
    if conn:
        try:
            cursor=conn.cursor()
            delete_query="DELETE FROM tarea WHERE id_tarea = %s"
            cursor.execute(delete_query,(id_tarea,))
            conn.commit()
            cursor.close()
            conn.close()
            return True
        except Exception as e:
            print(f"Error al eliminar la tarea:{e}")
        return False