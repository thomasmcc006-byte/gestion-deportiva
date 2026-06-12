from database import get_connection

# ALTA: recibe el nombre de la disciplina y la inserta en la tabla.
# Si el nombre ya existe, el UNIQUE de la BD lo rechaza y el except muestra el error.
def crear_disciplina(nombre):
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("INSERT INTO disciplina (nombre) VALUES (%s)", (nombre,))
        conn.commit()
        print("Disciplina creada correctamente.")
    except Exception as e:
        print(f"Error al crear disciplina: {e}")
    finally:
        cursor.close()
        conn.close()

# BAJA: recibe el id y elimina la disciplina.
# Si tiene actividades asociadas, MySQL rechaza la eliminacion por la foreign key.
def eliminar_disciplina(id_disciplina):
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("DELETE FROM disciplina WHERE id_disciplina = %s", (id_disciplina,))
        conn.commit()
        print("Disciplina eliminada correctamente.")
    except Exception as e:
        print(f"Error al eliminar disciplina: {e}")
    finally:
        cursor.close()
        conn.close()

# MODIFICACION: recibe el id y el nuevo nombre, actualiza el registro en la tabla.
def modificar_disciplina(id_disciplina, nombre):
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("UPDATE disciplina SET nombre=%s WHERE id_disciplina=%s", (nombre, id_disciplina))
        conn.commit()
        print("Disciplina modificada correctamente.")
    except Exception as e:
        print(f"Error al modificar disciplina: {e}")
    finally:
        cursor.close()
        conn.close()

# LISTAR: trae todas las disciplinas y las muestra en pantalla.
def listar_disciplinas():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id_disciplina, nombre FROM disciplina")
    disciplinas = cursor.fetchall()
    cursor.close()
    conn.close()
    if not disciplinas:
        print("No hay disciplinas registradas.")
        return
    print(f"\n{'ID':<5} {'Nombre'}")
    print("-" * 30)
    for d in disciplinas:
        print(f"{d[0]:<5} {d[1]}")

# MENU: muestra las opciones y llama a la funcion correspondiente segun lo que elija el usuario.
def menu_disciplinas():
    while True:
        print("\n--- ABM Disciplinas ---")
        print("1. Listar disciplinas")
        print("2. Crear disciplina")
        print("3. Modificar disciplina")
        print("4. Eliminar disciplina")
        print("0. Volver")
        opcion = input("Elegir opcion: ")

        if opcion == "1":
            listar_disciplinas()

        elif opcion == "2":
            nombre = input("Nombre de la disciplina: ")
            crear_disciplina(nombre)

        elif opcion == "3":
            listar_disciplinas()
            id_disc = input("ID de la disciplina a modificar: ")
            nombre  = input("Nuevo nombre: ")
            modificar_disciplina(id_disc, nombre)

        elif opcion == "4":
            listar_disciplinas()
            id_disc   = input("ID de la disciplina a eliminar: ")
            confirmar = input(f"Confirmar eliminacion de la disciplina {id_disc}? (s/n): ")
            if confirmar.lower() == "s":
                eliminar_disciplina(id_disc)

        elif opcion == "0":
            break