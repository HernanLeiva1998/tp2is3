import re

from src.web.controllers.validators.common_validators import (
    dict_values_are_none,
    dict_values_are_empty,
)


def validar_inputs(data):
    """Esta funcion valida que los inputs sean del tipo correcto."""
    if dict_values_are_none(data) or dict_values_are_empty(data):
        return False, "Todos los datos deben llenarse"

    regex_email = "^[A-Za-z0-9]+[\._]?[A-Za-z0-9]+[@]\w+[.]\w{2,3}$"
    if not (data["dni"].isdigit() and data["telefono"].isdigit()):
        return False, "El telefono y dni deben ser solo numeros, sin guiones ni puntos."
    elif not (
        re.fullmatch(r"[A-Za-z ]{1,50}", data["nombre"])
        and re.fullmatch(r"[A-Za-z ]{1,50}", data["apellido"])
    ):
        return False, "El nombre o apellido son incorrectos."
    elif not (re.search(regex_email, data["email"])):
        return False, "El email debe ser valido"
    elif len(data["dni"]) != 8:
        return False, "El dni debe contener 8 numeros"
    elif len(data["telefono"]) != 10 and len(data["telefono"]) != 7:
        return (
            False,
            "El numero de telefono debe tener 10 numeros si es celular y 7 si es de casa.",
        )
    elif (
        data["genero"] != "Masculino"
        and data["genero"] != "Femenino"
        and data["genero"] != "Otro"
    ):
        return False, "El genero debe estar dentro de las opciones."
    elif (
        data["tipo_documento"] != "DNI"
        and data["tipo_documento"] != "LE"
        and data["tipo_documento"] != "LC"
        and data["tipo_documento"] != "DE"
    ):
        return False, "El tipo de documento debe estar dentro de las opciones."
    else:
        return True, "Inputs Validos"


def validar_inscripcion(id_socio, id_disciplina):
    if not (id_socio.isdigit() and id_disciplina.isdigit()):
        return False, "No se ha seleccionado ninguna opcion"
    else:
        return True, "Seleccion valida"
