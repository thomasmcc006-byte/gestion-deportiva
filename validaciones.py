# VALIDACIONES: funciones simples para revisar los datos ingresados por el usuario
# ANTES de mandarlos a la base de datos. Si el dato no es valido, se devuelve
# un mensaje propio y claro, en vez de dejar que MySQL devuelva un error tecnico.

# Revisa que el texto no este vacio (ni sea solo espacios)
def validar_no_vacio(valor, nombre_campo):
    if not valor or not valor.strip():
        return False, f"{nombre_campo} no puede estar vacio."
    return True, None

# Revisa que el valor sea un numero entero mayor a cero (ej: cupo maximo)
def validar_entero_positivo(valor, nombre_campo):
    try:
        numero = int(valor)
    except ValueError:
        return False, f"{nombre_campo} debe ser un numero entero."
    if numero <= 0:
        return False, f"{nombre_campo} debe ser mayor a cero."
    return True, None

# Revisa un formato basico de email: algo@algo.algo
def validar_email(valor, nombre_campo="Email"):
    if not valor or "@" not in valor or "." not in valor.split("@")[-1]:
        return False, f"{nombre_campo} no tiene un formato valido (ejemplo: nombre@dominio.com)."
    return True, None