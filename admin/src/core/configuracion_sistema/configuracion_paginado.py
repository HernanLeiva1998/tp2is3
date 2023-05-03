from src.core.db import db


class Configuracion_paginado(db.Model):
    __tablename__ = "configuracion_paginado"

    id = db.Column(db.Integer, primary_key=True, nullable=False, unique=True)
    elementos_pagina = db.Column(db.Integer, nullable=False)

    def __init__(self, elementos_pagina):
        self.elementos_pagina = elementos_pagina
