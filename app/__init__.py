
from datetime import datetime
from flask import Flask, render_template, request, redirect, url_for, session, abort
from config import DB_CONNECTION_STRING, SECRET_KEY, VAR_ENV_1, VAR_ENV_2, VAR_ENV_3
import cx_Oracle
import base64
import pdb


app = Flask(__name__)
app.secret_key = SECRET_KEY

# Configurar temporalmente las variables de entorno

VAR_ENV_1
VAR_ENV_2
VAR_ENV_3

def get_db_connection():
    try:
        connection = cx_Oracle.connect(DB_CONNECTION_STRING)
        cursor = connection.cursor()
        return connection, cursor
    except cx_Oracle.DatabaseError as e:
        error, = e.args
        if error.code == 1047:
            print("DPI-1047: No se pudo encontrar la biblioteca del cliente de Oracle. Verifica la configuración.")
        else:
            print(f"Error de base de datos: {error}")
        return None, None

def close_db_connection(connection, cursor):
    if cursor:
        cursor.close()
    if connection:
        connection.close()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    conn, cursor = get_db_connection()
    rol = 2

    if request.method == 'POST':
        name = request.form['name']
        lastname = request.form['lastname']
        email = request.form['email']
        password = request.form['password']

        #Modifica la variable rol 
          # Rol 1 es Admin 
          # Role 2 es Usuario

        if "@admin.com" in email: 
            rol=1

        if conn and cursor:
            try:
                cursor.execute("INSERT INTO users (name, lastname, email, password, id_rol) VALUES (:name, :lastname, :email, :password, :rol)",
                               {"name": name, "lastname": lastname, "email": email, "password": password, "rol": rol})
                conn.commit()
                return redirect(url_for('login'))
            except cx_Oracle.IntegrityError as e:
                conn.rollback()
                error = "User already registered"
                return render_template('signup.html', error=error)
            except Exception as e:
                conn.rollback()
                error = "Failed to register user"
                return render_template('signup.html', error=error)
            finally:
                close_db_connection(conn, cursor)

    return render_template('signup.html')

# LOGIN 

@app.route('/login', methods=['GET', 'POST'])
def login():
    conn, cursor = get_db_connection()

    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        if conn and cursor:
            cursor.execute("SELECT * FROM users WHERE email = :email AND password = :password",
                           {"email": email, "password": password})
            user = cursor.fetchone()

            if user:
                session['user_id'] = user[0]
                session['id_rol'] =  user[5] #Campo del role

                #Condicional rol 
                if session['id_rol'] ==1:
                    return redirect(url_for('admin'))
                elif session ['id_rol'] ==2:
                    return redirect(url_for('home'))
            
            else:
                error = "Invalid credentials. Please try again."
                return render_template('login.html', error=error)

    return render_template('login.html')

@app.errorhandler(404)
def not_found(e):
    return render_template('notFound.html'), 404



#ROLES 

from functools import wraps
from flask import session, flash, redirect, url_for

def role_required(required_role):
    def decorator(func):
        @wraps(func)
        def decorated_function(*args, **kwargs):
            if 'id_rol' in session and session['id_rol'] == required_role:
                return func(*args, **kwargs)
            else:
                flash('You do not have the required permissions to access this page.', 'danger')
                return redirect('/')
        return decorated_function
    return decorator


#USER HOMEPAGE
@app.route('/home')
@role_required(required_role=2)
def home():
    if 'user_id' in session:
        return render_template('home.html')
    else:
        abort(404)


#ADMIN HOMEPAGE
@app.route('/admin')
@role_required(required_role=1)
def admin():
    if 'user_id' in session:
        return render_template('admin.html')
    else:
        abort(404)



#LOGOUT

@app.route('/logout')
def logout():
    session.pop('user_id', None)
    return redirect(url_for('login'))

@app.route('/facturas')
def facturas():
    conn, cursor = get_db_connection()

    # Obtener la lista de facturas desde la base de datos
    cursor.execute("SELECT * FROM Factura")
    
    # Obtener los nombres de las columnas
    columnas = [i[0] for i in cursor.description]

    facturas_list = cursor.fetchall()  # Obtener la lista de facturas

    close_db_connection(conn, cursor)

    return render_template('facturas.html', facturas=facturas_list, columnas=columnas)

@app.route('/factura/agregar', methods=['POST'])
def agregar_factura():
    conn, cursor = get_db_connection()

    if request.method == 'POST':
        fecha = request.form['fecha']
        id_cliente = request.form['id_cliente']
        total = request.form['total']

        # Llamar al bloque PL/SQL para insertar una nueva factura
        cursor.callproc("insertar_nueva_factura", [fecha, id_cliente, total])
        conn.commit()

    close_db_connection(conn, cursor)

    return redirect(url_for('facturas'))

    return redirect(url_for('facturas'))

