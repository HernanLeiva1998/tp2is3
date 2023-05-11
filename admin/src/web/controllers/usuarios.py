from flask import Blueprint, render_template, request, flash, redirect, session, abort

from src.core import usuarios
from src.web.helpers.permission import has_permission
from src.web.controllers.validators import validator_usuario
from src.web.controllers.validators.common_validators import es_entero
from src.web.decorators.login import login_requerido


usuario_blueprint = Blueprint("usuarios", __name__, url_prefix = "/usuarios")


@usuario_blueprint.route("/")
@login_requerido
def usuario_index():
    """Esta funcion llama al modulo correspondiente
    para obtener todos los usuarios paginados."""
    if not (has_permission(session["user"], "usuario_index")):
        return abort(403)
    pagina = request.args.get("page", 1, type = int)
    email = (
        request.args.get("busqueda", type = str)
        if request.args.get("busqueda", type = str) != ""
        else None
    )
    tipo = (
        request.args.get("tipo", type = str)
        if request.args.get("tipo", type = str) != ""
        else None
    )
    kwargs = {
        "usuarios": usuarios.listar_usuarios(pagina, email, tipo),
        "email": email,
        "tipo": tipo,
        "usuario": usuarios.buscar_usuario_email(session["user"]),
    }
    return render_template("usuarios/index.html", **kwargs)


@usuario_blueprint.route("/alta-usuario")
@login_requerido
def usuario_formulario():
    """Esta funcion devuelve el template con
    un formulario para dar de alta un usuario"""
    if not (has_permission(session["user"], "usuario_new")):
        return abort(403)
    kwargs = {"usuario": usuarios.buscar_usuario_email(session["user"])}
    return render_template("usuarios/alta_usuarios.html", **kwargs)


@usuario_blueprint.route("/<id>")
@login_requerido
def usuario_perfil(id):
    """Esta funcion llama al modulo correspondiente
    para obtener a un usuario por su id."""
    if (not es_entero(id)) or (usuarios.buscar_usuario(id) is None):
        return abort(404)
    kwargs = {
        "usuario": usuarios.buscar_usuario(id),
        "rol": usuarios.verificar_rol_usuario(id),
    }
    return render_template("usuarios/perfil_usuario.html", **kwargs)


@usuario_blueprint.post("/alta")
@login_requerido
def usuario_agregar():
    """Esta funcion llama al metodo 
    correspondiente para dar de alta un usuario."""
    datos_usuario = {
        "nombre": request.form.get("nombre"),
        "apellido": request.form.get("apellido"),
        "email": request.form.get("email"),
        "username": request.form.get("username"),
        "password": request.form.get("password"),
    }
    datos_rol_usuario = {
        "ROL_ADMINISTRADOR": request.form.get("rol_administrador"),
        "ROL_OPERADOR": request.form.get("rol_operador"),
    }
    validacion_inputs, mensaje = validator_usuario.validar_inputs_agregar(
        datos_usuario, datos_rol_usuario
    )
    if not validacion_inputs:
        flash(mensaje)
        return redirect("/usuarios/alta-usuario")

    datos_usuario["activo"] = True
    datos_usuario["nombre"] = datos_usuario["nombre"].capitalize()
    datos_usuario["apellido"] = datos_usuario["apellido"].capitalize()

    validacion, mensaje = usuarios.validar_datos_existentes(
        datos_usuario["email"], datos_usuario["username"], "alta"
    )
    if not validacion:
        flash(mensaje)
        return redirect("/usuarios/alta-usuario")
    usuario = usuarios.agregar_usuario(datos_usuario)
    usuarios.agregar_roles(usuario, datos_rol_usuario)
    return redirect("/usuarios")


@usuario_blueprint.post("/modificacion")
@login_requerido
def usuario_actualizar():
    """Esta funcion llama al metodo correspondiente
    para modificar los datos de un usuario."""
    if not (has_permission(session["user"], "usuario_update")):
        return abort(403)
    if usuarios.verificar_rol_usuario(request.form.get("id")):
        estado = True
    else:
        estado = usuarios.validar_estado(request.form.get("activo"))
    datos_usuario = {
        "id": request.form.get("id"),
        "nombre": request.form.get("nombre"),
        "apellido": request.form.get("apellido"),
        "email": request.form.get("email"),
        "username": request.form.get("username"),
    }
    validacion_inputs, mensaje = validator_usuario.validar_inputs(datos_usuario)
    if not validacion_inputs:
        flash(mensaje)
        return redirect("/usuarios/" + datos_usuario["id"])

    datos_usuario["activo"] = estado
    datos_usuario["nombre"] = datos_usuario["nombre"].capitalize()
    datos_usuario["apellido"] = datos_usuario["apellido"].capitalize()

    validacion, mensaje = usuarios.validar_datos_existentes(
        datos_usuario["email"],
        datos_usuario["username"],
        "modificacion",
        datos_usuario["id"],
    )
    if not validacion:
        flash(mensaje)
        return redirect("/usuarios/" + datos_usuario["id"])
    usuarios.modificar_usuario(datos_usuario)
    return redirect("/usuarios")


@usuario_blueprint.route("/eliminar/<id>", methods=["POST", "GET"])
@login_requerido
def usuario_eliminar(id):
    """Esta funcion llama al metodo 
    correspondiente para eliminar un usuario."""
    if not (has_permission(session["user"], "usuario_destroy")):
        return abort(403)
    if (not es_entero(id)) or (usuarios.buscar_usuario(id) is None):
        return abort(404)
    usuarios.eliminar_usuario(id)
    return redirect("/usuarios")
