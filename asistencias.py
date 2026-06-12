from database import get_connection
from actividades import listar_actividades

# REGISTRAR ASISTENCIA: verifica que el estudiante tenga inscripcion confirmada
# en la actividad antes de registrar. Si no esta confirmado, rechaza el registro.
# Tambien evita duplicados — no se puede registrar dos veces el mismo estudiante
# en la misma actividad para la misma fecha.
def registrar_asistencia(id_inscripcion, fecha):
    conn = get_connection()
    cursor = conn.cursor()
    try:
        # Verifica que la inscripcion exista y sea confirmada
        cursor.execute("""
            SELECT estado FROM inscripcion
            WHERE id_inscripcion = %s
        """, (id_inscripcion,))
        inscripcion = cursor.fetchone()
        if not inscripcion:
            print("Inscripcion no encontrada.")
            return
        if inscripcion[0] != 'confirmada':
            print("Solo se puede registrar asistencia de estudiantes con inscripcion confirmada.")
            return

        # Inserta la asistencia — si ya existe para esa fecha el UNIQUE de la BD lo rechaza
        cursor.execute("""
            INSERT INTO asistencia (id_inscripcion, fecha)
            VALUES (%s, %s)
        """, (id_inscripcion, fecha))
        conn.commit()
        print("Asistencia registrada correctamente.")

    except Exception as e:
        print(f"Error al registrar asistencia: {e}")
    finally:
        cursor.close()
        conn.close()

# LISTAR ASISTENCIA: muestra todos los registros de asistencia de una actividad
# para una fecha determinada, con los datos del estudiante.
def listar_asistencia(id_actividad, fecha):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT e.documento, e.nombre, e.apellido, a.fecha
        FROM asistencia a
        JOIN inscripcion i ON a.id_inscripcion = i.id_inscripcion
        JOIN estudiante e ON i.id_estudiante = e.id_estudiante
        WHERE i.id_actividad = %s AND a.fecha = %s
    """, (id_actividad, fecha))
    registros = cursor.fetchall()
    cursor.close()
    conn.close()
    if not registros:
        print("No hay asistencias registradas para esa fecha.")
        return
    print(f"\n{'Documento':<15} {'Nombre':<15} {'Apellido':<15} {'Fecha'}")
    print("-" * 55)
    for r in registros:
        print(f"{r[0]:<15} {r[1]:<15} {r[2]:<15} {str(r[3])}")

# MENU: muestra las opciones y llama a la funcion correspondiente segun lo que elija el usuario.
def menu_asistencias():
    while True:
        print("\n--- Registro de Asistencias ---")
        print("1. Registrar asistencia")
        print("2. Ver asistencia por actividad y fecha")
        print("0. Volver")
        opcion = input("Elegir opcion: ")

        if opcion == "1":
            listar_actividades()
            id_act  = input("ID de la actividad: ")
            from inscripciones import listar_inscriptos
            listar_inscriptos(id_act)
            id_insc = input("ID de la inscripcion: ")
            fecha   = input("Fecha (YYYY-MM-DD): ")
            registrar_asistencia(id_insc, fecha)

        elif opcion == "2":
            listar_actividades()
            id_act = input("ID de la actividad: ")
            fecha  = input("Fecha (YYYY-MM-DD): ")
            listar_asistencia(id_act, fecha)

        elif opcion == "0":
            break