@app.route('/factura/editar/<int:id_factura>')
def editar_factura(id_factura):
    conn, cursor = get_db_connection()

    # Obtener la factura por su ID desde la base de datos
    cursor.execute("SELECT * FROM Factura WHERE id_factura = :id", {"id": id_factura})
    factura = cursor.fetchone()

    close_db_connection(conn, cursor)

    return render_template('editar_factura.html', factura=factura)

@app.route('/factura/actualizar/<int:id_factura>', methods=['POST'])
def actualizar_factura(id_factura):
    conn, cursor = get_db_connection()

    if request.method == 'POST':
        total = request.form['total']

        # Llamar al bloque PL/SQL para actualizar una factura
        cursor.callproc("actualizar_factura", [id_factura, total])
        conn.commit()

    close_db_connection(conn, cursor)

    return redirect(url_for('facturas'))

@app.route('/factura/eliminar/<int:id_factura>')
def eliminar_factura(id_factura):
    conn, cursor = get_db_connection()

    # Llamar al bloque PL/SQL para eliminar una factura
    cursor.callproc("eliminar_factura", [id_factura])
    conn.commit()

    close_db_connection(conn, cursor)

    return redirect(url_for('facturas'))

    #reservaciones
#@app.route('/reservaciones', methods=['POST'])
#def reservaciones():
   # reserva_id = request.form['reserva_id']
  #  nombre = request.form['nombre']
 #   fecha = request.form['fecha']

    # Ejecutar un bloque PL/SQL para realizar la reserva en la base de datos
#    conn, cursor = get_db_connection()
#    try:
#        cursor.execute(
#           """ BEGIN
#                -- Tu bloque PL/SQL para realizar la reserva
#                -- Puedes usar las variables :reserva_id, :nombre, :fecha en el bloque PL/SQL
#            END;
#        """,# {'reserva_id': reserva_id, 'nombre': nombre, 'fecha': fecha})
#        conn, cursor = get_db_connection()
#        mensaje = 'Reserva exitosa'
#    except cx_Oracle.DatabaseError as e:
#        error, = e.args
#        mensaje = f'Error en la reserva: {error.message}'

#    return render_template('reservaciones.html')

#@app.route('/reservaciones')
#def reservaciones():
 #   conn, cursor = get_db_connection()

    # Obtener la lista de reservaciones desde la base de datos
  #  cursor.execute("SELECT * FROM Reservaciones")
    

   # reservaciones_list = cursor.fetchall()  # Obtener la lista de reservaciones

    #close_db_connection(conn, cursor)

    #return render_template('reservaciones.html', reservaciones=reservaciones_list)


# Pagos
@app.route('/pagos')

def pagos():
    conn, cursor = get_db_connection()
    cursor.execute("SELECT * FROM Pagos")
    pagos = cursor.fetchall()
    return render_template('pagos.html', pagos=pagos)


@app.route('/agregar', methods=['POST'])
def agregar():
    conn, cursor = get_db_connection()
    if request.method == 'POST':
        id_pago = request.form['id_pago']
        id_factura = request.form['id_factura']
        metodo_pago = request.form['metodo_pago']
        monto_pagado = request.form['monto_pagado']
        fecha_hora_pago_str = request.form['fecha_hora_pago']

        # Convertir la cadena de fecha a un objeto datetime de Python
        fecha_hora_pago = datetime.strptime(fecha_hora_pago_str, '%Y-%m-%dT%H:%M')

        # Llamar al procedimiento almacenado para insertar un pago
        cursor.callproc("insertar_pago", (id_pago, id_factura, metodo_pago, monto_pagado, fecha_hora_pago))
        conn.commit()

    return redirect('/pagos')


@app.route('/actualizar', methods=['POST'])
def actualizar():
    conn, cursor = get_db_connection()
    if request.method == 'POST':
        id_pago = request.form['id_pago']
        metodo_pago = request.form['metodo_pago']
        monto_pagado = float(request.form['monto_pagado']) 
        fecha_hora_pago = request.form['fecha_hora_pago']
        

        # Llamar al procedimiento almacenado para actualizar un pago
        cursor.callproc("actualizar_pago", (id_pago, metodo_pago, monto_pagado, fecha_hora_pago))
        conn.commit()

    return redirect('/pagos')

