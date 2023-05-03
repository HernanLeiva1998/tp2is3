from datetime import datetime

from src.core.db import db


Socio_Disciplina = db.Table(
    "Socio_Disciplina",
    db.Column("id_socio", db.Integer, db.ForeignKey("Socios.id"), nullable=False),
    db.Column(
        "id_disciplina", db.Integer, db.ForeignKey("Disciplinas.id"), nullable=False
    ),
)


class Disciplina(db.Model):
    __tablename__ = "Disciplinas"
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(50), nullable=False)
    categoria = db.Column(db.String(50), nullable=False)
    instructores = db.Column(db.String(200), nullable=False)
    horarios = db.Column(db.String(150), nullable=False)
    costo = db.Column(db.String, nullable=False)
    habilitada = db.Column(db.Boolean, nullable=False)
    inserted_at = db.Column(db.DateTime, default=datetime.now)
    socios = db.relationship("Socio", secondary=Socio_Disciplina, backref="disciplinas")

    def __init__(self, nombre, categoria, instructores, horarios, costo, habilitada):
        self.nombre = nombre
        self.categoria = categoria
        self.instructores = instructores
        self.horarios = horarios
        self.costo = costo
        self.habilitada = habilitada

    def __repr__(self):
        return f"Disciplina (id={self.id!r}, nombre={self.nombre!r}, categoria={self.categoria!r})"
