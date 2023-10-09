from flask_session import Session
from urllib import response
from wsgiref import headers
import requests
from cgitb import html
from http.client import NOT_FOUND
from flask import Flask, render_template, request,jsonify,Response,redirect,url_for,flash,session
from crear_usuario import crear_usuario
from registro_cliente import crear_cliente
from conection.conexion import conectar_db
from consulta_clientes import consulta_cliente
from acciones_cliente import info_cliente_id, modificar_cliente,eliminar_cliente
from acciones_caso import agregar_caso,obtener_nombres_clientes,obtener_nombres_areas,listar_casos,eliminar_caso,modificar_caso,info_caso_id,obtener_id_area,obtener_id_cliente
from acciones_exp import agregar_expediente,obtener_nombres_clientes,eliminar_expediente,modificar_expediente,obtener_expedientes_del_caso,obtener_id_caso_expediente,info_expediente_id
from acciones_area import crear_area,eliminar_area,modificar_area,info_area_id,listar_areas
from acciones_notificacion import crear_notificacion,lista_de_recordatorio,lista_de_recordatorio_all,modificar_record,info_noti_id,eliminar_record,modificar_record_estado
from acciones_tarea import crear_tarea,lista_de_tareas,modificar_tarea_estado,lista_de_tareas2, modificar_tarea,info_tarea_id,eliminar_tarea
import bcrypt

app=Flask(__name__)

app.config['SESSION_TYPE'] = 'filesystem'  
app.config['SESSION_PERMANENT'] = True      
app.config['SESSION_USE_SIGNER'] = False     
app.config['SECRET_KEY'] = 'josh7659.'

Session(app)


@app.route('/')
def home():
    return redirect(url_for('login'))

@app.route('/menu')
def menu():
    lista_tarea=lista_de_tareas()
    lista_record=lista_de_recordatorio()
    return render_template('/menu_principal.html', tareas=lista_tarea, recordatorios=lista_record)

@app.route('/login',methods=['POST','GET'])    
def login():
    if request.method=='POST':
       email=request.form.get('email')
       contraseña =request.form.get('contraseña')

       conn=conectar_db()
       if conn:
           cursor=conn.cursor()
           cursor.execute("SELECT * FROM usuarios WHERE email = %s",(email,))
           usuario=cursor.fetchone()
           conn.close()
           if usuario and bcrypt.checkpw(contraseña.encode('utf-8'), usuario[4].encode('utf-8')):
                session['usuario_id'] = usuario[0]
                return redirect('/menu')  # Cambia esto por la página a la que deseas redirigir al usuario después del inicio de sesión
           else:
                return "Credenciales incorrectas"
       else:
            return "Error de conexión de datos"

    else:
        if 'usuario_id' in session:
            return render_template('/menu_principal.html')  # Cambia esto por la página a la que deseas redirigir al usuario si ya está autenticado
        return render_template('/login.html')

@app.route('/logout')
def logout():
    if 'usuario_id' in session:
        # Elimina la información de la sesión del usuario
        session.pop('usuario_id', None)
    return redirect('/login')

@app.route('/registro',methods=['POST','GET'])    
def registro():
    if request.method=='POST':
        
        nombre=request.form.get('nombre')
        apellido=request.form.get('apellido')
        email=request.form.get('email')
        contraseña=request.form.get('contraseña')
        telefono=request.form.get('telefono')
        direccion=request.form.get('direccion')
        ciudad=request.form.get('ciudad')
        pais=request.form.get('pais')
        sexo=request.form.get('sexo')
        fecha_nacimiento=request.form.get('fecha_nacimiento')
        contraseña_hasheada = bcrypt.hashpw(contraseña.encode('utf-8'), bcrypt.gensalt())
        crear_usuario(nombre=nombre,apellido=apellido,email=email,contraseña=contraseña_hasheada,telefono=telefono,direccion=direccion,ciudad=ciudad,pais=pais,sexo=sexo,fecha_nacimiento=fecha_nacimiento)
        mensaje="Se ha registrado correctamente"
        return render_template('/mensaje_registro.html',mensaje=mensaje)
    else:
        return render_template('/registro.html')