@app.route('/eliminar/<int:id_pago>')
def eliminar(id_pago):
    conn, cursor = get_db_connection()
    # Llamar al procedimiento almacenado para eliminar un pago
    cursor.callproc("eliminar_pago", (id_pago,))
    conn.commit()

    return redirect('/pagos')

if __name__ == '__main__':
    app.run(debug=True)


# Empleados 
@app.route('/empleados')
def mostrar_empleados():
    conn, cursor = get_db_connection()
    cursor.execute("SELECT * FROM empleados")
    empleados = cursor.fetchall()
    return render_template('empleados.html', empleados=empleados)

@app.route('/crear_empleado', methods=['GET', 'POST'])
def crear_empleado():
    conn, cursor = get_db_connection()
    if request.method == 'POST':
        # Obtener datos del formulario
        id_empleado = request.form['id_empleado']
        nombre = request.form['nombre']
        apellido = request.form['apellido']
        direccion = request.form['direccion']
        telefono = request.form['telefono']
        puesto = request.form['puesto']

        # Convertir la fecha al formato adecuado
        fecha_contratacion_str = request.form['fecha_contratacion']
        fecha_contratacion = datetime.strptime(fecha_contratacion_str, '%Y-%m-%d').date()

        id_usuario = request.form['id_usuario']

        # Ejecutar el procedimiento PL/SQL para crear empleado
        cursor.callproc('crear_empleado', [id_empleado, nombre, apellido, direccion, telefono, puesto, fecha_contratacion, id_usuario])
        conn.commit()

        return redirect('/empleados')
    return render_template('empleados.html')

@app.route('/editar_empleado/<int:id_empleado>', methods=['GET', 'POST'])
def editar_empleado(id_empleado):
    conn, cursor = get_db_connection()

    if request.method == 'POST':
        # Obtener datos del formulario
        nombre = request.form['nombre']
        apellido = request.form['apellido']
        direccion = request.form['direccion']
        telefono = request.form['telefono']
        puesto = request.form['puesto']
        fecha_contratacion = request.form['fecha_contratacion']
        id_usuario = request.form['id_usuario']

        # Ejecutar el procedimiento PL/SQL para editar empleado
        cursor.callproc('editar_empleado', [id_empleado, nombre, apellido, direccion, telefono, puesto, fecha_contratacion, id_usuario])
        conn.commit()

        return redirect('/empleados')

    # Obtener los detalles del empleado para mostrar en el formulario
    cursor.execute("SELECT * FROM empleados WHERE id_empleado = :id", {'id': id_empleado})
    empleado = cursor.fetchone()

    formatted_fecha_contratacion = datetime.strftime(empleado[6], '%Y-%m-%d')

    return render_template('editar_empleado.html', empleado=empleado)


@app.route('/guardar_edicion/<int:id_empleado>', methods=['POST'])
def guardar_edicion(id_empleado):
    conn, cursor = get_db_connection()

    if request.method == 'POST':
        # Obtener datos del formulario
        nombre = request.form['nombre']
        apellido = request.form['apellido']
        direccion = request.form['direccion']
        telefono = request.form['telefono']
        puesto = request.form['puesto']
        fecha_contratacion_str = request.form['fecha_contratacion']
        fecha_contratacion = datetime.strptime(fecha_contratacion_str, '%Y-%m-%d').date()
        id_usuario = request.form['id_usuario']

        # Ejecutar el procedimiento PL/SQL para guardar la edición del empleado
        cursor.callproc('editar_empleado', [id_empleado, nombre, apellido, direccion, telefono, puesto, fecha_contratacion, id_usuario])
        conn.commit()

        return redirect('/empleados')

    return render_template('editar_empleado.html', empleado=empleado)

# Ruta para eliminar un empleado
@app.route('/eliminar_empleado/<int:id_empleado>')
def eliminar_empleado(id_empleado):
    conn, cursor = get_db_connection()
    cursor.callproc('eliminar_empleado', [id_empleado])
    conn.commit()
    return redirect('/empleados')

if __name__ == '__main__':
    app.run(debug=True)


#***************************PROMOS******************************

#PROMOS PERMISOS | ROLES

#@app.route('/promos')
#@role_required(required_role=2)
#def promo():
#    if 'user_id' in session:
#        return render_template('promos.html')
#    else:
#        abort(404)


    

# Listar proveedores
@app.route('/proveedores')

def listar_proveedores():
    conn, cursor = get_db_connection()

    try:
        cursor.execute("SELECT * FROM Proveedor")
        proveedores = cursor.fetchall()
        return render_template('proveedores.html', proveedores=proveedores)
    finally:
        # Asegúrate de cerrar la conexión en el bloque finally
        cursor.close()
        conn.close()

