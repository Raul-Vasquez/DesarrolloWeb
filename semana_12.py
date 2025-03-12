from flask import Flask, render_template
import json
import csv
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, IntegerField, EmailField
from wtforms.validators import DataRequired

app = Flask(__name__)
app.config['SECRET_KEY'] = 'tu_clave_secreta'  # ¡Reemplaza con una clave secreta segura!

# Definición del formulario
class MiFormulario(FlaskForm):
    nombre = StringField('Nombre', validators=[DataRequired()])
    edad = IntegerField('Edad', validators=[DataRequired()])
    correo = EmailField('Correo', validators=[DataRequired()])
    deporte = StringField('Deporte', validators=[DataRequired()])
    comida = StringField('Comida', validators=[DataRequired()])
    submit = SubmitField('Enviar')

# Ruta para el formulario
@app.route('/', methods=['GET', 'POST'])
def formulario():
    form = MiFormulario()
    if form.validate_on_submit():
        datos = {
            'nombre': form.nombre.data,
            'edad': form.edad.data,
            'correo': form.correo.data,
            'deporte': form.deporte.data,
            'comida': form.comida.data
        }

        # Guardar en TXT
        with open('datos/datos.txt', 'a', encoding='utf-8') as f: #Asegurate de agregar el encoding
            f.write(f"{datos['nombre']},{datos['edad']},{datos['correo']},{datos['deporte']},{datos['comida']}\n")

        # Guardar en JSON
        try:
            with open('datos/datos.json', 'r+') as f:
                lista_datos = json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            lista_datos = lista_datos.append(datos)
        with open('datos/datos.json', 'w', encoding='utf-8') as f: #Asegurate de agregar el encoding
            json.dump(lista_datos, f, indent=4)

        # Guardar en CSV
        with open('datos/datos.csv', 'a', newline='', encoding='utf-8') as f: #Asegurate de agregar el encoding
            writer = csv.writer(f)
            if f.tell() == 0:
                writer.writerow(datos.keys())
            writer.writerow(datos.values())

        return render_template('resultadoFormulario.html', datos=datos)

    return render_template('Formulario.html', form=form)

# Rutas para mostrar datos desde archivos
@app.route('/mostrar_txt')
def mostrar_txt():
    try:
        with open('datos/datos.txt', 'r', encoding='utf-8') as f: #Asegurate de agregar el encoding
            contenido = f.read()
        return f"<pre>{contenido}</pre>"
    except FileNotFoundError:
        return "Archivo datos.txt no encontrado"

@app.route('/mostrar_json')
def mostrar_json():
    try:
        with open('datos/datos.json', 'r', encoding='utf-8') as f: #Asegurate de agregar el encoding
            datos = json.load(f)
        return f"<pre>{json.dumps(datos, indent=4)}</pre>"
    except FileNotFoundError:
        return "Archivo datos.json no encontrado"

@app.route('/mostrar_csv')
def mostrar_csv():
    try:
        with open('datos/datos.csv', 'r', encoding='utf-8') as f: #Asegurate de agregar el encoding
            reader = csv.reader(f)
            contenido = ""
            for fila in reader:
                contenido += ", ".join(fila) + "<br>"
        return contenido
    except FileNotFoundError:
        return "Archivo datos.csv no encontrado"

if __name__ == '__main__':
    app.run(debug=True)