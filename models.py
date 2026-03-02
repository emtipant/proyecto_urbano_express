class Producto:
    def __init__(self, nombre, cantidad, precio):
        self.nombre = nombre
        self.cantidad = cantidad
        self.precio = precio

    def mostrar(self):
        return f"{self.nombre} - {self.cantidad} unidades - ${self.precio}"