@app.route('/registro_cliente',methods=['POST','GET'])    
def registro_cliente():
    if request.method=='POST':
        nombre=request.form.get('nombre')
        tipo=request.form.get('tipo')
        email=request.form.get('email')
        telefono=request.form.get('telefono')
        direccion=request.form.get('direccion')
        crear_cliente(nombre,tipo,email,telefono,direccion)
        return redirect('/clientes')
    else:
        return render_template('/registro_cliente.html')

@app.route('/clientes',methods=['POST','GET'])    
def listar_clientes():
    conn=conectar_db()
    if conn:
        cursor=conn.cursor()
        cursor.execute("SELECT * FROM cliente")
        lista_clientes=cursor.fetchall()
        conn.close()
    return render_template('/lista_clientes.html',clientes=lista_clientes)

@app.route('/consulta_clientes',methods=['POST','GET'])    
def consultar_clientes():
    if request.method=='POST':
        busqueda=request.form.get('busqueda')

        resultados=consulta_cliente(busqueda)

        if resultados:
            return render_template('/consulta_cliente.html', resultados=resultados)
        else:
            mensaje="No se econtraron resultados para la busqueda"
            return render_template('/mensaje.html',mensaje=mensaje)
    else:
        return render_template('/form-busqueda-clientes.html')                

@app.route('/modificar_cliente/<int:id_cliente>',methods=['GET'])
def mostrar_formulario_modificar(id_cliente):
    cliente=info_cliente_id(id_cliente)
    if cliente:
        return render_template('/form_modificar_cliente.html', cliente=cliente)
    else:
        return "Cliente no encontrado"

@app.route('/modificar_cliente/<int:id_cliente>',methods=['POST'])
def modificar_cliente_route(id_cliente):
    nuevo_nombre = request.form.get('nuevo_nombre')
    nuevo_tipo = request.form.get('nuevo_tipo')
    nuevo_email = request.form.get('nuevo_email')
    nuevo_telefono = request.form.get('nuevo_telefono')
    nueva_direccion = request.form.get('nueva_direccion')

    if modificar_cliente(id_cliente, nuevo_nombre, nuevo_tipo, nuevo_email, nuevo_telefono, nueva_direccion):
        return redirect('/clientes')
    
    return "Error al modificar el cliente"

@app.route('/casos',methods=['POST','GET'])    
def listar_casos_ex():
    lista_casos=listar_casos()
    return render_template('/lista_casos.html',casos=lista_casos)

@app.route('/eliminar_cliente/<int:id_cliente>',methods=['GET'])
def eliminar_cliente_route(id_cliente):
    if eliminar_cliente(id_cliente):
        return redirect ('/clientes')
    else:
        return "Error al eliminar el cliente"

@app.route('/agregar_caso',methods=['GET','POST'])
def insertar_caso():    
    if request.method=='POST':
        titulo=request.form.get('titulo')
        descripcion=request.form.get('descripcion')
        estado=request.form.get('estado')
        id_cliente=request.form.get('id_cliente')
        id_area=request.form.get('id_area')
        #nombre_cliente=obtener_id_cliente(id_cliente)
        #print(nombre_cliente)

        if agregar_caso(titulo,descripcion,estado,id_cliente,id_area):
            return redirect('/casos')
        else:
            return "Error al agregar el caso"
    
    else:
        nombres_cliente = obtener_nombres_clientes()
        nombres_area=obtener_nombres_areas()
        #print(nombres_cliente,nombres_area)

       
        #print(nombre_cliente)
        #print(nombre_area_legal)
    
        return render_template('/form_agregar_caso.html', nombres_cliente=nombres_cliente, nombres_area=nombres_area)

@app.route('/eliminar_caso/<int:id_caso>',methods=['GET'])
def eliminar_caso_route(id_caso):
    if eliminar_caso(id_caso):
        return redirect ('/casos')
    else:
        return "Error al eliminar el caso"

