from estudiantes import menu_estudiantes
from disciplinas import menu_disciplinas
from espacios import menu_espacios
from actividades import menu_actividades
from inscripciones import menu_inscripciones
from asistencias import menu_asistencias
from reportes import menu_reportes

# MENU PRINCIPAL: es el punto de entrada del sistema.
# Desde aca el usuario accede a todos los modulos del sistema.
# Cada opcion llama al menu correspondiente de cada archivo.
def main():
    while True:
        print("\n========================================")
        print("  Sistema de Gestion Deportiva UCU")
        print("========================================")
        print("1. Estudiantes")
        print("2. Disciplinas")
        print("3. Espacios deportivos")
        print("4. Actividades")
        print("5. Inscripciones")
        print("6. Asistencias")
        print("7. Reportes")
        print("0. Salir")
        opcion = input("Elegir opcion: ")

        if opcion == "1":
            menu_estudiantes()
        elif opcion == "2":
            menu_disciplinas()
        elif opcion == "3":
            menu_espacios()
        elif opcion == "4":
            menu_actividades()
        elif opcion == "5":
            menu_inscripciones()
        elif opcion == "6":
            menu_asistencias()
        elif opcion == "7":
            menu_reportes()
        elif opcion == "0":
            print("Saliendo del sistema.")
            break
        else:
            print("Opcion no valida.")

# Punto de entrada del programa — solo se ejecuta si corres este archivo directamente
if __name__ == "__main__":
    main()