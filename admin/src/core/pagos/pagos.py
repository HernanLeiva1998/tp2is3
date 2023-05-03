from datetime import datetime

from src.core.db import db


class Pago(db.Model):
    __tablename__ = "Pagos"
    id = db.Column(db.Integer, primary_key=True)
    total = db.Column(db.Integer, nullable=False)
    fecha_pago = db.Column(db.DateTime, nullable=True)
    nro_cuota = db.Column(db.Integer, nullable=False)
    año_cuota = db.Column(db.Integer, nullable=False, default=datetime.now().year)
    estado = db.Column(db.Boolean, nullable=False)
    socio_id = db.Column(db.Integer, db.ForeignKey("Socios.id"))
    socio = db.relationship("Socio", back_populates="pagos")

    def __init__(
        self, total, socio_id, nro_cuota, estado, año_cuota=None, fecha_pago=None
    ):
        self.total = total
        self.fecha_pago = fecha_pago
        self.socio_id = socio_id
        self.nro_cuota = nro_cuota
        self.estado = estado
        if año_cuota is not None:
            self.año_cuota = año_cuota

    def __repr__(self):
        return f"Socio(id={self.id!r}, total={self.total!r}, fecha={self.fecha_pago!r})"
