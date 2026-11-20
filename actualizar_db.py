import sqlite3

conexion = sqlite3.connect('SeverApp.db')
cursor = conexion.cursor()

cursor.execute('''
    CREATE TABLE IF NOT EXISTS ofertas (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        titulo TEXT NOT NULL,
        categoria TEXT NOT NULL,
        descripcion TEXT NOT NULL,
        ubicacion TEXT NOT NULL,
        fecha TEXT NOT NULL,
        remuneracion INTEGER NOT NULL,
        contratante TEXT NOT NULL
    )
''')

cursor.execute("SELECT COUNT(*) FROM ofertas")
if cursor.fetchone()[0] == 0:
    ofertas_prueba = [
        ('Ayuda con mudanza de apartamento', 'Mudanzas', 'Cargar y bajar cajas y muebles pequeños, 2 personas.', 'Chía', 'Sáb 24 oct, 8:00-12:00', 90000, 'Camila Reyes'),
        ('Paseo y cuidado de dos perros', 'Mascotas', 'Paseo de 1 hora por la tarde durante tres días.', 'Zipaquirá', 'Lun 26 oct, 4:00-5:00 p. m.', 40000, 'Andrés Mora'),
        ('Reparar grifo y cambiar bombillos', 'Reparaciones', 'Reparación sencilla en cocina y baño. Herramientas incluidas.', 'Bogotá', 'Mar 27 oct, 9:00-11:00', 70000, 'Laura Pardo'),
        ('Entrega de pedidos en moto', 'Entregas', 'Ruta de 6 entregas en el sector norte.', 'Bogotá', 'Jue 29 oct, 2:00-6:00 p. m.', 60000, 'Tienda La Esquina'),
        ('Apoyo logístico en evento familiar', 'Eventos', 'Montaje de mesas, recepción de invitados y desmontaje.', 'Cajicá', 'Sáb 31 oct, 3:00-10:00 p. m.', 120000, 'Camila Reyes'),
        ('Diligencia en notaría y banco', 'Diligencias', 'Radicar documentos y hacer una consignación.', 'Chía', 'Vie 30 oct, 8:00-11:00', 35000, 'Julián Soto')
    ]
    cursor.executemany('''
        INSERT INTO ofertas (titulo, categoria, descripcion, ubicacion, fecha, remuneracion, contratante) 
        VALUES (?, ?, ?, ?, ?, ?, ?)
    ''', ofertas_prueba)
    print("¡Ofertas de prueba insertadas!")

conexion.commit()
conexion.close()
print("Base de datos actualizada.")

