# Sistema de Gestión de Actividades Deportivas Universitarias

Trabajo Obligatorio — Base de Datos I — UCU 2026

## Integrantes
- Thomas Mc Cubbin
- Juan Francisco Marquez

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

## Paso 3 — Iniciar sesión

A diferencia de versiones anteriores, `database.py` ya **no tiene credenciales fijas**. La conexión a MySQL se establece según el usuario y contraseña que se ingresen al iniciar la aplicación (ver Paso 4).

El script `Script_Completo.sql` del Paso 1 crea automáticamente 3 usuarios de MySQL, uno por cada rol del sistema, cada uno con permisos distintos (`GRANT`/`REVOKE`):

| Usuario | Contraseña | Rol | Permisos |
|---|---|---|---|
| `admin_user` | `admin123` | Administrador | Acceso total a todas las tablas |
| `docente_user` | `docente123` | Docente | Lectura de todas las tablas; alta/modificación de asistencias |
| `estudiante_user` | `estudiante123` | Estudiante | Ver disciplinas, espacios y actividades; gestionar sus propias inscripciones; ver asistencias |

Estas credenciales son las que se usan en el login del Paso 4. No es necesario editar `database.py`.

## Paso 4 — Ejecutar la aplicación

Desde la terminal, dentro de la carpeta del proyecto:

```
py main.py
```

(En Linux/Mac: `python3 main.py`)

Al iniciar, el programa pide usuario y contraseña (ver tabla del Paso 3). Si las credenciales son correctas, se muestra el menú principal con el rol correspondiente indicado en el encabezado.

## Estructura del proyecto

```
gestion_deportiva/
├── database.py        → conexión a MySQL (credenciales de sesión, ver login.py)
├── login.py            → inicio de sesión y validación de rol
├── main.py             → menú principal
├── estudiantes.py      → ABM estudiantes
├── disciplinas.py       → ABM disciplinas deportivas
├── espacios.py           → ABM espacios deportivos
├── actividades.py        → ABM actividades
├── inscripciones.py      → gestión de inscripciones y cupos
├── asistencias.py        → registro de asistencias
├── reportes.py           → consultas y reportes
├── Script_Completo.sql   → script de creación de la base de datos, datos y usuarios/permisos
└── documentacion.html    → documentación técnica del proyecto
```

## Uso del sistema

Al ejecutar `main.py`, primero se solicita usuario y contraseña (ver Paso 3). Según el rol autenticado, se muestra un menú principal con 7 módulos:

1. **Estudiantes** — alta, baja, modificación y listado de estudiantes
2. **Disciplinas** — gestión del catálogo de disciplinas deportivas
3. **Espacios deportivos** — gestión de los espacios físicos
4. **Actividades** — creación y gestión de actividades concretas
5. **Inscripciones** — inscribir estudiantes a actividades, con control automático de cupo y lista de espera
6. **Asistencias** — registrar asistencia de estudiantes confirmados
7. **Reportes** — 10 consultas sobre el estado del sistema

Cada módulo tiene su propio submenú con las opciones correspondientes. Las operaciones para las que el usuario autenticado no tiene permiso (según su rol) son rechazadas por MySQL y mostradas como un mensaje de error, sin interrumpir el programa.
