from werkzeug.security import generate_password_hash

hash_password = generate_password_hash("Hola")
print(hash_password)