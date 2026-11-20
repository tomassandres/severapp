import sqlite3
from werkzeug.security import generate_password_hash

conexion = sqlite3.connect('SeverApp.db')
cursor = conexion.cursor()

cursor.execute('''
    CREATE TABLE IF NOT EXISTS usuarios (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nombre TEXT NOT NULL,
        correo TEXT NOT NULL UNIQUE,
        contrasena_hash TEXT NOT NULL,
        tipo_usuario TEXT NOT NULL
    )
''')

conexion.commit()
conexion.close()
print("¡Base de datos 'SeverApp.db' creada exitosamente!")

