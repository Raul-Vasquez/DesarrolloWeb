# Importar las clases necesarias
from flask import Flask, render_template, request, redirect, url_for
from flask_login import LoginManager, login_required, login_user
from conexion.conexion import conectar_db
from models.models import Usuario
from werkzeug.security import generate_password_hash

app = Flask(__name__)
app.config['SECRET_KEY'] = 'tu_clave_secreta'  # Reemplaza con una clave secreta segura

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

@login_manager.user_loader
def load_user(user_id):
    return Usuario.obtener_por_id(user_id)


@login_manager.user_loader
def load_user(user_id):
    return Usuario.obtener_por_id(user_id)

# Redirige a /login cuando se accede a la ruta raíz
@app.route('/')
def index():
    return redirect(url_for('login'))
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        usuario = Usuario.obtener_por_email(email)
        if usuario and usuario.verificar_password(password):
            login_user(usuario)
            return redirect(url_for('listar_productos'))  # Redirige a la página principal después del inicio de sesión
        else:
            return 'Correo o contraseña incorrectos'
    return render_template('login.html')

# Nueva ruta para insertar usuario
@app.route('/insertar_usuario', methods=['GET', 'POST'])
def insertar_usuario():
    if request.method == 'POST':
        nombre = request.form['nombre']
        email = request.form['email']
        password_plano = request.form['password']
        rol = request.form['rol']

        password_hasheado = generate_password_hash(password_plano) # Hashear la contraseña

        conexion = conectar_db()
        cursor = conexion.cursor()
        cursor.execute("INSERT INTO usuarios (nombre, email, password, rol) VALUES (%s, %s, %s, %s)", (nombre, email, password_hasheado, rol))
        conexion.commit()
        conexion.close()

        return redirect(url_for('login')) # Redirigir a la página de inicio de sesión

    return render_template('insertar_usuario.html') # Renderizar la plantilla para insertar usuario
# Crea la clase Producto que represente la tabla productos en tu base de datos:
class Producto:
    def __init__(self, id_producto, nombre, descripcion, precio, stock, tipo):
        self.id_producto = id_producto
        self.nombre = nombre
        self.descripcion = descripcion
        self.precio = precio
        self.stock = stock
        self.tipo = tipo

# Crear Rutas para la Gestión de Productos
# Crea una ruta para mostrar la lista de productos:
@app.route('/productos')
#@login_required
def listar_productos():
    conexion = conectar_db()
    cursor = conexion.cursor()
    cursor.execute("SELECT * FROM productos")
    productos_db = cursor.fetchall()
    productos = []
    for producto in productos_db:
        productos.append(Producto(*producto))
    conexion.close()
    return render_template('productos.html', productos=productos)

# Crea una ruta para agregar nuevos productos:
@app.route('/productos/agregar', methods=['GET', 'POST'])
@login_required
def agregar_producto():
    if request.method == 'POST':
        nombre = request.form['nombre']
        descripcion = request.form['descripcion']
        precio = request.form['precio']
        stock = request.form['stock']
        tipo = request.form['tipo']
        conexion = conectar_db()
        cursor = conexion.cursor()
        cursor.execute("INSERT INTO productos (nombre, descripcion, precio, stock, tipo) VALUES (%s, %s, %s, %s, %s)", (nombre, descripcion, precio, stock, tipo))
        conexion.commit()
        conexion.close()
        return redirect(url_for('listar_productos'))
    return render_template('agregar_producto.html')

# Crea una ruta para editar productos existentes:
@app.route('/productos/editar/<int:id_producto>', methods=['GET', 'POST'])
@login_required
def editar_producto(id_producto):
    conexion = conectar_db()
    cursor = conexion.cursor()
    if request.method == 'POST':
        nombre = request.form['nombre']
        descripcion = request.form['descripcion']
        precio = request.form['precio']
        stock = request.form['stock']
        tipo = request.form['tipo']
        cursor.execute("UPDATE productos SET nombre = %s, descripcion = %s, precio = %s, stock = %s, tipo = %s WHERE id_producto = %s", (nombre, descripcion, precio, stock, tipo, id_producto))
        conexion.commit()
        conexion.close()
        return redirect(url_for('listar_productos'))
    cursor.execute("SELECT * FROM productos WHERE id_producto = %s", (id_producto,))
    producto_db = cursor.fetchone()
    conexion.close()
    producto = Producto(*producto_db)
    return render_template('editar_producto.html', producto=producto)

# Crea una ruta para eliminar productos:
@app.route('/productos/eliminar/<int:id_producto>')
@login_required
def eliminar_producto(id_producto):
    conexion = conectar_db()
    cursor = conexion.cursor()
    cursor.execute("DELETE FROM productos WHERE id_producto = %s", (id_producto,))
    conexion.commit()
    conexion.close()
    return redirect(url_for('listar_productos'))

if __name__ == '__main__':
    app.run(debug=True)