import sqlite3
conn = sqlite3.connect('eventapp.db')
try:
    conn.execute('''
        CREATE TABLE IF NOT EXISTS calificaciones (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            evaluador_id INTEGER NOT NULL,
            evaluado_id INTEGER NOT NULL,
            puntuacion INTEGER NOT NULL,
            comentario TEXT,
            fecha TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (evaluador_id) REFERENCES usuarios(id),
            FOREIGN KEY (evaluado_id) REFERENCES usuarios(id)
        )
    ''')
    conn.commit()
    print('¡Tabla de calificaciones creada exitosamente!')
except Exception as e:
    print(f'Error: {e}')
conn.close()
