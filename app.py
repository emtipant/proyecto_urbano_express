from flask import Flask, render_template, request, redirect, make_response
import sqlite3
import json
import csv
import mysql.connector
from fpdf import FPDF

# 🔐 LOGIN
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user

app = Flask(__name__)
app.secret_key = "123456"

# ===============================
# LOGIN CONFIG
# ===============================
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"

# ===============================
# CONEXIÓN SQLITE
# ===============================
def conectar():
    conn = sqlite3.connect("urbano.db")
    conn.row_factory = sqlite3.Row
    return conn

# ===============================
# CONEXIÓN MYSQL
# ===============================
def conectar_mysql():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="1234",
        database="urbano_express"
    )

# ===============================
# CLASE USUARIO
# ===============================
class Usuario(UserMixin):
    def __init__(self, id, nombre, mail, password):
        self.id = id
        self.nombre = nombre
        self.mail = mail
        self.password = password

# ===============================
# CARGAR USUARIO
# ===============================
@login_manager.user_loader
def load_user(user_id):
    conn = conectar_mysql()
    cursor = conn.cursor()
    cursor.execute("SELECT id_usuario, nombre, mail, password FROM usuarios WHERE id_usuario=%s", (user_id,))
    user = cursor.fetchone()
    cursor.close()
    conn.close()

    if user:
        return Usuario(user[0], user[1], user[2], user[3])
    return None

# ===============================
# CLASE PRODUCTO
# ===============================
class Producto:
    def __init__(self, nombre, cantidad, precio):
        self.nombre = nombre
        self.cantidad = cantidad
        self.precio = precio

# ===============================
# INVENTARIO
# ===============================
class Inventario:
    def __init__(self):
        self.productos = {}

    def agregar(self, producto):
        self.productos[producto.nombre] = producto

inventario = Inventario()

# ===============================
# GUARDAR DATOS
# ===============================
def guardar_txt(nombre, cantidad, precio):
    with open("datos.txt", "a") as f:
        f.write(f"{nombre},{cantidad},{precio}\n")

def guardar_json(nombre, cantidad, precio):
    datos = {"nombre": nombre, "cantidad": cantidad, "precio": precio}
    try:
        with open("datos.json", "r") as f:
            lista = json.load(f)
    except:
        lista = []
    lista.append(datos)
    with open("datos.json", "w") as f:
        json.dump(lista, f, indent=4)

def guardar_csv(nombre, cantidad, precio):
    with open("datos.csv", "a", newline="") as f:
        writer = csv.writer(f)
        writer.writerow([nombre, cantidad, precio])

# ===============================
# CREAR TABLA SQLITE
# ===============================
def crear_tabla():
    conn = conectar()
    conn.execute("""
        CREATE TABLE IF NOT EXISTS productos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT,
            cantidad INTEGER,
            precio REAL
        )
    """)
    conn.commit()
    conn.close()

crear_tabla()

# ===============================
# LOGIN
# ===============================
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        mail = request.form['mail']
        password = request.form['password']

        conn = conectar_mysql()
        cursor = conn.cursor()
        cursor.execute("SELECT id_usuario, nombre, mail, password FROM usuarios WHERE mail=%s", (mail,))
        user = cursor.fetchone()
        cursor.close()
        conn.close()

        if user and user[3] == password:
            usuario = Usuario(user[0], user[1], user[2], user[3])
            login_user(usuario)
            return redirect('/inventario')

        return "Datos incorrectos"

    return render_template('login.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect('/login')

# ===============================
# RUTAS PRINCIPALES
# ===============================
@app.route('/')
def inicio():
    return render_template('index.html', titulo="Inicio",
                           mensaje="Bienvenido a Urbano Express - Sistema de Delivery Urbano")

@app.route('/about')
def about():
    return render_template('about.html', titulo="Acerca de")

# ===============================
# INVENTARIO (CRUD)
# ===============================
@app.route('/inventario')
@login_required
def ver_inventario():
    conn = conectar()
    productos = conn.execute("SELECT * FROM productos").fetchall()
    conn.close()
    return render_template("inventario.html", productos=productos)

@app.route('/agregar_producto', methods=["POST"])
@login_required
def agregar_producto():
    nombre = request.form["nombre"]
    cantidad = request.form["cantidad"]
    precio = request.form["precio"]

    nuevo = Producto(nombre, cantidad, precio)
    inventario.agregar(nuevo)

    conn = conectar()
    conn.execute(
        "INSERT INTO productos (nombre, cantidad, precio) VALUES (?, ?, ?)",
        (nombre, cantidad, precio)
    )
    conn.commit()
    conn.close()

    guardar_txt(nombre, cantidad, precio)
    guardar_json(nombre, cantidad, precio)
    guardar_csv(nombre, cantidad, precio)

    return redirect('/inventario')

@app.route('/eliminar_producto/<int:id>')
@login_required
def eliminar_producto(id):
    conn = conectar()
    conn.execute("DELETE FROM productos WHERE id=?", (id,))
    conn.commit()
    conn.close()
    return redirect('/inventario')

@app.route('/editar_producto/<int:id>', methods=['GET', 'POST'])
@login_required
def editar_producto(id):
    conn = conectar()
    cursor = conn.cursor()

    if request.method == 'POST':
        nombre = request.form['nombre']
        cantidad = request.form['cantidad']
        precio = request.form['precio']

        cursor.execute("UPDATE productos SET nombre=?, cantidad=?, precio=? WHERE id=?",
                       (nombre, cantidad, precio, id))
        conn.commit()
        conn.close()
        return redirect('/inventario')

    producto = cursor.execute("SELECT * FROM productos WHERE id=?", (id,)).fetchone()
    conn.close()
    return render_template('editar_producto.html', producto=producto)

# ===============================
# PDF
# ===============================
@app.route('/reporte_pdf')
@login_required
def reporte_pdf():
    conn = conectar()
    productos = conn.execute("SELECT * FROM productos").fetchall()
    conn.close()

    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    pdf.cell(200, 10, txt="Reporte de Productos", ln=True)

    for p in productos:
        pdf.cell(200, 10, txt=f"{p[1]} - {p[3]}", ln=True)

    response = make_response(pdf.output(dest='S').encode('latin-1'))
    response.headers['Content-Type'] = 'application/pdf'
    response.headers['Content-Disposition'] = 'attachment; filename=reporte.pdf'

    return response

# ===============================
# MYSQL USUARIOS
# ===============================
@app.route('/usuarios')
def usuarios():
    conn = conectar_mysql()
    cursor = conn.cursor()
    cursor.execute("SELECT id_usuario, nombre, mail FROM usuarios")
    usuarios = cursor.fetchall()
    cursor.close()
    conn.close()
    return render_template("usuarios.html", usuarios=usuarios)

@app.route('/agregar_usuario', methods=['POST'])
def agregar_usuario():
    nombre = request.form['nombre']
    mail = request.form['mail']
    password = request.form['password']

    conn = conectar_mysql()
    cursor = conn.cursor()

    sql = "INSERT INTO usuarios (nombre, mail, password) VALUES (%s,%s,%s)"
    cursor.execute(sql, (nombre, mail, password))
    conn.commit()

    cursor.close()
    conn.close()
    return redirect('/usuarios')

# ===============================
# EJECUTAR
# ===============================
if __name__ == '__main__':
    app.run(debug=True)