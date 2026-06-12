import mysql.connector

def get_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="Ingresar Contraseña",
        database="gestion_deportiva"
    )