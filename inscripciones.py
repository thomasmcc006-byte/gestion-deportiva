from database import get_connection
from estudiantes import listar_estudiantes
from actividades import listar_actividades

# INSCRIBIR: es la funcion principal del sistema.
# Primero verifica que la actividad este abierta.
# Luego verifica que el estudiante no este ya inscripto en esa actividad.
# Despues cuenta cuantos inscriptos confirmados hay y los compara con el cupo maximo.
# Si hay lugar disponible la inscripcion queda confirmada, si no queda en lista de espera.
def inscribir_estudiante(id_estudiante, id_actividad):
    conn = get_connection()
    cursor = conn.cursor()
    try:
        # Verifica que la actividad exista y este abierta
        cursor.execute("SELECT estado, cupo_maximo FROM actividad WHERE id_actividad = %s", (id_actividad,))
        actividad = cursor.fetchone()
        if not actividad:
            print("La actividad no existe.")
            return
        if actividad[0] != 'abierta':
            print(f"No se puede inscribir. La actividad esta '{actividad[0]}'.")
            return

        # Verifica que el estudiante no este ya inscripto
        cursor.execute("""
            SELECT id_inscripcion FROM inscripcion
            WHERE id_estudiante = %s AND id_actividad = %s
        """, (id_estudiante, id_actividad))
        if cursor.fetchone():
            print("El estudiante ya esta inscripto en esta actividad.")
            return

        # Cuenta los inscriptos confirmados y compara con el cupo
        cursor.execute("""
            SELECT COUNT(*) FROM inscripcion
            WHERE id_actividad = %s AND estado = 'confirmada'
        """, (id_actividad,))
        confirmados = cursor.fetchone()[0]

        if confirmados < actividad[1]:
            estado = 'confirmada'
        else:
            estado = 'lista_espera'

        # Inserta la inscripcion con el estado correspondiente
        cursor.execute("""
            INSERT INTO inscripcion (id_estudiante, id_actividad, estado)
            VALUES (%s, %s, %s)
        """, (id_estudiante, id_actividad, estado))
        conn.commit()
        print(f"Inscripcion realizada. Estado: {estado}.")

    except Exception as e:
        print(f"Error al inscribir: {e}")
    finally:
        cursor.close()
        conn.close()

# CANCELAR: elimina la inscripcion del estudiante.
# Si el estudiante cancelado tenia estado confirmada y hay alguien en lista de espera,
# automaticamente asciende al primero de la lista a confirmada — liberando el cupo.
def cancelar_inscripcion(id_inscripcion):
    conn = get_connection()
    cursor = conn.cursor()
    try:
        # Obtiene los datos de la inscripcion antes de eliminarla
        cursor.execute("""
            SELECT id_estudiante, id_actividad, estado FROM inscripcion
            WHERE id_inscripcion = %s
        """, (id_inscripcion,))
        inscripcion = cursor.fetchone()
        if not inscripcion:
            print("Inscripcion no encontrada.")
            return

        id_actividad = inscripcion[1]
        estado_cancelado = inscripcion[2]

        # Elimina la inscripcion
        cursor.execute("DELETE FROM inscripcion WHERE id_inscripcion = %s", (id_inscripcion,))

        # Si era confirmada, busca el primero en lista de espera y lo asciende
        if estado_cancelado == 'confirmada':
            cursor.execute("""
                SELECT id_inscripcion FROM inscripcion
                WHERE id_actividad = %s AND estado = 'lista_espera'
                ORDER BY fecha_inscripcion ASC
                LIMIT 1
            """, (id_actividad,))
            siguiente = cursor.fetchone()
            if siguiente:
                cursor.execute("""
                    UPDATE inscripcion SET estado = 'confirmada'
                    WHERE id_inscripcion = %s
                """, (siguiente[0],))
                print("Se ascendio al siguiente en lista de espera a confirmada.")

        conn.commit()
        print("Inscripcion cancelada correctamente.")

    except Exception as e:
        print(f"Error al cancelar inscripcion: {e}")
    finally:
        cursor.close()
        conn.close()

# LISTAR POR ACTIVIDAD: muestra todos los inscriptos de una actividad con su estado.
def listar_inscriptos(id_actividad):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT i.id_inscripcion, e.documento, e.nombre, e.apellido, i.estado, i.fecha_inscripcion
        FROM inscripcion i
        JOIN estudiante e ON i.id_estudiante = e.id_estudiante
        WHERE i.id_actividad = %s
        ORDER BY i.estado, i.fecha_inscripcion
    """, (id_actividad,))
    inscriptos = cursor.fetchall()
    cursor.close()
    conn.close()
    if not inscriptos:
        print("No hay inscriptos en esta actividad.")
        return
    print(f"\n{'ID Insc':<10} {'Documento':<15} {'Nombre':<15} {'Apellido':<15} {'Estado':<15} {'Fecha'}")
    print("-" * 85)
    for i in inscriptos:
        print(f"{i[0]:<10} {i[1]:<15} {i[2]:<15} {i[3]:<15} {i[4]:<15} {str(i[5])}")

# MENU: muestra las opciones y llama a la funcion correspondiente segun lo que elija el usuario.
def menu_inscripciones():
    while True:
        print("\n--- Gestion de Inscripciones ---")
        print("1. Inscribir estudiante")
        print("2. Cancelar inscripcion")
        print("3. Ver inscriptos de una actividad")
        print("0. Volver")
        opcion = input("Elegir opcion: ")

        if opcion == "1":
            listar_estudiantes()
            id_est = input("ID del estudiante: ")
            listar_actividades()
            id_act = input("ID de la actividad: ")
            inscribir_estudiante(id_est, id_act)

        elif opcion == "2":
            listar_actividades()
            id_act = input("ID de la actividad para ver inscriptos: ")
            listar_inscriptos(id_act)
            id_insc = input("ID de la inscripcion a cancelar: ")
            cancelar_inscripcion(id_insc)

        elif opcion == "3":
            listar_actividades()
            id_act = input("ID de la actividad: ")
            listar_inscriptos(id_act)

        elif opcion == "0":
            break