# Crear proveedor
@app.route('/crear', methods=['POST'])
def crear_proveedor():
    if request.method == 'POST':
        conn, cursor = get_db_connection()
        # Obtener datos del formulario
        id_proveedor = request.form['id_proveedor']
        nombre_empresa = request.form['nombre_empresa']
        nombre_contacto = request.form['nombre_contacto']
        telefono = request.form['telefono']
        correo_electronico = request.form['correo_electronico']

        # Llamar al procedimiento PL/SQL para crear un proveedor
        cursor.callproc('CrearProveedor', [id_proveedor, nombre_empresa, nombre_contacto, telefono, correo_electronico])
        conn.commit()

    return redirect(url_for('listar_proveedores'))

# Actualizar proveedor
@app.route('/actualizar/<int:id_proveedor>', methods=['POST'])
def actualizar_proveedor(id_proveedor):
    conn, cursor = get_db_connection()
    if request.method == 'POST':
        # Obtener datos del formulario
        nuevo_nombre_empresa = request.form['nuevo_nombre_empresa']
        nuevo_nombre_contacto = request.form['nuevo_nombre_contacto']
        nuevo_telefono = request.form['nuevo_telefono']
        nuevo_correo_electronico = request.form['nuevo_correo_electronico']

        # Llamar al procedimiento PL/SQL para actualizar un proveedor
        cursor.callproc('ActualizarProveedor', [id_proveedor, nuevo_nombre_empresa, nuevo_nombre_contacto, nuevo_telefono, nuevo_correo_electronico])
        conn.commit()

    return redirect(url_for('listar_proveedores'))

# Eliminar proveedor
@app.route('/eliminar_proveedor/<int:id_proveedor>')
def eliminar_proveedor(id_proveedor):
    conn, cursor = get_db_connection()
    # Llamar al procedimiento PL/SQL para eliminar un proveedor
    cursor.callproc('EliminarProveedor', [id_proveedor])
    conn.commit()

    return redirect(url_for('listar_proveedores'))

if __name__ == '__main__':
    app.run(debug=True)




# -----------------    PROMOCIONES    ----------------

#Formulario Promociones
@app.route('/admin/agregarPromo' ,methods = ['GET', 'POST'])
@role_required(required_role=1)
def file_upload ():
    conn, cursor = get_db_connection()
    

    if request.method == 'POST':
        #id = request.form ['id']
        titulo = request.form ['titulo']
        descripcion = request.form ['descripcion']
        fecha = request.form ['fecha']
        archivo = request.files['archivo'].read()

        if conn and cursor:
            try: 
                cursor.execute("INSERT INTO Promociones (titulo, descripcion, fecha, archivo)VALUES ( :titulo, :descripcion, :fecha, :archivo)",
                   {"titulo":titulo, "descripcion":descripcion,"fecha":fecha, "archivo":archivo })
                conn.commit()
                return redirect('/admin')
            except Exception as e:
                conn.rollback()
                error = "Failed to add promo"
                return render_template('promoForm.html', error = error)
            finally:
                close_db_connection(conn,cursor)
    return render_template('promoForm.html')

@app.route('/admin/promociones')
def mostrarpro():
    conn, cursor = get_db_connection()

    if conn and cursor:
        try:
            # Obtener datos de promociones desde la base de datos
            cursor.execute("SELECT * FROM Promociones")
            promociones = cursor.fetchall()
            
            for i in range(len(promociones)):
                promo_data = list(promociones[i])
                promo_data[4] = base64.b64encode(promo_data[4].read()).decode('utf-8')
                promociones[i] = promo_data

            # Renderizar la plantilla con los datos
            return render_template('promociones.html', promociones=promociones)
        except Exception as e:
            # Manejar errores si es necesario
            error = "Failed to fetch promotions"
            return render_template('promociones.html', error=error)
        finally:
            close_db_connection(conn, cursor)

    return render_template('promociones.html')


@app.route('/promos')
def mostrarprou():
    conn, cursor = get_db_connection()

    if conn and cursor:
        try:
            # Obtener datos de promociones desde la base de datos
            cursor.execute("SELECT * FROM Promociones")
            promociones = cursor.fetchall()
            
            for i in range(len(promociones)):
                promo_data = list(promociones[i])
                promo_data[4] = base64.b64encode(promo_data[4].read()).decode('utf-8')
                promociones[i] = promo_data

            # Renderizar la plantilla con los datos
            return render_template('promos.html', promociones=promociones)
        except Exception as e:
            # Manejar errores si es necesario
            error = "Failed to fetch promotions"
            return render_template('promos.html', error=error)
        finally:
            close_db_connection(conn, cursor)

    return render_template('promos.html')


