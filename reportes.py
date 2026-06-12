from database import get_connection

# REPORTE 1: muestra las actividades ordenadas por cantidad de inscriptos confirmados,
# de mayor a menor. Usa GROUP BY para agrupar por actividad y COUNT para contar inscriptos.
def actividades_mas_inscriptos():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT a.nombre, d.nombre, COUNT(i.id_inscripcion) AS total
        FROM actividad a
        JOIN disciplina d ON a.id_disciplina = d.id_disciplina
        LEFT JOIN inscripcion i ON a.id_actividad = i.id_actividad AND i.estado = 'confirmada'
        GROUP BY a.id_actividad, a.nombre, d.nombre
        ORDER BY total DESC
    """)
    resultados = cursor.fetchall()
    cursor.close()
    conn.close()
    print(f"\n{'Actividad':<30} {'Disciplina':<20} {'Inscriptos'}")
    print("-" * 65)
    for r in resultados:
        print(f"{r[0]:<30} {r[1]:<20} {r[2]}")

# REPORTE 2: muestra las actividades abiertas que todavia tienen cupos disponibles,
# calculando cupo_maximo menos la cantidad de inscriptos confirmados.
def actividades_con_cupo():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT a.nombre, a.cupo_maximo,
               COUNT(i.id_inscripcion) AS confirmados,
               a.cupo_maximo - COUNT(i.id_inscripcion) AS disponibles
        FROM actividad a
        LEFT JOIN inscripcion i ON a.id_actividad = i.id_actividad AND i.estado = 'confirmada'
        WHERE a.estado = 'abierta'
        GROUP BY a.id_actividad, a.nombre, a.cupo_maximo
        HAVING disponibles > 0
        ORDER BY disponibles DESC
    """)
    resultados = cursor.fetchall()
    cursor.close()
    conn.close()
    print(f"\n{'Actividad':<30} {'Cupo Max':<10} {'Confirmados':<13} {'Disponibles'}")
    print("-" * 65)
    for r in resultados:
        print(f"{r[0]:<30} {r[1]:<10} {r[2]:<13} {r[3]}")

# REPORTE 3: muestra la cantidad total de inscriptos confirmados agrupados por disciplina.
def inscriptos_por_disciplina():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT d.nombre, COUNT(i.id_inscripcion) AS total
        FROM disciplina d
        LEFT JOIN actividad a ON d.id_disciplina = a.id_disciplina
        LEFT JOIN inscripcion i ON a.id_actividad = i.id_actividad AND i.estado = 'confirmada'
        GROUP BY d.id_disciplina, d.nombre
        ORDER BY total DESC
    """)
    resultados = cursor.fetchall()
    cursor.close()
    conn.close()
    print(f"\n{'Disciplina':<25} {'Inscriptos'}")
    print("-" * 40)
    for r in resultados:
        print(f"{r[0]:<25} {r[1]}")

# REPORTE 4: muestra la cantidad de inscriptos confirmados agrupados por carrera y facultad.
def inscriptos_por_carrera():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT e.facultad, e.carrera, COUNT(i.id_inscripcion) AS total
        FROM estudiante e
        JOIN inscripcion i ON e.id_estudiante = i.id_estudiante AND i.estado = 'confirmada'
        GROUP BY e.facultad, e.carrera
        ORDER BY e.facultad, total DESC
    """)
    resultados = cursor.fetchall()
    cursor.close()
    conn.close()
    print(f"\n{'Facultad':<35} {'Carrera':<30} {'Inscriptos'}")
    print("-" * 75)
    for r in resultados:
        print(f"{r[0]:<35} {r[1]:<30} {r[2]}")

