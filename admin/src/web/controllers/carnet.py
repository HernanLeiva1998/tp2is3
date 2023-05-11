from flask import (
    Blueprint,
    render_template,
    request,
    flash,
    url_for,
    session,
    send_from_directory,
    url_for,
    abort,
)

from pathlib import Path

from src.core.socios import (
    buscar_socio,
    save_photo,
    get_photo_socio,
    estado_socio_boolean,
)
from src.web.exportaciones import carnet_PDF
from src.web.exportaciones.UploadForm import UploadForm, photos
from src.web.helpers.permission import has_permission
from src.web.decorators.login import login_requerido
from src.web.controllers.validators.common_validators import is_integer


carnet_blueprint = Blueprint("carnet", __name__, url_prefix = "/carnet")


@carnet_blueprint.route("public/uploads/<filename>")
@login_requerido
def conseguir_archivo(nombre_de_archivo):
    """Se usa para recuperar la dirección donde se guardara 
    la foto del carnet"""
    if not (has_permission(session["user"], "carnet_photo")):
        return abort(403)
    return send_from_directory("public/uploads", nombre_de_archivo)


@carnet_blueprint.route("/upload_image/<id>", methods = ["GET", "POST"])
@login_requerido
def cargar_imagen(id):
    """Maneja el módulo de cargar foto para el carnet del socio 
    tomando el id del mismo como parámetro"""

    if not (has_permission(session["user"], "carnet_upload")):
        return abort(403)
    if (not is_integer(id)) or (buscar_socio(id) is None):
        return abort(404)

    socio = buscar_socio(id)
    formulario = UploadForm()
    if formulario.validate_on_submit():
        nombre_de_archivo = photos.save(formulario.photo.data)
        url_del_archivo = url_for("carnet.get_file", filename = nombre_de_archivo)
        url_del_archivo = url_del_archivo.replace("/carnet", "")
        save_photo(id, url_del_archivo)
    else:
        url_del_archivo = None
        flash(
            "Tiene que subir un archivo con extensión de imagen."
            + "Por ejemplo: .jpg, .jpeg, .png"
        )
    return render_template(
        "/carnet/upload_image.html",
        form = formulario, 
        file_url = url_del_archivo, 
        socio=socio
    )


@carnet_blueprint.route("/<id>")
@login_requerido
def ver_licencia(id):
    """Maneja el módulo de mostrar el carnet de un socio existente."""
    if not (has_permission(session["user"], "carnet_license")):
        return abort(403)
    if (not is_integer(id)) or (buscar_socio(id) is None):
        return abort(404)

    socio = buscar_socio(id)
    kwargs = {
        "url": request.url,
        "socio": socio,
        "photo": get_photo_socio(id),
        "estado": estado_socio_boolean(id),
    }
    if not la_imagen_existe(kwargs["photo"]):
        kwargs["photo"] = direccion_predeterminada_de_la_foto()
    return render_template("carnet/carnet_template.html", **kwargs)


def direccion_completa_de_la_imagen(direccion):
    """Devuelve la dirección verdadera del parametro path.
    path guarda la dirección local del archivo, para conseguir
    la dirección verdadera necesita concatenar path con la dirección
     verdadera de la carpeta admin"""
    return str(Path(__file__).parent.parent.parent.parent) + direccion


def la_imagen_existe(direccion):
    """Comprueba si existe una imagen en 
    la dirección que recibe por parámetro"""
    direccion = direccion_completa_de_la_imagen(direccion)
    return Path(direccion).exists()


def direccion_de_foto_predeterminada():
    """Dirección a la foto por defecto que se usa para el carnet de los socios
    sin foto cargada."""
    return "/public/uploads/default_photo.jpg"


@carnet_blueprint.route("/download/<id>")
@login_requerido
def descarga_carnet_pdf(id):
    """Importa un pdf con los datos del carnet del socio que se corresponda
    al id que se recibe como parámetro"""
    if not (has_permission(session["user"], "carnet_download")):
        return abort(403)
    if (not is_integer(id)) or (buscar_socio(id) is None):
        return abort(404)

    socio = buscar_socio(id)
    direccion = direccion_completa_de_la_imagen(get_photo_socio(id))
    kwargs = {
        "socio": socio,
        "photo": direccion,
        "url": url_for("carnet.view_license", id=id),
        "estado": estado_socio_boolean(id),
    }
    archivo_pdf = carnet_PDF.generar_carnet_PDF(**kwargs)
    return archivo_pdf
