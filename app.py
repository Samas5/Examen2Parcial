import os
from flask import Flask, render_template, redirect, url_for, request, flash, get_flashed_messages
from flask_sqlalchemy import SQLAlchemy

ruta = os.path.abspath(os.path.dirname(__file__))
app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = f"sqlite:///{os.path.join(ruta, 'database', 'app.db')}"
db = SQLAlchemy(app)

app.config['SECRET_KEY'] = 'ñ'

class Pelicula(db.Model):
    __tablename__ = 'peliculas'
    id = db.Column(db.Integer, primary_key=True)
    titulo = db.Column(db.String(50))
    director = db.Column(db.String(50))
    fecha_lanzamiento = db.Column(db.String(10))
    genero = db.Column(db.String(50))
    estado = db.Column(db.Boolean)

@app.route('/')
def home():
    peliculas = Pelicula.query.all()
    return render_template('index.html', peliculas=peliculas)

@app.route('/pelicula', methods=['POST'])
def registrar_pelicula():
    titulo = request.form.get('titulo', '').strip()
    director = request.form.get('director', '').strip()
    fecha_lanzamiento = request.form.get('fecha', '').strip()
    genero = request.form.get('genero', '').strip()
    errores = {}
    if not titulo:
        errores['titulo'] = 'Título de la película obligatorio'
    if not director:
        errores['director'] = 'Nombre del director obligatorio'
    if not genero:
        errores['genero'] = 'Género obligatorio'
    if not fecha_lanzamiento:
        errores['fecha_lanzamiento'] = 'Año de lanzamiento obligatorio'
    elif not fecha_lanzamiento.isdigit() or int(fecha_lanzamiento) < 1900 or int(fecha_lanzamiento) > 2025:
        errores['fecha_lanzamiento'] = 'Ingresar una fecha de lanzamiento válida'
    if not errores:
        try:
            pelicula = Pelicula(titulo=titulo, director=director, fecha_lanzamiento=fecha_lanzamiento, genero=genero, estado=True)
            db.session.add(pelicula)
            db.session.commit()
            flash('Película insertada correctamente', 'ok')
            return redirect(url_for('home'))     
        except Exception as e:
            flash(f'Ocurrión un error {e}', 'error')
            return redirect(url_for('home'))
    else:
        for campo, mensaje in errores.items():
            flash(mensaje, 'error')
        return redirect(url_for('home'))
    
# Renderizar vista de eliminado
@app.route('/eliminar/<int:id>')
def eliminar(id):
    pelicula = Pelicula.query.get_or_404(id)
    return render_template('eliminar.html', pelicula=pelicula)
# Ejecutar eliminación
@app.route('/eliminar-pelicula/<int:id>', methods=['GET'])
def eliminar_pelicula(id):
    pelicula = Pelicula.query.get_or_404(id)
    try:
        pelicula.estado = False
        db.session.commit()
        flash('Película eliminada correctamente', 'ok')
        return redirect(url_for('home'))
    except Exception as e:
        flash(f'Error: {e}')
        return redirect(url_for('home'))
    
# Renderizar vista de editar
@app.route('/editar/<int:id>')
def editar(id):
    pelicula = Pelicula.query.get_or_404(id)
    return render_template('editar.html', pelicula=pelicula)

@app.route('/editar-pelicula/<int:id>', methods=['POST'])
def editar_pelicula(id):
    pelicula = Pelicula.query.get_or_404(id)
    titulo = request.form.get('titulo', '').strip()
    director = request.form.get('director', '').strip()
    fecha_lanzamiento = request.form.get('fecha', '').strip()
    genero = request.form.get('genero', '').strip()
    errores = {}
    if not titulo:
        errores['titulo'] = 'Título de la película obligatorio'
    if not director:
        errores['director'] = 'Nombre del director obligatorio'
    if not genero:
        errores['genero'] = 'Género obligatorio'
    if not fecha_lanzamiento:
        errores['fecha_lanzamiento'] = 'Año de lanzamiento obligatorio'
    elif not fecha_lanzamiento.isdigit() or int(fecha_lanzamiento) < 1900 or int(fecha_lanzamiento) > 2025:
        errores['fecha_lanzamiento'] = 'Ingresar una fecha de lanzamiento válida'
    if not errores:
        try:
            pelicula.titulo = titulo
            pelicula.director = director
            pelicula.genero = genero
            pelicula.fecha_lanzamiento = fecha_lanzamiento
            db.session.add(pelicula)
            db.session.commit()
            flash('Película actualizada correctamente', 'ok')
            return redirect(url_for('home'))     
        except Exception as e:
            flash(f'Ocurrión un error {e}', 'error')
            return redirect(url_for('home'))
    else:
        for campo, mensaje in errores.items():
            flash(mensaje, 'error')
        return redirect(url_for('editar', id=id))

if __name__ == '__main__':
    app.run(debug=True)
