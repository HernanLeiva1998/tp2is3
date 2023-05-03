from src.core import configuracion_sistema
from src.core.socios import buscar_socio
from src.core.socios import socios_habilitados_disciplina
from src.core.disciplinas.disciplinas import Disciplina
from src.core.db import db
from src.core.colores_aleatorios import generar_color


def buscar_disciplina(id):
    """Devuelve la disciplina con el id indicado"""
    if int(id) > 2147483647:
        return None
    return Disciplina.query.get(id)


def agregar_disciplina(data):
    """Dar de alta una disciplina en la BD"""
    disciplina = Disciplina(**data)
    db.session.add(disciplina)
    db.session.commit()
    return disciplina


def modificar_disciplina(data):
    """Modificar datos de una disciplina en la BD"""
    disciplina = buscar_disciplina(data["id"])
    disciplina.nombre = data["nombre"]
    disciplina.categoria = data["categoria"]
    disciplina.instructores = data["instructores"]
    disciplina.horarios = data["horarios"]
    disciplina.costo = data["costo"]
    disciplina.habilitada = data["habilitada"]
    db.session.commit()
    return disciplina


def eliminar_disciplina(id):
    """Dar de baja una disciplina en la BD buscandola por su id que seguro existe"""
    db.session.delete(buscar_disciplina(id))
    db.session.commit()


def relacionar_socio_disciplina(id_disciplina, id_socio):
    disciplina = buscar_disciplina(id_disciplina)
    disciplina.socios.append(buscar_socio(id_socio))
    db.session.commit()


def esta_habilitada(id):
    return buscar_disciplina(id).habilitada


def nombres_todas_las_disciplinas():
    """Devuelve los nombres de todas las disciplinas"""
    return db.session.query(Disciplina.nombre.distinct()).all()


def socios_habilitados_por_disciplina():
    """Retorna todos los socios inscriptos en alguna disciplina habilitado"""
    socios = socios_habilitados_disciplina()
    disciplinas = Disciplina.query.all()
    socios_disciplinas = {}
    lista = []
    for disciplina in disciplinas:
        socios_disciplinas[disciplina.nombre] = {"cantidad": 0, "color": generar_color()}
    for socio in socios:
        for dis_soc in socio.disciplinas:
            socios_disciplinas[dis_soc.nombre]["cantidad"] = (
                socios_disciplinas[dis_soc.nombre]["cantidad"] + 1
            )
    for key, value in socios_disciplinas.items():
        lista.append([key, value["cantidad"], value["color"]])
    return lista


def listar_disciplinas_diccionario():
    """Devuelve una lista de diccionarios con todas las disciplinas."""
    lista = []
    disciplinas = Disciplina.query.order_by(Disciplina.nombre).all()
    for disciplina in disciplinas:
        fila = disciplina.__dict__
        dias_horarios = fila["horarios"].split(" de ")
        diccionario = {
            "name": fila["nombre"],
            "days": dias_horarios[0],
            "time": dias_horarios[1],
            "teacher": fila["instructores"],
            "price": fila["costo"],
            "category": fila["categoria"],
        }
        lista.append(diccionario)
    return lista


def categorias_de_cada_disciplina():
    """Devuelve un diccionario donde cada clave es una disciplina y su valor es una lista de todas las categorias
    que tiene esa disciplina"""
    disciplinas = nombres_todas_las_disciplinas()
    todas_las_categorias = {}
    for disciplina in disciplinas:
        categorias = (
            db.session.query(Disciplina.categoria, Disciplina.id)
            .filter(Disciplina.nombre == disciplina[0])
            .all()
        )
        for categoria in categorias:
            todas_las_categorias[disciplina[0]] = categorias
    return todas_las_categorias


def listar_disciplinas(page):
    """Listado de las disciplinas según el paginado definido en el módulo de configuración"""
    return Disciplina.query.order_by(Disciplina.nombre).paginate(
        page, per_page=configuracion_sistema.get_paginado().elementos_pagina
    )


def validar_disciplina_repetida_alta(nombre, categoria):
    """Chequea que no haya ya una disciplina con mismo nombre y misma categoria"""
    if (
        Disciplina.query.filter_by(nombre=nombre)
        .filter(Disciplina.categoria == categoria)
        .first()
    ) is not None:
        return True, "La disciplina ya existe"
    return False, "La disciplina no existe aún"


def validar_disciplina_repetida_modificacion(nombre, categoria, id):
    """Chequea que no haya ya una disciplina con mismo nombre y misma categoria, pero distinto id ya que si fuera igual sería la misma disciplina que se está queriendo modificar"""
    if (
        Disciplina.query.filter_by(nombre=nombre)
        .filter(Disciplina.categoria == categoria)
        .filter(Disciplina.id != id)
        .first()
    ) is not None:
        return True, "La disciplina ya existe"
    return False, "La disciplina no existe aún"
