import sqlite3
conn = sqlite3.connect('SeverApp.db')
try:
    conn.execute('ALTER TABLE usuarios ADD COLUMN habilidades TEXT DEFAULT ""')
    conn.commit()
    print('¡Columna de habilidades agregada exitosamente!')
except sqlite3.OperationalError:
    print('La columna ya existía, todo bien.')
conn.close()

