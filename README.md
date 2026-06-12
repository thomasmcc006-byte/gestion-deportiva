# Sistema de Gestión de Actividades Deportivas Universitarias

Trabajo Obligatorio — Base de Datos I — UCU 2026

## Integrantes
- Thomas Mc Cubbin
- [Nombre compañero]

## Requisitos previos

- Python 3.10 o superior
- MySQL Server instalado y corriendo (local)
- Librería `mysql-connector-python`

## Paso 1 — Crear la base de datos

Abrir MySQL (por ejemplo desde DataGrip o desde la consola de MySQL) y ejecutar el script completo:

```
Script_Completo.sql
```

Este script crea la base de datos `gestion_deportiva`, las 6 tablas con sus relaciones y restricciones, y carga los datos maestros y de prueba (disciplinas, espacios, estudiantes, actividades, inscripciones y asistencias).

## Paso 2 — Instalar dependencias de Python

Desde la terminal, dentro de la carpeta del proyecto:

```
pip install mysql-connector-python
```

(En Windows, si `pip` no es reconocido, usar `py -m pip install mysql-connector-python`)

## Paso 3 — Configurar la conexión

Abrir el archivo `database.py` y verificar que los datos de conexión coincidan con tu instalación de MySQL:

```python
def get_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="TU_PASSWORD",
        database="gestion_deportiva"
    )
```

## Paso 4 — Ejecutar la aplicación

Desde la terminal, dentro de la carpeta del proyecto:

```
py main.py
```

(En Linux/Mac: `python3 main.py`)

## Estructura del proyecto

```
gestion_deportiva/
├── database.py        → conexión a MySQL
├── main.py             → menú principal
├── estudiantes.py      → ABM estudiantes
├── disciplinas.py       → ABM disciplinas deportivas
├── espacios.py           → ABM espacios deportivos
├── actividades.py        → ABM actividades
├── inscripciones.py      → gestión de inscripciones y cupos
├── asistencias.py        → registro de asistencias
├── reportes.py           → consultas y reportes
├── Script_Completo.sql   → script de creación de la base de datos
└── documentacion.html    → documentación técnica del proyecto
```

## Uso del sistema

Al ejecutar `main.py` aparece un menú principal con 7 módulos:

1. **Estudiantes** — alta, baja, modificación y listado de estudiantes
2. **Disciplinas** — gestión del catálogo de disciplinas deportivas
3. **Espacios deportivos** — gestión de los espacios físicos
4. **Actividades** — creación y gestión de actividades concretas
5. **Inscripciones** — inscribir estudiantes a actividades, con control automático de cupo y lista de espera
6. **Asistencias** — registrar asistencia de estudiantes confirmados
7. **Reportes** — 10 consultas sobre el estado del sistema

Cada módulo tiene su propio submenú con las opciones correspondientes.
