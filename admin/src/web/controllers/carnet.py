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


carnet_blueprint = Blueprint("carnet", __name__, url_prefix="/carnet")


@carnet_blueprint.route("public/uploads/<filename>")
@login_requerido
def get_file(filename):
    """Se usa para recuperar la dirección donde se guardara la foto del carnet"""
    if not (has_permission(session["user"], "carnet_photo")):
        return abort(403)
    return send_from_directory("public/uploads", filename)


@carnet_blueprint.route("/upload_image/<id>", methods=["GET", "POST"])
@login_requerido
def upload_image(id):
    """Maneja el módulo de cargar foto para el carnet del socio tomando el id del mismo como parámetro"""

    if not (has_permission(session["user"], "carnet_upload")):
        return abort(403)
    if (not is_integer(id)) or (buscar_socio(id) is None):
        return abort(404)

    socio = buscar_socio(id)
    form = UploadForm()
    if form.validate_on_submit():
        filename = photos.save(form.photo.data)
        file_url = url_for("carnet.get_file", filename=filename)
        file_url = file_url.replace("/carnet", "")
        save_photo(id, file_url)
    else:
        file_url = None
        flash(
            "Tiene que subir un archivo con extensión de imagen. Por ejemplo: .jpg, .jpeg, .png"
        )
    return render_template(
        "/carnet/upload_image.html", form=form, file_url=file_url, socio=socio
    )


@carnet_blueprint.route("/<id>")
@login_requerido
def view_license(id):
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
    if not image_exists(kwargs["photo"]):
        kwargs["photo"] = get_default_photo_path()
    return render_template("carnet/carnet_template.html", **kwargs)


def image_full_path(path):
    """Devuelve la dirección verdadera del parametro path.
    path guarda la dirección local del archivo, para conseguir
    la dirección verdadera necesita concatenar path con la dirección
     verdadera de la carpeta admin"""
    return str(Path(__file__).parent.parent.parent.parent) + path


def image_exists(path):
    """Comprueba si existe una imagen en la dirección que recibe por parámetro"""
    path = image_full_path(path)
    return Path(path).exists()


def get_default_photo_path():
    """Dirección a la foto por defecto que se usa para el carnet de los socios
    sin foto cargada."""
    return "/public/uploads/default_photo.jpg"


@carnet_blueprint.route("/download/<id>")
@login_requerido
def carnet_pdf_download(id):
    """Importa un pdf con los datos del carnet del socio que se corresponda
    al id que se recibe como parámetro"""
    if not (has_permission(session["user"], "carnet_download")):
        return abort(403)
    if (not is_integer(id)) or (buscar_socio(id) is None):
        return abort(404)

    socio = buscar_socio(id)
    path = image_full_path(get_photo_socio(id))
    kwargs = {
        "socio": socio,
        "photo": path,
        "url": url_for("carnet.view_license", id=id),
        "estado": estado_socio_boolean(id),
    }
    outpot = carnet_PDF.generar_carnet_PDF(**kwargs)
    return outpot
