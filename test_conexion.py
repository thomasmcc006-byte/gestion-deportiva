from database import get_connection

conn = get_connection()
print("Conexion exitosa!")
conn.close()