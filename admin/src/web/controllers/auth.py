from flask import Blueprint, render_template, request
from flask import flash, url_for, session, redirect
from src.core import usuarios
from src.web.controllers.validators import validator_usuario


auth_blueprint = Blueprint("auth", __name__, url_prefix="/auth")


@auth_blueprint.get("/")
def login():
    """Esta funcion retorna el template para logearse"""
    return render_template("auth/login.html")


@auth_blueprint.post("/authenticate")
def authenticate():
    """Esta funcion realiza la autenticacion de un usuario"""
    datos = {"email": request.form.get("email"),
              "password": request.form.get("password")}
    validacion, mensaje = validator_usuario.validar_inputs(datos)
    if not validacion:
        flash(mensaje, "error")
        return redirect(url_for("auth.login"))
    usuario = usuarios.buscar_usuario_email(datos["email"], datos["password"])
    if usuario is None:
        flash("Credenciales invalidas", "error")
        return redirect(url_for("auth.login"))
    elif not usuario.activo:
        flash("Usted no tiene permitido acceder al sistema", "error")
        return redirect(url_for("auth.login"))
    session["user"] = usuario.email
    session["nombre"] = usuario.nombre
    session["apellido"] = usuario.apellido
    flash("Sesión iniciada correctamente")
    return redirect(url_for("home"))


@auth_blueprint.get("/logout")
def logout():
    """Esta funcion realiza el logout de un usuario"""
    session.pop("user", None)
    flash("Sesión cerrada correctamente")
    return redirect(url_for("auth.login"))
