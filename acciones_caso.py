from conection.conexion import conectar_db

def agregar_caso(titulo,descripcion,estado,id_cliente,id_area):
    conn=conectar_db()
    if conn:
        try:
            cursor=conn.cursor()
            insert_query="INSERT INTO caso (titulo,descripcion,fecha_creacion,estado,id_cliente_asociado,id_area_caso) VALUES (%s, %s, NOW(),%s, %s,%s)"
            cursor.execute(insert_query,(titulo,descripcion,estado,id_cliente,id_area))
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

def obtener_nombres_areas():
    conn = conectar_db()
    nombres_areas = []

    if conn:
        try:
            cursor = conn.cursor()
            select_query = "SELECT id_area, nombre FROM area_legal"
            cursor.execute(select_query)
            resultados = cursor.fetchall()

            for resultado in resultados:
                id_area, nombre_area = resultado
                nombres_areas.append((id_area, nombre_area))

            cursor.close()
            conn.close()
            #print("Nombres de clientes obtenidos correctamente:", nombres_areas)
        except Exception as e:
            print(f"Error al obtener nombres de clientes: {e}")

    return nombres_areas

def listar_casos():
    conn = conectar_db()
    if conn:
        try:
            cursor = conn.cursor(dictionary=True)
            query="""
                SELECT
                    caso.id_caso,
                    caso.titulo,
                    caso.descripcion,
                    caso.fecha_creacion,
                    caso.estado,
                    cliente.nombre AS nombre_cliente,
                    area_legal.nombre AS nombre_area
                FROM
                    caso
                JOIN
                    cliente ON caso.id_cliente_asociado = cliente.id_cliente
                JOIN
                    area_legal ON caso.id_area_caso = area_legal.id_area
                ORDER BY
                    CASE
                        WHEN caso.estado = 'Activo' THEN 1
                        WHEN caso.estado = 'Pendiente' THEN 2
                        WHEN caso.estado = 'Fenecido' THEN 3
                        ELSE 4
                    END;
                """
            cursor.execute(query)
            lista_casos=cursor.fetchall()
            #print(lista_casos)
            cursor.close()
            conn.close()
            return lista_casos
        except Exception as e:
            print(f"Error al obtener nombres de clientes: {e}")
            return
        
def eliminar_caso(id_caso):
    conn=conectar_db()
    if conn:
        try:
            cursor=conn.cursor()
            delete_query="DELETE FROM caso WHERE id_caso = %s"
            cursor.execute(delete_query,(id_caso,))
            conn.commit()
            cursor.close()
            conn.close()
            return True
        except Exception as e:
            print(f"Error al eliminar el caso:{e}")
        return False
    
def modificar_caso(id_caso, nuevo_titulo, nueva_descripcion, nuevo_estado, nuevo_id_cliente, nuevo_id_area):
    conn=conectar_db()
    if conn:
        try:
            cursor=conn.cursor()
            update_query = "UPDATE caso SET titulo = %s, descripcion = %s, estado = %s, id_cliente_asociado = %s, id_area_caso = %s WHERE id_caso = %s"
            cursor.execute(update_query,(nuevo_titulo, nueva_descripcion, nuevo_estado, nuevo_id_cliente, nuevo_id_area, id_caso))
            conn.commit()
            cursor.close()
            conn.close()
            return True
        except Exception as e:
            print(f"Error al modificar el cliente:{e}")
        return False
    
def info_caso_id(id_caso):
    conn=conectar_db()
    if conn:
        try:
            cursor=conn.cursor(dictionary=True)
            select_query="SELECT * FROM caso WHERE id_caso = %s"
            cursor.execute(select_query, (id_caso,))
            cliente=cursor.fetchone()
            cursor.close()
            conn.close()
            return cliente
        except Exception as e:
            print(f"Error al obtener el caso:{e}")
        return None
    
def obtener_id_cliente(id_cliente):
    conn = conectar_db()
    if conn:
        try:
            cursor = conn.cursor()
            select_query = "SELECT nombre FROM cliente WHERE id_cliente = %s"
            cursor.execute(select_query, (id_cliente,))
            result = cursor.fetchone()
            if result:
                nombre_cliente = result[0]
                return nombre_cliente
            cursor.close()
            conn.close()
        except Exception as e:
            print(f"Error al obtener el cliente: {e}")
    return None

def obtener_id_area(id_area):
    conn = conectar_db()
    if conn:
        try:
            cursor = conn.cursor()
            select_query = "SELECT nombre FROM area_legal WHERE id_area = %s"
            cursor.execute(select_query, (id_area,))
            result = cursor.fetchone()
            if result:
                nombre_area = result[0]
                return nombre_area
            cursor.close()
            conn.close()
        except Exception as e:
            print(f"Error al obtener el área: {e}")
    return None