@app.route('/eliminar_promo/<string:id>')
def eliminar_promo(id):
    conn, cursor = get_db_connection()
    cursor.callproc('eliminar_promo', [id])
    conn.commit()
    return redirect('/admin/promociones')


@app.route('/editarpromo/<string:id>', methods=['GET', 'POST'])
def editarpromo(id):
    conn, cursor = get_db_connection()

    if request.method == 'POST':
        # Obtener datos del formulario
        #id = request.form['id']
        titulo = request.form['titulo']
        descripcion = request.form['descripcion']
        fecha = request.form['fecha']
        archivo = request.files['archivo'].read()

        # Ejecutar el procedimiento PL/SQL para editar 
        cursor.callproc('editar_promo', [id,titulo, descripcion, fecha, archivo])
        conn.commit()

        return redirect('/admin/promociones')

    # Obtener los detalles del empleado para mostrar en el formulario
    cursor.execute("SELECT * FROM promociones WHERE id = :id", {'id': id})
    promociones = cursor.fetchone()


    return render_template('editarpromo.html', promociones=promociones)

#*************************** END PROMOS******************************

#************************** INGREDIENTES ****************************

@app.route('/ingredientes')
@role_required(required_role=1)
def ingredientes():
    if 'user_id' in session:
        return render_template('/ingredientes/ingredientes.html')
    else:
        abort(404)

#listar ingredientes
@app.route('/tablaingredientes')

def listar_ingre():
    conn, cursor = get_db_connection()

    try:
        cursor.execute("SELECT * FROM Ingredientes")
        ingredientes = cursor.fetchall()
        return render_template('/ingredientes/ingrediente.html', ingredientes=ingredientes)
    finally:
        # Asegúrate de cerrar la conexión en el bloque finally
        cursor.close()
        conn.close()

#eliminar ingredientes
@app.route('/eliminar_ingrediente/<int:id_in>')
def eliminar_ingrediente(id_in):
    conn, cursor = get_db_connection()
    cursor.callproc('eliminar_ingrediente', [id_in])
    conn.commit()
    return redirect('/tablaingredientes')


#editar ingredientes 
@app.route('/editaringrediente/<int:id_in>', methods=['GET', 'POST'])
def editaringrediente(id_in):
    conn, cursor = get_db_connection()

         #obtener la lista de proveedores
    cursor.execute ("SELECT * from proveedor")
    proveedores = cursor.fetchall()

    if request.method == 'POST':
        # Obtener datos del formulario
       # id_in = request.form['id_in']
        nombre_in = request.form['nombre_in']
        proveedor_selected = request.form ['proveedor']
        precio = request.form['precio']

        # Ejecutar el procedimiento PL/SQL para editar 
        cursor.callproc('editar_ingrediente', [id_in,nombre_in, proveedor_selected, precio])
        conn.commit()

        return redirect('/tablaingredientes')

    # Obtener los detalles del empleado para mostrar en el formulario
    cursor.execute("SELECT * FROM ingredientes WHERE id_in = :id_in", {'id_in': id_in})
    ingrediente = cursor.fetchone()


    return render_template('/ingredientes/editaringred.html', proveedores=proveedores, ingrediente=ingrediente)

#agregar ingredientes
@app.route('/admin/addingrediente' ,methods = ['GET', 'POST'])
@role_required(required_role=1)
def agregar_ingre ():
    conn, cursor = get_db_connection()

     #obtener la lista de proveedores
    cursor.execute ("SELECT * from proveedor")
    proveedores = cursor.fetchall()
    

    if request.method == 'POST':
        #id_in = request.form['id_in']
        nombre_in = request.form['nombre']
        proveedor = request.form['proveedor']
        precio = request.form['precio']
       

        if conn and cursor:
            try: 
                #pdb.set_trace()
                #llamar SP
                
                cursor.callproc("INSERT_INGREDIENTE", [ nombre_in,proveedor, precio])
                conn.commit()
                return redirect('/admin')
            except Exception as e:
                conn.rollback()
                error = "Failed to add ingrediente"
                print(f"Error: {e}")
                return render_template('/ingredientes/ingreform.html', error = error, proveedores= proveedores)
            finally:
                close_db_connection(conn,cursor)
    return render_template('/ingredientes/ingreform.html', proveedores= proveedores)

#************************* END INGREDIENTES *************************

#platillos
@app.route('/platillos')
def listar_platillos():
    conn, cursor = get_db_connection()
    cursor.execute("SELECT * FROM Platillos")
    platillos = cursor.fetchall()
    close_db_connection(conn, cursor)
    return render_template('platillos.html', platillos=platillos)

