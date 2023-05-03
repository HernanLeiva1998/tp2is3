from src.core.db import db

# Tabla N a N de Usuario con Rol
Usuario_Rol = db.Table(
    "Usuario_Rol",
    db.Column(
        "id_usuario",
        db.Integer,
        db.ForeignKey("Usuarios.id"),
        nullable=False,
        primary_key=True,
    ),
    db.Column(
        "id_rol",
        db.Integer,
        db.ForeignKey("Roles.id"),
        nullable=False,
        primary_key=True,
    ),
)


class Rol(db.Model):
    __tablename__ = "Roles"

    # Columnas
    id = db.Column(db.Integer, primary_key=True, nullable=False, unique=True)
    nombre = db.Column(db.String(100), nullable=False)

    # Relacion
    usuarios = db.relationship("Usuario", secondary=Usuario_Rol, backref="roles")
