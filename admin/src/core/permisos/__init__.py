from src.core.permisos.permisos import Permiso


def listar_permisos():
    """Esta funcion lista los permisos disponibles"""
    return Permiso.query.all()

def buscar_permiso(permiso):
    """buscar un objeto permiso, segun el nombre que llego por parametro"""
    return Permiso.query.filter_by(nombre = permiso).first()