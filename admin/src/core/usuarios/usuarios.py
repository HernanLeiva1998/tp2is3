from datetime import datetime

from src.core.db import db


class Usuario(db.Model):
    __tablename__ = "Usuarios"
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String, nullable=False)
    apellido = db.Column(db.String, nullable=False)
    email = db.Column(db.String, unique=True, nullable=False)
    activo = db.Column(db.Boolean, nullable=False)
    username = db.Column(db.String, unique=True, nullable=False)
    password = db.Column(db.String, nullable=False)
    inserted_at = db.Column(db.DateTime, default=datetime.now)


def __init__(self, nombre, apellido, email, activo, username, password):
    self.nombre = nombre
    self.apellido = apellido
    self.email = email
    self.activo = activo
    self.username = username
    self.password = password


def __repr__(self):
    return (
        f"Usuario(id={self.id!r}, nombre={self.nombre!r}, apellido={self.apellido!r})"
    )
