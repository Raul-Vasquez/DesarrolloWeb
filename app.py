from flask import Flask

app = Flask(__name__)


#Ruta Princial
@app.route('/')
def hola_mundo():
    return '<h3>Esta es una prueba de pagina web</h3>'

# Ruta personalizada con usuario
# prueba
@app.route('/usuario/<nombre>')
def usuario(nombre):
    return (f'<h1>¡Bienvenido, {nombre}!</h1> '
            f'<p>Tu usuario fue registrado con exito por favor sigue practicando</p>'
            f'<p>La gente con la que pasas mas tiempo es en quien te conviertes</p>')


if __name__ == '__main__':
    app.run()
