import json

from flask import Blueprint, session, render_template, request, redirect, flash, abort

from src.core import socios
from src.core import pagos
from src.core import disciplinas
from src.core import usuarios
from src.web.exportaciones import socios_CSV
from src.web.exportaciones import socios_PDF
from src.web.helpers.permission import has_permission
from src.web.controllers.validators import validator_socio
from src.web.decorators.login import login_requerido
from src.web.controllers.validators.common_validators import is_integer


socio_blueprint = Blueprint("socios", __name__, url_prefix="/socios")


def json_informacion_socio(id):
    """Devuelve un json con la informacion del socio pasado por id"""
    return json.dumps(socios.informacion_socio(id))


def json_estado_socio(id):
    return json.dumps(socios.estado_socio(id))


def socios_por_año():
    """Retorna la cantidad de socios por año de los ultimos 7 años"""
    return json.dumps(socios.socios_por_años())


def disciplinas_socio(id):
    """Devuelve un json con todas las disciplinas que realiza el socio con id pasado por parametro"""
    return json.dumps(socios.disciplinas_socio_diccionario(id))


def socios_genero():
    """Retorna un json con los socios por genero"""
    return json.dumps(socios.socios_por_sexo())


@socio_blueprint.route("/")
@login_requerido
def socio_index():
    """Esta funcion llama al modulo correspondiente para obtener todos los socios paginados."""
    if not (has_permission(session["user"], "socio_index")):
        return abort(403)
    page = request.args.get("page", 1, type=int)
    apellido = (
        request.args.get("busqueda", type=str)
        if request.args.get("busqueda", type=str) != ""
        else None
    )
    tipo = (
        request.args.get("tipo", type=str)
        if request.args.get("tipo", type=str) != ""
        else None
    )
    kwargs = {
        "socios": socios.listar_socios(page, apellido, tipo),
        "apellido": apellido,
        "tipo": tipo,
        "usuario": usuarios.buscar_usuario_email(session["user"]),
    }
    return render_template("socios/index.html", **kwargs)


@socio_blueprint.route("/alta-socio")
@login_requerido
def form_socio():
    """Esta funcion devuelve el template con un formulario para dar de alta un usuario"""
    if not (has_permission(session["user"], "socio_new")):
        return abort(403)
    kwargs = {"usuario": usuarios.buscar_usuario_email(session["user"])}
    return render_template("socios/alta_socios.html", **kwargs)


@socio_blueprint.route("/<id>")
@login_requerido
def socio_profile(id):
    """Esta funcion llama al modulo correspondiente para obtener a un socio por su id."""
    if (not is_integer(id)) or (socios.buscar_socio(id) is None):
        return abort(404)
    kwargs = {
        "socio": socios.buscar_socio(id),
        "usuario": usuarios.buscar_usuario_email(session["user"]),
    }
    return render_template("socios/perfil_socio.html", **kwargs)


@socio_blueprint.post("/alta")
@login_requerido
def socio_add():
    """Esta funcion llama al metodo correspondiente para dar de alta un socio."""
    data_socio = {
        "nombre": request.form.get("nombre"),
        "apellido": request.form.get("apellido"),
        "email": request.form.get("email"),
        "password": request.form.get("password"),
        "tipo_documento": request.form.get("tipo_documento"),
        "dni": request.form.get("documento"),
        "genero": request.form.get("genero"),
        "direccion": request.form.get("direccion"),
        "telefono": request.form.get("telefono"),
    }
    validacion_inputs, mensaje = validator_socio.validar_inputs(data_socio)
    if not validacion_inputs:
        flash(mensaje)
        return redirect("/socios/alta-socio")
    validacion, mensaje = socios.validar_datos_existentes(
        data_socio["dni"], data_socio["email"], "alta"
    )
    if not validacion:
        flash(mensaje)
        return redirect("/socios/alta-socio")
    data_socio["activo"] = True
    data_socio["nombre"] = data_socio["nombre"].capitalize()
    data_socio["apellido"] = data_socio["apellido"].capitalize()

    socio = socios.agregar_socio(data_socio)
    pagos.generar_pagos(socio.id)
    return redirect("/socios")


