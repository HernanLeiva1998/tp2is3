from werkzeug.security import check_password_hash, generate_password_hash
from datetime import datetime

from src.core import configuracion_sistema
from src.core.socios.socios import Socio
from src.core.db import db
from src.core.colores_aleatorios import generar_color


def agregar_socio(data):
    """Esta funcion se utiliza para dar de alta un socio"""
    socio = Socio(**data)
    socio.password = generate_password_hash(socio.password, method="sha256")
    db.session.add(socio)
    db.session.commit()
    return socio


def socios_por_años():
    """Esta funcion devuelve una lista de los socios ingresados por año de los ultimos 7 años"""
    socios = Socio.query.all()
    lista = []
    dic_socios = {}
    for i in range(2015, 2023):
        dic_socios[str(i)] = 0
    for socio in socios:
        anio_str = socio.inserted_at.strftime("%Y")
        if anio_str in dic_socios:
            dic_socios[anio_str] += 1
    for key, value in dic_socios.items():
        lista.append([key, value])
    return lista


def socios_por_sexo():
    """Esta funcion devuelve una lista con los socios por sexo"""
    socios = Socio.query.all()
    lista = []
    dic_socios = {}
    for socio in socios:
        if socio.genero not in dic_socios.keys():
            dic_socios[socio.genero] = {"cantidad": 1, "color": generar_color()}
        else:
            dic_socios[socio.genero]["cantidad"] += 1
    for key, value in dic_socios.items():
        lista.append([key, value["cantidad"], value["color"]])
    return lista


def socios_habilitados_disciplina():
    """Retorna los socios habilitados"""
    return Socio.query.filter(Socio.activo.is_(True)).all()


def buscar_socio(id):
    """Esta funcion busca un socio por su id"""
    if int(id) > 2147483647:
        return None
    return Socio.query.get(id)


def buscar_socio_email(email):
    """Esta funcion busca un socio por su email"""
    return Socio.query.filter_by(email=email).first()


def modificar_socio(data):
    """Esta funcion realiza la modificacion de los datos de un socio"""
    socio = Socio.query.get(data["id"])
    socio.nombre = data["nombre"]
    socio.apellido = data["apellido"]
    socio.email = data["email"]
    socio.tipo_documento = data["tipo_documento"]
    socio.dni = data["dni"]
    socio.genero = data["genero"]
    socio.direccion = data["direccion"]
    socio.telefono = data["telefono"]
    db.session.commit()
    return socio


def eliminar_socio(id):
    """Esta funcion realiza la eliminacion de un socio de la BD"""
    socio = Socio.query.get(id)
    db.session.delete(socio)
    db.session.commit()


def esta_habilitado(id):
    """Esta funcion devuelve si el socio esta habilitado o no"""
    return Socio.query.get(id).activo


def disciplinas_socio_diccionario(id):
    """Devuelve una lista de diccionarios con todas las disciplinas que realiza el socio con id pasado por parametro"""
    socio = buscar_socio(id)
    lista = []
    for disciplina in socio.disciplinas:
        fila = disciplina.__dict__
        dias_horarios = fila["horarios"].split(" de ")
        diccionario = {
            "name": fila["nombre"],
            "days": dias_horarios[0],
            "time": dias_horarios[1],
            "teacher": fila["instructores"],
        }
        lista.append(diccionario)
    return lista


def todos_los_socios(apellido=None, tipo=None):
    """Retorna todos los socios en una lista de diccionarios"""
    data_socios = []
    if (apellido is not None) and (tipo is not None):
        if tipo == "true":
            socios = Socio.query.filter(
                Socio.apellido.contains(apellido.capitalize())
            ).filter(Socio.activo.is_(True))
        else:
            socios = Socio.query.filter(
                Socio.apellido.contains(apellido.capitalize())
            ).filter(Socio.activo.is_(False))
    elif apellido is not None:
        socios = Socio.query.filter(Socio.apellido.contains(apellido.capitalize()))
    elif tipo is not None:
        if tipo == "true":
            socios = Socio.query.filter(Socio.activo.is_(True))
        else:
            socios = Socio.query.filter(Socio.activo.is_(False))
    else:
        socios = Socio.query.all()
    for socio in socios:
        row = socio.__dict__
        row.pop("_sa_instance_state")
        row.pop("inserted_at")
        if row["activo"]:
            row["activo"] = "si"
        else:
            row["activo"] = "no"
        row["nro_socio"] = row["id"]
        del row["id"]
        data_socios.append(row)
    return data_socios


