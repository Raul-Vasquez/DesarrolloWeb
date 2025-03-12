from flask import Flask, render_template
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, IntegerField
from wtforms.validators import DataRequired, Email

app = Flask(__name__)
app.config['SECRET_KEY'] = 'tu_clave_secreta'

# Definimos la clase del formulario
class MiFormulario(FlaskForm):
    nombre = StringField('Ingresa tu nombre', validators=[DataRequired()])
    primer_apellido = StringField('Ingresa tu primer apellido', validators=[DataRequired()])
    segundo_apellido = StringField('Ingresa tu segundo apellido', validators=[DataRequired()])
    edad = IntegerField('Ingresa tu edad', validators=[DataRequired()])
    correo = StringField('Ingresa tu correo electrónico', validators=[DataRequired(), Email()])
    deporte = StringField('Ingresa tu deporte favorito', validators=[DataRequired()])
    comida = StringField('Ingresa tu comida favorita', validators=[DataRequired()])
    submit = SubmitField('Enviar')

# Ruta para mostrar y procesar el formulario
@app.route('/', methods=['GET', 'POST'])
def formulario():
    form = MiFormulario()
    if form.validate_on_submit():
        datos = {
            'nombre': form.nombre.data,
            'primer_apellido': form.primer_apellido.data,
            'segundo_apellido': form.segundo_apellido.data,
            'edad': form.edad.data,
            'correo': form.correo.data,
            'deporte': form.deporte.data,
            'comida': form.comida.data
        }
        return render_template('resultadoFormulario.html', **datos)
    return render_template('Formulario.html', form=form)

if __name__ == '__main__':
    app.run(debug=True)