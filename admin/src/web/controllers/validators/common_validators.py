ignored_keys = ["activar_pagos"]


def dict_values_are_none(data):
    for value in data.values():
        if value is None:
            return True
    return False


def dict_values_are_empty(data):
    """La key activar_pagos puede estar vacía."""
    for key, value in data.items():
        if value == "" and key not in ignored_keys:
            return True
    return False


def is_integer(dato):
    return dato.lstrip("-").isdigit()


def is_float(dato):
    try:
        float(dato)
    except ValueError:
        return False
    return True


def is_positive_float(dato):
    return float(dato) >= 0


def validar_longitud(dato, lenght=500):
    return len(dato) <= lenght


def valor_fuera_de_rango_float(dato, max_value=1_000_000):
    return float(dato) > max_value


def valor_fuera_de_rango_entero(dato, max_value=1_000_000):
    return int(dato) > max_value


def valor_es_negativo_entero(costo):
    return int(costo) < 0