@app.route('/modificar_caso/<int:id_caso>',methods=['GET'])
def mostrar_formulario_modificar_caso(id_caso):
    caso=info_caso_id(id_caso)
    nombres_cliente = obtener_nombres_clientes()
    nombres_area=obtener_nombres_areas()
    if caso:
        nombre_cliente_actual = obtener_id_cliente(caso['id_cliente_asociado'])
        nombre_area_actual = obtener_id_area(caso['id_area_caso'])
        #print(nombre_cliente_actual)
        #print(nombre_area_actual)
        return render_template('/form_modificar_caso.html', caso=caso,nombres_cliente=nombres_cliente,nombres_area=nombres_area, nombre_cliente_actual=nombre_cliente_actual, nombre_area_actual=nombre_area_actual)
    else:
        return "Caso no encontrado"

@app.route('/modificar_caso/<int:id_caso>',methods=['POST'])
def modificar_caso_route(id_caso):
    nuevo_titulo = request.form.get('nuevo_titulo')
    nueva_descripcion = request.form.get('nueva_descripcion')
    nuevo_estado = request.form.get('nuevo_estado')
    nuevo_id_cliente = request.form.get('nuevo_id_cliente')
    nuevo_id_area = request.form.get('nuevo_id_area')

    if modificar_caso(id_caso, nuevo_titulo, nueva_descripcion, nuevo_estado, nuevo_id_cliente, nuevo_id_area):
        return redirect('/casos')
    
    return "Error al modificar el caso"

@app.route('/agregar_expediente/<int:id_caso>',methods=['GET'])
def mostrar_insertar_expediente(id_caso):
        return render_template('/form_agregar_expediente.html', id_caso=id_caso)

@app.route('/agregar_expediente/<int:id_caso>',methods=['POST'])
def insertar_expediente(id_caso):
        nombre_expediente=request.form.get('nombre_expediente')
        correlativo_expediente=request.form.get('correlativo_expediente')
        descripcion=request.form.get('descripcion')
        if agregar_expediente(nombre_expediente,descripcion,id_caso, correlativo_expediente):
            return redirect('/casos')
        else:
            return ('Error al agregar el expediente')

@app.route('/expedientes/<int:id_caso>',methods=['POST','GET'])    
def listar_expedientes(id_caso):
    expedientes=obtener_expedientes_del_caso(id_caso)
    return render_template('/lista_expediente.html',expedientes=expedientes)

@app.route('/eliminar_expediente/<int:id_expediente>',methods=['GET'])
def eliminar_expediente_route(id_expediente):
    id_caso=obtener_id_caso_expediente(id_expediente)
    if id_caso is not None:
        if eliminar_expediente(id_expediente):      
            return redirect (f'/expedientes/{id_caso}')
        else:
            return "Error al eliminar el expediente"
    else:
        return"expediente no encontrado o no vinculado"

@app.route('/modificar_expediente/<int:id_expediente>',methods=['GET'])
def mostrar_formulario_modificar_expediente(id_expediente):
        expediente=info_expediente_id(id_expediente)
        if expediente:
            return render_template('/form_modificar_expediente.html', expediente=expediente)
        else:
            return "Expediente no encontrado"

@app.route('/modificar_expediente/<int:id_expediente>',methods=['POST'])
def modificar_expediente_route(id_expediente):
    nuevo_nombre = request.form.get('nuevo_nombre')
    nueva_descripcion = request.form.get('nueva_descripcion')
    nuevo_corre_expediente = request.form.get('nuevo_corre_expediente')
    id_caso=obtener_id_caso_expediente(id_expediente)
    if id_caso is not None:
        if modificar_expediente(id_expediente,nuevo_nombre,nueva_descripcion,nuevo_corre_expediente):
            return redirect(f'/expedientes/{id_caso}')
        else:
            return "Error al modificar el expediente"
    else:
        return"expediente no encontrado o no vinculado"

@app.route('/registro_area',methods=['POST','GET'])    
def agregar_area():
    if request.method=='POST':
        nombre=request.form.get('nombre')
        descripcion=request.form.get('descripcion')
    
        crear_area(nombre,descripcion)
        return redirect('/casos')
    else:
        return render_template('/registro_area.html')   

