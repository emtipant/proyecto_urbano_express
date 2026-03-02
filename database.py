import sqlite3

def crear_bd():
    conexion = sqlite3.connect("inventario.db")
    cursor = conexion.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS productos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT,
            cantidad INTEGER,
            precio REAL
        )
    """)

    conexion.commit()
    conexion.close()


def agregar_producto(nombre, cantidad, precio):
    conexion = sqlite3.connect("inventario.db")
    cursor = conexion.cursor()

    cursor.execute("INSERT INTO productos (nombre, cantidad, precio) VALUES (?, ?, ?)",
                   (nombre, cantidad, precio))

    conexion.commit()
    conexion.close()


def obtener_productos():
    conexion = sqlite3.connect("inventario.db")
    cursor = conexion.cursor()

    cursor.execute("SELECT * FROM productos")
    datos = cursor.fetchall()

    conexion.close()
    return datos


def eliminar_producto(id):
    conexion = sqlite3.connect("inventario.db")
    cursor = conexion.cursor()

    cursor.execute("DELETE FROM productos WHERE id=?", (id,))

    conexion.commit()
    conexion.close()