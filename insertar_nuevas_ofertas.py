import sqlite3

conexion = sqlite3.connect('eventapp.db')
cursor = conexion.cursor()

ofertas_nuevas = [
    ('Maquillaje para evento social', 'Belleza', 'Servicio de maquillaje profesional para fiesta o evento especial.', 'Bogotá', 'Sáb 15 nov, 4:00-6:00 p. m.', 85000, 'Valentina Gómez'),
    ('Corte y peinado a domicilio', 'Belleza', 'Corte de cabello básico y peinado para mujer u hombre.', 'Chía', 'Dom 16 nov, 10:00-12:00', 50000, 'Estética Glamour'),
    ('Asesoría legal para pequeña empresa', 'Servicios Profesionales', 'Consulta sobre contratos y obligaciones legales básicas.', 'Virtual', 'Lun 17 nov, 2:00-4:00 p. m.', 150000, 'Dr. Fernando Rojas'),
    ('Diseño de sala y comedor', 'Diseño de Interiores', 'Asesoría para reorganizar muebles y elegir colores.', 'Bogotá', 'Mar 18 nov, 9:00-12:00', 200000, 'Arq. Lucía Méndez'),
    ('Armar estantería y clóset', 'Carpintería', 'Ensamblar muebles de madera y ajustar puertas.', 'Zipaquirá', 'Mié 19 nov, 8:00-1:00 p. m.', 95000, 'Maderas del Norte'),
    ('Ayuda espontánea en feria local', 'Espontáneo', 'Apoyo temporal en montaje de stands y atención al público.', 'Cajicá', 'Jue 20 nov, 7:00-3:00 p. m.', 70000, 'Eventos Creativos')
]

cursor.executemany('''
    INSERT INTO ofertas (titulo, categoria, descripcion, ubicacion, fecha, remuneracion, contratante) 
    VALUES (?, ?, ?, ?, ?, ?, ?)
''', ofertas_nuevas)

conexion.commit()
conexion.close()
print("¡Ofertas nuevas insertadas con éxito, mi rey!")
