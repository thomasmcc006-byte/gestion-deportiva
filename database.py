import mysql.connector

# Credenciales activas de la sesion. Se establecen despues del login (ver login.py).
# Por defecto arrancan vacias; set_credenciales() las completa al iniciar sesion.
_usuario_actual = None
_password_actual = None

# Guarda las credenciales del usuario que inicio sesion, para que
# get_connection() las use en todas las conexiones de esta sesion.
def set_credenciales(usuario, password):
    global _usuario_actual, _password_actual
    _usuario_actual = usuario
    _password_actual = password

def get_connection():
    return mysql.connector.connect(
        host="localhost",
        user=_usuario_actual,
        password=_password_actual,
        database="gestion_deportiva"
    )