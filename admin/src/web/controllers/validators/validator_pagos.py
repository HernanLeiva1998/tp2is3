from src.web.controllers.validators.common_validators import (
    es_entero,
    valores_dicc_none,
    valores_dicc_vacios,
)


def validar_inputs(json):
    # El json en sí siempre va a ser enviado, por cómo está definido
    # el frontend y por tener el jwt_required en la api.
    if valores_dicc_none(json) or valores_dicc_vacios(json):
        return False  # El mes y el monto deben estar presentes
    if not es_entero(json["month"]):
        return False  # El mes no es un número
    if not es_entero(json["amount"]):
        return False  # El monto no es un número
    if not es_mes(json["month"]):
        return False  # El mes no es un mes
    return True  # Datos válidos


def es_mes(mes):
    return int(mes) in range(1, 13)
