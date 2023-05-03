import json

from flask import Blueprint, render_template, request, redirect, flash, session, abort

from src.core import disciplinas
from src.core import usuarios
from src.web.controllers.validators import validator_disciplinas
from src.web.controllers.validators.common_validators import is_integer
from src.web.helpers.permission import has_permission
from src.web.decorators.login import login_requerido


disciplina_blueprint = Blueprint("disciplinas", __name__, url_prefix="/disciplinas")


def disciplina_json():
    """Retorna el json con todas las disciplinas"""
    return json.dumps(disciplinas.listar_disciplinas_diccionario())


def disciplinas_socios():
    """Retorna un json con la cantidad de socios por disciplina"""
    return json.dumps(disciplinas.socios_habilitados_por_disciplina())


@disciplina_blueprint.route("/")
@login_requerido
def disciplina_index():
    """Muestra las disciplinas de la página indicada en el request. Si no hay request, la página será la primera"""
    if not (has_permission(session["user"], "disciplina_index")):
        return abort(403)
    page = request.args.get("page", 1, type=int)
    kwargs = {
        "disciplinas": disciplinas.listar_disciplinas(page),
        "usuario": usuarios.buscar_usuario_email(session["user"]),
    }
    return render_template("disciplinas/index.html", **kwargs)


@disciplina_blueprint.route("/alta-disciplina")
@login_requerido
def form_disciplina():
    """Devuelve el template con el formulario para agregar una disciplina"""
    if not (has_permission(session["user"], "disciplina_new")):
        return abort(403)
    kwargs = {"usuario": usuarios.buscar_usuario_email(session["user"])}
    return render_template("disciplinas/alta_disciplinas.html", **kwargs)


@disciplina_blueprint.route("/<id>")
@login_requerido
def disciplina_profile(id):
    """Busca una disciplina por el id indicado en la URL y devuelve el template con el formulario para modificar una disciplina"""
    if (not is_integer(id)) or (disciplinas.buscar_disciplina(id) is None):
        return abort(404)
    kwargs = {
        "disciplina": disciplinas.buscar_disciplina(id),
        "usuario": usuarios.buscar_usuario_email(session["user"]),
    }
    return render_template("disciplinas/perfil_disciplinas.html", **kwargs)


@disciplina_blueprint.post("/alta")
@login_requerido
def disciplina_add():
    """Llama al validador de inputs para validar los inputs del formulario para agregar una disciplina. Si los inputs son validos, valida que la disciplina no exista ya. Si no existe, se la agrega."""
    if not (has_permission(session["user"], "disciplina_new")):
        return abort(403)
    data_disciplina = {
        "nombre": request.form.get("nombre"),
        "categoria": request.form.get("categoria"),
        "instructores": request.form.get("instructores"),
        "horarios": request.form.get("horarios"),
        "costo": request.form.get("costo"),
        "habilitada": request.form.get("habilitada"),
    }
    inputs_validos, mensaje = validator_disciplinas.validar_inputs(data_disciplina)
    if not inputs_validos:
        flash(mensaje)
        return redirect("/disciplinas/alta-disciplina")

    data_disciplina["nombre"] = data_disciplina["nombre"].capitalize()
    data_disciplina["categoria"] = data_disciplina["categoria"].capitalize()
    data_disciplina["habilitada"] = data_disciplina["habilitada"] == "Si"

    existe, mensaje = disciplinas.validar_disciplina_repetida_alta(
        data_disciplina["nombre"], data_disciplina["categoria"]
    )
    if existe:
        flash(mensaje)
        return redirect("/disciplinas/alta-disciplina")
    disciplinas.agregar_disciplina(data_disciplina)
    return redirect("/disciplinas")


@disciplina_blueprint.post("/modificacion")
@login_requerido
def disciplina_update():
    """Llama al validador de inputs para validar los inputs del formulario para modificar una disciplina. Si los inputs son validos, valida que la disciplina no exista ya. Si no existe, se la modifica."""
    if not (has_permission(session["user"], "disciplina_update")):
        return abort(403)
    data_disciplina = {
        "id": request.form.get("id"),
        "nombre": request.form.get("nombre"),
        "categoria": request.form.get("categoria"),
        "instructores": request.form.get("instructores"),
        "horarios": request.form.get("horarios"),
        "costo": request.form.get("costo"),
        "habilitada": request.form.get("habilitada"),
    }
    inputs_validos, mensaje = validator_disciplinas.validar_inputs(data_disciplina)
    if not inputs_validos:
        flash(mensaje)
        return redirect("/disciplinas/" + data_disciplina["id"])
    data_disciplina["nombre"] = data_disciplina["nombre"].capitalize()
    data_disciplina["categoria"] = data_disciplina["categoria"].capitalize()
    data_disciplina["habilitada"] = data_disciplina["habilitada"] == "Si"

    existe, mensaje = disciplinas.validar_disciplina_repetida_modificacion(
        data_disciplina["nombre"],
        data_disciplina["categoria"],
        data_disciplina["id"],
    )
    if existe:
        flash(mensaje)
        return redirect("/disciplinas/" + data_disciplina["id"])
    disciplinas.modificar_disciplina(data_disciplina)
    return redirect("/disciplinas")


@disciplina_blueprint.route("/eliminar/<id>", methods=["DELETE", "GET"])
@login_requerido
def disciplina_delete(id):
    """Le dice al modelo que borre la disciplina enviada"""
    if not (has_permission(session["user"], "disciplina_destroy")):
        return abort(403)
    if (not is_integer(id)) or (disciplinas.buscar_disciplina(id) is None):
        return abort(404)
    disciplinas.eliminar_disciplina(id)
    return redirect("/disciplinas")