@app.route('/platillo/agregar', methods=['POST'])
def agregar_platillo():
    conn, cursor = get_db_connection()
    if request.method == 'POST':
        id_platillo = request.form['id_platillo']
        nombre = request.form['nombre']
        descripcion = request.form['descripcion']
        precio = request.form['precio']
        tipo_platillo = request.form['tipo_platillo']

        cursor.callproc("InsertarPlatillo", [id_platillo, nombre, descripcion, precio, tipo_platillo])
        conn.commit()


    return redirect(url_for('listar_platillos'))

@app.route('/platillo/editar/<int:id_platillo>', methods=['GET', 'POST'])
def editar_platillo(id_platillo):
    conn, cursor = get_db_connection()
    cursor.execute("SELECT * FROM Platillos WHERE IDPlatillo = :id", {'id': id_platillo})
    platillo = cursor.fetchone()

    if request.method == 'POST':
        nombre = request.form['nombre']
        descripcion = request.form['descripcion']
        precio = request.form['precio']
        tipo_platillo = request.form['tipo_platillo']

        cursor.callproc("ActualizarPlatillo", [id_platillo, nombre, descripcion, precio, tipo_platillo])
        conn.commit()

        close_db_connection(conn, cursor)
        return redirect(url_for('listar_platillos'))

    
    return render_template('platillos.html', platillos=[platillo])

@app.route('/platillo/eliminar/<int:id_platillo>')
def eliminar_platillo(id_platillo):
    conn, cursor = get_db_connection()
    cursor.callproc("EliminarPlatillo", [id_platillo])
    conn.commit()

    close_db_connection(conn, cursor)
    return redirect(url_for('listar_platillos'))

if __name__ == '__main__':
    app.run(debug=True)

#mesas

@app.route('/mesas')
def listar_mesas():
    conn, cursor = get_db_connection()
    cursor.execute("SELECT * FROM Mesas")
    mesas = cursor.fetchall()
    close_db_connection(conn, cursor)
    return render_template('mesas.html', mesas=mesas)

@app.route('/mesa/agregar', methods=['POST'])
def agregar_mesa():
    conn, cursor = get_db_connection()
    if request.method == 'POST':
        numero_mesa = request.form['numero_mesa']
        capacidad = request.form['capacidad']

        with conn.cursor() as cursor:
            cursor.execute("INSERT INTO Mesas (ID_DE_MESA, NUMERO_DE_MESA, CAPACIDAD) VALUES (SEQ_MESAS.NEXTVAL, :1, :2)",
                           (numero_mesa, capacidad))
            conn.commit()

    return redirect(url_for('listar_mesas'))

@app.route('/mesa/editar/<int:id_mesa>', methods=['GET', 'POST'])
def editar_mesa(id_mesa):
    conn, cursor = get_db_connection()
    if request.method == 'POST':
        numero_mesa = request.form['numero_mesa']
        capacidad = request.form['capacidad']

        with conn.cursor() as cursor:
            cursor.execute("UPDATE Mesas SET NUMERO_DE_MESA = :1, CAPACIDAD = :2 WHERE ID_DE_MESA = :3",
                           (numero_mesa, capacidad, id_mesa))
            conn.commit()

        return redirect(url_for('listar_mesas'))

    with conn.cursor() as cursor:
        cursor.execute("SELECT * FROM Mesas WHERE ID_DE_MESA = :1", (id_mesa,))
        mesa = cursor.fetchone()

    return render_template('mesas.html', mesas=[mesa])

@app.route('/mesa/eliminar/<int:id_mesa>')
def eliminar_mesa(id_mesa):
    conn, cursor = get_db_connection()
    with conn.cursor() as cursor:
        cursor.execute("DELETE FROM Mesas WHERE ID_DE_MESA = :1", (id_mesa,))
        conn.commit()

   
    return redirect(url_for('listar_mesas'))

# ************* PEDIDOS *************
@app.route('/pedidos')
def pedidos():
    return render_template('pedidos.html')

def obtener_proximo_id_pedido():
    # Función para obtener el próximo ID_pedido disponible
    conn, cursor = get_db_connection()
    cursor.execute("SELECT MAX(ID_pedido) FROM Pedidos")
    result = cursor.fetchone()[0]
    cursor.close()
    conn.close()
    return result + 1 if result else 1

