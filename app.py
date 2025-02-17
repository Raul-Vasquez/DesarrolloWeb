from flask import Flask

app = Flask(__name__)


# Ruta principal
@app.route('/')
def hello_world(): # Colocar aqui el codigo principal
    return 'Practica de Pagina Web!'

# Ruta personalizada con usuario
@app.route('/usuario/<nombre>')
def usuario(nombre):
    return f'<h1>¡Bienvenido, {nombre}!</h1><p>Tu usuario ha sido registrado correctamente.</p>'


if __name__ == '__main__':
    app.run()
