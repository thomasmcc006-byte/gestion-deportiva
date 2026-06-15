from database import get_connection
from disciplinas import listar_disciplinas
from espacios import listar_espacios
from validaciones import validar_entero_positivo
# ALTA: recibe todos los datos de la actividad y la inserta en la tabla.
# Muestra primero las disciplinas y espacios disponibles para que el usuario elija por ID.
def crear_actividad(nombre, id_disciplina, id_espacio, cupo_maximo, dia, horario):
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("""
            INSERT INTO actividad (nombre, id_disciplina, id_espacio, cupo_maximo, dia, horario, estado)
            VALUES (%s, %s, %s, %s, %s, %s, 'abierta')
        """, (nombre, id_disciplina, id_espacio, cupo_maximo, dia, horario))
        conn.commit()
        print("Actividad creada correctamente.")
    except Exception as e:
        print(f"Error al crear actividad: {e}")
    finally:
        cursor.close()
        conn.close()

# BAJA: recibe el id y elimina la actividad.
# Si tiene inscripciones asociadas, MySQL rechaza la eliminacion por la foreign key.
def eliminar_actividad(id_actividad):
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("DELETE FROM actividad WHERE id_actividad = %s", (id_actividad,))
        conn.commit()
        print("Actividad eliminada correctamente.")
    except Exception as e:
        print(f"Error al eliminar actividad: {e}")
    finally:
        cursor.close()
        conn.close()

# MODIFICACION: actualiza los datos editables de la actividad.
# El estado se cambia aparte con cambiar_estado para mayor control.
def modificar_actividad(id_actividad, nombre, cupo_maximo, dia, horario):
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("""
            UPDATE actividad SET nombre=%s, cupo_maximo=%s, dia=%s, horario=%s
            WHERE id_actividad=%s
        """, (nombre, cupo_maximo, dia, horario, id_actividad))
        conn.commit()
        print("Actividad modificada correctamente.")
    except Exception as e:
        print(f"Error al modificar actividad: {e}")
    finally:
        cursor.close()
        conn.close()

# CAMBIAR ESTADO: cambia el estado de la actividad (abierta/cerrada/finalizada/cancelada).
# Es una operacion separada porque tiene impacto directo en las reglas de negocio
# — una actividad cerrada o cancelada no acepta nuevas inscripciones.
def cambiar_estado(id_actividad, nuevo_estado):
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute(
            "UPDATE actividad SET estado=%s WHERE id_actividad=%s",
            (nuevo_estado, id_actividad)
        )
        conn.commit()
        print(f"Estado actualizado a '{nuevo_estado}'.")
    except Exception as e:
        print(f"Error al cambiar estado: {e}")
    finally:
        cursor.close()
        conn.close()

# LISTAR: trae todas las actividades con el nombre de su disciplina y espacio,
# usando JOIN para mostrar los nombres en vez de solo los IDs.
def listar_actividades():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT a.id_actividad, a.nombre, d.nombre, e.nombre, a.cupo_maximo, a.dia, a.horario, a.estado
        FROM actividad a
        JOIN disciplina d ON a.id_disciplina = d.id_disciplina
        JOIN espacio_deportivo e ON a.id_espacio = e.id_espacio
    """)
    actividades = cursor.fetchall()
    cursor.close()
    conn.close()
    if not actividades:
        print("No hay actividades registradas.")
        return
    print(f"\n{'ID':<5} {'Nombre':<25} {'Disciplina':<15} {'Espacio':<20} {'Cupo':<6} {'Dia':<12} {'Horario':<10} {'Estado'}")
    print("-" * 105)
    for a in actividades:
        print(f"{a[0]:<5} {a[1]:<25} {a[2]:<15} {a[3]:<20} {a[4]:<6} {a[5]:<12} {str(a[6]):<10} {a[7]}")

# MENU: muestra las opciones y llama a la funcion correspondiente segun lo que elija el usuario.
def menu_actividades():
    estados_validos = ['abierta', 'cerrada', 'finalizada', 'cancelada']
    dias_validos    = ['Lunes', 'Martes', 'Miercoles', 'Jueves', 'Viernes', 'Sabado', 'Domingo']

    while True:
        print("\n--- ABM Actividades ---")
        print("1. Listar actividades")
        print("2. Crear actividad")
        print("3. Modificar actividad")
        print("4. Cambiar estado")
        print("5. Eliminar actividad")
        print("0. Volver")
        opcion = input("Elegir opcion: ")

        if opcion == "1":
            listar_actividades()

        elif opcion == "2":
            listar_disciplinas()
            id_disc = input("ID de la disciplina: ")
            listar_espacios()
            id_esp  = input("ID del espacio: ")
            nombre  = input("Nombre de la actividad: ")
            cupo    = input("Cupo maximo: ")

            ok, error = validar_entero_positivo(cupo, "El cupo maximo")
            if not ok:
                print(f"Error: {error}")
                continue

            print(f"Dias disponibles: {', '.join(dias_validos)}")
            dia     = input("Dia: ")
            if dia not in dias_validos:
                print("Error: dia no valido. Debe ser uno de los dias listados.")
                continue

            horario = input("Horario (HH:MM): ")
            crear_actividad(nombre, id_disc, id_esp, cupo, dia, horario)

        elif opcion == "3":
            listar_actividades()
            id_act  = input("ID de la actividad a modificar: ")
            nombre  = input("Nuevo nombre: ")
            cupo    = input("Nuevo cupo maximo: ")
            print(f"Dias disponibles: {', '.join(dias_validos)}")
            dia     = input("Nuevo dia: ")
            horario = input("Nuevo horario (HH:MM): ")
            modificar_actividad(id_act, nombre, cupo, dia, horario)

        elif opcion == "4":
            listar_actividades()
            id_act = input("ID de la actividad: ")
            print(f"Estados disponibles: {', '.join(estados_validos)}")
            estado = input("Nuevo estado: ")
            if estado in estados_validos:
                cambiar_estado(id_act, estado)
            else:
                print("Estado no valido.")

        elif opcion == "5":
            listar_actividades()
            id_act    = input("ID de la actividad a eliminar: ")
            confirmar = input(f"Confirmar eliminacion de la actividad {id_act}? (s/n): ")
            if confirmar.lower() == "s":
                eliminar_actividad(id_act)

        elif opcion == "0":
            break
