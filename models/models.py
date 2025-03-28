from flask_login import UserMixin
from conexion.conexion import conectar_db
from werkzeug.security import check_password_hash

class Usuario(UserMixin):
    def __init__(self, id_usuario, nombre, email, password): # Cambiado idusuarios a id_usuario
        self.id = id_usuario
        self.nombre = nombre
        self.email = email
        self.password = password

    @staticmethod
    def obtener_por_email(email):
        conexion = conectar_db()
        cursor = conexion.cursor()
        cursor.execute("SELECT id_usuario, nombre, email, password FROM usuarios WHERE email = %s", (email,)) # Cambiado idusuarios a id_usuario
        fila = cursor.fetchone()
        if fila:
            return Usuario(*fila)
        return None

    @staticmethod
    def obtener_por_id(id_usuario): # Cambiado idusuarios a id_usuario
        conexion = conectar_db()
        cursor = conexion.cursor()
        cursor.execute("SELECT id_usuario, nombre, email, password FROM usuarios WHERE id_usuario = %s", (id_usuario,)) # Cambiado idusuarios a id_usuario
        fila = cursor.fetchone()
        if fila:
            return Usuario(*fila)
        return None

    def verificar_password(self, password_plano):
        password_hasheado = self.password.strip()  # Eliminar espacios en blanco y decodificar a UTF-8
        return check_password_hash(password_hasheado, password_plano)