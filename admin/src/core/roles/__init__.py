from src.core.roles.roles import Rol


def listar_roles():
    """Esta funcion lista los roles disponibles"""
    return Rol.query.all()


def buscar_rol(rol):
    return Rol.query.filter_by(nombre=rol).first()
