from conection.conexion import conectar_db

def crear_cliente(nombre,tipo,email,telefono,direccion):
    conn=conectar_db()
    if conn:
        try:
            cursor=conn.cursor()
            cursor.execute("INSERT INTO cliente (nombre,tipo,email,telefono,direccion,fecha_creacion) VALUES (%s,%s,%s,%s,%s,NOW())",(nombre,tipo,email,telefono,direccion))
            conn.commit()
            conn.close()
            #print('datos ingresados correctamente')
        except Exception as e:
            print('error al ingresar los datos')

