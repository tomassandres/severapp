from flask import Flask, render_template, request, redirect, url_for, session
import sqlite3
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.secret_key = 'severapp_secreto_2026' 

def get_db_connection():
    conn = sqlite3.connect('eventapp.db')
    conn.row_factory = sqlite3.Row
    return conn

@app.route("/")
def index():
    if 'usuario_id' in session:
        return redirect(url_for('panel'))
    return redirect(url_for('login'))

@app.route("/registro", methods=["GET", "POST"])
def registro():
    if request.method == "POST":
        nombre = request.form["nombre"]
        correo = request.form["correo"]
        contrasena = request.form["contrasena"]
        tipo_usuario = request.form["tipo_usuario"]
        hash_pass = generate_password_hash(contrasena)
        conn = get_db_connection()
        try:
            conn.execute("INSERT INTO usuarios (nombre, correo, contrasena_hash, tipo_usuario) VALUES (?, ?, ?, ?)", (nombre, correo, hash_pass, tipo_usuario))
            conn.commit()
            return redirect(url_for('login'))
        except sqlite3.IntegrityError:
            return render_template("registro.html", error="Este correo ya está registrado.")
        finally:
            conn.close()
    return render_template("registro.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        correo = request.form["correo"]
        contrasena = request.form["contrasena"]
        conn = get_db_connection()
        usuario = conn.execute("SELECT * FROM usuarios WHERE correo = ?", (correo,)).fetchone()
        conn.close()
        if usuario and check_password_hash(usuario["contrasena_hash"], contrasena):
            session['usuario_id'] = usuario['id']
            session['usuario_nombre'] = usuario['nombre']
            # Guardamos el rol original y el modo actual (que empieza siendo el mismo)
            session['usuario_tipo_original'] = usuario['tipo_usuario']
            session['modo_actual'] = usuario['tipo_usuario']
            return redirect(url_for('panel'))
        else:
            return render_template("login.html", error="Correo o contraseña incorrectos.")
    return render_template("login.html")

@app.route("/cambiar_modo")
def cambiar_modo():
    if 'usuario_id' not in session:
        return redirect(url_for('login'))
    # Si está en modo trabajador, pasa a contratante. Y viceversa.
    if session.get('modo_actual') == 'Trabajador':
        session['modo_actual'] = 'Contratante'
    else:
        session['modo_actual'] = 'Trabajador'
    return redirect(url_for('panel'))

@app.route("/panel")
def panel():
    if 'usuario_id' not in session:
        return redirect(url_for('login'))
    
    busqueda = request.args.get('buscar', '')
    conn = get_db_connection()
    
    # Ahora nos fijamos es en el MODO ACTUAL, no en el tipo original
    if session.get('modo_actual') == 'Trabajador':
        if busqueda:
            query = "SELECT * FROM ofertas WHERE titulo LIKE ? OR categoria LIKE ?"
            param = f"%{busqueda}%"
            ofertas = conn.execute(query, (param, param)).fetchall()
        else:
            ofertas = conn.execute("SELECT * FROM ofertas").fetchall()
        conn.close()
        return render_template("panel_trabajador.html", nombre=session['usuario_nombre'], ofertas=ofertas, busqueda=busqueda)
    else:
        ofertas = conn.execute("SELECT * FROM ofertas WHERE contratante = ?", (session['usuario_nombre'],)).fetchall()
        total_postulaciones = 0
        ofertas_con_conteo = []
        for of in ofertas:
            count = conn.execute("SELECT COUNT(*) FROM postulaciones WHERE oferta_id = ?", (of['id'],)).fetchone()[0]
            total_postulaciones += count
            of_dict = dict(of)
            of_dict['postulaciones_count'] = count
            ofertas_con_conteo.append(of_dict)
        conn.close()
        return render_template("panel_contratante.html", nombre=session['usuario_nombre'], ofertas=ofertas_con_conteo, total_postulaciones=total_postulaciones)

@app.route("/perfil", methods=["GET", "POST"])
def perfil():
    if 'usuario_id' not in session:
        return redirect(url_for('login'))
    conn = get_db_connection()
    if request.method == "POST":
        habilidades = request.form.get("habilidades", "")
        conn.execute("UPDATE usuarios SET habilidades = ? WHERE id = ?", (habilidades, session['usuario_id']))
        conn.commit()
    usuario = conn.execute("SELECT * FROM usuarios WHERE id = ?", (session['usuario_id'],)).fetchone()
    
    calificaciones = conn.execute("SELECT AVG(puntuacion) as promedio, COUNT(*) as total FROM calificaciones WHERE evaluado_id = ?", (session['usuario_id'],)).fetchone()
    promedio = round(calificaciones['promedio'], 1) if calificaciones['promedio'] else 0
    total_calif = calificaciones['total']
    
    conn.close()
    return render_template("perfil.html", usuario=usuario, promedio=promedio, total_calif=total_calif)

@app.route("/crear_oferta", methods=["GET", "POST"])
def crear_oferta():
    if 'usuario_id' not in session or session.get('modo_actual') != 'Contratante':
        return redirect(url_for('login'))
    if request.method == "POST":
        titulo = request.form["titulo"]
        categoria = request.form["categoria"]
        descripcion = request.form["descripcion"]
        ubicacion = request.form["ubicacion"]
        fecha = request.form["fecha"]
        remuneracion = request.form["remuneracion"]
        contratante = session['usuario_nombre']
        conn = get_db_connection()
        conn.execute("INSERT INTO ofertas (titulo, categoria, descripcion, ubicacion, fecha, remuneracion, contratante) VALUES (?, ?, ?, ?, ?, ?, ?)", (titulo, categoria, descripcion, ubicacion, fecha, remuneracion, contratante))
        conn.commit()
        conn.close()
        return redirect(url_for('panel'))
    return render_template("crear_oferta.html")

@app.route("/ver_postulaciones/<int:oferta_id>")
def ver_postulaciones(oferta_id):
    if 'usuario_id' not in session or session.get('modo_actual') != 'Contratante':
        return redirect(url_for('login'))
    conn = get_db_connection()
    oferta = conn.execute("SELECT * FROM ofertas WHERE id = ?", (oferta_id,)).fetchone()
    postulantes = conn.execute('''
        SELECT u.id as trabajador_id, u.nombre, u.correo, p.estado, p.id as postulacion_id
        FROM postulaciones p JOIN usuarios u ON p.trabajador_id = u.id
        WHERE p.oferta_id = ?
    ''', (oferta_id,)).fetchall()
    conn.close()
    return render_template("ver_postulaciones.html", oferta=oferta, postulantes=postulantes)

@app.route("/cambiar_estado/<int:postulacion_id>/<estado>")
def cambiar_estado(postulacion_id, estado):
    if 'usuario_id' not in session or session.get('modo_actual') != 'Contratante':
        return redirect(url_for('login'))
    if estado in ['Aceptada', 'Rechazada', 'Pendiente']:
        conn = get_db_connection()
        conn.execute("UPDATE postulaciones SET estado = ? WHERE id = ?", (estado, postulacion_id))
        conn.commit()
        conn.close()
    return redirect(request.referrer)

@app.route("/calificar/<int:trabajador_id>", methods=["GET", "POST"])
def calificar(trabajador_id):
    if 'usuario_id' not in session or session.get('modo_actual') != 'Contratante':
        return redirect(url_for('login'))
    conn = get_db_connection()
    trabajador = conn.execute("SELECT * FROM usuarios WHERE id = ?", (trabajador_id,)).fetchone()
    conn.close()
    return render_template("calificar.html", trabajador=trabajador)

@app.route("/guardar_calificacion/<int:trabajador_id>", methods=["POST"])
def guardar_calificacion(trabajador_id):
    if 'usuario_id' not in session or session.get('modo_actual') != 'Contratante':
        return redirect(url_for('login'))
    puntuacion = request.form["puntuacion"]
    comentario = request.form.get("comentario", "")
    conn = get_db_connection()
    conn.execute("INSERT INTO calificaciones (evaluador_id, evaluado_id, puntuacion, comentario) VALUES (?, ?, ?, ?)", (session['usuario_id'], trabajador_id, puntuacion, comentario))
    conn.commit()
    conn.close()
    return redirect(url_for('panel'))

@app.route("/postular/<int:oferta_id>")
def postular(oferta_id):
    if 'usuario_id' not in session: return redirect(url_for('login'))
    if session.get('modo_actual') != 'Trabajador': return "Solo trabajadores pueden postularse.", 403
    conn = get_db_connection()
    ya_postulado = conn.execute("SELECT * FROM postulaciones WHERE oferta_id = ? AND trabajador_id = ?", (oferta_id, session['usuario_id'])).fetchone()
    if not ya_postulado:
        conn.execute("INSERT INTO postulaciones (oferta_id, trabajador_id) VALUES (?, ?)", (oferta_id, session['usuario_id']))
        conn.commit()
        mensaje = "¡Postulación enviada con éxito! 🎉"
    else:
        mensaje = "Ya te habías postulado a esta oferta. 😉"
    conn.close()
    return redirect(url_for('panel', mensaje=mensaje))

@app.route("/mis_postulaciones")
def mis_postulaciones():
    if 'usuario_id' not in session: return redirect(url_for('login'))
    conn = get_db_connection()
    postulaciones = conn.execute('''
        SELECT p.estado, o.titulo, o.remuneracion, o.fecha 
        FROM postulaciones p JOIN ofertas o ON p.oferta_id = o.id
        WHERE p.trabajador_id = ?
    ''', (session['usuario_id'],)).fetchall()
    conn.close()
    return render_template("mis_postulaciones.html", postulaciones=postulaciones)

@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for('login'))

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True)