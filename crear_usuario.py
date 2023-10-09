from conection.conexion import conectar_db

def crear_usuario(nombre,apellido,email,contraseña,telefono,direccion,ciudad,pais,sexo,fecha_nacimiento):
    conn=conectar_db()
    if conn:
        try:
            cursor=conn.cursor()
            cursor.execute("INSERT INTO usuarios (nombre, apellido, email, contraseña, telefono, direccion, ciudad, pais, sexo, fecha_nacimiento) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)",(nombre,apellido,email,contraseña,telefono,direccion,ciudad,pais,sexo,fecha_nacimiento))
            conn.commit()
            conn.close()
            #print('datos ingresados correctamente')
        except Exception as e:
            print('error al ingresar los datos')

