from flask import Flask, render_template, jsonify
from config import DB_CONNECTION_STRING
# from Course_App import app
import cx_Oracle

app = Flask(__name__)

# Configuración de la conexión a la base de datos Oracle
conn = cx_Oracle.connect(DB_CONNECTION_STRING)

print(conn.version)

@app.route('/')
def index():
    # Aquí puedes realizar consultas a la base de datos Oracle
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM NOMBRES')
    data = cursor.fetchall()
    cursor.close()

    return render_template('index.html', data=data)

if __name__ == '__main__':
    app.run(debug=True)