# REPORTE 5: calcula el porcentaje de ocupacion de cada actividad
# dividiendo los inscriptos confirmados sobre el cupo maximo y multiplicando por 100.
def porcentaje_ocupacion():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT a.nombre, a.cupo_maximo,
               COUNT(i.id_inscripcion) AS confirmados,
               ROUND(COUNT(i.id_inscripcion) * 100.0 / a.cupo_maximo, 1) AS porcentaje
        FROM actividad a
        LEFT JOIN inscripcion i ON a.id_actividad = i.id_actividad AND i.estado = 'confirmada'
        GROUP BY a.id_actividad, a.nombre, a.cupo_maximo
        ORDER BY porcentaje DESC
    """)
    resultados = cursor.fetchall()
    cursor.close()
    conn.close()
    print(f"\n{'Actividad':<30} {'Cupo':<8} {'Confirmados':<13} {'Ocupacion %'}")
    print("-" * 65)
    for r in resultados:
        print(f"{r[0]:<30} {r[1]:<8} {r[2]:<13} {r[3]}%")

# REPORTE 6: calcula el porcentaje de asistencia por actividad,
# comparando la cantidad de asistencias registradas contra el total de clases posibles
# (inscriptos confirmados multiplicado por la cantidad de fechas distintas registradas).
def porcentaje_asistencia():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT a.nombre,
               COUNT(DISTINCT ast.fecha) AS clases,
               COUNT(DISTINCT i.id_inscripcion) AS confirmados,
               COUNT(ast.id_asistencia) AS asistencias_totales,
               ROUND(COUNT(ast.id_asistencia) * 100.0 /
                     NULLIF(COUNT(DISTINCT i.id_inscripcion) * COUNT(DISTINCT ast.fecha), 0), 1) AS porcentaje
        FROM actividad a
        LEFT JOIN inscripcion i ON a.id_actividad = i.id_actividad AND i.estado = 'confirmada'
        LEFT JOIN asistencia ast ON i.id_inscripcion = ast.id_inscripcion
        GROUP BY a.id_actividad, a.nombre
        ORDER BY porcentaje DESC
    """)
    resultados = cursor.fetchall()
    cursor.close()
    conn.close()
    print(f"\n{'Actividad':<30} {'Clases':<8} {'Confirmados':<13} {'Asistencias':<13} {'Asistencia %'}")
    print("-" * 75)
    for r in resultados:
        print(f"{r[0]:<30} {r[1]:<8} {r[2]:<13} {r[3]:<13} {r[4] or 0}%")

# REPORTE 7: lista los estudiantes que tienen 3 o mas inasistencias registradas.
# Una inasistencia es una clase que ocurrio (hay asistencia de otros ese dia)
# pero el estudiante confirmado no aparece en los registros de asistencia.
def estudiantes_con_inasistencias():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT e.nombre, e.apellido, e.documento, a.nombre AS actividad,
               COUNT(DISTINCT ast_otros.fecha) - COUNT(DISTINCT ast_propio.fecha) AS inasistencias
        FROM inscripcion i
        JOIN estudiante e ON i.id_estudiante = e.id_estudiante
        JOIN actividad a ON i.id_actividad = a.id_actividad
        LEFT JOIN asistencia ast_propio ON ast_propio.id_inscripcion = i.id_inscripcion
        LEFT JOIN asistencia ast_otros ON ast_otros.id_inscripcion != i.id_inscripcion
            AND ast_otros.id_inscripcion IN (
                SELECT id_inscripcion FROM inscripcion
                WHERE id_actividad = i.id_actividad AND estado = 'confirmada'
            )
        WHERE i.estado = 'confirmada'
        GROUP BY i.id_inscripcion, e.nombre, e.apellido, e.documento, a.nombre
        HAVING inasistencias >= 3
        ORDER BY inasistencias DESC
    """)
    resultados = cursor.fetchall()
    cursor.close()
    conn.close()
    if not resultados:
        print("No hay estudiantes con 3 o mas inasistencias.")
        return
    print(f"\n{'Nombre':<15} {'Apellido':<15} {'Documento':<15} {'Actividad':<25} {'Inasistencias'}")
    print("-" * 80)
    for r in resultados:
        print(f"{r[0]:<15} {r[1]:<15} {r[2]:<15} {r[3]:<25} {r[4]}")

# REPORTE 8 (propuesto): muestra actividades que tienen estudiantes en lista de espera,
# util para saber donde hay demanda no satisfecha y considerar abrir mas cupos.
def actividades_con_lista_espera():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT a.nombre, d.nombre, COUNT(i.id_inscripcion) AS en_espera
        FROM actividad a
        JOIN disciplina d ON a.id_disciplina = d.id_disciplina
        JOIN inscripcion i ON a.id_actividad = i.id_actividad AND i.estado = 'lista_espera'
        GROUP BY a.id_actividad, a.nombre, d.nombre
        ORDER BY en_espera DESC
    """)
    resultados = cursor.fetchall()
    cursor.close()
    conn.close()
    if not resultados:
        print("No hay actividades con lista de espera.")
        return
    print(f"\n{'Actividad':<30} {'Disciplina':<20} {'En espera'}")
    print("-" * 60)
    for r in resultados:
        print(f"{r[0]:<30} {r[1]:<20} {r[2]}")

