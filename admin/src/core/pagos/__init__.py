from datetime import datetime, date
from src.core.socios import check_fecha_cuota_es_presente_o_pasada

from src.core import socios
from src.core import configuracion_sistema
from src.core.pagos.pagos import Pago
from src.core.db import db
from src.web.controllers.validators.validator_configuracion import (
    valor_fuera_de_rango_float,
)


def listar_pagos_diccionario(id):
    """devuelve una lista de diccionarios con los pagos ya pagados de un socio
    month: numero de cuota
    amount: costo de la cuota
    year: año de la cuota
    date:fecha en la que se pago."""
    socio = socios.buscar_socio(id)
    todos_los_pagos = socio.pagos
    pagos_pagados = []
    for pago in todos_los_pagos:
        if pago.estado:
            diccionario = {
                "month": pago.nro_cuota,
                "amount": pago.total,
                "year": pago.año_cuota,
                "date": pago.fecha_pago.strftime("%d/%m/%Y"),
            }
            pagos_pagados.append(diccionario)
    return pagos_pagados


def listar_pagos_adeudados_diccionario(id):
    """devuelve un diccionario con los pagos adeudados de un socio
    month: numero de cuota
    amount: costo de la cuota
    year: año de la cuota"""
    socio = socios.buscar_socio(id)
    todos_los_pagos = socio.pagos
    pagos_adeudados = []
    for pago in todos_los_pagos:
        if not pago.estado and check_fecha_cuota_es_presente_o_pasada(pago):
            diccionario = {
                "month": pago.nro_cuota,
                "amount": calcular_cuota(pago.id, socio.id),
                "year": pago.año_cuota,
            }
            pagos_adeudados.append(diccionario)
    return pagos_adeudados


def pagar_con_api(diccionario, id):
    """recibe un diccionario con los datos de un pago.
    Devuelve un booleano y un mensaje dependiendo de como concluye la operación

    Datos que contiene le diccionario:
    month: numero de cuota
    amount: costo de la cuota
    year: año de la cuota"""
    socio = socios.buscar_socio(id)
    for pago in socio.pagos:
        if (
            pago.nro_cuota == int(diccionario["month"])
            and pago.año_cuota == datetime.now().year
            and not pago.estado
            and (int(diccionario["amount"])) == calcular_cuota(pago.id, pago.socio.id)
        ):
            pago.total = diccionario["amount"]
            pago.fecha_pago = datetime.now()
            pago.estado = True
            db.session.commit()
            return True
    return False


def get_cuota(id):
    """Busca una cuota por id"""
    if int(id) > 2147483647:
        return None
    return Pago.query.get(id)


def generar_pagos(id_socio):
    """Esta funcion genera los cuotas a pagar por el socio cuando se lo da de alta."""
    año_actual = str(datetime.now().year)
    fecha_ingreso = datetime.now().date()
    fecha_diciembre = datetime.strptime("30/12/" + año_actual, "%d/%m/%Y").date()
    cuotas = int(
        (fecha_diciembre.year - fecha_ingreso.year) * 12
        + (fecha_diciembre.month - fecha_ingreso.month)
    )
    desde = 12 - cuotas
    for i in range(desde, 13):
        data_pago = {
            "total": 0,
            "socio_id": id_socio,
            "nro_cuota": i,
            "estado": False,
        }
        pago = Pago(**data_pago)
        db.session.add(pago)
        db.session.commit()
    hasta = 12 - (12 - desde)
    for j in range(1, hasta):
        data_pago = {
            "total": 0,
            "socio_id": id_socio,
            "nro_cuota": j,
            "estado": False,
            "año_cuota": str((int(año_actual) + 1)),
        }
        pago = Pago(**data_pago)
        db.session.add(pago)
        db.session.commit()


def listar_pagos_socio(id, page):
    """Esta funcion realiza la consulta para obtener los pagos del socio recibido"""
    pagos = (
        Pago.query.filter_by(socio_id=id)
        .order_by(Pago.estado, Pago.año_cuota, Pago.nro_cuota)
        .paginate(page, per_page=configuracion_sistema.get_paginado().elementos_pagina)
    )

    for pago in pagos.items:
        if not pago.estado or pago.total == 0:
            pago.total = calcular_cuota(pago.id, id)
    return pagos


def pagar_cuota(id_pago, id_socio):
    """Cambia el estado de una cuota la cual pasa de impaga a paga"""
    cuota = get_cuota(id_pago)
    if cuota.total == 0:
        cuota.total = calcular_cuota(id_pago, id_socio)
    validar = valor_fuera_de_rango_float(cuota.total)
    if validar:
        return False
    cuota.fecha_pago = datetime.now()
    cuota.estado = True
    db.session.commit()
    return True


def calcular_cuota(id_pago, id_socio):
    """
    Calcula el valor de una cuota teniendo en cuenta cuota base,
    costo de cada disciplina del socio y si la cuota esta vencida
    """
    cuota = configuracion_sistema.get_configuracion_general().cuota_base
    recargo = configuracion_sistema.get_configuracion_general().porcentaje_recargo
    socio = socios.buscar_socio(id_socio)

    for disciplina in socio.disciplinas:
        cuota = cuota + int(disciplina.costo)
    if cuota_esta_vencida(id_pago):
        cuota = cuota + ((cuota * recargo) / 100)
    return round(cuota)


def cuota_esta_vencida(id_pago):
    """Devuelve verdadero si el pago esta vencido y falso en caso contrario"""
    cuota = get_cuota(id_pago)
    vencimiento = date(int(cuota.año_cuota), int(cuota.nro_cuota), 10)
    return vencimiento < datetime.now().date()
