from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileRequired, FileAllowed
from wtforms import SubmitField
from flask_uploads import UploadSet, IMAGES


photos = UploadSet("photos", IMAGES)


class UploadForm(FlaskForm):
    photo = FileField(
        validators=[
            FileAllowed(photos, "Solo se permite subir imagenes"),
            FileRequired("El campo archivo no debería estar vacio"),
        ]
    )
    submit = SubmitField("upload")
