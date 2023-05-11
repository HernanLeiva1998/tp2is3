from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileRequired, FileAllowed
from wtforms import SubmitField
from flask_uploads import UploadSet, IMAGES


fotos = UploadSet("photos", IMAGES)


class UploadForm(FlaskForm):
    foto = FileField(
        validators = [
            FileAllowed(fotos, "Solo se permite subir imagenes"),
            FileRequired("El campo archivo no debería estar vacio"),
         ]
     )
    entregar = SubmitField("upload")
