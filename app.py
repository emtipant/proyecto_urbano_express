from flask import Flask, render_template

app = Flask(__name__)

# -------------------
# Ruta principal
# -------------------
@app.route('/')
def inicio():
    return render_template('index.html', titulo="Inicio", mensaje="Bienvenido a Urbano Express - Sistema de Delivery Urbano")

# -------------------
# Acerca de
# -------------------
@app.route('/about')
def about():
    return render_template('about.html', titulo="Acerca de")

# -------------------
# Pedido dinámico
# -------------------
@app.route('/pedido/<cliente>')
def pedido(cliente):
    mensaje = f"Hola {cliente}, tu pedido está en proceso de envío."
    return render_template('pedido.html', titulo="Pedido", mensaje=mensaje)

# -------------------
# Seguimiento dinámico
# -------------------
@app.route('/seguimiento/<codigo>')
def seguimiento(codigo):
    mensaje = f"El pedido con código {codigo} está en camino."
    return render_template('seguimiento.html', titulo="Seguimiento", mensaje=mensaje)

# -------------------
# Cliente dinámico
# -------------------
@app.route('/clientes/<nombre>')
def clientes(nombre):
    mensaje = f"Información del cliente: {nombre}"
    return render_template('cliente.html', titulo="Cliente", mensaje=mensaje)

# -------------------
# Producto dinámico
# -------------------
@app.route('/producto/<codigo>')
def producto(codigo):
    mensaje = f"Detalle del producto con código {codigo}"
    return render_template('producto.html', titulo="Producto", mensaje=mensaje)

# -------------------
# Factura dinámica
# -------------------
@app.route('/factura/<numero>')
def factura(numero):
    mensaje = f"Detalle de la factura número {numero}"
    return render_template('factura.html', titulo="Factura", mensaje=mensaje)

# -------------------
# Ejecutar app
# -------------------
if __name__ == '__main__':
    app.run(debug=True)