# CREATE
@app.route('/crear_pedido', methods=['GET', 'POST'])
def crear_pedido():
    if request.method == 'POST':
        # Obtener el próximo ID_pedido disponible
        id_pedido = obtener_proximo_id_pedido()

        fecha_hora_pedido = datetime.now()
        estado_pedido = request.form['estado_pedido']
        id_cliente = request.form['id_cliente']
        id_empleado = request.form['id_empleado']

        conn, cursor = get_db_connection()
        cursor.callproc('Insertar_Pedido', [id_pedido, fecha_hora_pedido, estado_pedido, id_cliente, id_empleado])
        cursor.close()
        conn.commit()

        # Después de crear el pedido, renderizar el formulario de nuevo
        return render_template('crear_pedido.html')

    # Si es una solicitud GET, simplemente renderizar el formulario
    return render_template('crear_pedido.html')


# READ
@app.route('/listar_pedidos')
def listar_pedidos():
    conn, cursor = get_db_connection()

    result_cursor = cursor.var(cx_Oracle.CURSOR)
    cursor.execute("BEGIN OPEN :result_cursor FOR SELECT * FROM Pedidos; END;", result_cursor=result_cursor)

    result = result_cursor.getvalue().fetchall()

    cursor.close()
    conn.close()

    return render_template('listar_pedidos.html', pedidos=result)


# UPDATE
@app.route('/editar_pedido/<int:id_pedido>', methods=['GET', 'POST'])
def editar_pedido(id_pedido):
    conn, cursor = get_db_connection()
    pedido = cursor.execute('SELECT * FROM Pedidos WHERE ID_pedido = :id', {'id': id_pedido}).fetchone()
    cursor.close()

    if request.method == 'POST':
        fecha_hora_pedido = pedido[1]
        estado_pedido = request.form['estado_pedido']
        id_cliente = request.form['id_cliente']
        id_empleado = request.form['id_empleado']

        conn, cursor = get_db_connection()
        cursor.callproc('Actualizar_Pedido', [id_pedido, fecha_hora_pedido, estado_pedido, id_cliente, id_empleado])
        cursor.close()
        conn.commit()

        return redirect(url_for('listar_pedidos'))

    return render_template('editar_pedido.html', pedido=pedido)

# DELETE
@app.route('/eliminar_pedido/<int:id_pedido>')
def eliminar_pedido(id_pedido):
    conn, cursor = get_db_connection()
    cursor.callproc('Eliminar_Pedido', [id_pedido])
    cursor.close()
    conn.commit()

    return redirect(url_for('listar_pedidos'))


# ***** CRUD RESENAS *****
@app.route('/resenas')
def mostrar_resenas():
    connection, cursor = get_db_connection()
    if connection:
        try:
            resenas_cursor = cursor.callfunc('obtener_resenas', cx_Oracle.CURSOR)
            resenas = resenas_cursor.fetchall()
            return render_template('resenas.html', resenas=resenas)
        finally:
            close_db_connection(connection, cursor)

@app.route('/insertar_resena', methods=['POST'])
def insertar_resena():
    if request.method == 'POST':
        comentario = request.form['comentario']
        calificacion = int(request.form['calificacion'])
        fecha_resena = datetime.now()
        id_cliente = int(request.form['id_cliente'])

        connection, cursor = get_db_connection()
        if connection:
            try:
                cursor.callproc('insertar_resena', [comentario, calificacion, fecha_resena, id_cliente])
                return redirect(url_for('mostrar_resenas'))
            except cx_Oracle.IntegrityError as e:
                error, = e.args
                if error.code == 2291:
                    # Manejar el error de clave foránea no encontrada
                    return render_template('error.html', message="ID Cliente no encontrado.")
                else:
                    raise
            finally:
                close_db_connection(connection, cursor)

@app.route('/actualizar_resena/<int:id_resena>', methods=['POST'])
def actualizar_resena(id_resena):
    if request.method == 'POST':
        comentario = request.form['comentario']
        calificacion = int(request.form['calificacion'])
        fecha_resena = datetime.now()

        connection, cursor = get_db_connection()
        if connection:
            try:
                cursor.callproc('actualizar_resena', [id_resena, comentario, calificacion, fecha_resena])
                return redirect(url_for('mostrar_resenas'))
            finally:
                close_db_connection(connection, cursor)

@app.route('/eliminar_resena/<int:id_resena>')
def eliminar_resena(id_resena):
    connection, cursor = get_db_connection()
    if connection:
        try:
            cursor.callproc('eliminar_resena', [id_resena])
            return redirect(url_for('mostrar_resenas'))
        finally:
            close_db_connection(connection, cursor)


if __name__ == '__main__':
    app.run(debug=True)

