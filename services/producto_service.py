def obtener_productos(conn):
    return conn.execute("SELECT * FROM productos").fetchall()