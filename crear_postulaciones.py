import sqlite3

conexion = sqlite3.connect('SeverApp.db')
cursor = conexion.cursor()

cursor.execute('''
    CREATE TABLE IF NOT EXISTS postulaciones (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        oferta_id INTEGER NOT NULL,
        trabajador_id INTEGER NOT NULL,
        fecha_postulacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        estado TEXT DEFAULT 'Pendiente',
        FOREIGN KEY (oferta_id) REFERENCES ofertas(id),
        FOREIGN KEY (trabajador_id) REFERENCES usuarios(id)
    )
''')

conexion.commit()
conexion.close()
print("¡Tabla de postulaciones creada exitosamente!")

