import re

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
    """Chequea que los datos del formulario sean válidos"""

    if valores_dicc_none(dato) or valores_dicc_vacios(dato):
        return False, "Todos los datos deben llenarse"
    if not es_entero(dato["costo"]):
        return False, "El costo debe ser un numero"
    if valor_es_negativo_entero(dato["costo"]):
        return False, "El costo no puede ser negativo"
    if valor_fuera_de_rango_entero(dato["costo"]):
        return False, "El costo no puede superar un millon(1000000)"
    if not nombre_es_valido(dato["nombre"]):
        return False, "El nombre de la disciplina no puede tener numeros"
    if not horario_es_valido(dato["horarios"]):
        return (
            False,
            'El formato de los horarios es incorrecto, debe ser "Dia1 Dia2 (opcional) de X a Yhs"',
        )
    return True, "Los datos son validos"


def nombre_es_valido(nombre):
    return re.fullmatch(r"[A-Za-z ]{1,50}", nombre)


def horario_es_valido(horarios):
    return "de" in horarios
