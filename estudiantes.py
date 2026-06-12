from database import get_connection

# ALTA: recibe los datos del estudiante y los inserta en la tabla estudiante
def crear_estudiante(documento, nombre, apellido, email, carrera, facultad):
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("""
            INSERT INTO estudiante (documento, nombre, apellido, email, carrera, facultad)
            VALUES (%s, %s, %s, %s, %s, %s)
        """, (documento, nombre, apellido, email, carrera, facultad))
        conn.commit()
        print("Estudiante creado correctamente.")
    except Exception as e:
        print(f"Error al crear estudiante: {e}")
    finally:
        cursor.close()
        conn.close()

# BAJA: recibe el id del estudiante y lo elimina de la tabla
def eliminar_estudiante(id_estudiante):
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("DELETE FROM estudiante WHERE id_estudiante = %s", (id_estudiante,))
        conn.commit()
        print("Estudiante eliminado correctamente.")
    except Exception as e:
        print(f"Error al eliminar estudiante: {e}")
    finally:
        cursor.close()
        conn.close()

# MODIFICACION: recibe el id y los nuevos datos, actualiza el registro en la tabla
def modificar_estudiante(id_estudiante, nombre, apellido, email, carrera, facultad):
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("""
            UPDATE estudiante
            SET nombre=%s, apellido=%s, email=%s, carrera=%s, facultad=%s
            WHERE id_estudiante=%s
        """, (nombre, apellido, email, carrera, facultad, id_estudiante))
        conn.commit()
        print("Estudiante modificado correctamente.")
    except Exception as e:
        print(f"Error al modificar estudiante: {e}")
    finally:
        cursor.close()
        conn.close()

# LISTAR: trae todos los estudiantes de la tabla y los muestra en pantalla con formato de tabla
def listar_estudiantes():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id_estudiante, documento, nombre, apellido, carrera, facultad FROM estudiante")
    estudiantes = cursor.fetchall()
    cursor.close()
    conn.close()
    if not estudiantes:
        print("No hay estudiantes registrados.")
        return
    print(f"\n{'ID':<5} {'Documento':<15} {'Nombre':<15} {'Apellido':<15} {'Carrera':<25} {'Facultad'}")
    print("-" * 90)
    for e in estudiantes:
        print(f"{e[0]:<5} {e[1]:<15} {e[2]:<15} {e[3]:<15} {e[4]:<25} {e[5]}")

# MENU: muestra las opciones en pantalla y llama a la funcion correspondiente segun lo que elija el usuario
def menu_estudiantes():
    while True:
        print("\n--- ABM Estudiantes ---")
        print("1. Listar estudiantes")
        print("2. Crear estudiante")
        print("3. Modificar estudiante")
        print("4. Eliminar estudiante")
        print("0. Volver")
        opcion = input("Elegir opcion: ")

        if opcion == "1":
            listar_estudiantes()

        elif opcion == "2":
            documento = input("Documento: ")
            nombre   = input("Nombre: ")
            apellido = input("Apellido: ")
            email    = input("Email: ")
            carrera  = input("Carrera: ")
            facultad = input("Facultad: ")
            crear_estudiante(documento, nombre, apellido, email, carrera, facultad)

        elif opcion == "3":
            listar_estudiantes()
            id_est   = input("ID del estudiante a modificar: ")
            nombre   = input("Nuevo nombre: ")
            apellido = input("Nuevo apellido: ")
            email    = input("Nuevo email: ")
            carrera  = input("Nueva carrera: ")
            facultad = input("Nueva facultad: ")
            modificar_estudiante(id_est, nombre, apellido, email, carrera, facultad)

        elif opcion == "4":
            listar_estudiantes()
            id_est = input("ID del estudiante a eliminar: ")
            confirmar = input(f"Confirmar eliminacion del estudiante {id_est}? (s/n): ")
            if confirmar.lower() == "s":
                eliminar_estudiante(id_est)

        elif opcion == "0":
            break
