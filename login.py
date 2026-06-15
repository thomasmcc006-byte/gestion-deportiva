import mysql.connector

# CREDENCIALES POR ROL: cada usuario de MySQL corresponde a un rol del sistema.
# Esto es lo mismo que se definio en Script_Completo.sql con CREATE USER y GRANT.
USUARIOS = {
    "admin_user":      {"password": "admin123",      "rol": "administrador"},
    "docente_user":    {"password": "docente123",    "rol": "docente"},
    "estudiante_user": {"password": "estudiante123", "rol": "estudiante"},
}

# LOGIN: pide usuario y contraseña, y verifica contra MySQL directamente.
# Si la conexion es exitosa, ademas confirma el rol segun el diccionario USUARIOS.
# Devuelve una tupla (usuario, password, rol) si el login es correcto, o None si falla.
def login():
    print("\n=== Inicio de sesion ===")
    usuario = input("Usuario: ")
    password = input("Contraseña: ")

    if usuario not in USUARIOS:
        print("Usuario no reconocido.")
        return None

    if USUARIOS[usuario]["password"] != password:
        print("Contraseña incorrecta.")
        return None

    # Verifica que las credenciales realmente funcionen contra MySQL
    try:
        conn = mysql.connector.connect(
            host="localhost",
            user=usuario,
            password=password,
            database="gestion_deportiva"
        )
        conn.close()
    except Exception as e:
        print(f"Error al conectar con la base de datos: {e}")
        return None

    rol = USUARIOS[usuario]["rol"]
    print(f"Bienvenido, {usuario}. Rol: {rol}")
    return usuario, password, rol