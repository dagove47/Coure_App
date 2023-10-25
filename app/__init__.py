from flask import Flask, render_template, request, redirect, url_for, session
from config import DB_CONNECTION_STRING, SECRET_KEY
import cx_Oracle

app = Flask(__name__)
app.secret_key = SECRET_KEY

conn = cx_Oracle.connect(DB_CONNECTION_STRING)

cursor = conn.cursor()


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']

        cursor.execute("INSERT INTO users (username, email, password) VALUES (:username, :email, :password)",
                       {"username": username, "email": email, "password": password})
        conn.commit()
        return redirect(url_for('login'))
    return render_template('signup.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        cursor.execute("SELECT * FROM users WHERE username = :username AND password = :password",
                       {"username": username, "password": password})
        user = cursor.fetchone()

        if user:
            session['user_id'] = user[0]
            return redirect(url_for('home'))
        else:
            error = "Invalid credentials. Please try again."
            return render_template('login.html', error=error)

    return render_template('login.html')


@app.route('/home')
def home():
    if 'user_id' in session:
        return render_template('home.html')
    else:
        return redirect(url_for('login'))


@app.route('/logout')
def logout():
    session.pop('user_id', None)
    return redirect(url_for('login'))


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
