from flask import Flask
import os

app = Flask(__name__)

# Ruta principal
@app.route('/')
def inicio():
    return "Bienvenido a Urbano Express - Sistema de Delivery Urbano"

# Ruta dinámica pedido
@app.route('/pedido/<cliente>')
def pedido(cliente):
    return f"Hola {cliente}, tu pedido está en proceso de envío."

# Ruta dinámica seguimiento
@app.route('/seguimiento/<codigo>')
def seguimiento(codigo):
    return f"El pedido con código {codigo} está en camino."

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)