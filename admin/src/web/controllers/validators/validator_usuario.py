import re

from src.web.controllers.validators.common_validators import (
    dict_values_are_none,
    dict_values_are_empty,
)

REGEX_EMAIL = "^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w{2,3}$"


def validar_inputs_add(data, roles):
    """Esta funcion valida que los inputs sean
    del tipo correcto durante la adición."""
    if dict_values_are_none(data) or dict_values_are_empty(data):
        return False, "Todos los datos deben llenarse"
    if roles["ROL_OPERADOR"] is None and roles["ROL_ADMINISTRADOR"] is None:
        return False, "Se debe seleccionar un rol"
    if roles["ROL_OPERADOR"] == "" and roles["ROL_ADMINISTRADOR"] == "":
        return False, "Se debe seleccionar un rol"
    return validar_email(data["email"])


def validar_inputs(data):
    """Esta funcion valida que los inputs sean
    del tipo correcto durante la modificación o el auth."""
    if dict_values_are_none(data) or dict_values_are_empty(data):
        return False, "Todos los datos deben llenarse"
    return validar_email(data["email"])


def validar_email(email):
    if not (re.search(REGEX_EMAIL, email)):
        return False, "El email debe ser valido"
    else:
        return True, "Credenciales validas"