@app.route('/tareas',methods=['POST','GET'])    
def listar_tareas():
    listar_tarea2=lista_de_tareas2()
    return render_template('/Tareas.html', tareas2=listar_tarea2)

@app.route('/notificaciones',methods=['POST','GET'])    
def listar_notificaciones():
    listar_record2=lista_de_recordatorio_all()
    return render_template('/recordatorio.html', record2=listar_record2)
    
@app.route('/registro_notificacion/<int:id_expediente>',methods=['GET'])    
def mostrar_registro_noti(id_expediente):
    return render_template('/registro_notificacion.html',id_expediente=id_expediente)

@app.route('/registro_notificacion/<int:id_expediente>',methods=['POST'])    
def registro_noti(id_expediente):
    mensaje=request.form.get('mensaje')
    fecha_limite=request.form.get('fecha_limite')
    estado="activo"
    id_expediente_asociado=request.form.get('id_expediente_asociado')
    prioridad=request.form.get('prioridad')
    if crear_notificacion(mensaje=mensaje,id_expediente_asociado= id_expediente,fecha_limite=fecha_limite,estado=estado,prioridad=prioridad):
        return redirect('/notificaciones')
    else:
        return "Error al agregar la notificacion"
    
@app.route('/registro_tarea/<int:id_expediente>',methods=['GET'])    
def mostrar_registro_tarea(id_expediente):
    return render_template('/registro_tarea.html',id_expediente=id_expediente)

@app.route('/registro_tarea/<int:id_expediente>',methods=['POST'])    
def registro_work(id_expediente):
    descripcion_tarea=request.form.get('descripcion_tarea')
    fecha_creacion=request.form.get('fecha_creacion')
    fecha_limite=request.form.get('fecha_limite')
    estado="No iniciado"
    id_expediente_tarea=request.form.get('id_expediente_asociado')
    prioridad=request.form.get('prioridad')
    if crear_tarea(descripcion_tarea,fecha_creacion,fecha_limite,estado,id_expediente_tarea=id_expediente,prioridad=prioridad):
        return redirect('/tareas')
    else:
        return "Error al agregar la notificacion"

@app.route('/modificar_tarea/<int:id_tarea>',methods=['GET'])
def mostrar_form_modificar_tarea(id_tarea):
    tarea=info_tarea_id(id_tarea)
    if tarea:
        return render_template('/form_modificar_tarea.html', tarea=tarea)
    else:
        return "Tarea no encontrada"

@app.route('/modificar_tarea/<int:id_tarea>',methods=['POST'])
def modificar_tarea_route(id_tarea):
    nueva_descripcion = request.form.get('nueva_descripcion')
    nueva_fc = request.form.get('nueva_fc')
    nueva_fl = request.form.get('nueva_fl')
    nueva_prioridad = request.form.get('nueva_prioridad')
    if modificar_tarea(id_tarea,nueva_descripcion,nueva_fc,nueva_fl,nueva_prioridad):
        return redirect('/tareas')
    else:
        return "Error al modificar la tarea"

@app.route('/eliminar_tarea/<int:id_tarea>',methods=['GET'])
def eliminar_tarea_route(id_tarea):
    if eliminar_tarea(id_tarea):      
        return redirect ('/tareas')
    else:
        return "Error al eliminar la tarea"
    
@app.route('/modificar_recordatorio/<int:id_notificacion>',methods=['GET'])
def mostrar_form_modificar_recordatorio(id_notificacion):
    recordatorio=info_noti_id(id_notificacion)
    if recordatorio:
        return render_template('/form_modificar_recordatorio.html', recordatorio=recordatorio)
    else:
        return "Recordatorio no encontrada"

