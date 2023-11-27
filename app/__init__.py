
from datetime import datetime
from flask import Flask, render_template, request, redirect, url_for, session, abort
from config import DB_CONNECTION_STRING, SECRET_KEY, VAR_ENV_1, VAR_ENV_2, VAR_ENV_3
import cx_Oracle


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
                return redirect(url_for('/'))
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

#PROMOS
@app.route('/promos')
@role_required(required_role=2)
def promo():
    if 'user_id' in session:
        return render_template('promos.html')
    else:
        abort(404)


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

@app.route('/reservaciones')
def reservaciones():
    conn, cursor = get_db_connection()

    # Obtener la lista de reservaciones desde la base de datos
    cursor.execute("SELECT * FROM Reservaciones")
    

    reservaciones_list = cursor.fetchall()  # Obtener la lista de reservaciones

    close_db_connection(conn, cursor)

    return render_template('reservaciones.html', reservaciones=reservaciones_list)


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







# print("************* TEST ---------")

# @app.route('/')
# def index():
#     # Aquí puedes realizar consultas a la base de datos Oracle
#     cursor = conn.cursor()
#     cursor.execute('SELECT * FROM NOMBRES')
#     data = cursor.fetchall()
#     cursor.close()

#     return render_template('index.html', data=data)

# @app.route('/get_names')
# def get_names():
#     cursor = conn.cursor()
#     cursor.execute("SELECT NOMBRE FROM NOMBRES")
#     data = cursor.fetchall()
#     cursor.close()

#     return jsonify(data)

# @app.route('/signin')
# def signin():
#     return render_template('signin.html')