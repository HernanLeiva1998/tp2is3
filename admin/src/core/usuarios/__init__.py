from werkzeug.security import check_password_hash, generate_password_hash

from src.core import configuracion_sistema
from src.core import roles
from src.core.usuarios.usuarios import Usuario
from src.core.db import db


def agregar_usuario(data):
    """Esta funcion se utiliza para dar de alta un usuario"""
    usuario = Usuario(**data)
    usuario.password = generate_password_hash(usuario.password, method="sha256")
    db.session.add(usuario)
    db.session.commit()
    return usuario


def buscar_usuario(id):
    """Esta funcion busca un usuario por su id"""
    if int(id) > 2147483647:
        return None
    return Usuario.query.get(id)


def buscar_usuario_email(email):
    """Esta funcion retorna a un usuario buscado por su email"""
    with db.session.no_autoflush:
        usuario = Usuario.query.filter_by(email=email).first()
    return usuario


def modificar_usuario(data):
    """Esta funcion realiza la modificacion de los datos de un usuario"""
    usuario = Usuario.query.get(data["id"])
    usuario.nombre = data["nombre"]
    usuario.apellido = data["apellido"]
    usuario.email = data["email"]
    usuario.activo = data["activo"]
    usuario.username = data["username"]
    db.session.commit()
    return usuario


def eliminar_usuario(id):
    """Esta funcion realiza la eliminacion de un usuario de la BD"""
    usuario = Usuario.query.get(id)
    db.session.delete(usuario)
    db.session.commit()


def listar_usuarios(page, email=None, tipo=None):
    """Esta funcion devuelve todos los usuarios de forma paginada segun la configuracion, y segun si se esta realizando una busqueda."""
    if (email is not None) and (tipo is not None):
        if tipo == "true":
            usuarios = (
                Usuario.query.filter(Usuario.email.contains(email))
                .filter(Usuario.activo.is_(True))
                .paginate(
                    page, per_page=configuracion_sistema.get_paginado().elementos_pagina
                )
            )
        else:
            usuarios = (
                Usuario.query.filter(Usuario.email.contains(email))
                .filter(Usuario.activo.is_(False))
                .paginate(
                    page, per_page=configuracion_sistema.get_paginado().elementos_pagina
                )
            )
    elif email is not None:
        usuarios = Usuario.query.filter(Usuario.email.contains(email)).paginate(
            page, per_page=configuracion_sistema.get_paginado().elementos_pagina
        )
    elif tipo is not None:
        if tipo == "true":
            usuarios = Usuario.query.filter(Usuario.activo.is_(True)).paginate(
                page, per_page=configuracion_sistema.get_paginado().elementos_pagina
            )
        else:
            usuarios = Usuario.query.filter(Usuario.activo.is_(False)).paginate(
                page, per_page=configuracion_sistema.get_paginado().elementos_pagina
            )
    else:
        usuarios = Usuario.query.paginate(
            page, per_page=configuracion_sistema.get_paginado().elementos_pagina
        )
    return usuarios


def find_user_by_mail_and_pass(email, password):
    """esta funcion verifica que el usuario ingresado en login exista"""
    usuario = Usuario.query.filter(Usuario.email == email).first()
    if usuario is None:
        return None
    elif check_password_hash(usuario.password, password):
        return usuario


def validar_estado(estado):
    """Esta funcion valida el dato enviado al modificar el estado de un usuario"""
    return estado == "activo"


def validar_datos_existentes(email, username, accion, id=None):
    """Esta funcion valida que el dni o el email ingresados para dar de alta o modificar un usuario no existan."""
    if accion == "alta":
        email_existente = Usuario.query.filter_by(email=email).first()
        username_existente = Usuario.query.filter_by(username=username).first()
        if email_existente is not None:
            return False, "El Email ya esta cargado en el sistema."
        elif username_existente is not None:
            return False, "El Nombre de Usuario ya esta cargado en el sistema"
        else:
            return True, "Ambos son validos"
    elif accion == "modificacion":
        email_existente = (
            Usuario.query.filter_by(email=email).filter(Usuario.id != id).first()
        )
        username_existente = (
            Usuario.query.filter_by(username=username).filter(Usuario.id != id).first()
        )
        if email_existente is not None:
            return False, "El Email ya esta cargado en el sistema."
        elif username_existente is not None:
            return False, "El Nombre de Usuario ya esta cargado en el sistema."
        else:
            return True, "Ambos son validos"


def agregar_roles(usuario, roles_usuario):
    for nombre_rol, valor in roles_usuario.items():
        if valor == "on":
            rol = roles.buscar_rol(nombre_rol)
            usuario.roles.append(rol)
    db.session.commit()


def verificar_rol_usuario(id):
    usuario = buscar_usuario(id)
    rol_admin = roles.buscar_rol("ROL_ADMINISTRADOR")
    return rol_admin in usuario.roles
