from src.core.db import db


class Configuracion_general(db.Model):
    __tablename__ = "configuracion_general"

    id = db.Column(db.Integer, primary_key=True, nullable=False, unique=True)
    activar_pagos = db.Column(db.Boolean, nullable=False)
    encabezado_recibos = db.Column(db.String(500), nullable=False)
    informacion_contacto = db.Column(db.String(500), nullable=False)
    cuota_base = db.Column(db.Float, nullable=False)
    porcentaje_recargo = db.Column(db.Float, nullable=False)

    def __init__(
        self,
        activar_pagos,
        encabezado_recibos,
        informacion_contacto,
        cuota_base,
        porcentaje_recargo,
    ):
        self.activar_pagos = activar_pagos
        self.encabezado_recibos = encabezado_recibos
        self.informacion_contacto = informacion_contacto
        self.cuota_base = cuota_base
        self.porcentaje_recargo = porcentaje_recargo

    def __repr__(self):
        return f"ConfigGeneral({self.encabezado_recibos} {self.informacion_contacto} {self.cuota_base} {self.porcentaje_recargo} activar pagos {self.activar_pagos} )"
