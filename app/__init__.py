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

    if request.method == 'POST':
        name = request.form['name']
        lastname = request.form['lastname']
        email = request.form['email']
        password = request.form['password']

        if conn and cursor:
            try:
                cursor.execute("INSERT INTO users (name, lastname, email, password) VALUES (:name, :lastname, :email, :password)",
                               {"name": name, "lastname": lastname, "email": email, "password": password})
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
                return redirect(url_for('home'))
            else:
                error = "Invalid credentials. Please try again."
                return render_template('login.html', error=error)

    return render_template('login.html')

@app.errorhandler(404)
def not_found(e):
    return render_template('not_found.html'), 404

@app.route('/home')
def home():
    if 'user_id' in session:
        return render_template('home.html')
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