##reservaciones
@app.route('/reservaciones')
def listar_reservaciones():
    conn, cursor = get_db_connection()
    cursor = conn.cursor()

    # Obtener todas las reservaciones
    cursor.execute('SELECT * FROM Reservaciones')
    reservaciones = cursor.fetchall()

    cursor.close()
    conn.close()

    return render_template('reservaciones.html', reservaciones=reservaciones)

@app.route('/crearreservacion', methods=['GET', 'POST'])
def crear_reservacion():
    if request.method == 'POST':
        conn, cursor = get_db_connection()
        cursor = conn.cursor()

        # Obtener datos del formulario
        id_reservacion = request.form['id_reservacion']
        fecha_hora = request.form['fecha_hora']
        numero_personas = request.form['numero_personas']

        # Convertir la cadena de fecha y hora a un objeto datetime
        fecha_hora = datetime.strptime(fecha_hora, '%Y-%m-%dT%H:%M')

        # Lógica para crear una nueva reservación
        cursor.callproc('insertar_reservacion', [id_reservacion, fecha_hora, numero_personas])
        conn.commit()

        cursor.close()
        conn.close()

        return redirect(url_for('listar_reservaciones'))

    return render_template('reservaciones.html')


@app.route('/editarreservacion/<int:id_reservacion>', methods=['GET', 'POST'])
def editar_reservacion(id_reservacion):
    conn, cursor = get_db_connection()
    cursor = conn.cursor()

    # Obtener datos de la reservación a editar
    cursor.callfunc('obtener_reservacion',[id_reservacion])
    reservacion = cursor.fetchone()

    if request.method == 'POST':
        # Obtener nuevos datos del formulario
        nueva_fecha_hora = request.form['nueva_fecha_hora']
        nuevo_numero_personas = request.form['nuevo_numero_personas']

        # Lógica para actualizar la reservación
        cursor.callproc('actualizar_reservacion', [id_reservacion, nueva_fecha_hora, nuevo_numero_personas])
        conn.commit()

        cursor.close()
        conn.close()

        return redirect(url_for('listar_reservaciones'))

    cursor.close()
    conn.close()

    return render_template('reservaciones.html', reservacion=reservacion)

@app.route('/eliminarreservacion/<int:id_reservacion>')
def eliminar_reservacion(id_reservacion):
    conn, cursor = get_db_connection()
    cursor = conn.cursor()

    # Lógica para eliminar la reservación
    cursor.callproc('eliminar_reservacion', [id_reservacion])
    conn.commit()

    cursor.close()
    conn.close()

    return redirect(url_for('listar_reservaciones'))

#if __name__ == '__main__':
#    app.run(debug=True)



## ------------   DETALLES DEL PEDIDO   --------------
@app.route('/detallespedido' , methods=['GET', 'POST'])
@role_required(required_role=1)
def detalles_pedido():
    conn, cursor = get_db_connection()
    try:
        if request.method == 'POST':
            search_term = request.form['search_term']
            resultado = cursor.var(cx_Oracle.CURSOR)
            cursor.callproc("buscar_platillos", [search_term, resultado])
            detalles_pedidos_cursor = resultado.getvalue()
            detalles_pedidos = detalles_pedidos_cursor.fetchall()

        else:
            resultado = cursor.var(cx_Oracle.CURSOR)
            cursor.callproc("ObtenerDetallesPedidos" , [resultado])
            detalles_pedidos_cursor = resultado.getvalue()
            detalles_pedidos = detalles_pedidos_cursor.fetchall()
            print(f"detalles_pedidos : {detalles_pedidos}")
        
        return render_template('detallespedido.html', detalles_pedidos=detalles_pedidos)
    except Exception as e:
        error = "Failed to fetch details of orders"
        print(f"Error: {e}")
        return render_template('detallespedido.html', error=error)
       
    finally:
        close_db_connection(conn, cursor)

        #cursor.execute("select * from detallespedido")

        #cursor.execute( """
        #SELECT dp.id_dt, ped.id_pedido, p.nombre, p.descripcion, p.tipoplatillo
        #FROM detallespedido dp
        #JOIN platillos p ON dp.id_platillo = p.idplatillo
        #JOIN pedidos ped ON dp.id_pedido = ped.id_pedido
        #ORDER BY ped.Fecha_hora_pedido DESC
        # """)

@app.route('/eliminar_detalle_pedido/<int:id_dt>')
@role_required(required_role=1)
def eliminar_detalle_pedido(id_dt):
    conn, cursor = get_db_connection()
    #id_dt = request.form['id_dt']
    cursor.callproc("eliminar_detalle_pedido", [id_dt])
    conn.commit()
    close_db_connection(conn,cursor)
    return redirect(url_for('detalles_pedido'))
    
    