@socio_blueprint.post("/modificacion")
@login_requerido
def socio_update():
    """Esta funcion llama al metodo correspondiente para modificar los datos de un socio."""
    if not (has_permission(session["user"], "socio_update")):
        return abort(403)
    socio = socios.buscar_socio(request.form.get("id"))
    password = socio.password
    data_socio = {
        "id": request.form.get("id"),
        "nombre": request.form.get("nombre"),
        "apellido": request.form.get("apellido"),
        "email": request.form.get("email"),
        "password": password,
        "tipo_documento": request.form.get("tipo_documento"),
        "dni": request.form.get("documento"),
        "genero": request.form.get("genero"),
        "direccion": request.form.get("direccion"),
        "telefono": request.form.get("telefono"),
    }
    validacion_inputs, mensaje = validator_socio.validar_inputs(data_socio)
    if not validacion_inputs:
        flash(mensaje)
        return redirect("/socios/" + data_socio["id"])
    validacion_datos_existentes, mensaje = socios.validar_datos_existentes(
        data_socio["dni"], data_socio["email"], "modificacion", data_socio["id"]
    )
    if not validacion_datos_existentes:
        flash(mensaje)
        return redirect("/socios/" + data_socio["id"])
    data_socio["activo"] = True
    data_socio["nombre"] = data_socio["nombre"].capitalize()
    data_socio["apellido"] = data_socio["apellido"].capitalize()

    socios.modificar_socio(data_socio)
    return redirect("/socios")


@socio_blueprint.route("/eliminar/<id>", methods=["DELETE", "GET"])
@login_requerido
def socio_delete(id):
    """Esta funcion llama al metodo correspondiente para eliminar un socio."""
    if not (has_permission(session["user"], "socio_destroy")):
        return abort(403)
    if (not is_integer(id)) or (socios.buscar_socio(id) is None):
        return abort(404)
    socios.eliminar_socio(id)
    return redirect("/socios")


@socio_blueprint.route("/exportar-csv")
@login_requerido
def exportar_csv():
    """Esta funcion genera un archivo CSV a partir de los datos solicitados de socios"""
    apellido = (
        request.args.get("busqueda", type=str)
        if request.args.get("busqueda", type=str) != ""
        else None
    )
    tipo = (
        request.args.get("tipo", type=str)
        if request.args.get("tipo", type=str) != ""
        else None
    )
    data_socios = socios.todos_los_socios(apellido, tipo)
    output = socios_CSV.generar_CSV(data_socios)
    return output


@socio_blueprint.route("/exportar-pdf")
@login_requerido
def exportar_pdf():
    """Esta funcion genera un archivo PDF a partir de los datos solicitados de socios"""
    apellido = (
        request.args.get("busqueda", type=str)
        if request.args.get("busqueda", type=str) != ""
        else None
    )
    tipo = (
        request.args.get("tipo", type=str)
        if request.args.get("tipo", type=str) != ""
        else None
    )
    data_socios = socios.todos_los_socios(apellido, tipo)
    output = socios_PDF.generar_PDF(data_socios)
    return output


@socio_blueprint.route("/inscripcion-socio/<id>")
@login_requerido
def inscripcion_socio(id):
    """Esta funcion retorna el formulario para la inscripcion del socio a una disciplina"""
    if not (has_permission(session["user"], "socio_new")):
        return abort(403)
    if (not is_integer(id)) or (socios.buscar_socio(id) is None):
        return abort(404)
    kwargs = {
        "id_socio": id,
        "disciplinas": disciplinas.nombres_todas_las_disciplinas(),
        "categorias": disciplinas.categorias_de_cada_disciplina(),
        "usuario": usuarios.buscar_usuario_email(session["user"]),
    }
    return render_template("/socios/inscripcion_socios.html", **kwargs)


@socio_blueprint.post("/inscripcion")
@login_requerido
def add_inscripcion():
    """Esta funcion realiza la inscripcion de un socio a una disciplina"""
    id_socio = request.form.get("id_socio")
    id_disciplina = request.form.get("categoria")
    validacion_inputs, message = validator_socio.validar_inscripcion(
        id_socio, id_disciplina
    )
    if validacion_inputs:
        if socios.esta_habilitado(id_socio) and disciplinas.esta_habilitada(
            id_disciplina
        ):
            disciplinas.relacionar_socio_disciplina(id_disciplina, id_socio)
            flash("Socio inscripto correctamente.")
            return redirect("/socios/")
        else:
            flash("La disciplina o el socio no están habilitados.")
            return redirect("/socios/inscripcion-socio/" + id_socio)
    else:
        flash(message)
        return redirect("/socios/inscripcion-socio/" + id_socio)
