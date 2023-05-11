import re

from src.web.controllers.validators.common_validators import (
    is_integer,
    valor_fuera_de_rango_entero,
    valor_es_negativo_entero,
    dict_values_are_empty,
    dict_values_are_none,
)


def validar_inputs(data):
    """Chequea que los datos del formulario sean válidos"""

    if dict_values_are_none(data) or dict_values_are_empty(data):
        return False, "Todos los datos deben llenarse"
    if not is_integer(data["costo"]):
        return False, "El costo debe ser un numero"
    if valor_es_negativo_entero(data["costo"]):
        return False, "El costo no puede ser negativo"
    if valor_fuera_de_rango_entero(data["costo"]):
        return False, "El costo no puede superar un millon(1000000)"
    if not nombre_es_valido(data["nombre"]):
        return False, "El nombre de la disciplina no puede tener numeros"
    if not horario_es_valido(data["horarios"]):
        return (
            False,
            'El formato de los horarios es incorrecto, debe ser "Dia1 Dia2 (opcional) de X a Yhs"',
        )
    return True, "Los datos son validos"


def nombre_es_valido(nombre):
    return re.fullmatch(r"[A-Za-z ]{1,50}", nombre)


def horario_es_valido(horarios):
    return "de" in horarios
