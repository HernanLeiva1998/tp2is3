llaves_ignoradas = ["activar_pagos"]


def valores_dicc_none(dato):
    for value in dato.values():
        if value is None:
            return True
    return False


def valores_dicc_vacios(dato):
    """La key activar_pagos puede estar vacía."""
    for key, value in dato.items():
        if value == "" and key not in llaves_ignoradas:
            return True
    return False


def es_entero(dato):
    return dato.lstrip("-").isdigit()


def es_float(dato):
    try:
        float(dato)
    except ValueError:
        return False
    return True


def es_float_positivo(dato):
    return float(dato) >= 0


def validar_longitud(dato, longitud = 500):
    return len(dato) <= longitud


def valor_fuera_de_rango_float(dato, valor_max = 1_000_000):
    return float(dato) > valor_max


def valor_fuera_de_rango_entero(dato, valor_max = 1_000_000):
    return int(dato) > valor_max


def valor_es_negativo_entero(costo):
    return int(costo) < 0
