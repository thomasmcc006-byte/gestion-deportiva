from database import get_connection

# ALTA: recibe nombre y descripcion del espacio deportivo y lo inserta en la tabla.
# La descripcion es opcional — si no se ingresa nada se guarda como None (NULL en la BD).
def crear_espacio(nombre, descripcion):
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute(
            "INSERT INTO espacio_deportivo (nombre, descripcion) VALUES (%s, %s)",
            (nombre, descripcion or None)
        )
        conn.commit()
        print("Espacio deportivo creado correctamente.")
    except Exception as e:
        print(f"Error al crear espacio: {e}")
    finally:
        cursor.close()
        conn.close()

# BAJA: recibe el id y elimina el espacio deportivo.
# Si tiene actividades asociadas, MySQL rechaza la eliminacion por la foreign key.
def eliminar_espacio(id_espacio):
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("DELETE FROM espacio_deportivo WHERE id_espacio = %s", (id_espacio,))
        conn.commit()
        print("Espacio deportivo eliminado correctamente.")
    except Exception as e:
        print(f"Error al eliminar espacio: {e}")
    finally:
        cursor.close()
        conn.close()

# MODIFICACION: recibe el id y los nuevos datos, actualiza el registro en la tabla.
def modificar_espacio(id_espacio, nombre, descripcion):
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute(
            "UPDATE espacio_deportivo SET nombre=%s, descripcion=%s WHERE id_espacio=%s",
            (nombre, descripcion or None, id_espacio)
        )
        conn.commit()
        print("Espacio deportivo modificado correctamente.")
    except Exception as e:
        print(f"Error al modificar espacio: {e}")
    finally:
        cursor.close()
        conn.close()

# LISTAR: trae todos los espacios deportivos y los muestra en pantalla.
def listar_espacios():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id_espacio, nombre, descripcion FROM espacio_deportivo")
    espacios = cursor.fetchall()
    cursor.close()
    conn.close()
    if not espacios:
        print("No hay espacios registrados.")
        return
    print(f"\n{'ID':<5} {'Nombre':<25} {'Descripcion'}")
    print("-" * 70)
    for e in espacios:
        print(f"{e[0]:<5} {e[1]:<25} {e[2] or '-'}")

# MENU: muestra las opciones y llama a la funcion correspondiente segun lo que elija el usuario.
def menu_espacios():
    while True:
        print("\n--- ABM Espacios Deportivos ---")
        print("1. Listar espacios")
        print("2. Crear espacio")
        print("3. Modificar espacio")
        print("4. Eliminar espacio")
        print("0. Volver")
        opcion = input("Elegir opcion: ")

        if opcion == "1":
            listar_espacios()

        elif opcion == "2":
            nombre      = input("Nombre del espacio: ")
            descripcion = input("Descripcion (opcional, Enter para omitir): ")
            crear_espacio(nombre, descripcion)

        elif opcion == "3":
            listar_espacios()
            id_esp      = input("ID del espacio a modificar: ")
            nombre      = input("Nuevo nombre: ")
            descripcion = input("Nueva descripcion (opcional, Enter para omitir): ")
            modificar_espacio(id_esp, nombre, descripcion)

        elif opcion == "4":
            listar_espacios()
            id_esp    = input("ID del espacio a eliminar: ")
            confirmar = input(f"Confirmar eliminacion del espacio {id_esp}? (s/n): ")
            if confirmar.lower() == "s":
                eliminar_espacio(id_esp)

        elif opcion == "0":
            break