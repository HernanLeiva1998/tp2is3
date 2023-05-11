from flask import render_template


def not_found_error(e):
    kwargs = {
        "error_name": "404 Not found Error",
        "error_description": "La URL a la que intenta acceder no existe",
        "redirect_to": "home",
        "destino": "homepage",
    }
    return render_template("error.html", **kwargs), 404


def not_authenticated_error(e):
    kwargs = {
        "error_name": "401 Unauthorized Error",
        "error_description": "Debe autenticarse para acceder a esta URL",
        "redirect_to": "auth.login",
        "destino": "login",
    }
    return render_template("error.html", **kwargs), 401


def not_authorized_error(e):
    kwargs = {
        "error_name": "403 Forbidden Error",
        "error_description": "No tiene los permisos para acceder a esta URL",
        "redirect_to": "home",
        "destino": "homepage",
    }
    return render_template("error.html", **kwargs), 403
