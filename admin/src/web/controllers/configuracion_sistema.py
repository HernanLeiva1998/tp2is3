import json

from flask import Blueprint, render_template, request, redirect, flash, session, abort

from src.web.helpers.permission import has_permission
from src.core import configuracion_sistema
from src.web.controllers.validators import validator_configuracion
from src.web.decorators.login import login_requerido


configuracion_sistema_blueprint = Blueprint(
    "configuracion_sistema", __name__, url_prefix="/configuracion_del_sistema"
)


def info_contacto_json():
    """Retorna el json con todas las disciplinas"""
    return json.dumps(configuracion_sistema.get_info_contacto_diccionario())


@configuracion_sistema_blueprint.get("/")
@login_requerido
def configuracion_index():
    """
    muestra el modulo de configuracion del sistema con los valores actuales
    almacenados en la base de datos. Si no existe la tupla en la base de datos
    se crea automaticamente con una configuracion predeterminada
    """
    if not (has_permission(session["user"], "config_index")):
        return abort(403)
    paginado = {"paginado": configuracion_sistema.get_paginado()}
    config = {"config": configuracion_sistema.get_configuracion_general()}
    if config["config"] is None or paginado["paginado"] is None:
        configuracion_sistema.configuracion_predeterminada()
        paginado = {"paginado": configuracion_sistema.get_paginado()}
        config = {"config": configuracion_sistema.get_configuracion_general()}

    if config["config"].activar_pagos:
        config["config"].activar_pagos = "checked"
    else:
        config["config"].activar_pagos = ""
    kwargs = {**paginado, **config}

    return render_template("configuracion_sistema/configuracion_sistema.html", **kwargs)


@configuracion_sistema_blueprint.post("/update")
@login_requerido
def configuracion_actualizar():
    """
    Recibe la informacion del formularlio de configuracion_sistema.html.
    Luego se validan los datos recibidos y si son correctos se actualiza
    la tupla de configuracion general y la tupla de configuracion
    paginado
    """
    if not (has_permission(session["user"], "config_update")):
        return abort(403)
    configuracion = {
        "elementos_pagina": request.form.get("elementos_pagina"),
        "activar_pagos": request.form.get("activar_pagos"),
        "encabezado_recibos": request.form.get("encabezado_recibos"),
        "informacion_contacto": request.form.get("informacion_contacto"),
        "cuota_base": request.form.get("cuota_base"),
        "porcentaje_recargo": request.form.get("porcentaje_recargo"),
    }
    inputs_validos, mensaje = validator_configuracion.validar_inputs(configuracion)
    if not inputs_validos:
        flash(mensaje)
        return redirect("/configuracion_del_sistema/")
    configuracion["activar_pagos"] = configuracion["activar_pagos"] == "pagos activados"
    paginado = {"elementos_pagina": configuracion["elementos_pagina"]}
    configuracion_sistema.modificar_configuracion(configuracion, paginado)
    return redirect("/configuracion_del_sistema/")
