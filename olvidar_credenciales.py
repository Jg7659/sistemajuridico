from conection.conexion import conectar_db
import secrets
import datetime



def olvido_contraseña(email_usuario):
    conn=conectar_db()
    token=secrets.token_hex(32)
    expiration=datetime.datetime.now()+ datetime.timedelta(hours=12)
    if conn:
            try:
                cursor=conn.cursor()
                update_query="UPDATE usuarios SET cambio_contraseña_token = %s, cambio_contraseña_expiracion = %s WHERE email = %s"
                cursor.execute(update_query, (token,expiration,email_usuario))
                conn.commit()
                cursor.close()
                conn.close()
                
            except Exception as e:
                print(f"Error al obtener el cliente:{e}")
        

