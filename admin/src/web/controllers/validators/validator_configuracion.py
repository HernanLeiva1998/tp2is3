from src.web.controllers.validators.common_validators import (
    is_integer,
    valor_fuera_de_rango_float,
    validar_longitud,
    is_positive_float,
    is_float,
    dict_values_are_empty,
    dict_values_are_none,
)


def validar_inputs(data):
    if dict_values_are_none(data) or dict_values_are_empty(data):
        return False, "Todos los datos deben llenarse"
    if not is_integer(data["elementos_pagina"]):
        return False, "Elementos por página debe ser un numero"
    if not is_float(data["porcentaje_recargo"]):
        return False, "El porcentaje de recargo no es un flotante"
    if not is_float(data["cuota_base"]):
        return False, "La cuota base no es un flotante"
    if not is_positive_float(data["porcentaje_recargo"]):
        return False, "El porcentaje de recargo no es positivo"
    if not is_positive_float(data["cuota_base"]):
        return False, "La cuota base no es positiva"
    if not validar_longitud(data["informacion_contacto"]):
        return False, "La información de contacto es demasiado larga"
    if not validar_longitud(data["encabezado_recibos"]):
        return False, "El encabezado de los recibos es demasiado largo"
    if valor_fuera_de_rango_float(data["cuota_base"]):
        return False, "La cuota base es demasiado grande"
    return True, "Los datos son validos"