def listar_socios(page, apellido=None, tipo=None):
    """Esta funcion devuelve todos los socios de forma paginada segun la configuracion
    y segun si se esta realizando un tipo de busqueda."""
    if (apellido is not None) and (tipo is not None):
        if tipo == "true":
            socios = (
                Socio.query.filter(Socio.apellido.contains(apellido.capitalize()))
                .filter(Socio.activo.is_(True))
                .order_by(Socio.apellido, Socio.nombre)
                .paginate(
                    page, per_page=configuracion_sistema.get_paginado().elementos_pagina
                )
            )
        else:
            socios = (
                Socio.query.filter(Socio.apellido.contains(apellido.capitalize()))
                .filter(Socio.activo.is_(False))
                .order_by(Socio.apellido, Socio.nombre)
                .paginate(
                    page, per_page=configuracion_sistema.get_paginado().elementos_pagina
                )
            )
    elif apellido is not None:
        socios = (
            Socio.query.filter(Socio.apellido.contains(apellido.capitalize()))
            .order_by(Socio.apellido, Socio.nombre)
            .paginate(
                page, per_page=configuracion_sistema.get_paginado().elementos_pagina
            )
        )
    elif tipo is not None:
        if tipo == "true":
            socios = (
                Socio.query.filter(Socio.activo.is_(True))
                .order_by(Socio.apellido, Socio.nombre)
                .paginate(
                    page, per_page=configuracion_sistema.get_paginado().elementos_pagina
                )
            )
        else:
            socios = (
                Socio.query.filter(Socio.activo.is_(False))
                .order_by(Socio.apellido, Socio.nombre)
                .paginate(
                    page, per_page=configuracion_sistema.get_paginado().elementos_pagina
                )
            )
    else:
        socios = Socio.query.order_by(Socio.apellido, Socio.nombre).paginate(
            page, per_page=configuracion_sistema.get_paginado().elementos_pagina
        )
    return socios


def validar_datos_existentes(dni, email, accion, id=None):
    """Esta funcion valida que el dni o el email ingresados para dar de alta o modificar un socio no existan."""
    if accion == "alta":
        dni_existente = Socio.query.filter_by(dni=dni).first()
        email_existente = Socio.query.filter_by(email=email).first()
    elif accion == "modificacion":
        dni_existente = Socio.query.filter_by(dni=dni).filter(Socio.id != id).first()
        email_existente = (
            Socio.query.filter_by(email=email).filter(Socio.id != id).first()
        )
    if dni_existente is not None:
        return False, "El Dni ya esta cargado en el sistema."
    elif email_existente is not None:
        return False, "El Email ya esta cargado en el sistema."
    else:
        return True, "Ambos son validos"


def estado_socio(id):
    """Devuelve un diccionario con el estado actual del socio que seguro existe"""
    socio = buscar_socio(id)
    datos_perfil = {
        "user": socio.apellido + " " + socio.nombre,
        "email": socio.email,
        "number": socio.id,
        "document_type": socio.tipo_documento,
        "document_number": socio.dni,
        "gender": socio.genero,
        "gender_other": socio.genero,
        "address": socio.direccion,
        "phone": socio.telefono,
    }
    for pago in socio.pagos:
        if check_fecha_cuota_es_presente_o_pasada(pago):
            if not pago.estado:
                return {
                    "status": "BAD",
                    "description": "El socio registra deuda o sanción.",
                    "profile": datos_perfil,
                }
    return {
        "status": "OK",
        "description": "El socio no registra deuda ni sanción.",
        "profile": datos_perfil,
    }


def estado_socio_boolean(id):
    """chequea el estado del socio respecto a las cuotas que ha pagado o debe pagar.
    True significa que esta al día, False significa que no lo esta."""
    socio = buscar_socio(id)
    for pago in socio.pagos:
        if check_fecha_cuota_es_presente_o_pasada(pago):
            if not pago.estado:
                return False
    return True


def check_fecha_cuota_es_presente_o_pasada(pago):
    """Chequea si al fecha es del mes actual o anterior para verificar si debe tenerse
    en cuanta al verificar que un socio esta al día con los pagos"""
    if pago.año_cuota < datetime.now().year or (
        pago.año_cuota == datetime.now().year and pago.nro_cuota <= datetime.now().month
    ):
        return True
    return False


def save_photo(id, photo_path):
    socio = buscar_socio(id)
    if socio is not None:
        socio.photo_path = photo_path
        db.session.commit()


def get_photo_socio(id):
    socio = buscar_socio(id)
    if socio is not None and socio.photo_path is not None:
        return socio.photo_path
    return "/public/uploads/default_photo.jpg"


def find_socio_by_email_and_pass(email, password):
    """esta funcion verifica que el socio ingresado en login publico exista"""
    socio = Socio.query.filter(Socio.email == email).first()
    if socio is None:
        return None
    elif check_password_hash(socio.password, password):
        return socio


def informacion_socio(id):
    socio = buscar_socio(id)
    datos_perfil = {
        "nombre": socio.nombre,
        "apellido": socio.apellido,
        "email": socio.email,
        "id": socio.id,
        "document_type": socio.tipo_documento,
        "document_number": socio.dni,
        "gender": socio.genero,
        "gender_other": socio.genero,
        "address": socio.direccion,
        "phone": socio.telefono,
    }
    return {
        "status": "OK",
        "descripcion": "Informacion del socio jwt",
        "profile": datos_perfil,
    }
