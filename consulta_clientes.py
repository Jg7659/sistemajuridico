from conection.conexion import conectar_db

def consulta_cliente(busqueda):
    conn=conectar_db()
    if conn:
            cursor=conn.cursor()
            consulta="SELECT * FROM cliente WHERE nombre LIKE %s OR tipo LIKE %s"
            valor_busqueda=f"%{busqueda}%"

            cursor.execute(consulta,(valor_busqueda,valor_busqueda))
            resultados=cursor.fetchall()
            conn.close()
            return resultados
    else:
        return[]
       