# REPORTE 9 (propuesto): muestra los estudiantes con mas inscripciones confirmadas,
# util para identificar los estudiantes mas activos deportivamente.
def estudiantes_mas_activos():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT e.nombre, e.apellido, e.carrera, COUNT(i.id_inscripcion) AS actividades
        FROM estudiante e
        JOIN inscripcion i ON e.id_estudiante = i.id_estudiante AND i.estado = 'confirmada'
        GROUP BY e.id_estudiante, e.nombre, e.apellido, e.carrera
        ORDER BY actividades DESC
        LIMIT 10
    """)
    resultados = cursor.fetchall()
    cursor.close()
    conn.close()
    print(f"\n{'Nombre':<15} {'Apellido':<15} {'Carrera':<25} {'Actividades'}")
    print("-" * 65)
    for r in resultados:
        print(f"{r[0]:<15} {r[1]:<15} {r[2]:<25} {r[3]}")

# REPORTE 10 (propuesto): muestra actividades sin ningun inscripto,
# util para detectar actividades que no generaron interes y considerar cancelarlas.
def actividades_sin_inscriptos():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT a.nombre, d.nombre, a.estado
        FROM actividad a
        JOIN disciplina d ON a.id_disciplina = d.id_disciplina
        LEFT JOIN inscripcion i ON a.id_actividad = i.id_actividad
        WHERE i.id_inscripcion IS NULL
        ORDER BY a.nombre
    """)
    resultados = cursor.fetchall()
    cursor.close()
    conn.close()
    if not resultados:
        print("Todas las actividades tienen al menos un inscripto.")
        return
    print(f"\n{'Actividad':<30} {'Disciplina':<20} {'Estado'}")
    print("-" * 60)
    for r in resultados:
        print(f"{r[0]:<30} {r[1]:<20} {r[2]}")

# MENU REPORTES: muestra todas las consultas disponibles y ejecuta la elegida.
def menu_reportes():
    while True:
        print("\n--- Reportes ---")
        print("1.  Actividades con mas inscriptos confirmados")
        print("2.  Actividades con cupos disponibles")
        print("3.  Inscriptos por disciplina")
        print("4.  Inscriptos por carrera y facultad")
        print("5.  Porcentaje de ocupacion por actividad")
        print("6.  Porcentaje de asistencia por actividad")
        print("7.  Estudiantes con 3 o mas inasistencias")
        print("8.  Actividades con lista de espera")
        print("9.  Estudiantes mas activos")
        print("10. Actividades sin inscriptos")
        print("0.  Volver")
        opcion = input("Elegir opcion: ")

        if opcion == "1":
            actividades_mas_inscriptos()
        elif opcion == "2":
            actividades_con_cupo()
        elif opcion == "3":
            inscriptos_por_disciplina()
        elif opcion == "4":
            inscriptos_por_carrera()
        elif opcion == "5":
            porcentaje_ocupacion()
        elif opcion == "6":
            porcentaje_asistencia()
        elif opcion == "7":
            estudiantes_con_inasistencias()
        elif opcion == "8":
            actividades_con_lista_espera()
        elif opcion == "9":
            estudiantes_mas_activos()
        elif opcion == "10":
            actividades_sin_inscriptos()
        elif opcion == "0":
            break
        else:
            print("Opcion no valida.")