@app.route('/modificar_recordatorio/<int:id_notificacion>',methods=['POST'])
def modificar_record_route(id_notificacion):
    nuevo_mensaje = request.form.get('nuevo_mensaje')
    nueva_fl = request.form.get('nueva_fl')
    nueva_prioridad = request.form.get('nueva_prioridad')
    if modificar_record(id_notificacion,nuevo_mensaje,nueva_fl,nueva_prioridad):
        return redirect('/notificaciones')
    else:
        return "Error al modificar el recordatorio"

@app.route('/eliminar_recordatorio/<int:id_notificacion>',methods=['GET'])
def eliminar_record_route(id_notificacion):
    if eliminar_record(id_notificacion):      
        return redirect ('/notificaciones')
    else:
        return "Error al eliminar el recordatorio"

@app.route('/estado_finalizado/<int:id_tarea>',methods=['POST'])
def cambiar_finalizado(id_tarea):
    nuevo_estado="Finalizado"
    if modificar_tarea_estado(id_tarea,nuevo_estado):
        #print(f"Tarea {id_tarea} cambiada a estado {nuevo_estado}")
        return redirect('/menu')
    else:
        #print("Error al cambiar el estado")
        return "Error"
    
@app.route('/estado_enproceso/<int:id_tarea>',methods=['POST'])
def cambiar_enproceso(id_tarea):
    nuevo_estado="En curso"
    if modificar_tarea_estado(id_tarea,nuevo_estado):
        #print(f"Tarea {id_tarea} cambiada a estado {nuevo_estado}")
        return redirect('/menu')
    else:
        #print("Error al cambiar el estado")
        return "Error"
    
@app.route('/estado_finalizado_record/<int:id_notificacion>',methods=['POST'])
def cambiar_finalizado_record(id_notificacion):
    nuevo_estado="Finalizado"
    if modificar_record_estado(id_notificacion,nuevo_estado):
        #print(f"Tarea {id_tarea} cambiada a estado {nuevo_estado}")
        return redirect('/menu')
    else:
        #print("Error al cambiar el estado")
        return "Error"
    
@app.route('/estado_pospuesto_record/<int:id_notificacion>',methods=['POST'])
def cambiar_pospuesto_record(id_notificacion):
    nuevo_estado="Pospuesto"
    if modificar_record_estado(id_notificacion, nuevo_estado):
        #print(f"Tarea {id_tarea} cambiada a estado {nuevo_estado}")
        return redirect('/menu')
    else:
        #print("Error al cambiar el estado")
        return "Error"

@app.route('/estado_cancelado_record/<int:id_notificacion>',methods=['POST'])
def cambiar_cancelado_record(id_notificacion):
    nuevo_estado="Cancelado"
    if modificar_record_estado(id_notificacion,nuevo_estado):
        #print(f"Tarea {id_tarea} cambiada a estado {nuevo_estado}")
        return redirect('/menu')
    else:
        #print("Error al cambiar el estado")
        return "Error"

@app.route('/modificar_area/<int:id_area>',methods=['GET'])
def mostrar_formulario_modificar_area(id_area):
    area=info_area_id(id_area)
    if area:
        return render_template('/form_modificar_area.html', area=area)
    else:
        return "Area no encontrado"

@app.route('/modificar_area/<int:id_area>',methods=['POST'])
def modificar_area_route(id_area):
    nuevo_nombre = request.form.get('nuevo_nombre')
    nueva_descripcion = request.form.get('nueva_descripcion')
    if modificar_area(id_area, nuevo_nombre, nueva_descripcion):
        return redirect('/areas')
    else:
        return "Error al modificar el area legal"

@app.route('/eliminar_area/<int:id_area>',methods=['GET'])
def eliminar_area_route(id_area):
    if eliminar_area(id_area):
        return redirect ('/areas')
    else:
        return "Error al eliminar el area"

@app.route('/areas',methods=['POST','GET'])    
def listar_areas_legal():
    lista_areas=listar_areas()
    return render_template('/lista_areas.html',areas=lista_areas)

@app.errorhandler(404)
def not_found(error=None):
    message = {
        'message': 'Resource Not Found ' + request.url,
        'status': 404
    }
    response = jsonify(message)
    response.status_code = 404
    return response

if __name__ == "__main__":
    app.run(port=5000)