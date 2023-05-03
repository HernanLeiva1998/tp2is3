from src.web.controllers.validators.common_validators import (
    is_integer,
    dict_values_are_none,
    dict_values_are_empty,
)


def validar_inputs(json):
    # El json en sí siempre va a ser enviado, por cómo está definido
    # el frontend y por tener el jwt_required en la api.
    if dict_values_are_none(json) or dict_values_are_empty(json):
        return False  # El mes y el monto deben estar presentes
    if not is_integer(json["month"]):
        return False  # El mes no es un número
    if not is_integer(json["amount"]):
        return False  # El monto no es un número
    if not es_mes(json["month"]):
        return False  # El mes no es un mes
    return True  # Datos válidos


def es_mes(mes):
    return int(mes) in range(1, 13)
