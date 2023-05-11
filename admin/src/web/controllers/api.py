from flask import Blueprint, make_response, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from flask_jwt_extended import unset_jwt_cookies
from flask_jwt_extended import create_token_acceso, set_access_cookies

from src.core.socios import find_socio_by_email_and_pass
from src.web.controllers import disciplinas
from src.web.controllers import socios
from src.web.controllers import configuracion_sistema
from src.web.controllers import pagos
from src.web.controllers.socios import json_informacion_socio
from src.web.controllers.validators import validator_usuario
from src.web.controllers.validators import validator_pagos

api_blueprint = Blueprint("api", __name__, url_prefix="/api")


def hacer_respuesta_json(data, code = 200):
    respuesta = make_response(data, code)
    respuesta.headers["Content-Type"] = "application/json"
    return respuesta


@api_blueprint.get("/club/disciplinas")
def obtener_disciplinas():
    """Retorna un json con todas las disciplinas que se practican en el club"""
    return hacer_respuesta_json(disciplinas.disciplina_json())


@api_blueprint.get("/club/socios-años")
def socios_por_año():
    """Retorna un json con la cantidad de socios por año"""
    return hacer_respuesta_json(socios.socios_por_año())


@api_blueprint.get("/club/socios-genero")
def socios_genero():
    """Retorna un json con la cantidad de socios por genero"""
    return hacer_respuesta_json(socios.socios_genero())


@api_blueprint.get("/club/socios-disciplinas")
def obtener_socios_disciplinas():
    """Retorna un json con los socios por disciplinas"""
    return hacer_respuesta_json(disciplinas.disciplinas_socios())


@api_blueprint.get("/club/info")
def obtener_info_club():
    """Retorna el json con la información de contacto del club"""
    return hacer_respuesta_json(configuracion_sistema.info_contacto_json())


@api_blueprint.get("/me/disciplinas")
@jwt_required()
def obtener_disciplinas_socio():
    """Retorna el json con todas las disciplinas que realiza
    el socio que está logueado actualmente en la app pública (JWT)"""
    return hacer_respuesta_json(socios.disciplinas_socio(get_jwt_identity()))


@api_blueprint.get("/me/license")
@jwt_required()
def obtener_info_y_estado_socio():
    """Retorna el json con el estado de credencial y los datos
    del socio que está logueado actualmente en la app pública (JWT)"""
    return hacer_respuesta_json(socios.json_estado_socio(get_jwt_identity()))


@api_blueprint.get("/me/payments")
@jwt_required()
def obtener_pagos_socio():
    """Retorna la lista de pagos registrados
    del socio que está logueado actualmente en la app pública (JWT)"""
    return hacer_respuesta_json(pagos.pagos_json(get_jwt_identity()))


@api_blueprint.get("/me/pending_payments")
@jwt_required()
def obtener_pagos_adeudados_socio():
    """Retorna la lista de pagos adeudados
    del socio que está logueado actualmente en la app pública (JWT)"""
    return hacer_respuesta_json(pagos.pagos_adeudados_json(get_jwt_identity()))


@api_blueprint.post("/me/payments")
@jwt_required()
def registrar_pago_socio():
    """Registra un nuevo pago para
    el socio que está logueado actualmente en la app pública (JWT)"""
    if not validator_pagos.validar_inputs(request.get_json()):
        return make_response({"Error": "El request fue incorrecto."}, 400)
    if not pagos.pagar_json(request.get_json(), get_jwt_identity()):
        return make_response({"Error": "La cuota o el mes no existen."}, 404)
    return hacer_respuesta_json({"msg": "Pago exitoso."}, 201)


@api_blueprint.post("/auth")
def auth():
    """Esta funcion loguea al usuario y devuelve el token
    jwt en caso de ser correcto"""
    if not (request.data):
        return jsonify(mensaje = "No se envió un json."), 400
    json = request.get_json()
    if not (("email") in json.keys() and ("password") in json.keys()):
        return jsonify(mensaje = "No se envió el email o la password."), 400
    validacion, mensaje = validator_usuario.validar_inputs(json)
    if not validacion:
        return jsonify(mensaje = mensaje), 400
    socio = find_socio_by_email_and_pass(json["email"], json["password"])
    if socio is None:
        return jsonify(mensaje = "Credenciales Invalidas"), 400
    token_acceso = create_token_acceso(identity = socio.id)
    respuesta = jsonify(token = token_acceso)
    set_access_cookies(respuesta, token_acceso)
    return hacer_respuesta_json(respuesta, 201)


@api_blueprint.get("/logout_publico")
@jwt_required()
def logout_publico():
    """Esta funcion desloguea a un socio de la app publica"""
    respuesta = jsonify()
    unset_jwt_cookies(respuesta)
    return respuesta, 200


@api_blueprint.get("/socio_jwt")
@jwt_required()
def socio_jwt():
    """Esta funcion devuelve la informacion del socio en caso
    que el logueo sea exitoso"""
    socio_actual = get_jwt_identity()
    respuesta = make_response(json_informacion_socio(socio_actual))
    return respuesta, 200
