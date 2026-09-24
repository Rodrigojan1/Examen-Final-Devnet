from flask import Flask, request, render_template_string
import sqlite3
from werkzeug.security import generate_password_hash, check_password_hash
app = Flask(__name__)

BASE_DATOS = "usuarios.db"

def crear_base_datos():
    conexion = sqlite3.connect(BASE_DATOS)
    cursor = conexion.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS usuarios (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            usuario TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL
        )
    """)
    conexion.commit()
    conexion.close()

def registrar_usuario(usuario, password):
    conexion = sqlite3.connect(BASE_DATOS)
    cursor = conexion.cursor()
    password_hash = generate_password_hash(password)

    try:
        cursor.execute(
            "INSERT INTO usuarios (usuario, password) VALUES (?, ?)",
            (usuario, password_hash)
        )
        conexion.commit()
        mensaje = "Usuario registrado correctamente."
    except sqlite3.IntegrityError:
        mensaje = "El usuario ya existe."
    conexion.close()
    return mensaje


def validar_usuario(usuario, password):
    conexion = sqlite3.connect(BASE_DATOS)
    cursor = conexion.cursor()
    cursor.execute(
        "SELECT password FROM usuarios WHERE usuario = ?",
        (usuario,)
    )

    resultado = cursor.fetchone()
    conexion.close()
    if resultado and check_password_hash(resultado[0], password):
        return True
    return False


PAGINA = """
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <title>Examen Final DevNet</title>
</head>

<body>

    <h1>Examen Final DevNet</h1>
    <h2>Gestión de Usuarios</h2>
    <h3>Registrar usuario</h3>

    <form method="POST" action="/registrar">

        Usuario:
        <input type="text" name="usuario" required>
        <br><br>

        Contraseña:
        <input type="password" name="password" required>
        <br><br>

        <button type="submit">Registrar</button>

    </form>
    <hr>
    <h3>Validar usuario</h3>
    <form method="POST" action="/login">

        Usuario:
        <input type="text" name="usuario" required>
        <br><br>

        Contraseña:
        <input type="password" name="password" required>
        <br><br>

        <button type="submit">Validar</button>

    </form>
</body>
</html>
"""


@app.route("/")
def inicio():
    return render_template_string(PAGINA)

@app.route("/registrar", methods=["POST"])
def registrar():

    usuario = request.form["usuario"]
    password = request.form["password"]
    mensaje = registrar_usuario(usuario, password)

    return f"""
        <h2>{mensaje}</h2>
        <a href="/">Volver</a>
    """

@app.route("/login", methods=["POST"])
def login():

    usuario = request.form["usuario"]
    password = request.form["password"]

    if validar_usuario(usuario, password):
        mensaje = "Usuario y contraseña correctos."
    else:
        mensaje = "Usuario o contraseña incorrectos."

    return f"""
        <h2>{mensaje}</h2>
        <a href="/">Volver</a>
    """

if __name__ == "__main__":

    crear_base_datos()
    print("Servidor DevNet iniciado")
    print("Puerto: 5800")
    app.run(
        host="0.0.0.0",
        port=5800,
        debug=False
    )