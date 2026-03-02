from flask import Flask, render_template, request, redirect
import sqlite3

app = Flask(__name__)

# ===============================
# CONEXIÓN A SQLITE
# ===============================
def conectar():
    conn = sqlite3.connect("urbano.db")
    conn.row_factory = sqlite3.Row
    return conn

# ===============================
# CREAR TABLA PRODUCTOS
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
# CLASE PRODUCTO (POO)
# ===============================
class Producto:
    def __init__(self, nombre, cantidad, precio):
        self.nombre = nombre
        self.cantidad = cantidad
        self.precio = precio

# ===============================
# CLASE INVENTARIO (DICCIONARIO)
# ===============================
class Inventario:
    def __init__(self):
        self.productos = {}

    def agregar(self, producto):
        self.productos[producto.nombre] = producto

inventario = Inventario()

# ===============================
# RUTAS 
# ===============================

@app.route('/')
def inicio():
    return render_template('index.html', 
                           titulo="Inicio", 
                           mensaje="Bienvenido a Urbano Express - Sistema de Delivery Urbano")

@app.route('/about')
def about():
    return render_template('about.html', titulo="Acerca de")

@app.route('/pedido/<cliente>')
def pedido(cliente):
    mensaje = f"Hola {cliente}, tu pedido está en proceso de envío."
    return render_template('pedido.html', titulo="Pedido", mensaje=mensaje)

@app.route('/seguimiento/<codigo>')
def seguimiento(codigo):
    mensaje = f"El pedido con código {codigo} está en camino."
    return render_template('seguimiento.html', titulo="Seguimiento", mensaje=mensaje)

@app.route('/clientes/<nombre>')
def clientes(nombre):
    mensaje = f"Información del cliente: {nombre}"
    return render_template('cliente.html', titulo="Cliente", mensaje=mensaje)

@app.route('/producto/<codigo>')
def producto(codigo):
    mensaje = f"Detalle del producto con código {codigo}"
    return render_template('producto.html', titulo="Producto", mensaje=mensaje)

@app.route('/factura/<numero>')
def factura(numero):
    mensaje = f"Detalle de la factura número {numero}"
    return render_template('factura.html', titulo="Factura", mensaje=mensaje)

# ===============================
# NUEVO: INVENTARIO
# ===============================

# Mostrar productos
@app.route('/inventario')
def ver_inventario():
    conn = conectar()
    productos = conn.execute("SELECT * FROM productos").fetchall()
    conn.close()
    return render_template("inventario.html", productos=productos)

# Agregar producto
@app.route('/agregar_producto', methods=["POST"])
def agregar_producto():
    nombre = request.form["nombre"]
    cantidad = request.form["cantidad"]
    precio = request.form["precio"]

    nuevo = Producto(nombre, cantidad, precio)
    inventario.agregar(nuevo)

    conn = conectar()
    conn.execute("INSERT INTO productos (nombre, cantidad, precio) VALUES (?, ?, ?)",
                 (nombre, cantidad, precio))
    conn.commit()
    conn.close()

    return redirect('/inventario')

# Eliminar producto
@app.route('/eliminar_producto/<int:id>')
def eliminar_producto(id):
    conn = conectar()
    conn.execute("DELETE FROM productos WHERE id=?", (id,))
    conn.commit()
    conn.close()
    return redirect('/inventario')

# ===============================
# EJECUTAR APP
# ===============================
if __name__ == '__main__':
    app.run(debug=True)