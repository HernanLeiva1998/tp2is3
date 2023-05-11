import re

from src.web.controllers.validators.common_validators import (
    valores_dicc_none,
    valores_dicc_vacios,
)


def validar_inputs(dato):
    """Esta funcion valida que los inputs sean del tipo correcto."""
    if valores_dicc_none(dato) or valores_dicc_vacios(dato):
        return False, "Todos los datos deben llenarse"

    email_regular = "^[A-Za-z0-9]+[\._]?[A-Za-z0-9]+[@]\w+[.]\w{2,3}$"
    if not (dato["dni"].isdigit() and dato["telefono"].isdigit()):
        return (False,
                "El telefono y dni deben ser solo numeros, sin guiones ni puntos.")
    elif not (
        re.fullmatch(r"[A-Za-z ]{1,50}", dato["nombre"])
        and re.fullmatch(r"[A-Za-z ]{1,50}", dato["apellido"])
    ):
        return False, "El nombre o apellido son incorrectos."
    elif not (re.search(email_regular, dato["email"])):
        return False, "El email debe ser valido"
    elif len(dato["dni"]) != 8:
        return False, "El dni debe contener 8 numeros"
    elif len(dato["telefono"]) != 10 and len(dato["telefono"]) != 7:
        return (
            False,
            "El numero de telefono debe tener 10 numeros si es celular y 7 si es de casa.",
         )
    elif (
        dato["genero"] != "Masculino"
        and dato["genero"] != "Femenino"
        and dato["genero"] != "Otro"
    ):
        return False, "El genero debe estar dentro de las opciones."
    elif (
        dato["tipo_documento"] != "DNI"
        and dato["tipo_documento"] != "LE"
        and dato["tipo_documento"] != "LC"
        and dato["tipo_documento"] != "DE"
    ):
        return False, "El tipo de documento debe estar dentro de las opciones."
    else:
        return True, "Inputs Validos"


def validar_inscripcion(id_socio, id_disciplina):
    if not (id_socio.isdigit() and id_disciplina.isdigit()):
        return False, "No se ha seleccionado ninguna opcion"
    else:
        return True, "Seleccion valida"
