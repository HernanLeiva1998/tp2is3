import re

from src.web.controllers.validators.common_validators import (
    valores_dicc_none,
    valores_dicc_vacios,
)

EMAIL_REGULAR = "^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w{2,3}$"


def validar_inputs_agregar(dato, roles):
    """Esta funcion valida que los inputs sean
    del tipo correcto durante la adición."""
    if valores_dicc_none(dato) or valores_dicc_vacios(dato):
        return False, "Todos los datos deben llenarse"
    if roles["ROL_OPERADOR"] is None and roles["ROL_ADMINISTRADOR"] is None:
        return False, "Se debe seleccionar un rol"
    if roles["ROL_OPERADOR"] == "" and roles["ROL_ADMINISTRADOR"] == "":
        return False, "Se debe seleccionar un rol"
    return validar_email(data["email"])


def validar_inputs(dato):
    """Esta funcion valida que los inputs sean
    del tipo correcto durante la modificación o el auth."""
    if valores_dicc_none(dato) or valores_dicc_vacios(dato):
        return False, "Todos los datos deben llenarse"
    return validar_email(dato["email"])


def validar_email(email):
    if not (re.search(EMAIL_REGULAR, email)):
        return False, "El email debe ser valido"
    else:
        return True, "Credenciales validas"
