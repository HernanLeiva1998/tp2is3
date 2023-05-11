from src.web.controllers.validators.common_validators import (
    es_entero,
    valor_fuera_de_rango_float,
    validar_longitud,
    es_float_positivo,
    es_float,
    valores_dicc_none,
    valores_dicc_vacios,
)


def validar_inputs(dato):
    if valores_dicc_none(dato) or valores_dicc_vacios(dato):
        return False, "Todos los datos deben llenarse"
    if not es_entero(dato["elementos_pagina"]):
        return False, "Elementos por página debe ser un numero"
    if not es_float(dato["porcentaje_recargo"]):
        return False, "El porcentaje de recargo no es un flotante"
    if not es_float(dato["cuota_base"]):
        return False, "La cuota base no es un flotante"
    if not es_float_positivo(dato["porcentaje_recargo"]):
        return False, "El porcentaje de recargo no es positivo"
    if not es_float_positivo(dato["cuota_base"]):
        return False, "La cuota base no es positiva"
    if not validar_longitud(dato["informacion_contacto"]):
        return False, "La información de contacto es demasiado larga"
    if not validar_longitud(dato["encabezado_recibos"]):
        return False, "El encabezado de los recibos es demasiado largo"
    if valor_fuera_de_rango_float(dato["cuota_base"]):
        return False, "La cuota base es demasiado grande"
    return True, "Los datos son validos"
