from functools import wraps

from flask import session, abort


def login_requerido(f):
    """Esta decorador es utilizado para verificar
    si hay una sesion existente del usuario"""

    @wraps(f)
    def decorated_function(*args, **kwargs):
        if "user" not in session:
            abort(401)
        return f(*args, **kwargs)

    return decorated_function
